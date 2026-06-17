# Bare-Metal Provisioning

[<- Back to Infrastructure](../README.md)

This directory documents how bare-metal nodes are prepared before Kubernetes takes over.

During the Ubuntu phase, provisioning is expected to use Ansible. During the later Talos phase, most node configuration should move into Talos machine configuration and GitOps-controlled Kubernetes resources.

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

| Component | Status | Location | Recommendation | Role | Documentation |
|---|---|---|---|---|---|
| Ansible | ⚫ Inactive | Local automation against bare-metal nodes | Ubuntu-phase provisioning standard | Repeatable node setup before Kubernetes | [ansible](./ansible) |

---

## Provisioning Rule

Manual work is acceptable while learning, but once a step is understood it should move into one of these places:

- Ansible for Ubuntu node setup
- Terraform for network infrastructure
- Talos machine configuration for immutable node setup
- GitOps for Kubernetes resources

The long-term goal is that a node can be wiped and rebuilt without relying on memory or terminal history.
