# Harbor

[<- Back to Container Registry](../README.md)

Harbor is a full-featured container registry with projects, access control, vulnerability scanning and image retention policies.

Harbor stores container images and OCI artifacts. Developers or CI pipelines push images to Harbor, and Kubernetes pulls those images when deploying workloads.

Compared with a minimal `registry:2` container, Harbor adds platform features: projects, users, robot accounts, vulnerability scanning, replication, retention rules and a web UI. That makes it useful for learning how private container registries are operated beyond a simple image store.

---

## Why It Fits

Harbor is useful once the homelab builds and runs multiple custom images. It teaches registry operations beyond simply pushing images to a public service.

It also fits a security learning path. A registry is part of the software supply chain, so access control, scanning, retention and image provenance matter.

---

## Used For

- hosting internal container images
- image retention policies
- vulnerability scanning experiments
- project-level access control
- robot accounts for CI/CD
- OCI artifact experiments

---

## Strengths

- Full-featured self-hosted container registry.
- Stronger governance than a plain registry.
- Supports projects, users and robot accounts.
- Can integrate image scanning and retention policies.
- Good learning tool for private Kubernetes image workflows.

---

## Weaknesses

- Heavier than using GitHub Container Registry or a plain registry.
- It focuses on images and OCI artifacts, not every package ecosystem.
- Needs storage, backup, SSO and token planning.
- Running it only for one or two images may not justify the overhead.

---

## Alternatives

| Alternative | Notes |
|---|---|
| GitHub Container Registry | Simple and good enough for many projects |
| Docker Hub | Common but rate limits and public defaults matter |
| Plain registry:2 | Lightweight, fewer platform features |
| Nexus Repository | Broader package repository, less container-specialized than Harbor |

---

## Runtime Status

Harbor is currently `⚫ Inactive`. Start with an external registry unless self-hosting images becomes a learning goal.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/registry/harbor/
```

---

## Learning Links

- [Harbor documentation](https://goharbor.io/docs/)
- [Open Container Initiative](https://opencontainers.org/)
- [Wikipedia: Container registry](https://en.wikipedia.org/wiki/Container_registry)
- [Kubernetes image documentation](https://kubernetes.io/docs/concepts/containers/images/)
