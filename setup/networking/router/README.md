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
- **terminate the internet connection** — the WAN cable from the ISP router goes **directly into a dedicated 2.5G port of the MS-01**, not through the switch, so untrusted traffic never becomes a VLAN on the switch at all

It deliberately does **not** do the heavy lifting between trusted zones. East-west traffic between the cluster and storage stays on the switch (and the NAS keeps a direct leg in the cluster VLAN), so the router never becomes the bottleneck of the homelab. The [switch documentation](../README.md) explains that split from the other side.

---

## Why It Runs As A Virtual Machine

The router is not a physical box in this design — it runs as a **VM on the Proxmox host** ([`pve0`](../../compute/proxmox-cluster)), connected to the switch through a single tagged trunk. All VLAN interfaces are virtual legs on that one link, the pattern commonly called *router on a stick*.

| | Why it is good here | What it costs |
|---|---|---|
| **Virtual** | No extra hardware, no extra power draw, snapshots before every risky rule change, config restored in minutes after a rebuild, 10G-capable NICs already present | The router shares fate with the hypervisor: if `pve0` is down or being upgraded, the whole network loses its gateway |

That trade-off is accepted knowingly, and it is the reason for two safeguards elsewhere in this project: the cross-watchdog responder that can power-cycle `pve0` through Intel vPro, and the option to let the switch route between the trusted VLANs so a rescue path does not run through the machine that is being rescued.

---

## The ISP Router Problem

Today the ISP router — a **Telekom Speedport** — is still the gateway of the house, and the homelab lives behind it. That is workable while the lab is flat, but it blocks the interim architecture in several concrete ways. These are worth listing precisely, because together they are the reason a **Fritz!Box 7490** is planned as its replacement.

### What the Speedport cannot do

| Limitation | What breaks because of it |
|---|---|
| **No static routes** | This is the big one. A phone in the home network that opens `jellyfin.home` sends the packet to its gateway — the Speedport — which has no idea that `10.0.20.0/24` lives behind OPNsense and drops it. Without a static route, **nothing in the home network can reach anything in the lab.** |
| **No DHCP reservations** | Every device that needs a stable address has to configure it statically and hope the DHCP pool never hands the same address to a phone. That is why `pve0` sits at `.250`, deliberately far above the pool — a workaround, not a solution. |
| **No custom DNS handout** | The router hands out *itself* as the DNS server and cannot be told to hand out another. That means [AdGuard Home](../../../infrastructure/platform/dns/adguard-home) cannot become the resolver for the household without touching every device by hand — no filtering, no split DNS, no internal names. |
| **No VLAN support (802.1Q)** | It cannot participate in a tagged network at all, so it can never be the gateway for more than one zone. |
| **Weak or absent bridge mode** | Putting a second router behind it produces double NAT, which complicates inbound paths and makes some protocols awkward. |

### What the Fritz!Box 7490 fixes

The 7490 is old hardware (2013) and deliberately not bought for performance — it is bought for the configuration surface a consumer router normally lacks:

- **Static routes** (*Heimnetz → Netzwerkeinstellungen → IPv4-Routen*): the one setting that makes the interim architecture work at all — `10.0.0.0/16` via the OPNsense address, and the home network can reach lab services.
- **A configurable DNS server for DHCP clients**: AdGuard becomes the resolver for the whole house through one field, instead of per device.
- **DHCP reservations** per MAC address, so infrastructure gets stable addresses properly.
- **Exposed Host** for cleanly forwarding everything inbound to OPNsense once it takes over.
- **A second life afterwards**: when the target architecture arrives and OPNsense becomes the only router, the 7490 does not become junk — it continues as **modem and WiFi access point** in IP-client mode behind OPNsense.

Being honest about its limits: the 7490 tops out at roughly 100 Mbit VDSL and WiFi AC, and it has no fibre modem. If the internet connection is or becomes faster than that, it is a bottleneck as the main router — which is a further argument for its long-term role as an access point rather than a gateway.

### The two paths, and why the purchase is still worth it

| Path | What it means | Static route needed? |
|---|---|---|
| **Home network stays in front** *(interim)* | Only the lab sits behind OPNsense; the ISP box remains the gateway for phones, TVs and laptops | **Yes** — which is exactly what the Speedport cannot provide and the Fritz!Box can |
| **Everything moves behind OPNsense** *(target)* | The ISP box degrades to a plain internet uplink; the home WLAN comes from an access point behind OPNsense, which becomes the gateway for every network | **No** — the problem disappears entirely, because one router knows all networks |

The target path removes the need for static routes altogether, so the Fritz!Box is not a permanent dependency. It is bought for the **transition**: the months in which the lab already has VLANs but the family still hangs on the ISP router. Without it, that phase either means no access from the home network to lab services, or an all-or-nothing switch to the final architecture in one evening — which is exactly the kind of big-bang change this project tries to avoid.

---

## Alternatives

| Name | Path | Status | Runs on | Recommendation | Role |
|---|---|---|---|---|---|
| OPNsense | [docs](./opnsense) | ⚫ Inactive | vm | Chosen router and firewall | Full routing, firewall, DHCP, DNS and VPN platform |
| Fritz!Box 7490 | — | ⬜ To buy | hardware | Planned interim gateway, then modem + access point | Replaces the Speedport for static routes and DNS handout |
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
