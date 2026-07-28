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
