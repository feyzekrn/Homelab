# Container Registry

[<- Back to Kubernetes](../README.md)

A registry stores images and packages built for services and internal tooling.

The cluster can start without an internal registry by using public registries or GitHub Container Registry. A self-hosted registry becomes useful once there are many custom services, private packages or image scanning requirements.

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

| Product | Path | Status | Location | Recommendation | Role |
|---|---|---|---|---|---|
| Harbor | [`./harbor`](./harbor) | ⚫ Inactive | Self-hosted | Homelab container registry | Full-featured container registry |
| Nexus Repository | [`./artifact-repository`](./artifact-repository) | ⚫ Inactive | Self-hosted | Homelab artifact standard | Docker, npm, NuGet and generic repositories |
| JFrog Artifactory | [`./artifact-repository`](./artifact-repository) | ⚫ Inactive | Self-hosted or external | Business artifact standard | Enterprise-grade artifact management |
| GitHub Packages | [`./artifact-repository`](./artifact-repository) | ⚫ Inactive | External | Optional hosted alternative | Hosted container and package registry |
