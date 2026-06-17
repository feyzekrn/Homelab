# Flux

[<- Back to GitOps](../README.md)

Flux is the recommended first GitOps controller for this homelab.

It watches Git repositories and applies Kubernetes resources, Helm charts and Kustomize overlays to the cluster.

---

## Why It Fits

Flux fits the repository style well because future deployment files such as `HelmRelease`, `Kustomization` and values files can stay versioned and reviewed. It also keeps the cluster close to the principle: if it matters, it should be in Git.

---

## Used For

- reconciling platform services
- deploying Helm charts through HelmRelease resources
- applying Kustomize overlays
- managing environment-specific configuration
- reducing manual cluster drift

---

## Alternatives

| Alternative | Notes |
|---|---|
| Argo CD | Strong UI and application view |
| Raw Helm CLI | Simple, but easy to drift from Git |
| kubectl apply scripts | Useful for learning, weak long-term state management |

---

## Runtime Status

Flux is currently `⚫ Inactive`. It should become a core component once the cluster moves beyond manual learning steps.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/gitops/flux/
```
