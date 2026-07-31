# 🖥️ Compute — Two Worlds, One Homelab

[← Back to Setup Overview](../README.md)

The compute layer is split into **two deliberately separate worlds**. The split is not about hardware — it is about availability classes and blast radius:

- The **Kubernetes cluster** is the experimentation field. Things get deployed, broken and rebuilt here. Anything that must survive a node failure lives here, because only Kubernetes can heal dead hardware by rescheduling workloads.
- The **Proxmox cluster** is the stable infrastructure world. It carries the services the family relies on — NAS, router/firewall, DNS, media and cloud apps. It heals process failures (systemd restarts, `onboot=1`), gets reproduced through code and is not touched by cluster experiments.

Each world can die without taking the other one down: the k8s cluster can be wiped and rebuilt while the family still reaches their photos — and the Proxmox box can be in maintenance while every cluster app keeps its ingress.

---

## The Two Worlds

| | [☸️ k8s-cluster](./k8s-cluster) | [🐙 proxmox-cluster](./proxmox-cluster) |
|---|---|---|
| **Hardware** | 3× Lenovo ThinkCentre M910q Tiny | 1× Minisforum MS-01 Workstation |
| **Node names** | `node0`, `node1`, `node2` | `pve0` |
| **OS** | [Ubuntu Server → Talos](./k8s-cluster/os) | [Proxmox VE](./proxmox-cluster/os) |
| **Role** | Bare-metal Kubernetes: custom apps, HA workloads, learning | Hypervisor: NAS, OPNsense, DNS, family apps, VMs & LXCs |
| **Availability class** | High availability through replication | Stable single node, self-healing processes |
| **Naming philosophy** | Cattle — numbered, replaceable | Pet — unique, load-bearing |
| **Failure handling** | Cluster reschedules workloads | systemd restarts, `onboot=1`, config as code |

Both worlds watch each other: a responder service on each side monitors the health of the other and can revive dead machines through Intel vPro/AMT — documented in the automation section once built.

---

## The Bridge: One Node With A Foot In Both Worlds

The two-world split has one weakness, and it shows up the moment a service has users on both sides. [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) is the example that forced the question: the family apps live on `pve0` so that cluster experiments cannot reach them — but if their *login* is a cluster workload, rebuilding the cluster locks the family out anyway. The dependency returns through the front door.

The answer is a deliberate bridge. **A VM on `pve0` permanently joins the Kubernetes cluster as a node**, and workloads that must survive a cluster rebuild are constrained to always keep one replica on it.

```text
        Kubernetes cluster
   ┌──────────┬──────────┬──────────┬─────────────────┐
   │  node0   │  node1   │  node2   │  pve-node (VM)  │
   │  Tiny    │  Tiny    │  Tiny    │  on pve0        │
   └──────────┴──────────┴──────────┴─────────────────┘
        experimentation field         the anchor
        wiped and rebuilt freely      survives the rebuild
```

Keycloak then runs three replicas: two on the Tiny nodes, one on the anchor. Wipe the three Tinys and an instance is still serving logins, on a machine that was never part of the experiment.

### What makes it actually work

Three things decide whether this is real resilience or a diagram:

| Concern | Why it matters |
|---|---|
| **The database must be anchored too** | Pods are stateless; the state is in PostgreSQL. If that runs on cluster storage, the surviving pod has nothing to authenticate against. Anchored workloads keep their database as an LXC on `pve0` |
| **Running pods survive a dead control plane** | Kubelet does not stop pods when the API server is unreachable — so the anchored replica keeps working during a rebuild. If it *crashes* in that window, nothing reschedules it |
| **Control-plane membership is a real choice** | Making the anchor a control-plane member closes the gap above. That argues for 2 Tinys + the VM as control plane rather than 3 Tinys + a worker, to keep the etcd count odd |

### The placement rule this produces

The bridge only earns its complexity for a specific class of workload, so the rule that decides placement is worth stating plainly:

> **Place a component by who consumes it, not by how much availability it needs.**

- Consumers **only inside the cluster** → runs on the cluster, no anchor. [Argo CD](../../infrastructure/kubernetes/gitops/argocd) is the clearest case: it is useless when the cluster is gone, so its availability is coupled to the cluster's by nature. Moving it out would also convert GitOps from a pull model into a push model holding cluster credentials outside the cluster.
- Consumers **only outside the cluster** → runs on `pve0`. [Caddy](../../infrastructure/platform/ingress/caddy), [AdGuard Home](../../infrastructure/platform/dns/adguard-home), the NAS.
- Consumers **in both worlds** → runs on the cluster **with an anchor**, or on `pve0` if the cluster adds nothing. Keycloak takes the first path; [MinIO](../../infrastructure/platform/storage/minio) takes the second, because a backup target must outlive the thing it backs up.

Anchoring is not free — it costs a permanent VM, RAM on `pve0` and a scheduling constraint that has to be maintained. It is meant for the short list of services whose outage is felt by people who never asked for a homelab.

---

## ⚠️ The Proxmox Host Is Optional

Anyone rebuilding this setup should know up front: **the MS-01 is not a requirement. The homelab this repository describes is the Kubernetes cluster, and that runs on three mini PCs for well under 300 €.** The workstation was added later, when the project grew beyond "learn Kubernetes" into "also host the household's data".

Everything the Proxmox host does can be done differently:

