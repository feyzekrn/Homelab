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

## Sections

### [☸️ k8s-cluster — The Bare-Metal Kubernetes Nodes](./k8s-cluster)

The three Lenovo M910q Tiny nodes: hardware decisions, CPU/RAM/storage choices, salvaged parts and the upgrade path — plus the [OS strategy](./k8s-cluster/os) (Ubuntu Server for the learning phase, Talos for the rebuild).

### [🐙 proxmox-cluster — The Infrastructure Workstation](./proxmox-cluster)

The Minisforum MS-01 running Proxmox VE (currently a single node): what is inside, why this machine, what it will host — and the [Proxmox VE installation](./proxmox-cluster/os) including the macOS bootable-USB workflow.
