# Kubernetes Cluster

[<- Back to Infrastructure](../README.md)

This directory documents the Kubernetes cluster itself — only the pieces that make the cluster exist and function.

Kubernetes is a platform for running containers across a group of machines. It schedules workloads, restarts failed containers, exposes services, mounts storage and provides a declarative API for infrastructure automation.

The boundary of this directory is deliberately narrow. Everything here answers one question: **what does it take to have a working, manageable cluster?** The services that run *on* the cluster — DNS, ingress, databases, observability, backups — live in [`../platform`](../platform). The apps people actually use live in [`../applications`](../../applications).

That boundary is the reading order of the whole repository:

1. [`../../setup`](../../setup): hardware and node operating systems (incl. [`../../setup/compute/os`](../../setup/compute/os))
2. [`../../setup/networking`](../../setup/networking): the physical network underneath everything
3. [`../provisioning`](../provisioning): turning machines into consistent servers
4. **this directory**: creating and operating the cluster
5. [`../platform`](../platform): shared services on the cluster
6. [`../../applications`](../../applications) and [`../../services`](../../services): what the platform is for

---

## Why This Matters

A cluster is not installed once; it is operated. Bootstrap decides how nodes become a cluster and how it can be rebuilt. The CNI decides how pods communicate at all. MetalLB decides how anything outside the cluster reaches a Service. GitOps decides how change enters the system. Operators decide how complex software is automated.

In a homelab, keeping these five concerns visible — instead of buried under a pile of app documentation — is exactly the understanding that managed cloud Kubernetes hides.

In companies, this layer is what platform teams own. Everything above it is negotiable per workload; this layer is shared fate.

---

## Component Catalog

Status meanings:

- `🟢 Active`: currently deployed or actively operated in the cluster
- `⚫ Inactive`: documented, planned or available for future use, but not currently running

Each row links up to three locations, following the [Component Layout Convention](../../README.md#component-layout-convention): `docs` (local README), `chart` (planned Helm chart under [`../../helm-charts`](../../helm-charts)) and `config` (optional Terraform next to the docs). Chart and config directories are created when a component becomes active.

`Idle RAM` is a rough per-instance ballpark at homelab scale; `/ node` values run on every node. The whole cluster core (Cilium, MetalLB, Flux) costs roughly 1 GB across three nodes — see the [platform catalog](../platform/README.md#how-to-read-this-catalog) for how to read the column.

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Bootstrap | [docs](./bootstrap) · [chart](../../helm-charts/infrastructure/kubernetes/bootstrap) · [config](./bootstrap/terraform) | ⚫ Inactive | — | The first process that creates the Kubernetes cluster | Unavoidable | 2026-06-17 |
| Cilium | [docs](./cilium) · [chart](../../helm-charts/infrastructure/kubernetes/cilium) · [config](./cilium/terraform) | ⚫ Inactive | ~150–200 MB / node | The pod network layer (CNI) for Kubernetes | Unavoidable CNI choice | 2026-06-17 |
| MetalLB | [docs](./metallb) · [chart](../../helm-charts/infrastructure/kubernetes/metallb) · [config](./metallb/terraform) | ⚫ Inactive | ~50 MB + ~50 MB / node | LoadBalancer IP provider for bare-metal clusters | Bare-metal standard | 2026-06-17 |
| Flux | [docs](./gitops/flux) · [chart](../../helm-charts/infrastructure/kubernetes/gitops/flux) · [config](./gitops/flux/terraform) | ⚫ Inactive | ~200–300 MB | GitOps controller that keeps the cluster synced from Git | Recommended standard | 2026-06-17 |
| Argo CD | [docs](./gitops/argocd) · [chart](../../helm-charts/infrastructure/kubernetes/gitops/argocd) · [config](./gitops/argocd/terraform) | ⚫ Inactive | ~0.5–1 GB | GitOps platform with a strong visual application UI | Optional alternative | 2026-06-17 |
| Operators | [docs](./operators) · [chart](../../helm-charts/infrastructure/kubernetes/operators) | ⚫ Inactive | ~50–150 MB each | Controllers that automate lifecycle of complex software (category) | Use selectively | 2026-06-17 |

---

## Directory Layout

```text
infrastructure/kubernetes/
├── bootstrap/
├── cilium/
├── metallb/
├── gitops/
│   ├── argocd/
│   └── flux/
└── operators/
```

---

## Placement Rule

Something belongs in this directory only when all of these are true:

- the cluster cannot exist or cannot be operated without deciding on it
- it is not a service that workloads consume (that is [`../platform`](../platform))
- users never interact with it directly (that is [`../applications`](../../applications))

Borderline example: CoreDNS as *cluster DNS* is installed by bootstrap and belongs to the cluster; CoreDNS as *LAN DNS for the homelab* is a platform service and is documented under [`../platform/dns`](../platform/dns).

---

## Deployment Rule

This directory answers what a component is and why the cluster needs it. Deployment assets follow the repository convention:

```text
../../helm-charts/infrastructure/kubernetes/<component>/    # Helm chart / HelmRelease values
./<component>/terraform/                  # optional Terraform for configuration
```

---

## Learning Links

- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
- [Kubernetes concepts documentation](https://kubernetes.io/docs/concepts/)
- [Wikipedia: Containerization](https://en.wikipedia.org/wiki/OS-level_virtualization)
- [Wikipedia: DevOps](https://en.wikipedia.org/wiki/DevOps)
