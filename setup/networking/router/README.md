# 🧭 Router & Firewall — The Gateway Layer

[← Back to Networking](../README.md)

**In this folder:** [`opnsense`](./opnsense) — the chosen router/firewall with its configuration and Terraform · [`pfsense`](./pfsense) — documented alternative.

The switch decides *where a frame goes*. The router decides *whether it may go there at all*, and how one network reaches another. This folder covers the second half of the [network design](../design.md): the device that owns every VLAN gateway, enforces the trust zones and terminates the connection to the internet.

---

## Its Role In This Homelab

The router is the only component that touches every part of the system. Concretely it will:

- **be the gateway of every VLAN** — one IP per zone (k8s, services, management, IoT, DMZ), so every packet that crosses a zone boundary passes through it
- **enforce the trust model** — the firewall rules from [`design.md`](../design.md) are implemented here: IoT reaches nothing but the MQTT broker, the family reaches apps but never management, exposed services sit caged in the DMZ
- **hand out addresses and answer name queries** — DHCP per VLAN, DNS forwarding to AdGuard Home
- **terminate the internet connection** — NAT, edge filtering, and later the WAN side of the home network itself

It deliberately does **not** do the heavy lifting between trusted zones. East-west traffic between the cluster and storage stays on the switch (and the NAS keeps a direct leg in the cluster VLAN), so the router never becomes the bottleneck of the homelab. The [switch documentation](../README.md) explains that split from the other side.

---

## Why It Runs As A Virtual Machine

The router is not a physical box in this design — it runs as a **VM on the Proxmox host** ([`pve0`](../../compute/proxmox-cluster)), connected to the switch through a single tagged trunk. All VLAN interfaces are virtual legs on that one link, the pattern commonly called *router on a stick*.

| | Why it is good here | What it costs |
|---|---|---|
| **Virtual** | No extra hardware, no extra power draw, snapshots before every risky rule change, config restored in minutes after a rebuild, 10G-capable NICs already present | The router shares fate with the hypervisor: if `pve0` is down or being upgraded, the whole network loses its gateway |

That trade-off is accepted knowingly, and it is the reason for two safeguards elsewhere in this project: the cross-watchdog responder that can power-cycle `pve0` through Intel vPro, and the option to let the switch route between the trusted VLANs so a rescue path does not run through the machine that is being rescued.

---

## The Home Router Problem

Today the ISP router (Telekom Speedport) is still the gateway of the house, and the homelab lives behind it. That arrangement has a hard limit: **a device in the home network that wants to reach a lab address asks the ISP router for the way, and that router cannot be taught one.** Consumer ISP boxes offer no static routes.

There are two ways out, and they decide whether a router purchase is needed at all:

| Path | What it means | Static route needed? |
|---|---|---|
| **Home network stays in front** | Only the lab sits behind OPNsense; the ISP box remains the gateway for phones, TVs and laptops | **Yes** — and the Speedport cannot do it, so this path requires replacing it with a router that can (a Fritz!Box, for example) |
| **Everything moves behind OPNsense** *(target)* | The ISP box degrades to a plain internet uplink; the home WLAN comes from an access point behind OPNsense, which becomes the gateway for every network | **No** — the problem disappears entirely, because one router knows all networks |

The second path is the goal, which is why no router purchase is planned for now. A future physical device may still join later — most likely as **modem and access point** rather than as a router, or as a dedicated firewall appliance if the virtual router ever needs to become independent of the hypervisor.

---

## Alternatives

| Name | Path | Status | Runs on | Recommendation | Role |
|---|---|---|---|---|---|
| OPNsense | [docs](./opnsense) | ⚫ Inactive | vm | Chosen router and firewall | Full routing, firewall, DHCP, DNS and VPN platform |
| pfSense | [docs](./pfsense) | ⚫ Inactive | — | Documented alternative | The older, closely related BSD firewall distribution |
| OpenWrt | — | — | — | Not planned | Excellent on small hardware, weaker as a multi-VLAN firewall platform |
| RouterOS (CHR) | — | — | — | Not planned | Would keep everything in the MikroTik world, but is a steep, CLI-first learning curve |

The decision for OPNsense and the reasoning against the others is documented in [`opnsense`](./opnsense).

---

## Configuration Rule

This folder follows the same pattern as [`mikrotik`](../mikrotik): the device documentation lives next to its living configuration.

```text
setup/networking/router/opnsense/README.md      # what it is, why, how it is set up
setup/networking/router/opnsense/terraform/     # optional configuration as code
```
