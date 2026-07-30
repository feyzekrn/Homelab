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

### Why a Fritz!Box and not "one router less"

The obvious objection: OPNsense is already going to be a router — why buy another one? Because the Fritz!Box is not bought as a router:

- **The DSL line needs a modem, and a modem alone costs more.** A standalone VDSL modem runs 60–100 €; a used 7490 costs 20–40 € and brings the modem plus a router, WiFi and DECT. Paying more for less would be the strange decision here.
- **The household should not depend on the hypervisor.** Because it is there anyway, the Fritz!Box keeps serving the home network directly — phones, TVs and laptops never route through OPNsense. `pve0` can then be rebooted or broken in the middle of the evening without the family losing internet access. Lab outages stay lab outages.

The full three-device discussion, including whether the switch could be cheaper, is in the [networking overview](../README.md#wait--three-routers).

### What the Fritz!Box 7490 fixes

The 7490 is old hardware (2013) and deliberately not bought for performance — it is bought for the configuration surface a consumer router normally lacks:

- **Static routes** (*Heimnetz → Netzwerkeinstellungen → IPv4-Routen*): the one setting that makes the interim architecture work at all — `10.0.0.0/16` via the OPNsense address, and the home network can reach lab services.
- **A configurable DNS server for DHCP clients**: AdGuard becomes the resolver for the whole house through one field, instead of per device.
- **DHCP reservations** per MAC address, so infrastructure gets stable addresses properly.
- **Exposed Host** for cleanly forwarding everything inbound to OPNsense once it takes over.
- **A second life afterwards**: when the target architecture arrives and OPNsense becomes the only router, the 7490 does not become junk — it stays at the WAN edge as the **modem** terminating the DSL line.

Being honest about its limits: the 7490 tops out at roughly 100 Mbit VDSL and WiFi AC, and it has no fibre modem. If the internet connection is or becomes faster than that, it is a bottleneck as a gateway — another reason to reduce it to modem duty as soon as OPNsense takes over.

> ⚠️ **It cannot be modem and house WiFi at the same time.** As the modem it sits *in front of* OPNsense at the WAN edge; an access point has to sit *behind* OPNsense in the home VLAN. Its own WiFi would therefore land on the untrusted side of the firewall, which is exactly where the family should not be. So the household WLAN needs a **separate access point** on switch port 7 — and one that can tag VLANs, because it has to serve the home and IoT zones as separate networks. That purchase belongs to **phase 2 only** — as long as the interim setup runs, the Fritz!Box's own WLAN serves the house and no AP exists; see the phase table below and the [port assignment](../README.md#port-assignment--every-port-on-the-crs310).

### The two paths, and why the purchase is still worth it

| Path | What it means | Static route needed? |
|---|---|---|
| **Home network stays in front** *(interim)* | Only the lab sits behind OPNsense; the ISP box remains the gateway for phones, TVs and laptops | **Yes** — which is exactly what the Speedport cannot provide and the Fritz!Box can |
| **Everything moves behind OPNsense** *(target)* | The ISP box degrades to a plain internet uplink; the home WLAN comes from an access point behind OPNsense, which becomes the gateway for every network | **No** — the problem disappears entirely, because one router knows all networks |

The target path removes the need for static routes altogether, so the Fritz!Box is not a permanent dependency. It is bought for the **transition**: the phase — deliberately open-ended, see below — in which the lab already has VLANs but the family still hangs on the ISP router. Without it, that phase either means no access from the home network to lab services, or an all-or-nothing switch to the final architecture in one evening — which is exactly the kind of big-bang change this project tries to avoid.

### Where the house WiFi comes from in each phase

The two paths above are not just a routing question — they decide which device serves the household WLAN. This table spells it out, because it is easy to get confused about why an access point appears in the target design when the Fritz!Box "already has WiFi":

| Phase | Family gateway | House WiFi comes from | Separate AP needed? |
|---|---|---|---|
| **Today** | Speedport | Speedport | no |
| **Phase 1 — interim** *(current plan)* | Fritz!Box | The Fritz!Box's own WLAN | **no** |
| **Phase 2 — target** | OPNsense | Access point behind the switch (port 7) | **yes** |

The logic: in phase 1 the Fritz!Box is a normal home router — it routes the family *and* radiates the WLAN, exactly as consumer routers do. In phase 2 it is demoted to a modem *in front of* OPNsense, which puts its WiFi on the untrusted side of the firewall — anyone connecting there would stand outside every zone. At that moment, and only at that moment, the house needs a new WLAN source *behind* the firewall: the access point on switch port 7 (bought, or the old Speedport recycled as a dumb untagged AP for the home VLAN only).

### Why phase 2 is the better and safer design

Phase 2 is documented as the target because it is genuinely superior, not just tidier:

- **One router knows every network.** The static-route workaround disappears; nothing depends on a consumer box forwarding packets correctly into the lab.
- **The firewall finally covers the family.** In phase 1, home devices never pass OPNsense — the zone model only protects the lab from the house, not the house from anything. In phase 2, every WiFi client is a real member of VLAN 1: it reaches the apps, it can never reach Proxmox, the switch or vPro.
- **The IoT cage becomes real for wireless devices.** A VLAN-tagging AP serves a second SSID mapped to VLAN 40, so a smart plug shares airwaves with the family but can reach nothing except the MQTT broker. In phase 1, every wireless device — bulb or laptop — sits in the same flat home network.
- **DNS and DHCP are enforced, not offered.** OPNsense hands out AdGuard per zone and can block devices that try to bypass it (hardcoded DNS, DoH) — a Fritz!Box can only politely suggest a resolver.
- **One administration surface.** Firewall rules, leases, VPN and monitoring live in one UI instead of being split across OPNsense and a consumer router.

### Decision: staying in phase 1 for the foreseeable future

**This project deliberately stays in phase 1, with no date set for phase 2.** The reasoning, stated honestly so future-me does not mistake this for an oversight:

- **The added safety protects against threats that are not present yet.** Wireless zone enforcement matters once untrusted IoT devices exist and once services are exposed to the internet. Neither is the case today — the enterprise-grade WLAN zoning solves next year's problem at this year's cost.
- **Phase 2 has real switching costs.** It needs the VLAN-capable AP (~50–70 €), an evening of migration in which the whole house changes gateway, and from then on the family's internet shares fate with the OPNsense VM far more deeply. Phase 1 keeps the household on a boring appliance that never reboots because of a lab experiment.
- **The lab loses nothing.** All VLANs, firewall zones, the 10G trunk and the DMZ exist in full behind OPNsense either way — phase 1 only leaves the *wireless family devices* out of the zone model, not the infrastructure.

**What would trigger phase 2:** exposing services directly to the internet (the DMZ then earns its firewall), buying WiFi IoT devices that deserve the cage, an internet uplink faster than the 7490 can route, or simply the day the zone model itself becomes the thing worth learning. Until one of those happens, the interim architecture *is* the architecture.

---

## Alternatives

| Name | Path | Status | Runs on | Recommendation | Role |
|---|---|---|---|---|---|
| OPNsense | [docs](./opnsense) | ⚫ Inactive | vm | Chosen router and firewall | Full routing, firewall, DHCP, DNS and VPN platform |
| Fritz!Box 7490 | — | ⬜ To buy | hardware | Planned interim gateway, then modem | Replaces the Speedport for static routes and DNS handout |
| RouterOS 7 on the CRS310 | [switch docs](../mikrotik) | 🟡 Available | hardware | Held in reserve | The switch could route and filter by itself — see below |
| pfSense | [docs](./pfsense) | ⚫ Inactive | — | Documented alternative | The older, closely related BSD firewall distribution |
| OpenWrt | — | — | — | Not planned | Excellent on small hardware, weaker as a multi-VLAN firewall platform |

### The switch is already a router — so why add another one?

Worth stating clearly, because it is easy to miss: **the CRS310 runs RouterOS 7 and could do this job.** It has hardware Layer 3 routing, and RouterOS brings a genuinely stateful firewall (connection tracking, NAT, address lists) plus DHCP and DNS. A homelab built purely around it is a legitimate design — no VM, one device, hardware-speed inter-VLAN routing.

It is not chosen here for four reasons:

- **It merges the switch and the security boundary.** One configuration mistake would then affect both how packets move *and* who is allowed to reach what. Keeping them apart means the firewall can be rebuilt without the network going dark.
- **No snapshots, no easy rollback.** A firewall rule that locks out management is a rite of passage. On a VM that costs one click; on the switch it costs a reset button and a serial cable.
- **Firewall ergonomics.** RouterOS rules are ordered chains configured through Winbox or CLI. They are powerful and they are unforgiving — for a first serious zone model, OPNsense's per-interface rules with aliases and a visible rule table are the far better teacher.
- **Hardware offloading conflicts.** The moment connection tracking and firewall rules are active on a flow, RouterOS can no longer offload it to the switch chip — so the main argument for routing on the switch (wire-speed hardware forwarding) partly disappears precisely when it is used as a firewall.

What stays true: the capability is there and **held in reserve**. If inter-VLAN traffic ever measurably strains OPNsense, routing between the trusted zones can move to the switch through a transit network — and it is also the natural rescue path when the hypervisor that hosts OPNsense is the thing that broke.

*Not to be confused with **RouterOS CHR**, the same operating system packaged as a virtual machine. That would be a direct alternative to OPNsense and was ruled out for the same ergonomic reasons.*

The decision for OPNsense and the reasoning against the others is documented in [`opnsense`](./opnsense).

---

## Configuration Rule

This folder follows the same pattern as [`mikrotik`](../mikrotik): the device documentation lives next to its living configuration.

```text
setup/networking/router/opnsense/README.md      # what it is, why, how it is set up
setup/networking/router/opnsense/terraform/     # optional configuration as code
```
