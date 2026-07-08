# Network Design

[<- Back to Networking](./README.md)

This directory is reserved for network-level infrastructure: switch configuration, VLANs, routing, DNS, DHCP, firewall rules and physical topology.

The current target is a MikroTik-based network with a clear split between management traffic and cluster data traffic.

The network is the foundation underneath Kubernetes. Nodes need IP addresses, users need DNS names, services need reachable routes and exposed applications need firewall boundaries.

In a cloud environment, much of this is provided by the cloud provider. In a bare-metal homelab, the owner has to design it: which VLANs exist, which IP ranges are used, where DHCP runs, how DNS names resolve and which traffic is allowed between zones.

This directory documents those decisions so Kubernetes networking does not float in isolation. MetalLB, Traefik and service exposure depend on the physical and logical network being planned correctly.

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

| Name | Path | Status | Location | Recommendation | Role |
|---|---|---|---|---|---|
| MikroTik CRS310 | [docs](./mikrotik) · [config](./mikrotik/terraform) | ⚫ Inactive | Self-hosted hardware | Homelab network standard | Managed switch, VLANs, routing and service exposure |

---

## Learning Questions

- Which IP ranges are reserved for nodes, services and management?
- Which VLAN contains Kubernetes node traffic?
- Which network can access admin interfaces?
- Where does DNS live and how are internal names resolved? (planned answer: [`../../infrastructure/platform/dns`](../../infrastructure/platform/dns) — AdGuard Home as LAN resolver, CoreDNS for internal zones, handed out via MikroTik DHCP)
- Which IP range is reserved for MetalLB?
- Which services may be exposed outside the trusted LAN?

---

## Future Deployment Assets

Terraform or RouterOS configuration should be linked from here once created.

Expected future paths:

```text
setup/networking/mikrotik/terraform/   # Switch IaC lives next to its documentation
helm-charts/                  # Kubernetes deployments only, not switch config
```

Once Terraform modules exist, this README should link to the exact module and state backend notes.

---

## Learning Links

- [Wikipedia: Computer network](https://en.wikipedia.org/wiki/Computer_network)
- [Wikipedia: Virtual LAN](https://en.wikipedia.org/wiki/VLAN)
- [Wikipedia: Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol)
- [Wikipedia: Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System)
