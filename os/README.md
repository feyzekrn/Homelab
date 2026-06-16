# Operating System Strategy

[← Back to Repository Overview](../README.md)

This section documents which operating system is used for which stage of the homelab and why. The decision is intentionally split into two phases: first a learning-heavy Linux phase, then a stricter bare-metal Kubernetes phase.

The long-term goal of this project is not only to run workloads. The goal is to understand the layers underneath them: Linux, networking, storage, Kubernetes, automation, GitOps, infrastructure as code and hardware operations. Because of that, the first operating system is chosen for learning depth, not for the cleanest production end state.

---

## Decision Summary

| Phase | Duration | Operating system | Used for | Main reason |
|---|---:|---|---|---|
| 1 | ~1 year | [Ubuntu Server 24.04 LTS](./installations/ubuntu-server-24.04) | First cluster build, Linux administration, Kubernetes learning, networking experiments, storage and service hosting | Exposes the underlying system instead of hiding it |
| 2 | After phase 1 | [Talos Linux](./installations/talos) | Rebuilt bare-metal Kubernetes cluster with immutable nodes and IaC from the start | Closer to the real target architecture |

Phase 1 is not the final architecture. It is the training ground.

Phase 2 is the real bare-metal Kubernetes approach: wipe the nodes, install Talos on every machine, rebuild the cluster from code and treat manual configuration as a failure that needs to be moved into infrastructure as code.

---

## Phase 1 — Ubuntu Server 24.04 LTS

For the first year all nodes run **[Ubuntu Server 24.04 LTS](./installations/ubuntu-server-24.04)**.

Ubuntu is the right starting point because it keeps the full Linux system visible. That matters for this project. Before making the cluster minimal and immutable, I want to understand what is actually happening on the nodes: boot process, services, logs, packages, network interfaces, kernel modules, disks, mounts, systemd units and the way Kubernetes interacts with all of it.

This phase is where most of the foundational skills are built:

- Linux server installation and administration
- SSH, users, sudo, firewalling and hardening basics
- systemd services, journald logs and boot debugging
- disk layout, filesystems and mount behavior
- container runtime installation and troubleshooting
- Kubernetes installation and node lifecycle management
- CNI behavior, pod networking and service routing
- Longhorn storage behavior on real disks
- database and message broker operation on Kubernetes
- MikroTik networking, VLANs, routing and failure testing
- Ansible-based provisioning and repeatable node setup
- Terraform-based network configuration
- GitOps for cluster components and applications

The point is to see the complexity before removing it.

### What Ubuntu is used for

Ubuntu is used for the first complete cluster build:

- base OS on all Lenovo M910q Tiny nodes
- first Kubernetes control plane and worker setup
- first CNI, Longhorn, MetalLB and ingress experiments
- first self-hosted databases and message brokers
- early hardware automation work against Intel vPro
- early monitoring, dashboards and admin tooling

Manual work is acceptable at the beginning of this phase, but only as a learning step. Once something is understood, it should move into documentation, Ansible, Terraform or GitOps.

### What Ubuntu is not meant to become

Ubuntu is not the final node operating system for this project.

It is not chosen because it is the most minimal Kubernetes host. It is chosen because it is practical, familiar enough to start quickly and open enough to inspect deeply. After the learning phase, the nodes are expected to be wiped.

In the long run, Ubuntu is also not the cleanest productive Kubernetes node OS for this homelab. A general-purpose Linux server has a larger operational surface: package updates, local services, SSH access, user state, manual fixes and configuration drift all have to be managed carefully. That is useful while learning, because it exposes the real system and makes debugging possible at every layer. But for a mature cluster, those same freedoms become maintenance burden and risk compared to Talos, where the node is intentionally small, immutable and managed declaratively.

This does not make Ubuntu the wrong first choice. It just means its value is strongest in the learning phase. The direct access to the OS is essential for understanding Linux, networking, storage and Kubernetes internals before moving to a stricter production-style model.

---

## Phase 2 — Talos Linux

After roughly one year, the cluster gets rebuilt from scratch with **[Talos Linux](./installations/talos)** on every node.

Talos is the target operating system for the serious bare-metal Kubernetes phase. It removes the traditional Linux server surface: no SSH-based administration, no package manager workflows, no manual node changes. Nodes are managed through declarative machine configuration and Kubernetes APIs.

That is exactly the direction this project should move toward once the fundamentals are learned.

### What Talos is used for

Talos is used for the second full cluster build:

- immutable Kubernetes-focused node OS
- declarative machine configuration
- reproducible bare-metal cluster bootstrap
- stricter separation between infrastructure code and runtime state
- production-style rebuilds instead of manual repair sessions
- safer experiments around node replacement and disaster recovery

The Talos phase should start with infrastructure as code from day one. If updates to the repository structure, Ansible roles, Terraform modules, GitOps layout or bootstrap scripts are needed at that point, they should be made before the rebuild starts.

### What changes when moving to Talos

The operating model changes from "log into a Linux server and fix it" to "change the declared state and roll it out".

That means:

- no long-lived manual configuration on nodes
- no SSH as the normal operations path
- no undocumented package or service changes
- no fixing a node in place if rebuilding it is cleaner
- every important setting must live in Git

This is the point where the homelab becomes much closer to the intended final architecture.

---

## Why not start with Talos immediately?

Starting with Talos would make the first cluster cleaner, but it would skip too much of the learning path.

Talos is excellent when the operator already understands Linux, Kubernetes networking, storage behavior and node failure modes. It intentionally hides or removes many traditional Linux administration paths. That is good for a mature cluster, but bad for learning the layers underneath it.

The project exists to build skills, especially around cloud-native infrastructure and networking. Ubuntu gives more surface area to inspect, break and understand. Talos comes after that foundation is real.

---

## Installation Media

Installer images and version notes live under:

[`./installations`](./installations)

This directory is the local staging area for the operating system images that are written to USB sticks:

- Ubuntu Server 24.04 LTS ISO for the first cluster phase
- Talos Linux metal image for the later rebuild phase

Large ISO and image files should stay out of Git. The repository tracks the version, filename, source URL and checksum notes; the actual installer files can be placed in the matching local folder when needed.

---

## Current OS Plan

| Node | Phase 1 OS | Phase 2 OS |
|---|---|---|
| Node 1 | [Ubuntu Server 24.04 LTS](./installations/ubuntu-server-24.04) | [Talos Linux](./installations/talos) |
| Node 2 | [Ubuntu Server 24.04 LTS](./installations/ubuntu-server-24.04) | [Talos Linux](./installations/talos) |
| Node 3 | [Ubuntu Server 24.04 LTS](./installations/ubuntu-server-24.04) | [Talos Linux](./installations/talos) |

If more nodes are added during the Ubuntu phase, they should follow the same rule: Ubuntu first for learning and consistency, Talos later during the full rebuild.

---

## Decision Log

| Date | Decision |
|---|---|
| 2026-06-17 | Start with Ubuntu Server 24.04 LTS on all nodes for roughly one year to build Linux, cloud-native and networking skills. Rebuild later with Talos Linux and infrastructure as code from the beginning. |
