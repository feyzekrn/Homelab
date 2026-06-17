# Container Registry

[<- Back to Kubernetes](../README.md)

A registry stores images and packages built for services and internal tooling.

The cluster can start without an internal registry by using public registries or GitHub Container Registry. A self-hosted registry becomes useful once there are many custom services, private packages or image scanning requirements.

---

## Components

| Component | Status | Location | Recommendation | Role | Documentation |
|---|---|---|---|---|---|
| Harbor | ⚫ Inactive | Self-hosted | Homelab container registry | Full-featured container registry | [harbor](./harbor) |
| Nexus Repository | ⚫ Inactive | Self-hosted | Homelab artifact standard | Docker, npm, NuGet and generic repositories | [artifact-repository](./artifact-repository) |
| JFrog Artifactory | ⚫ Inactive | Self-hosted or external | Business artifact standard | Enterprise-grade artifact management | [artifact-repository](./artifact-repository) |
| GitHub Packages | ⚫ Inactive | External | Optional hosted alternative | Hosted container and package registry | [artifact-repository](./artifact-repository) |
