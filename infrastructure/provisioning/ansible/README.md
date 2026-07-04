# Ansible

[<- Back to Bare-Metal Provisioning](../README.md)

Ansible is the planned provisioning tool for the Ubuntu Server phase of this homelab.

It should automate repeatable node setup before Kubernetes and GitOps take over.

Ansible is an automation tool that connects to machines, usually over SSH, and applies a desired configuration. Its instructions are written as playbooks. A playbook might create users, install packages, configure SSH, mount disks or prepare Kubernetes prerequisites.

Ansible is useful because it makes manual server setup steps explicit and repeatable. Instead of remembering a sequence of shell commands, the project can keep a playbook that describes the intended node configuration.

For beginners, the important word is idempotent. A good Ansible task can be run more than once without breaking the system or duplicating work.

---

## Why It Fits

Ansible is a good first provisioning tool because it works over SSH, is readable, and makes manual Linux setup steps explicit.

During the Ubuntu phase, that is useful: the goal is not to hide Linux, but to understand it and then make the setup repeatable.

---

## Used For

- creating users and SSH access
- configuring sudo rules
- installing base packages
- setting hostnames
- preparing disks and mounts
- configuring container runtime dependencies
- applying firewall basics
- preparing kubeadm or Kubernetes prerequisites
- documenting repeatable node changes

---

## Strengths

- Agentless SSH-based model is easy to start.
- Playbooks are readable compared with many low-level scripts.
- Good for Linux host configuration.
- Strong ecosystem of modules and roles.
- Fits the Ubuntu learning phase well.

---

## Weaknesses

- Not the best long-term owner for Kubernetes resources in a GitOps platform.
- Playbooks can become messy if they are used as shell-script wrappers.
- Requires careful inventory and variable organization as the environment grows.
- Immutable systems such as Talos reduce the need for SSH-based host changes.

---

## What Does Not Belong Here

Ansible should not become the long-term source of truth for Kubernetes resources.

Use:

- Ansible for Ubuntu node preparation
- Terraform for MikroTik and network infrastructure if feasible
- Flux or another GitOps controller for Kubernetes resources
- Talos machine configuration during the later Talos phase

---

## Planned Layout

```text
infrastructure/provisioning/ansible/
├── README.md
├── inventories/
├── playbooks/
├── roles/
└── group_vars/
```

These folders should be created once real playbooks exist. Until then, this README documents the intended ownership boundary.

---

## Application Examples

- Install the same base packages on all Lenovo M910q nodes.
- Configure SSH hardening consistently.
- Prepare Longhorn disk mount points before the cluster is installed.
- Install Kubernetes prerequisites during the Ubuntu learning phase.
- Rebuild a node without copying commands from terminal history.

---

## Comparison Notes

| Tool | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| Ansible | Local control machine | Recommended for Ubuntu phase | Common standard | Simple SSH-based provisioning |
| cloud-init | Node boot/install phase | Good | Common cloud/server standard | Great for first boot, less interactive later |
| Talos machine config | Node OS config | Target for phase 2 | Strong Kubernetes-node model | Best once moving to Talos |
| Terraform | Infrastructure APIs | Good for network/IaC | Business standard | Not ideal for package-level Linux config |

---

## Hands-On Start

Start with an inventory and one safe read-only playbook:

```bash
ansible all -i inventories/homelab.ini -m ping
ansible all -i inventories/homelab.ini -m setup
```

Then add small idempotent playbooks:

1. base users and SSH keys
2. hostnames
3. base packages
4. disk preparation
5. Kubernetes prerequisites

---

## Runtime Status

Ansible provisioning is currently `⚫ Inactive`. It should become active during the Ubuntu Server phase, before the cluster is rebuilt with Talos.

---

## Documentation

- [Ansible documentation](https://docs.ansible.com/)
- [Ansible inventory guide](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)
- [Wikipedia: Ansible](https://en.wikipedia.org/wiki/Ansible_(software))
- [Wikipedia: Configuration management](https://en.wikipedia.org/wiki/Configuration_management)
