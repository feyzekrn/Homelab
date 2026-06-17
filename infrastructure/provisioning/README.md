# Bare-Metal Provisioning

[<- Back to Infrastructure](../README.md)

This directory documents how bare-metal nodes are prepared before Kubernetes takes over.

During the Ubuntu phase, provisioning is expected to use Ansible. During the later Talos phase, most node configuration should move into Talos machine configuration and GitOps-controlled Kubernetes resources.

---

## Why This Matters

Provisioning is the step between raw hardware and a usable Kubernetes node. It covers the repeatable setup of operating system basics, users, SSH, packages, disks, runtime dependencies and Kubernetes prerequisites.

In a homelab, provisioning starts as manual learning. That is fine at the beginning, but repeated commands should eventually become automation. Otherwise every rebuild depends on memory, shell history or undocumented fixes.

In companies, provisioning is expected to be reproducible. New nodes should be built consistently, patched predictably and replaced without heroic manual work. This directory documents the homelab version of that discipline.

---

## What You Can Do With It

- prepare Ubuntu nodes consistently
- configure users, SSH and sudo
- install base packages
- prepare disks and mount points
- install Kubernetes prerequisites
- make node rebuilds repeatable
- define the transition path from Ubuntu to Talos

---

## Scope

This area should document:

- host naming
- SSH access during the Ubuntu phase
- base packages
- users and sudo rules
- disk preparation
- container runtime setup
- kubeadm or other Kubernetes bootstrap steps
- idempotent Ansible playbooks
- transition notes for Talos

---

## Components

| Path | Status | Location | Recommendation | Role |
|---|---|---|---|---|
| [`./ansible`](./ansible) | ⚫ Inactive | Local automation against bare-metal nodes | Ubuntu-phase provisioning standard | Repeatable node setup before Kubernetes |

---

## Provisioning Rule

Manual work is acceptable while learning, but once a step is understood it should move into one of these places:

- Ansible for Ubuntu node setup
- Terraform for network infrastructure
- Talos machine configuration for immutable node setup
- GitOps for Kubernetes resources

The long-term goal is that a node can be wiped and rebuilt without relying on memory or terminal history.
