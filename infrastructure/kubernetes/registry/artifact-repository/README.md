# Artifact Repository

[<- Back to Container Registry](../README.md)

An Artifact Repository stores build outputs that should stay private: Docker images, npm packages, NuGet packages, Helm charts, binaries and generic release artifacts.

This is broader than Harbor. Harbor is excellent for container images and OCI artifacts, but a full-stack homelab also needs private package feeds for application development.

Software projects produce artifacts. A Docker image is an artifact. A Helm chart is an artifact. A private npm package, NuGet package, generated SDK or compiled binary is also an artifact.

An artifact repository stores those outputs so other systems can download known versions. CI publishes artifacts after building them. Developers and deployment tools pull artifacts later. This creates a controlled chain between source code, build output and deployment.

For beginners, the important distinction is that Git stores source code, while an artifact repository stores built or packaged outputs. Kubernetes should usually pull images from a registry, not build them directly from Git.

---

## Project Goal

The goal is one private internal place for:

- Docker and OCI images
- npm packages
- NuGet packages
- Helm charts
- generic binaries and release files
- internal libraries shared between services

This matters once custom services, shared TypeScript packages, .NET libraries, generated SDKs or internal tooling start to grow.

---

## Candidate Systems

| System | Location | Homelab recommendation | Business recommendation | Best fit | Notes |
|---|---|---|---|---|---|
| Sonatype Nexus Repository | Self-hosted | Recommended standard | Good | Multi-format private repositories | Strong practical candidate for Docker, npm, NuGet and Maven-style ecosystems |
| JFrog Artifactory | Self-hosted or external | Advanced | Recommended standard | Enterprise-grade artifact management | Very capable and broad package support, but may be heavier |
| Gitea Packages | Self-hosted | Good if Gitea is used | Limited | Git-integrated package registry | Good if Gitea becomes the internal Git platform |
| GitHub Packages | External | Optional | Good hosted option | Hosted package registry | Simple if private cloud hosting is acceptable |
| Harbor | Self-hosted | Container-image standard | Good for OCI workflows | Container images and OCI artifacts | Keep for image registry use cases, not full package management |

---

## Recommendation

Use Nexus Repository or Artifactory as the general artifact repository. Keep Harbor as a container-focused option if image scanning, OCI workflows or Kubernetes-native registry experiments become important.

For this homelab, Nexus is a strong first candidate because it is commonly used, supports the needed package formats and is easier to justify than a heavier enterprise Artifactory setup.

For a business-style standard, Artifactory is the stronger reference platform. For this homelab, Nexus is the more pragmatic first installation.

Check the current license, edition and feature limits before installing any repository product. The architecture decision should not depend on an outdated free-tier assumption.

---

## Strengths

- Central place for internal packages and release outputs.
- Makes CI/CD workflows repeatable and private.
- Supports versioned deployment artifacts for GitOps.
- Allows scoped publish and read credentials.
- Teaches software supply-chain concepts used in companies.

---

## Weaknesses

- Adds operational responsibility for storage, backups and access control.
- Package repositories can overlap, so product boundaries must be clear.
- Self-hosted artifact repositories need retention policies to avoid uncontrolled growth.
- Credentials must be managed carefully because publish tokens can affect the whole platform.

---

## Application Examples

- A private npm package contains shared TypeScript API clients.
- A private NuGet package contains shared .NET contracts or generated clients.
- CI builds Docker images and pushes them to the internal registry.
- Helm charts are published internally before Flux deploys them.
- A Go or Java service downloads internal tooling artifacts during build.

---

## Access And Security

The Artifact Repository should integrate with Rights Management and Secret Store:

- developers authenticate through SSO when possible
- CI/CD uses scoped publish tokens
- read tokens are separated from publish tokens
- apps do not receive package publishing credentials
- package tokens are stored in the Secret Store
- audit logs are retained for package publish and delete operations

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`. For the first evaluation, install one candidate and create separate repositories for each package type:

- Docker hosted repository for private images
- npm hosted repository for internal TypeScript packages
- NuGet hosted repository for private .NET packages
- raw or generic repository for binaries and release files

Then test one full loop:

1. build a Docker image
2. push it to the private repository
3. publish a private npm or NuGet package
4. pull both from a local development machine
5. configure CI tokens through the Secret Store

---

## Runtime Status

Artifact Repository is currently `⚫ Inactive`. It becomes important once private Docker images, npm packages or NuGet packages are produced by the project.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/registry/artifact-repository/
```

---

## References

- [Sonatype Nexus Repository documentation](https://help.sonatype.com/en/sonatype-nexus-repository.html)
- [JFrog Artifactory documentation](https://jfrog.com/help/r/jfrog-artifactory-documentation/jfrog-artifactory)
- [GitHub Packages documentation](https://docs.github.com/en/packages)
- [Gitea Packages documentation](https://docs.gitea.com/usage/packages/overview)
- [Wikipedia: Software repository](https://en.wikipedia.org/wiki/Software_repository)
- [Wikipedia: Package manager](https://en.wikipedia.org/wiki/Package_manager)
