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

| Name | Path | Status | Location | Recommendation | Role |
|---|---|---|---|---|---|
| Harbor | [docs](./harbor) · [chart](../../../helm-charts/infrastructure/platform/registry/harbor) · [config](./harbor/terraform) | ⚫ Inactive | Self-hosted | Homelab container registry | Full-featured container registry |
| Nexus Repository | [docs](./artifact-repository) · [chart](../../../helm-charts/infrastructure/platform/registry/artifact-repository) · [config](./artifact-repository/terraform) | ⚫ Inactive | Self-hosted | Homelab artifact standard | Docker, npm, NuGet and generic repositories |
| JFrog Artifactory | [docs](./artifact-repository) | ⚫ Inactive | Self-hosted or external | Business artifact standard | Enterprise-grade artifact management |
| GitHub Packages | [docs](./artifact-repository) | ⚫ Inactive | External | Optional hosted alternative | Hosted container and package registry |

---

## Decision Guide

Start with an external registry such as GitHub Container Registry if the project only has a few private images. Add a self-hosted registry when the homelab needs to learn supply-chain operations, image scanning, internal package feeds or fully local artifact hosting.

Do not install every registry product at once. Harbor and Nexus can overlap for Docker images. Choose the product based on whether the main goal is container-image operations or broad package management.

---

## Learning Links

- [Wikipedia: Container registry](https://en.wikipedia.org/wiki/Container_registry)
- [Wikipedia: Software repository](https://en.wikipedia.org/wiki/Software_repository)
- [Open Container Initiative](https://opencontainers.org/)
- [Kubernetes image documentation](https://kubernetes.io/docs/concepts/containers/images/)
