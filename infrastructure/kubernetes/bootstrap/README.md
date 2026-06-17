# Kubernetes Bootstrap

[<- Back to Kubernetes](../README.md)

Bootstrap covers the first steps required to turn prepared nodes into a working cluster.

In the Ubuntu phase, this may involve kubeadm or another explicit installation path. In the Talos phase, bootstrap should be declarative and based on Talos machine configuration.

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

## Recommended Direction

For learning, start explicit and visible. A kubeadm-based Ubuntu cluster exposes the parts that matter: certificates, kubelet, container runtime, CNI install order and control plane components.

For the mature rebuild, prefer Talos. It removes SSH-based drift and makes node configuration declarative.

---

## Future Deployment Link

Bootstrap scripts and configuration should be linked here once they exist.
