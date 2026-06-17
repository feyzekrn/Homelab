# Network Infrastructure

[<- Back to Infrastructure](../README.md)

This directory is reserved for network-level infrastructure: switch configuration, VLANs, routing, DNS, DHCP, firewall rules and physical topology.

The current target is a MikroTik-based network with a clear split between management traffic and cluster data traffic.

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

| Component | Status | Location | Recommendation | Role | Documentation |
|---|---|---|---|---|---|
| MikroTik CRS310 | ⚫ Inactive | Self-hosted hardware | Homelab network standard | Managed switch, VLANs, routing and service exposure | [mikrotik](./mikrotik) |

---

## Future Deployment Assets

Terraform or RouterOS configuration should be linked from here once created.

Expected future paths:

```text
helm-charts/              # Kubernetes only, not switch config
infrastructure/network/   # Documentation and network IaC references
```

If Terraform modules are added later, this README should link to the exact module and state backend notes.
