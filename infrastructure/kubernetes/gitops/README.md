# GitOps

[<- Back to Kubernetes](../README.md)

GitOps means the desired cluster state lives in Git and an in-cluster controller reconciles Kubernetes toward that state.

This is the natural operating model for this homelab once manual installation steps are understood.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Flux | Lightweight GitOps controller with strong HelmRelease support | [flux](./flux) |
| Argo CD | UI-focused GitOps platform and application dashboard | [argocd](./argocd) |

---

## Recommendation

Start with Flux if the goal is a clean Git-driven platform with HelmRelease resources. Evaluate Argo CD later if a strong visual application dashboard becomes important.

Do not run both unless there is a clear split of responsibility.
