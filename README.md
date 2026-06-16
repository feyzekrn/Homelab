# Bare-Metal Kubernetes Homelab Cluster

**A living documentation of building, breaking and rebuilding a self-hosted infrastructure — from raw hardware to production-grade services.**

---

## What is this?

Three budget mini PCs. One managed switch. A Kubernetes cluster running on a shelf at home.

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

**Kubernetes on bare metal** — not managed, not abstracted. Custom CNI configuration, distributed block storage with Longhorn, real multi-node failure scenarios and the debugging that comes with them. Databases and message brokers — PostgreSQL, MongoDB, Redis, RabbitMQ — self-hosted and actually maintained.

**Go** is the language I have never used professionally and want to change that. The plan is to learn it by building things that run on the cluster itself: custom Kubernetes operators and cloud-native microservices.

**Python for hardware automation** — the nodes support Intel vPro, which is a hardware management interface that works independently of the operating system. The idea is to write tooling that talks to this layer: automated reboots, node isolation based on cluster health and power-triggered events from temperature or load metrics.

**Infrastructure as Code across the whole stack** — Terraform for the MikroTik network configuration, Ansible for bare-metal provisioning, GitOps for application deployment. The goal is that nothing is configured manually without it being tracked somewhere.

**Next.js and Flutter** — a proper admin dashboard with real-time data and a mobile companion app for cluster monitoring and hardware control from a phone.

---

## Repository Structure

This repository is not only a codebase — it also serves as the primary documentation, guide and decision log for the entire project. Code, config, architecture decisions and setup instructions all live here together.

Where a section grows large enough to justify its own repository, it moves out and gets linked back from here. The same applies to third-party tools and open source projects in use — they get a reference entry rather than being copied in.

---

### 🔧 Hardware & Operating System

| Path                       | Status | Content |
|----------------------------|---|---|
| [`/setup`](/setup)         | ✅ Active | Hardware decisions, shopping list, specs, costs and reasoning |
| [`/os`](/os)               | ✅ Active | Operating system strategy, installation media and node OS decisions |

### 🏗️ Infrastructure

IaC for everything below the application layer — network, provisioning and core cluster components.

| Path | Status | Content |
|---|---|---|
| [`/infrastructure`](/infrastructure) | 🔜 Planned | Terraform (MikroTik), Ansible (bare-metal provisioning), core K8s components (CNI, Longhorn, MetalLB) |
| [`/helm-charts`](/helm-charts) | 🔜 Planned | Open source Helm charts in use and any custom charts created for this cluster |
| [`/db-designs`](/db-designs) | 🔜 Planned | ER diagrams and design patterns for the hosted databases |

### ⚙️ Services

Backend services and microservices running on the cluster. Language-agnostic — implementations may live here directly or link out to a dedicated repository if the project grows large enough.

| Path | Status | Content |
|---|---|---|
| [`/services`](/services) | 🔜 Planned | Microservices, APIs and Kubernetes operators |

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

## The physical setup

Three Lenovo Tiny nodes sit side by side in 3D-printed 1U mounts with custom Keystone slots. A matte-black 1U patch panel with 0.25m slim patch cables keeps the dual network lines — management and data — routed cleanly to the switches. The goal was a setup that looks deliberate, not like a pile of hardware on a desk.

---

*Started small. Breaks occasionally. Gets better every time.*
