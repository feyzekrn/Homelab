# Container Registry

[<- Back to Platform](../README.md)

A registry stores images and packages built for services and internal tooling.

The cluster can start without an internal registry by using public registries or GitHub Container Registry. A self-hosted registry becomes useful once there are many custom services, private packages or image scanning requirements.

Kubernetes usually runs container images. Those images must be stored somewhere before the cluster can pull and run them. A container registry is the storage and distribution system for those images.

Modern projects often need more than container images. They may also publish Helm charts, npm packages, NuGet packages, generated SDKs, binaries and release archives. That broader category is artifact management.

This directory separates Harbor from a general artifact repository because they overlap but are not identical. Harbor is strong for container images and OCI artifacts. Nexus or Artifactory can handle many package ecosystems in one place.

---

## Why This Matters

Every application that runs on Kubernetes eventually becomes an artifact: a container image, a Helm chart, a package, a generated client library or a release archive. A registry is the place where those artifacts are stored, versioned and retrieved.

In a small homelab, public registries are enough at the beginning. Once private services, shared packages or repeatable deployments appear, an internal registry becomes part of the delivery pipeline. It lets CI publish artifacts privately and lets the cluster pull known versions from a controlled location.

In a company, artifact management is a core supply-chain concern. Registries are tied to access control, vulnerability scanning, retention policies, provenance, audit logs and release promotion between environments.

---

## What You Can Do With It

- store private Docker and OCI images
- publish private npm and NuGet packages
- publish Helm charts for GitOps deployment
- separate read tokens from publish tokens
- scan images and artifacts for vulnerabilities
- keep internal libraries private
- reproduce deployments from versioned artifacts

---

## Components

| Name | Path | Status | Runs on | Idle RAM | Recommendation | Role |
|---|---|---|---|---|---|---|
| Harbor | [docs](./harbor) · [chart](../../../helm-charts/infrastructure/platform/registry/harbor) · [config](./harbor/terraform) | ⚫ Inactive | k8s | ~1–2 GB | Chosen registry | Images, Helm charts and OCI artifacts, with scanning and RBAC |
| Nexus Repository | [docs](./artifact-repository) · [chart](../../../helm-charts/infrastructure/platform/registry/artifact-repository) · [config](./artifact-repository/terraform) | ⚫ Inactive | k8s | ~1.5–2.5 GB | Planned later | npm, NuGet, Maven and generic packages — the formats Harbor cannot serve |
| GitHub Packages | [docs](./github-packages) | ⚫ Inactive | — | — (external) | Not planned | The free bridge for private npm until Nexus exists |
| Forgejo / Gitea | [docs](./forgejo) | ⚫ Inactive | — | ~0.3 GB | Documented alternative | Git server with a built-in multi-format package registry |
| JFrog Artifactory | [docs](./artifact-repository) | ⚫ Inactive | — | ~2–4 GB | Documented alternative | The commercial counterpart to Nexus, common in companies |

**The split that matters:** Harbor is an *OCI* registry — container images and Helm charts. It does not speak npm, Maven or NuGet. Anything in those formats needs a second system, which is why Nexus stays on the roadmap and GitHub Packages fills the gap in the meantime.

---

## Decision Guide

This homelab goes straight to [Harbor](./harbor), because custom images appear early and image scanning, robot accounts and retention policies are exactly the supply-chain concepts worth learning. [Nexus](./artifact-repository) follows only when private npm packages become real — until then [GitHub Packages](./github-packages) covers that need without a second server.

Do not install every registry product at once. Harbor and Nexus overlap for Docker images; run Harbor for containers and let Nexus handle the language ecosystems when it arrives.

---

## Learning Links

- [Wikipedia: Container registry](https://en.wikipedia.org/wiki/Container_registry)
- [Wikipedia: Software repository](https://en.wikipedia.org/wiki/Software_repository)
- [Open Container Initiative](https://opencontainers.org/)
- [Kubernetes image documentation](https://kubernetes.io/docs/concepts/containers/images/)
