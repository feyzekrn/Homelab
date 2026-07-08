# Helm Charts

[<- Back to Repository Overview](../README.md)

This directory holds all deployment assets for the cluster: Helm charts, values files and release definitions.

It is intentionally separate from the documentation and kept at the top level for two reasons:

- GitOps tools (Argo CD, Flux) can point at this one tree to install and update everything automatically.
- If deployments grow large enough, this whole directory can move to a dedicated repository without touching any documentation.

## Structure Convention

This tree **mirrors the documentation tree 1:1**. Given any docs path, the chart path is derivable without lookup — and vice versa:

```text
infrastructure/kubernetes/cilium/README.md   →  helm-charts/infrastructure/kubernetes/cilium/
infrastructure/platform/dns/coredns/README.md →  helm-charts/infrastructure/platform/dns/coredns/
applications/nextcloud/README.md              →  helm-charts/applications/nextcloud/
```

Optional Terraform for a component does **not** live here; it lives next to the component's documentation (e.g. `infrastructure/platform/dns/coredns/terraform/`). See the [Component Layout Convention](../README.md#component-layout-convention).

## Status

`🔜 Planned` — chart directories are created as components become active. Most documented components are still `⚫ Inactive`, so most chart paths referenced from the docs intentionally do not exist yet.
