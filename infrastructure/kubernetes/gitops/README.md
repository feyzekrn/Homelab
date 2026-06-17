# GitOps

[<- Back to Kubernetes](../README.md)

GitOps means the desired cluster state lives in Git and an in-cluster controller reconciles Kubernetes toward that state.

This is the natural operating model for this homelab once manual installation steps are understood.

---

## Why This Matters

Manual cluster changes are easy at the beginning, but they do not scale. After a few services, it becomes hard to remember what was installed, which values were changed and how to rebuild the cluster after a failure.

GitOps moves that desired state into Git. The repository becomes the source of truth, and a controller applies the declared state to the cluster. This makes rebuilds, reviews, history and rollback much easier to reason about.

In a homelab, GitOps is the bridge from learning-by-hand to repeatable infrastructure. In companies, it is often part of the standard platform workflow because it gives reviewability, auditability and controlled rollout of infrastructure changes.

---

## What You Can Do With It

- deploy platform services from Git
- keep Helm values versioned
- review infrastructure changes before applying them
- rebuild cluster state after a wipe
- separate documentation from deployment assets
- reduce manual drift
- prepare for multi-environment layouts later

---

## Components

| Path | Role |
|---|---|
| [`./flux`](./flux) | Lightweight GitOps controller with strong HelmRelease support |
| [`./argocd`](./argocd) | UI-focused GitOps platform and application dashboard |

---

## Recommendation

Start with Flux if the goal is a clean Git-driven platform with HelmRelease resources. Evaluate Argo CD later if a strong visual application dashboard becomes important.

Do not run both unless there is a clear split of responsibility.
