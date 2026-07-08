# Infrastructure

[<- Back to Repository Overview](../README.md)

This directory holds the software infrastructure of the homelab: how machines are provisioned, how the Kubernetes cluster is built, and which shared services run on it.

The physical world lives in [`../setup`](../setup) — hardware, switch, cabling, power and the node operating systems. This directory starts where the hardware ends: everything here is code-defined, rebuildable and documented per component.

The boundary between the three areas inside:

| Area | Question it answers |
|---|---|
| [`./provisioning`](./provisioning) | How does a freshly installed machine become a consistent server? |
| [`./kubernetes`](./kubernetes) | What makes the cluster exist and function? (bootstrap, CNI, MetalLB, GitOps, operators) |
| [`./platform`](./platform) | Which shared services run on the cluster? (DNS, ingress, storage, databases, security, observability, ...) |

User-facing apps deliberately live outside this directory in [`../applications`](../applications) — they consume the platform, they are not part of it. Custom code lives in [`../services`](../services).

---

## Reading Order

For a first read, follow the build order:

1. [`../setup`](../setup): hardware, network device configuration and node OS
2. [`./provisioning`](./provisioning): turning machines into consistent servers
3. [`./kubernetes`](./kubernetes): creating and operating the cluster
4. [`./platform`](./platform): the shared services on top
5. [`../applications`](../applications): what all of it is for

---

## Documentation Rule

Every component gets a local `README.md` and follows the [Component Layout Convention](../README.md#component-layout-convention): documentation here, the Helm chart under [`../helm-charts`](../helm-charts) at the mirrored path, and optional Terraform in a `terraform/` folder next to the docs.

```text
infrastructure/platform/dns/coredns/README.md        # docs
helm-charts/infrastructure/platform/dns/coredns/     # chart
infrastructure/platform/dns/coredns/terraform/       # config
```

---

## Learning Links

- [Wikipedia: Infrastructure as code](https://en.wikipedia.org/wiki/Infrastructure_as_code)
- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
- [Wikipedia: Platform engineering](https://en.wikipedia.org/wiki/Platform_engineering)
