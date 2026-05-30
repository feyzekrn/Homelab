# Bare-Metal Kubernetes Homelab Cluster

**A living documentation of building, breaking and rebuilding a self-hosted infrastructure — from raw hardware to production-grade services.**

---

## What is this?

Three budget mini PCs. One managed switch. A Kubernetes cluster running on a shelf at home.

This repository documents everything: the hardware decisions, the network design, the software stack and every problem I ran into along the way. It is not a polished tutorial and it is not meant to be. Things will break here, get rebuilt differently and evolve over time. If you are looking for a clean, finished reference — this is not that. If you are interested in watching something grow from scratch and seeing the real reasoning behind every decision, stick around.

If you spot something that could be done better, I am genuinely open to that conversation.

---

## Who is behind this?

I work as a software engineer during the day — full-stack, mostly TypeScript and C#, with a fair amount of AWS and Kubernetes on the managed side. Studies in Business Informatics fill whatever time is left. This project lives in the gaps between both.

The honest reason this exists: managed cloud services are great at hiding complexity. After a while you stop understanding what is actually happening underneath and just trust that it works. This homelab is the counterweight to that. Running Kubernetes on bare metal, configuring a switch by hand, writing operators that talk to hardware APIs — these are things that do not come up in a day job where infrastructure is someone else's problem.

It is also just something I enjoy. Not everything needs a professional justification.

---

## What is being built here?

The cluster is the foundation, but it is not the goal. It is the environment where everything else runs and gets learned. Here is what that looks like in practice:

**Kubernetes on bare metal** — not managed, not abstracted. Custom CNI configuration, distributed block storage with Longhorn, real multi-node failure scenarios and the debugging that comes with them. Databases and message brokers — PostgreSQL, MongoDB, Redis, RabbitMQ — self-hosted and actually maintained.

**Go** is the language I have never used professionally and want to change that. The plan is to learn it by building things that run on the cluster itself: custom Kubernetes operators and cloud-native microservices.

**Python / C, C++ for hardware automation** — the nodes support Intel vPro, which is a hardware management interface that works independently of the operating system. The idea is to write tooling that talks to this layer: automated reboots, node isolation based on cluster health and power-triggered events from temperature or load metrics.

**Infrastructure as Code across the whole stack** — Terraform for the MikroTik network configuration, Ansible for bare-metal provisioning, GitOps for application deployment. The goal is that nothing is configured manually without it being tracked somewhere.

**Next.js and Flutter** — a proper admin dashboard with real-time data and a mobile companion app for cluster monitoring and hardware control from a phone.

**C# and Java** - mainly my backend-languages which i am already good in but still love the code with (could be used for other application and probably makes no sense in some points but who cares, I never said I will do everything the right way ... sometimes we should stick to things we like the most)

---

## How it is documented

Each area of the project has its own section:

| Path | Content |
|---|---|
| `/setup` | Hardware decisions, full shopping list, specs and reasoning |
| `/talus` | OS configuration on the nodes |
| `/terraform` | Network infrastructure as code — VLANs and L3 routing on the MikroTik |
| `/k8s-infra` | Core cluster components: CNI, Longhorn, MetalLB |
| `/db-designs` | ER diagrams and design patterns for the hosted databases |
| `/k8s-apps` | GitOps declarations for databases, caches and logging |
| `/services-go` | Go microservices and Kubernetes operators |
| `/automation-py` | Hardware automation and vPro integrations |
| `/dashboard_next.js` | Web-based cluster management dashboard |
| `/mobile-flutter` | Cross-platform companion app |

The hardware build, cost breakdown and upgrade path are fully documented in [`/setup`](/setup). Everything in this README is intentionally kept at the project level so the two documents do not repeat each other.

---

## The physical setup

Three Lenovo Tiny nodes sit side by side in 3D-printed 1U mounts with custom Keystone slots. A matte-black 1U patch panel with 0.25m slim patch cables keeps the dual network lines — management and data — routed cleanly to the switches. The goal was a setup that looks deliberate, not like a pile of hardware on a desk.

---

*Started small. Breaks occasionally. Gets better every time.*