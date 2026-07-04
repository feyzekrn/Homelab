# GitOps

[<- Back to Kubernetes](../README.md)

GitOps means the desired state of infrastructure lives in Git, and an automated controller continuously reconciles the real system toward that desired state.

This is the natural operating model for this homelab once manual installation steps are understood.

In a manual Kubernetes setup, an operator runs commands like `helm install`, `kubectl apply` or `kubectl edit` and the cluster changes immediately. That is easy while learning, but it creates an important problem: the cluster may contain changes that exist only in somebody's terminal history.

GitOps changes the workflow. Instead of treating the cluster as the source of truth, the repository becomes the source of truth. A change is made by editing files, reviewing the diff and merging the change. A controller inside the cluster notices the Git change and applies it. If somebody changes the cluster manually later, the controller can detect the drift and move the cluster back toward the declared Git state.

This model is related to Infrastructure as Code, but GitOps is more specific: it focuses on the reconciliation loop between Git and a running system. Kubernetes is a strong fit for GitOps because Kubernetes already uses declarative resources and controllers.

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

## CI/CD vs GitOps

CI/CD and GitOps are related, but they are not the same thing.

CI/CD usually describes the pipeline that tests, builds and publishes software. A CI pipeline might run unit tests, build a Docker image and push that image to a registry. A CD pipeline might deploy that image to an environment.

GitOps moves the deployment decision into Git. The pipeline can publish a new image, but the cluster changes when a Git commit updates the desired state, such as a Helm values file or an image tag. The GitOps controller then pulls the change from Git and reconciles the cluster.

This separation is useful because build systems and deployment systems have different responsibilities:

- CI proves that code can be built and tested.
- Artifact registries store versioned build outputs.
- GitOps repositories describe what should run.
- GitOps controllers make the cluster match that description.

---

## Strengths

- Changes are reviewable through normal Git pull requests.
- Rollback often means reverting a commit instead of reconstructing manual steps.
- The cluster can be rebuilt more easily because desired state is stored outside the cluster.
- Drift is easier to detect because manual changes differ from the declared state.
- Permissions can be narrower because users change Git instead of getting broad cluster-admin access.
- The same pattern scales from one homelab cluster to multiple environments.

---

## Weaknesses And Risks

- GitOps does not remove the need to understand Kubernetes, Helm or networking.
- Secret handling needs a separate design because plain secrets must not be committed to Git.
- Bootstrap remains a special problem: the first controller must still be installed somehow.
- A bad commit can break the cluster quickly if review and validation are weak.
- Running multiple GitOps tools without a clear boundary can create duplicate ownership and confusing drift behavior.

---

## When This Project Needs It

GitOps should become active after the first manual learning phase. Early manual installation is useful because it exposes the moving parts: CNI, storage classes, ingress, certificates and Helm values. Once those steps are understood, GitOps should take over so the homelab can be rebuilt from a documented state.

This project should use GitOps for platform services such as Cilium, MetalLB, Traefik, cert-manager, Longhorn, databases, observability and application releases. It should not be used as a place to hide unclear decisions. The documentation in this directory should explain why a component exists; the GitOps manifests should describe exactly how it is deployed.

---

## Components

| Path | Role |
|---|---|
| [`./flux`](./flux) | Kubernetes-native GitOps controller with strong HelmRelease and Kustomize support |
| [`./argocd`](./argocd) | UI-focused GitOps platform with application views, diffs and sync controls |

---

## Recommendation

Start with Flux if the goal is a clean Git-driven platform with HelmRelease resources. Evaluate Argo CD later if a strong visual application dashboard becomes important.

Do not run both unless there is a clear split of responsibility.

---

## Learning Links

- [Wikipedia: GitOps](https://en.wikipedia.org/wiki/GitOps)
- [Wikipedia: CI/CD](https://en.wikipedia.org/wiki/CI/CD)
- [Wikipedia: Infrastructure as code](https://en.wikipedia.org/wiki/Infrastructure_as_code)
- [OpenGitOps principles](https://opengitops.dev/)
- [Flux documentation](https://fluxcd.io/flux/)
- [Argo CD documentation](https://argo-cd.readthedocs.io/)
