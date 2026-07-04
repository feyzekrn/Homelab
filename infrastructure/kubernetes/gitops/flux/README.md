# Flux

[<- Back to GitOps](../README.md)

Flux is the recommended first GitOps controller for this homelab. It is a Kubernetes-native system that watches Git repositories and other sources, then applies the declared Kubernetes resources to the cluster.

Flux is best understood as a set of controllers. Those controllers reconcile Git sources, Kustomize overlays, Helm charts, Helm releases, image updates and notifications. Instead of a human running `helm upgrade` manually, Flux reads the desired release state from Git and keeps the cluster aligned with it.

Flux is the tool that can make a Kubernetes cluster "follow" a Git repository. If the repository says Traefik should run with a specific Helm chart version and a specific values file, Flux applies that state. If the repository later changes, Flux updates the cluster. If somebody changes the cluster manually and the change conflicts with Git, Flux can reconcile it back.

For a beginner, the important idea is reconciliation. Flux does not just run once like a script. It keeps checking whether reality matches the desired state. This is the same mental model Kubernetes itself uses for Deployments, Services and other resources.

---

## Why It Is A Standard GitOps Choice

Flux is a CNCF GitOps project and is widely used in Kubernetes environments that prefer declarative resources over UI-driven workflows. It fits well with Kubernetes because its configuration is expressed as Kubernetes custom resources such as `GitRepository`, `Kustomization`, `HelmRepository` and `HelmRelease`.

That design makes Flux easy to store in Git and easy to review. The deployment workflow becomes visible in normal YAML resources instead of being hidden in a separate deployment server UI. This is especially useful in a homelab because the same repository can explain the platform and deploy it.

---

## Why It Fits

Flux fits the repository style well because future deployment files such as `HelmRelease`, `Kustomization` and values files can stay versioned and reviewed. It also keeps the cluster close to the principle: if it matters, it should be in Git.

It is also a good first choice because it does not require a large web UI to be useful. The main workflow is Git, Kubernetes resources and `flux` CLI inspection. That is a better fit for a documentation-first platform where understanding the state matters more than clicking through a dashboard.

---

## Used For

- reconciling platform services
- deploying Helm charts through HelmRelease resources
- applying Kustomize overlays
- managing environment-specific configuration
- reducing manual cluster drift

---

## Strengths

- Strong Kubernetes-native model based on custom resources.
- Excellent fit for HelmRelease and Kustomize workflows.
- Pull-based reconciliation from inside the cluster, so CI does not need broad cluster credentials.
- Small operational footprint compared with heavier UI-centered platforms.
- Works naturally with pull requests, branch history and commit review.
- Image automation can update image tags in Git when that pattern is desired.

---

## Weaknesses

- The default experience is CLI/YAML-first, so beginners may miss a visual application dashboard.
- Debugging requires understanding Flux resources, events and controller logs.
- It does not solve secret management by itself; External Secrets, SOPS, Sealed Secrets or another strategy is still needed.
- It can feel abstract until the relationship between Git sources, Kustomizations and HelmReleases is understood.

---

## Flux vs Argo CD

| Topic | Flux | Argo CD |
|---|---|---|
| Primary workflow | Git, Kubernetes resources and CLI | Git plus strong web UI |
| Best fit | Platform-as-code, HelmRelease, Kustomize, compact operations | Visual app management, manual sync inspection, team dashboards |
| Learning curve | YAML/controller concepts first | UI makes state easier to inspect early |
| Operational style | Lightweight and composable | More product-like platform |
| Homelab recommendation | First choice | Evaluate later if a UI becomes important |

---

## Application Examples

- Flux installs Cilium after bootstrap and keeps the CNI configuration versioned.
- Flux deploys Traefik from a Helm chart and applies the local values file.
- Flux applies a `Kustomization` for `observability` after storage and networking are ready.
- A future CI pipeline builds an image, updates an image tag in Git and lets Flux roll it out.
- A cluster rebuild installs Flux first, then Flux restores the rest of the platform from Git.

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

## Operating Notes

Before enabling Flux, decide the repository layout for environments, Helm values and shared components. Bootstrap should be documented carefully because Flux cannot reconcile itself until the first controller installation is complete.

For this homelab, Flux should not be responsible for raw hardware provisioning, MikroTik configuration or personal password management. It should reconcile Kubernetes resources and link to the systems that own those other concerns.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/gitops/flux/
```

---

## Learning Links

- [Flux documentation](https://fluxcd.io/flux/)
- [Flux GitOps Toolkit components](https://fluxcd.io/flux/components/)
- [OpenGitOps principles](https://opengitops.dev/)
- [Wikipedia: GitOps](https://en.wikipedia.org/wiki/GitOps)
- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
