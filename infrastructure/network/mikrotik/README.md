# MikroTik

[<- Back to Network Infrastructure](../README.md)

MikroTik is the planned network foundation for this homelab.

The current target device is the MikroTik CRS310. It should provide the managed switching and routing layer needed for a realistic bare-metal Kubernetes setup.

MikroTik is a vendor of routers, switches and wireless networking equipment. RouterOS is the operating system used on many MikroTik devices. In this homelab, the MikroTik device is expected to handle the network layer around the Kubernetes cluster.

That means it is responsible for practical things: VLANs, switch ports, routing, firewall rules, DHCP, static addresses and possibly DNS forwarding. Kubernetes does not replace these responsibilities. Kubernetes networking sits on top of the physical and routed network.

---

## Why It Fits

MikroTik hardware is powerful enough for serious networking experiments while still being affordable for a homelab.

For this project, it is especially useful because Kubernetes on bare metal needs the operator to understand real networking: VLANs, routing, firewall rules, DHCP, DNS and LoadBalancer IP ranges.

The CRS310 is also relevant because a homelab cluster benefits from faster LAN links and managed switching while still staying under direct local control.

---

## Used For

- 2.5G data network between cluster nodes
- management network separation
- VLAN experiments
- static IP planning
- routing between LAN and cluster networks
- firewall boundaries
- MetalLB address pool planning
- future Terraform-managed RouterOS configuration

---

## Strengths

- Powerful feature set for the price.
- Strong learning value for real routing, VLAN and firewall concepts.
- Good fit for self-contained homelab networking.
- RouterOS can be exported and potentially automated.
- Supports more low-level control than many simplified home-network systems.

---

## Weaknesses

- Steeper learning curve than consumer or UniFi-style interfaces.
- Misconfiguration can break management access.
- RouterOS concepts should be documented carefully to avoid "works but unknown" setups.
- Business environments may prefer different support models or managed network platforms.

---

## Planned Network Areas

| Area | Purpose |
|---|---|
| Management network | Out-of-band or admin access to nodes and hardware |
| Cluster data network | Kubernetes node, pod and service traffic |
| Service IP range | MetalLB LoadBalancer addresses |
| Internal DNS | Stable names for dashboards and platform services |
| Firewall rules | Explicit boundaries between LAN, management and cluster services |

---

## Application Examples

- MetalLB receives a dedicated address range from the MikroTik-managed network.
- Traefik gets a stable LoadBalancer IP and routes HTTP(S) services.
- Management interfaces stay separate from application traffic.
- Node replacement is easier because static addressing and naming are documented.
- Terraform can eventually apply RouterOS configuration from Git.

---

## Comparison Notes

| System | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| MikroTik RouterOS | Self-hosted hardware | Recommended | Good for small business and labs | Powerful, affordable, steep learning curve |
| UniFi | Self-hosted controller plus hardware | Good | Good SMB fit | Easier UI, less low-level control |
| pfSense / OPNsense | Self-hosted firewall/router | Good | Good edge firewall option | Strong firewalling, separate switch still needed |
| Cloud-managed networking | External/cloud-managed | Optional | Common business model | Less self-contained learning |

---

## Hands-On Start

Start manually before automating:

1. Document physical ports and connected devices.
2. Assign management IPs to the switch and nodes.
3. Define VLANs for management and cluster traffic.
4. Reserve a LoadBalancer range for MetalLB.
5. Test basic routing and DNS before installing Kubernetes services.

Once the design is stable, move configuration into Terraform or RouterOS export files.

---

## Runtime Status

MikroTik networking is currently `⚫ Inactive` in this repository. The hardware and configuration should become active before Kubernetes service exposure is configured.

---

## Future IaC Link

Planned configuration location:

```text
../../../infrastructure/network/mikrotik/
```

If Terraform is used later, this README should link to the exact module and state backend notes.

---

## Documentation

- [MikroTik RouterOS documentation](https://help.mikrotik.com/docs/)
- [MikroTik CRS310 product page](https://mikrotik.com/product/crs310_8g_2s_in)
- [Wikipedia: MikroTik](https://en.wikipedia.org/wiki/MikroTik)
- [Wikipedia: RouterOS](https://en.wikipedia.org/wiki/RouterOS)
