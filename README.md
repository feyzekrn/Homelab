# All-in-One Homelab — Bare-Metal Kubernetes + Proxmox

**A living documentation of building, breaking and rebuilding a self-hosted infrastructure — from raw hardware to production-grade services.**

---

## What is this?

Three budget mini PCs running bare-metal Kubernetes. One workstation running Proxmox. One managed switch. A complete homelab on a shelf at home.

The setup is deliberately split into **two worlds**: the Kubernetes cluster is the experimentation field where things get deployed, broken and rebuilt — and the Proxmox side is the stable infrastructure that carries what the family relies on: NAS, router/firewall, DNS and the self-hosted apps. Each world can fail without taking the other one down.

This repository documents everything: the hardware decisions, the network design, the software stack and every problem I ran into along the way. It is not a polished tutorial and it is not meant to be. Things will break here, get rebuilt differently and evolve over time. If you are looking for a clean, finished reference — this is not that. If you are interested in watching something grow from scratch and seeing the real reasoning behind every decision, stick around.

If you spot something that could be done better, I am genuinely open to that conversation.

---

## Who is behind this?

I work as a software engineer during the day — full-stack, mostly TypeScript and Java, with a fair amount of AWS and Kubernetes on the managed side. Studies in Business Informatics fill whatever time is left. This project lives in the gaps between both.

The honest reason this exists: managed cloud services are great at hiding complexity. After a while you stop understanding what is actually happening underneath and just trust that it works. This homelab is the counterweight to that. Running Kubernetes on bare metal, configuring a switch by hand, writing operators that talk to hardware APIs — these are things that do not come up in a day job where infrastructure is someone else's problem.

It is also just something I enjoy. Not everything needs a professional justification.

---

## What is being built here?

The cluster is the foundation, but it is not the goal. It is the environment where everything else runs and gets learned. Here is what that looks like in practice:

**Kubernetes on bare metal** — not managed, not abstracted. Custom CNI configuration, distributed block storage with Longhorn, real multi-node failure scenarios and the debugging that comes with them. Databases and message brokers — PostgreSQL, Redis, NATS — self-hosted and actually maintained.

**Virtualization with Proxmox** — the second world: a Minisforum MS-01 running Proxmox VE as the infrastructure anchor. OPNsense as router and firewall, a ZFS-backed NAS, DNS and the family-facing apps as VMs and LXC containers — plus reserve VMs that can join the Kubernetes cluster as extra nodes when needed.

**Go** is the language I have never used professionally and want to change that. The plan is to learn it by building things that run on the cluster itself: custom Kubernetes operators and cloud-native microservices.

**Python for hardware automation** — the nodes support Intel vPro, which is a hardware management interface that works independently of the operating system. The idea is to write tooling that talks to this layer: automated reboots, node isolation based on cluster health and power-triggered events from temperature or load metrics.

**Infrastructure as Code across the whole stack** — Terraform for the MikroTik and OPNsense network configuration, Ansible for bare-metal provisioning, GitHub Actions for CI and Argo CD for GitOps deployment. The goal is that nothing is configured manually without it being tracked somewhere.

**Next.js and Flutter** — a proper admin dashboard with real-time data and a mobile companion app for cluster monitoring and hardware control from a phone.

---

## Repository Structure

This repository is not only a codebase — it also serves as the primary documentation, guide and decision log for the entire project. Code, config, architecture decisions and setup instructions all live here together.

Where a section grows large enough to justify its own repository, it moves out and gets linked back from here. The same applies to third-party tools and open source projects in use — they get a reference entry rather than being copied in.

The top level is split into two big halves plus the things built on top: `setup/` is the physical world (hardware with its OS and network config in one place), `infrastructure/` is the software world (provisioning, cluster, platform services) — followed by the applications people use and the custom code written for this homelab.

```text
Homelab/
├── setup/                # The physical world
│   ├── compute/          #   The two compute worlds
│   │   ├── k8s-cluster/      # 3× Lenovo Tiny: bare-metal Kubernetes nodes
│   │   │   └── os/           #   Ubuntu Server now, Talos later
│   │   └── proxmox-cluster/  # 1× Minisforum MS-01: Proxmox VE host
│   │       └── os/           #   Proxmox VE + macOS USB workflow
│   ├── networking/       #   Network design, switch and router
│   │   ├── mikrotik/     #     Switch docs + Terraform
│   │   └── router/       #     OPNsense (VM): gateways, firewall zones
│   └── power-supply/     #   PSU, DC/DC conversion, fuse box
├── infrastructure/       # The software infrastructure
│   ├── provisioning/     #   Ansible: machines become consistent servers
│   ├── kubernetes/       #   Cluster core: bootstrap, Cilium, MetalLB, GitOps, operators
│   └── platform/         #   Shared services: DNS, ingress, storage, databases,
│                         #   messaging, security, observability, backup, ...
├── applications/         # User-facing apps: Nextcloud, Immich, Jellyfin, ...
├── services/             # Custom code: APIs, workers, operators
├── helm-charts/          # All Helm charts — mirrors the docs tree 1:1
├── automation/           # (planned) Cluster automation: Intel vPro, health triggers
├── dashboards/           # (planned) Monitoring panels and admin interfaces
└── apps/                 # (planned) Mobile and desktop companion apps
```

---

### 🔧 Setup — The Physical World

Hardware decisions and everything attached to them: each hardware area is a folder that also holds its living configuration — the compute nodes with their operating system, the network hardware with its design and Terraform.

