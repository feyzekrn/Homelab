# Argo CD

[<- Back to GitOps](../README.md)

Argo CD is a GitOps platform for Kubernetes with a strong web UI for inspecting applications, sync status, diffs and resource health.

It continuously compares the desired state in Git with the live state in the cluster. When the two differ, Argo CD shows the drift and can sync the cluster back to the desired state automatically or through a manual approval flow.

Argo CD is the GitOps tool many people first understand visually. It shows applications, the Kubernetes resources that belong to them and whether those resources match Git. A user can open the UI and see that an app is healthy, degraded, synced or out of sync.

For a beginner, this is useful because Kubernetes deployments otherwise feel invisible. Argo CD turns GitOps into a dashboard: Git says what should exist, the cluster shows what actually exists, and Argo CD highlights the difference.

---

## Why It Is Chosen

Argo CD is the **chosen GitOps controller** for this cluster, and the deciding factor is what it makes visible. Both controllers implement reconciliation correctly, so the difference that matters here is pedagogical: Argo CD shows the application tree, the live-versus-declared diff and the sync status of every resource in a UI. That is exactly the feedback loop that turns GitOps from an abstract principle into something observable while learning it. [Flux](../flux)'s state lives in CRDs and controller logs — leaner, but a harder place to learn from.

The second reason is trajectory: [Argo Rollouts](../argo-rollouts) comes from the same project family, so blue/green and canary releases later are an addition to a familiar tool rather than a new one.

Argo CD is also the more common choice in the environments this project is preparing for. It is widely used in organizations that need developers, platform engineers and operators to inspect deployment state without giving everyone direct cluster-admin workflows.

---

## What It Runs On

Argo CD runs **on the Kubernetes cluster** (`k8s`) — it is a cluster component by definition and reconciles only cluster resources. It has no authority over the Proxmox world: the guests on [`pve0`](../../../../../setup/compute/proxmox-cluster) are defined as code separately, because Argo CD reconciles Kubernetes resources and nothing else. Two worlds, two deployment mechanisms.

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
| Decision here | **Chosen** — the visible diff is the learning tool | Documented alternative, deliberately not run alongside |
| Risk | UI can encourage click-ops if boundaries are loose | Less visual while learning |

---

## Runtime Status

Argo CD is `⚫ Inactive` and is the **chosen GitOps controller**. It becomes active once the cluster runs and the first components move from manual installation into Git. The visual application tree and live-versus-declared diffs are the deciding argument while learning GitOps; [Flux](../flux) stays documented as the alternative and is deliberately not run alongside it.

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
