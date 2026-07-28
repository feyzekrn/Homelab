# OPNsense

[← Back to Router & Firewall](../README.md)

OPNsense is an open-source firewall and routing platform based on FreeBSD, administered through a web interface and configurable through an API. It is the **chosen router** for this homelab and runs as a virtual machine on [`pve0`](../../../compute/proxmox-cluster).

Everything the [network design](../../design.md) describes on paper is implemented here: the gateway of each VLAN, the firewall rules between zones, DHCP, DNS forwarding and the connection to the internet.

---

## Why OPNsense

- **It is a platform, not an appliance.** Multi-VLAN routing, stateful firewalling, DHCP per interface, DNS, VPN, IDS/IPS and reporting come in one system — exactly the feature set the zone model needs.
- **The rules are readable.** Firewall rules are expressed per interface with aliases and are easy to reason about, which matters when the goal is to *understand* a trust model rather than to click one together.
- **It fits the "config as code" goal.** OPNsense exposes a full REST API and keeps its entire configuration in a single XML file, so the setup can be backed up, diffed and restored — and eventually managed through Terraform.
- **It virtualizes well.** A modest VM (2 vCPU, 2–4 GB RAM) routes far more than this network will ever carry, and snapshots make risky rule changes reversible.
- **Active, community-driven development** with a predictable release cadence and no feature paywall.

Against the alternatives: [pfSense](../pfsense) is the closest relative and equally capable, but its community edition has drifted behind a more commercial product strategy. OpenWrt shines on small routers and weak hardware, but its firewall and VLAN management get awkward at this number of zones. RouterOS as a virtual machine would keep everything in the MikroTik ecosystem, but its learning curve is steep and its firewall ergonomics are unfriendly for a first serious zone model.

---

## Role In The System

| Function | What it does here |
|---|---|
| Inter-VLAN routing | Owns the gateway IP of every VLAN — every zone crossing passes through it |
| Firewall | Enforces the trust zones from [`design.md`](../../design.md): home, k8s, services, management, IoT, DMZ |
| DHCP | Address assignment per VLAN, with static mappings for infrastructure |
| DNS | Forwards clients to AdGuard Home; resolves upstream when the filter is unavailable |
| NAT / WAN | The edge towards the internet once the home network moves behind it |
| VPN *(optional)* | WireGuard termination — a fallback path if NetBird is ever unavailable |

---

## Planned Setup

**Virtual machine on `pve0`**

- 2 vCPU, 2–4 GB RAM, small virtual disk — comfortably enough for a home network
- One virtual NIC on the **untagged trunk** to the switch: OPNsense creates its own VLAN interfaces (tags 10/20/30/40/50) on top of it, giving it a leg in every network from a single link
- A second NIC for the WAN side, facing the ISP uplink
- `onboot=1`, so the network comes back on its own after a host reboot

**On the switch:** the port towards the Proxmox host carries all VLANs tagged. The router creates no VLANs itself — tagging happens on the switch, addressing and rules happen here. That division is documented in [`design.md`](../../design.md).

**Bring-up order:** one zone at a time. First the cluster VLAN plus the home network, then management, then services, IoT last. Every zone is tested before the next one is added — five half-configured VLANs at once is the fastest way to spend an evening chasing a silent black hole.

---

## Operational Notes

- **The XML config is the source of truth.** Export it after every meaningful change; a restore rebuilds the entire router in minutes.
- **VLAN tags must match in three places** — switch port, OPNsense VLAN interface and the Proxmox guest tag. Nothing validates this for you, and a mismatch fails silently.
- **Snapshot before rule surgery.** A firewall rule that locks out the management interface is a classic; a VM snapshot turns that from an evening into a click.
- **mDNS does not cross VLANs.** Discovery protocols (AirPlay, Chromecast, HomeKit) need the mDNS repeater once media devices and services live in different zones.
- **Watch the dependency.** OPNsense shares fate with `pve0`. Anything that must survive a hypervisor outage — the rescue path to the vPro interfaces above all — must not depend on this router.

---

## Runtime Status

`⚫ Inactive` — planned as the first virtual machine on `pve0`, after the storage layout is in place. Until then the ISP router remains the gateway and the homelab runs in a flat network.

---

## Configuration Link

Configuration as code lives next to this page once the router exists:

```text
setup/networking/router/opnsense/terraform/
```

---

## Documentation

- [OPNsense documentation](https://docs.opnsense.org/)
- [OPNsense API reference](https://docs.opnsense.org/development/api.html)
- [Wikipedia: OPNsense](https://en.wikipedia.org/wiki/OPNsense)
