# Network Infrastructure

[<- Back to Infrastructure](../README.md)

This directory is reserved for network-level infrastructure: switch configuration, VLANs, routing, DNS, DHCP, firewall rules and physical topology.

The current target is a MikroTik-based network with a clear split between management traffic and cluster data traffic.

---

## Why This Matters

The network decides how nodes, users and services reach each other. In cloud Kubernetes, many networking details are hidden behind provider-managed load balancers and virtual networks. In a bare-metal homelab, those details are your responsibility.

In a homelab, documenting the network prevents confusion around IP ranges, VLANs, static addresses, DNS names and exposed services. It also makes it easier to safely experiment without mixing management access and application traffic.

In companies, network design is tied to segmentation, access control, compliance, routing, firewalling and availability. The homelab version should stay simpler, but it should still teach the same fundamentals.

---

## What You Can Do With It

- separate management and data traffic
- plan VLANs and address ranges
- define MetalLB LoadBalancer pools
- document switch ports and connected devices
- plan internal DNS names
- define firewall boundaries
- prepare Terraform or RouterOS-based network automation

---

## Scope

This area should document:

- MikroTik CRS310 configuration
- VLAN design
- management network
- Kubernetes node data network
- DHCP and static addressing strategy
- DNS zones for internal services
- firewall boundaries
- routing between homelab, LAN and internet

---

## Components

| Path | Status | Location | Recommendation | Role |
|---|---|---|---|---|
| [`./mikrotik`](./mikrotik) | ⚫ Inactive | Self-hosted hardware | Homelab network standard | Managed switch, VLANs, routing and service exposure |

---

## Future Deployment Assets

Terraform or RouterOS configuration should be linked from here once created.

Expected future paths:

```text
helm-charts/              # Kubernetes only, not switch config
infrastructure/network/   # Documentation and network IaC references
```

If Terraform modules are added later, this README should link to the exact module and state backend notes.
