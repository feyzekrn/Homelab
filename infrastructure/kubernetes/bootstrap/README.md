# Kubernetes Bootstrap

[<- Back to Kubernetes Cluster](../README.md)

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

## Prerequisites

| Requirement | Why |
|---|---|
| Three provisioned nodes | Hardware is already bought — see [k8s-cluster](../../../setup/compute/k8s-cluster) |
| [Ansible](../../provisioning/ansible) run against them | Container runtime, kubelet, `open-iscsi`, kernel settings, swap off |
| An IP plan | Node addresses, pod CIDR and service CIDR that collide with nothing |
| Network reachability between nodes | The flat interim network is enough; VLANs are not required to start |
| A decision on the [anchor node](../../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds) | Whether the `pve0` VM is a control-plane member or a worker — see below |

**The switch is not a prerequisite.** The three Tiny nodes are purchased and a cluster runs perfectly well on the current flat network at 1G. The CRS310 brings VLANs and 2.5G, both of which can be introduced underneath a running cluster later. Waiting for hardware that only changes the network layer delays the entire learning path for no reason.

### The control-plane decision

This is the one bootstrap choice that is expensive to change later, because it determines etcd quorum:

| Layout | etcd members | Consequence |
|---|---|---|
| 3 Tinys control plane + anchor as worker | 3 | Simple. Rebuilding all three Tinys loses the API server; the anchored pod keeps running but nothing can reschedule it |
| 2 Tinys + anchor as control plane | 3 | The API server survives a full Tiny rebuild — which is what makes the anchor genuinely resilient rather than partially |

The second is the better fit for the [bridge architecture](../../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds), and it costs nothing extra. Decide it before running `kubeadm init`, not after.

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
2. Decide control plane and worker roles — including the [anchor node](#the-control-plane-decision).
3. Create the first Kubernetes control plane.
4. Join the remaining nodes, including the `pve0` VM.
5. Install [Cilium](../cilium) so pod networking works — nodes stay `NotReady` until this is done.
6. Confirm cluster DNS and basic pod scheduling.
7. Install [MetalLB](../metallb), then [Longhorn](../../platform/storage/longhorn) as the first storage class.
8. Label the anchor node: `homelab/world=pve` and `node.longhorn.io/create-default-disk=false`.
9. Install [Argo CD](../gitops/argocd) and hand off.
10. Let GitOps deploy the rest of the platform.

Step 8 is easy to forget and awkward to notice: without the labels, Longhorn will happily place replicas on the anchor's virtual disk and the scheduling constraints that keep [Keycloak](../../platform/security/rights-management/keycloak) anchored have nothing to match on.

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