| What it provides | How to do it without | What is lost |
|---|---|---|
| Router / firewall (OPNsense) | A dedicated router (Fritz!Box), or OPNsense on any old PC, or the Layer 3 features of the CRS310 | Multi-zone firewalling; the switch does no stateful filtering |
| NAS / storage | An existing NAS, an old desktop with disks, or [Longhorn](../../infrastructure/platform/storage/longhorn) plus a USB disk for backups | Capacity and the ZFS dataset model — Longhorn on 256 GB SSDs is not a media library |
| Family apps (Jellyfin, Immich, Nextcloud) | Run them on the cluster instead | The failure separation: rebuilding the cluster then takes the family's data offline with it |
| Extra Kubernetes nodes on demand | Add a fourth Tiny for ~50 € | Nothing — a real node is better than a VM node |
| Future GPU / AI workloads | Any desktop with a PCIe slot | Nothing, if such a machine is available |

**Start with the three nodes.** Build the cluster, break it, rebuild it — that is where the learning is, and none of it needs a hypervisor. The MS-01 becomes worth its ~500 € at a specific point: when the lab stops being only an experiment and starts holding things other people depend on. Before that point it is comfort, not infrastructure.

The reverse is also true, and worth saying: a Proxmox host alone, without the cluster, is a perfectly reasonable homelab too. It just teaches virtualization and self-hosting rather than Kubernetes.

### What actually justifies it — and what does not

**Not the router.** OPNsense uses 2 vCPU and 2–4 GB of a 14-core, 32 GB machine. Nobody needs a 500 € workstation to route a household's packets, and the network would work without it: a [Fritz!Box](../networking/router) handles the home network, and the CRS310 could route between zones in hardware if it had to. The router is a *tenant* on this machine, not the reason it was bought.

**The apps and their storage are the reason** — and specifically, the three Tiny nodes cannot host them:

| Constraint on the Tiny nodes | Why it blocks the family apps |
|---|---|
| **256 GB SATA SSD per node** | 768 GB raw across the cluster, roughly 250 GB usable after Longhorn's three-way replication. A photo library and a media collection are measured in terabytes, not gigabytes |
| **Only 2.5" and M.2 slots** | Cheap bulk storage comes from 3.5" HDDs — 4 TB for around 90 €. The same capacity as a 2.5" SSD costs roughly 250 €, and the Tiny cannot fit anything else |
| **8–16 GB RAM per node** | Immich's machine learning alone wants 2–4 GB, and the cluster components already take their share. Adding Nextcloud, PostgreSQL and Jellyfin on top leaves nothing for the experiments the cluster exists for |
| **Skylake-era iGPU (i5-6500T)** | Transcoding works for older codecs, but modern libraries (HEVC 10-bit, AV1) fall back to CPU — on four cores without hyper-threading that is a stuttering stream |

Put plainly: **the cluster is fine as a cluster.** It fails as a media and storage server, and that is the gap the MS-01 fills.

### The honest cheap alternatives

If the goal is only "somewhere for the files and the family apps", these are the paths worth comparing before spending 500 €:

| Path | Cost | Reality check |
|---|--:|---|
| **Another Tiny node** | ~ 50 € | Cheapest by far — but it has the exact same limits: no 3.5" bay, no bulk storage. It solves compute, never storage |
| **Raspberry Pi 5 as a NAS** | ~ 150–180 € | Board, PSU, cooling, SD card and a SATA/NVMe HAT add up to **three times the price of a Tiny**, and it is still 1 Gbit, 8 GB RAM and USB- or single-lane-attached disks. Fine as a pure file server; it will not transcode Jellyfin and will not run Immich's ML |
| **Used office desktop** (OptiPlex/ProDesk SFF) | ~ 60–120 € | **The genuinely sensible budget answer.** Takes 2–4 disks including 3.5" HDDs, has free RAM slots and a PCIe slot, and runs Proxmox or TrueNAS perfectly well. Costs are ~30–50 €/year higher in electricity, and it is bulky and louder |
| **MS-01** *(chosen)* | ~ 500 € | Everything above in one small, quiet, low-power box — plus 10G, plus 14 cores for reserve cluster nodes, plus a PCIe slot for a future GPU |

The honest conclusion: **a used desktop for around 100 € would have covered the actual requirement.** The MS-01 was chosen for the things beyond it — the 10G trunk, the compact silent form factor, modern transcoding, and headroom for AI workloads later. That is a comfort and future-proofing decision, and it should be read as one. The Raspberry Pi, meanwhile, is the option that looks cheap and is not: at 150–180 € it costs three Tiny nodes' worth of money for less capability than a 100 € desktop.

---

## Sections

### [☸️ k8s-cluster — The Bare-Metal Kubernetes Nodes](./k8s-cluster)

The three Lenovo M910q Tiny nodes: hardware decisions, CPU/RAM/storage choices, salvaged parts and the upgrade path — plus the [OS strategy](./k8s-cluster/os) (Ubuntu Server for the learning phase, Talos for the rebuild).

### [🐙 proxmox-cluster — The Infrastructure Workstation](./proxmox-cluster)

The Minisforum MS-01 running Proxmox VE (currently a single node): what is inside, why this machine, what it will host — and the [Proxmox VE installation](./proxmox-cluster/os) including the macOS bootable-USB workflow.
