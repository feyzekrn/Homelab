# Argo CD

[<- Back to GitOps](../README.md)

Argo CD is a GitOps platform for Kubernetes with a strong web UI for inspecting applications, sync status, diffs and resource health.

It continuously compares the desired state in Git with the live state in the cluster. When the two differ, Argo CD shows the drift and can sync the cluster back to the desired state automatically or through a manual approval flow.

Argo CD is the GitOps tool many people first understand visually. It shows applications, the Kubernetes resources that belong to them and whether those resources match Git. A user can open the UI and see that an app is healthy, degraded, synced or out of sync.

For a beginner, this is useful because Kubernetes deployments otherwise feel invisible. Argo CD turns GitOps into a dashboard: Git says what should exist, the cluster shows what actually exists, and Argo CD highlights the difference.

---

## Why It Is Documented

Argo CD is one of the most common GitOps tools in Kubernetes environments. It is worth understanding even if Flux becomes the first choice for this repository.

Argo CD is especially relevant in teams where people want an application-centric view of the platform. It is common in organizations that need developers, platform engineers and operators to inspect deployment state without giving everyone direct cluster-admin workflows.

---

## Why It Might Fit Later

Flux is a better first match for this repository because the planned workflow is compact, Git-driven and HelmRelease-oriented. Argo CD becomes attractive if the homelab grows into many applications or if a visual dashboard becomes valuable for learning, demos or day-to-day operations.

Argo CD can also be useful when comparing GitOps models. Flux teaches the Kubernetes-controller-first approach. Argo CD teaches the application-dashboard approach.

---

## Used For

- visual application deployment tracking
- manual sync and diff inspection
- learning GitOps concepts through a UI
- multi-application platform views

---

## Strengths

- Excellent web UI for app health, resource trees, diffs and sync state.
- Easy for new users to understand because the cluster state is visible.
- Strong ecosystem around app-of-apps, ApplicationSets and multi-cluster views.
- Good fit for teams that want controlled manual sync or visual approvals.
- Common in production Kubernetes environments, so it is useful to learn.

---

## Weaknesses

- Heavier than Flux when the project only needs a Git-driven reconciler.
- The UI can encourage click-based operations if boundaries are not clear.
- It still needs a separate secret-management strategy.
- Running it together with Flux requires a strict ownership split to avoid duplicate reconciliation.

---

## Argo CD vs Flux

| Topic | Argo CD | Flux |
|---|---|---|
| Primary advantage | Visual application operations | Kubernetes-native declarative controllers |
| Best first impression | UI, resource tree and health state | Git, CRDs and controller reconciliation |
| Homelab timing | Later, when a dashboard helps | First GitOps controller |
| Risk | Duplicate ownership if paired badly | Less visual for beginners |

---

## Runtime Status

Argo CD is currently `⚫ Inactive`. It should be evaluated later if a visual GitOps application dashboard becomes useful. Running both Argo CD and Flux can be useful for learning, but creates duplicate responsibility if not clearly separated.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/kubernetes/gitops/argocd/
```

---

## Learning Links

- [Argo CD documentation](https://argo-cd.readthedocs.io/)
- [Argo CD ApplicationSet documentation](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/)
- [OpenGitOps principles](https://opengitops.dev/)
- [Wikipedia: GitOps](https://en.wikipedia.org/wiki/GitOps)
- [Wikipedia: Continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery)