| Path | Status | Content |
|---|---|---|
| [`/setup`](/setup) | ✅ Active | Shopping list, costs and reasoning across all hardware |
| [`/setup/compute`](/setup/compute) | ✅ Active | The two compute worlds and their operating systems |
| [`/setup/compute/k8s-cluster`](/setup/compute/k8s-cluster) | ✅ Active | The 3 Kubernetes nodes (CPU, RAM, storage) and the [OS running on them](/setup/compute/k8s-cluster/os) |
| [`/setup/compute/proxmox-cluster`](/setup/compute/proxmox-cluster) | ✅ Active | The MS-01 Proxmox host and its [Proxmox VE installation](/setup/compute/proxmox-cluster/os) |
| [`/setup/networking`](/setup/networking) | ✅ Active | Switch purchase, [network design](/setup/networking/design.md), [MikroTik config](/setup/networking/mikrotik) and the [router/firewall](/setup/networking/router) |
| [`/setup/power-supply`](/setup/power-supply) | ✅ Active | PSU, DC/DC conversion and fuse box |

### 🏗️ Infrastructure — The Software World

Everything code-defined between the hardware and the apps: provisioning, the cluster itself and the shared services on it.

| Path | Status | Content |
|---|---|---|
| [`/infrastructure/provisioning`](/infrastructure/provisioning) | ✅ Active | Ansible-based bare-metal node provisioning |
| [`/infrastructure/kubernetes`](/infrastructure/kubernetes) | ✅ Active | The cluster core only: bootstrap, Cilium (CNI), MetalLB, GitOps, operators |
| [`/infrastructure/platform`](/infrastructure/platform) | ✅ Active | Shared services on the cluster: DNS, ingress, storage, databases, messaging, security, observability, backup, registry, runtime |

### 📦 Applications

| Path | Status | Content |
|---|---|---|
| [`/applications`](/applications) | ✅ Active | User-facing apps: Nextcloud, Immich, Jellyfin and documented alternatives |

### 🚀 Deployment Assets

| Path | Status | Content |
|---|---|---|
| [`/helm-charts`](/helm-charts) | 🔜 Planned | All Helm charts, mirroring the docs tree — kept at top level so they can be referenced by Argo CD or moved to a dedicated repo later |
| [`/db-designs`](/db-designs) | 🔜 Planned | ER diagrams and design patterns for the hosted databases |

### ⚙️ Services

Backend services and microservices running on the cluster. Language-agnostic — implementations may live here directly or link out to a dedicated repository if the project grows large enough.

| Path | Status | Content |
|---|---|---|
| [`/services`](/services) | ✅ Active | Custom application services, APIs, workers and Kubernetes operators written for this homelab |

### 🤖 Automation

Scripts, controllers and tooling that interact with hardware, cluster health or external systems. Language-agnostic — same linking approach as services.

| Path | Status | Content |
|---|---|---|
| [`/automation`](/automation) | 🔜 Planned | Hardware automation, Intel vPro integrations, cluster event triggers |

### 📊 Dashboards

Everything visual — from simple metric displays to full admin controllers.

| Path | Status | Content |
|---|---|---|
| [`/dashboards`](/dashboards) | 🔜 Planned | Cluster monitoring panels, admin interfaces and real-time analytics |

### 📱 Apps

Mobile and desktop companion apps. If an app grows into a serious project it gets its own repository and is linked back from here.

| Path | Status | Content |
|---|---|---|
| [`/apps`](/apps) | 🔜 Planned | Mobile and desktop interfaces — may link to external repos |

---

## Component Layout Convention

Every component in this repository follows the same three-part layout, so both readers and future automation can find everything deterministically:

```text
<domain>/<...>/<component>/README.md       # 1. Documentation: what it is, why, alternatives
helm-charts/<domain>/<...>/<component>/    # 2. Helm chart / values — mirrors the docs path exactly
<domain>/<...>/<component>/terraform/      # 3. Optional Terraform for configuration
```

Catalog tables across the repository link these three locations as `docs` · `chart` · `config`. Chart and config directories are created when a component becomes active — a dead link there simply means "not deployed yet". Documented alternatives that will never be deployed get a `docs` link only.

Example for CoreDNS:

```text
infrastructure/platform/dns/coredns/README.md        # concept and decision
helm-charts/infrastructure/platform/dns/coredns/     # how it gets deployed
infrastructure/platform/dns/coredns/terraform/       # optional config IaC (zones, records)
```

The rules behind this:

- **Docs explain, charts deploy.** A README never contains manifests; a chart directory never explains concepts.
- **`helm-charts/` mirrors the docs tree 1:1.** Given any docs path, the chart path is derivable without lookup — which is what a one-click rebuild script or Argo CD needs. Keeping charts in one top-level tree also allows extracting them into a dedicated repo later without touching the documentation.
- **Terraform lives next to the component it configures** (`setup/networking/mikrotik/terraform/`, `infrastructure/platform/dns/coredns/terraform/`). Terraform here is configuration extras, not the deployment mechanism — so it stays close to the docs where a reader looks first. Automation checks one known location per component: if `terraform/` exists, apply it after the chart.

---

## The physical setup

Three Lenovo Tiny nodes sit side by side in 3D-printed 1U mounts with custom Keystone slots. A matte-black 1U patch panel with 0.25m slim patch cables keeps the dual network lines — management and data — routed cleanly to the switches. Next to them, the Minisforum MS-01 runs the Proxmox world. The goal was a setup that looks deliberate, not like a pile of hardware on a desk.

---

*Started small. Breaks occasionally. Gets better every time.*
