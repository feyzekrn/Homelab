# Flux

[<- Back to GitOps](../README.md)

Flux is a Kubernetes-native GitOps system that watches Git repositories and other sources, then applies the declared Kubernetes resources to the cluster.

In this homelab, Flux is the **documented alternative** to [Argo CD](../argocd), which is the chosen GitOps controller. It is not planned for deployment — this page exists because Flux is the other half of the standard GitOps comparison, and a decision deserves a documented loser, not just a winner.

Flux is best understood as a set of controllers. Those controllers reconcile Git sources, Kustomize overlays, Helm charts, Helm releases, image updates and notifications. Instead of a human running `helm upgrade` manually, Flux reads the desired release state from Git and keeps the cluster aligned with it.

Flux is the tool that can make a Kubernetes cluster "follow" a Git repository. If the repository says Traefik should run with a specific Helm chart version and a specific values file, Flux applies that state. If the repository later changes, Flux updates the cluster. If somebody changes the cluster manually and the change conflicts with Git, Flux can reconcile it back.

For a beginner, the important idea is reconciliation. Flux does not just run once like a script. It keeps checking whether reality matches the desired state. This is the same mental model Kubernetes itself uses for Deployments, Services and other resources.

---

## Why It Is A Standard GitOps Choice

Flux is a CNCF GitOps project and is widely used in Kubernetes environments that prefer declarative resources over UI-driven workflows. It fits well with Kubernetes because its configuration is expressed as Kubernetes custom resources such as `GitRepository`, `Kustomization`, `HelmRepository` and `HelmRelease`.

That design makes Flux easy to store in Git and easy to review. The deployment workflow becomes visible in normal YAML resources instead of being hidden in a separate deployment server UI. This is especially useful in a homelab because the same repository can explain the platform and deploy it.

---

## Why It Lost — And What Would Change That

The case for Flux is real: `HelmRelease`, `Kustomization` and values files stay versioned and reviewed, it needs no web UI to be useful, and its footprint is a fraction of Argo CD's (~200–300 MB against ~0.5–1 GB). For a purely declarative, documentation-first platform that is an honest fit.

It lost on one criterion — **visibility while learning**. Flux's state lives in CRDs, events and controller logs, which means understanding "what does the cluster think it should be running, and how does that differ from reality?" requires knowing which resources to inspect first. Argo CD answers that question on a screen. Since learning GitOps is an explicit goal here rather than a means to an end, the heavier tool that shows its work won.

What would reverse the decision: if the cluster ever runs unattended and the UI stops being read, Argo CD's RAM becomes rent paid for nothing — and Flux becomes the better tenant.

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
| Idle RAM | ~200–300 MB | ~0.5–1 GB |
| Decision here | Documented alternative — not deployed | **Chosen GitOps controller** |

---

## What It Would Look Like Here

Not the plan — but the shape of the alternative, for comparison against [how Argo CD does it](../argocd):

- a `GitRepository` resource points at this repository and a `Kustomization` reconciles it
- a `HelmRelease` deploys Traefik from its chart with the local values file
- `Kustomization` dependencies order the stack: CNI, then storage, then observability
- image automation updates a tag in Git when CI publishes a new build
- a cluster rebuild installs Flux first, and Flux restores everything else from Git

The last point is the property both tools share, and the reason either is worth running: the cluster is rebuildable from the repository rather than from memory.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Argo CD | Strong UI and application view |
| Raw Helm CLI | Simple, but easy to drift from Git |
| kubectl apply scripts | Useful for learning, weak long-term state management |

---

## Runtime Status

Flux is `⚫ Inactive` and **not planned**. [Argo CD](../argocd) is the chosen GitOps controller for this cluster — see the [GitOps overview](../README.md#recommendation) for the reasoning. This page stays because Flux is the other half of the standard GitOps comparison, and because that decision deserves a documented loser, not just a winner.

---

## Operating Notes — Valid For Either Tool

Two constraints apply regardless of which controller is chosen, and both are worth stating once:

- **Bootstrap is a special case.** The first controller cannot reconcile itself into existence; it has to be installed by hand or by [`bootstrap`](../../bootstrap) before it can take over.
- **A GitOps controller owns Kubernetes resources and nothing else.** Bare-metal provisioning belongs to [Ansible](../../../provisioning/ansible), switch and router configuration to [Terraform](../../../../setup/networking/mikrotik), Proxmox guests to the Proxmox world, and human passwords to [Vaultwarden](../../../platform/security/password-manager/bitwarden). Widening a GitOps controller past the cluster boundary is how it becomes the thing nobody understands.

---

## Learning Links

- [Flux documentation](https://fluxcd.io/flux/)
- [Flux GitOps Toolkit components](https://fluxcd.io/flux/components/)
- [OpenGitOps principles](https://opengitops.dev/)
- [Wikipedia: GitOps](https://en.wikipedia.org/wiki/GitOps)
- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
