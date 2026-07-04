# Kubernetes Bootstrap

[<- Back to Kubernetes](../README.md)

Bootstrap covers the first steps required to turn prepared nodes into a working cluster.

In the Ubuntu phase, this may involve kubeadm or another explicit installation path. In the Talos phase, bootstrap should be declarative and based on Talos machine configuration.

Bootstrap is the "cluster birth" phase. Before GitOps, ingress, storage or databases can exist, something must create the first working Kubernetes control plane and install the minimum components required for pods to run.

For beginners, this phase is often confusing because Kubernetes depends on several layers at once: Linux nodes, container runtime, kubelet, API server, controller manager, scheduler, etcd, CNI networking and kubeconfig access. Bootstrap is the documented sequence that turns those parts into a usable cluster.

Bootstrap is also different from normal application deployment. A GitOps controller can manage many things after it exists, but it cannot install itself into a cluster that does not exist yet. That first handoff must be explicit.

---

## Why This Matters

A cluster that cannot be rebuilt is only partially understood. Bootstrap documentation explains how to go from prepared hardware to the first working Kubernetes API. It should make rebuilds repeatable and reduce reliance on memory, terminal history or one-off commands.

In this homelab, bootstrap also marks the learning transition. The first Ubuntu/kubeadm phase should expose the Kubernetes internals. The later Talos phase should reduce mutable host drift and make node configuration more declarative.

---

## What Belongs Here

Document:

- chosen Kubernetes distribution or bootstrap method
- node roles
- control plane layout
- pod and service CIDR ranges
- kubeconfig handling
- first CNI installation
- first storage class
- GitOps handoff point

---

## Bootstrap Sequence

The exact commands are not defined yet, but the conceptual sequence should be:

1. Provision nodes through the chosen OS workflow.
2. Decide control plane and worker roles.
3. Create the first Kubernetes control plane.
4. Join worker nodes.
5. Install the CNI so pod networking works.
6. Confirm DNS and basic pod scheduling.
7. Install the first storage class if needed.
8. Install or hand off to the GitOps controller.
9. Let GitOps deploy the rest of the platform.

---

## Recommended Direction

For learning, start explicit and visible. A kubeadm-based Ubuntu cluster exposes the parts that matter: certificates, kubelet, container runtime, CNI install order and control plane components.

For the mature rebuild, prefer Talos. It removes SSH-based drift and makes node configuration declarative.

---

## Strengths Of The Two Phases

| Phase | Strength | Tradeoff |
|---|---|---|
| Ubuntu + kubeadm | Teaches Kubernetes internals and Linux-level setup | More mutable host state and more manual drift risk |
| Talos | Declarative, immutable Kubernetes node model | Less beginner-friendly if Kubernetes internals are not understood yet |

---

## What Not To Put Here

Do not put normal application deployment instructions here. Once the cluster can run workloads and GitOps exists, platform services should move into GitOps-managed Helm charts and Kustomize overlays.

Bootstrap should stay focused on the minimum process needed to create a usable cluster and hand control to the normal deployment system.

---

## Future Deployment Link

Bootstrap scripts and configuration should be linked here once they exist.

---

## Learning Links

- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
- [Kubernetes kubeadm documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
- [Talos Linux documentation](https://www.talos.dev/latest/introduction/what-is-talos/)
- [Wikipedia: Bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping)
