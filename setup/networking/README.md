# 🔌 Networking — Switches & Physical Topology

[← Back to Setup Overview](../README.md)

**In this folder:** [`design.md`](./design.md) — VLANs, DHCP, firewall zones and addressing · [`cabling.md`](./cabling.md) — cable colours, per-device port assignment and the shopping list · [`mikrotik`](./mikrotik) — switch configuration docs and Terraform · [`router`](./router) — the gateway layer: OPNsense as router and firewall.

The network is built by two devices with a clean division of labour: the **switch** carries the VLANs and moves frames at wire speed, the **router** owns every VLAN gateway and enforces the trust zones. This page covers the physical side — switch, patch panel, cabling; the router has its [own folder](./router).

---

## The Whole Picture

Every cable and every zone of the target design in one view:

```text
                      ┌──────────────────────────┐
   Internet ──────────┤  ISP router / Fritz!Box  │   modem + WAN edge
                      └────────────┬─────────────┘
                                   │  1× RJ45 — the only internet cable
                                   ▼
        ┌──────────────────────────────────────────────────┐
        │  pve0 — Minisforum MS-01 (Proxmox VE)            │
        │                                                  │
        │   [OPNsense VM]  gateway + firewall of all zones  │
        │   [NAS/shares]   ZFS pool: media, photos, backups │
        │   [Caddy]  [AdGuard]  [cloudflared]  [Vaultwarden]│
        │   [family apps: Jellyfin · Immich · Nextcloud]    │
        └────────────────────────┬─────────────────────────┘
                                 │  SFP+ 1 — 10G trunk, all VLANs tagged
                                 ▼
        ┌──────────────────────────────────────────────────┐
        │  MikroTik CRS310  —  pure Layer 2, VLAN tagging   │
        └──┬────────┬────────┬─────────┬───────┬───────────┘
           │1,2,3   │4,5,6   │  7      │  8    │ SFP+2
           ▼        ▼        ▼         ▼       ▼
      node0–2   node0–2   pve0 mgmt  WiFi AP  free
      (2.5G)    (1G)      (2.5G)     (tagged)
      VLAN 10   VLAN 60   VLAN 30    VLAN 1+40
      🔵 data   🟡 uplink  🔴 mgmt    ⚪ trunk
         │
         └── bare-metal Kubernetes: apps, Home Assistant, Longhorn, Traefik
```

Every cable above has a colour, and the colour is the plane it belongs to — 🔵 homelab data, 🟡 internet uplink, 🔴 management, ⚪ tagged trunk. The full scheme, the per-device port assignment and the shopping list live in [`cabling.md`](./cabling.md).

| Zone | VLAN | Who lives there | Reachable from |
|---|---|---|---|
| Home | 1 (untagged) | Family phones, laptops, TVs | Internet; apps via 80/443 only |
| Kubernetes | 10 | The three nodes, MetalLB range | Home (apps), management |
| Services | 20 | NAS shares, family app containers | Home (apps), k8s (storage paths) |
| Management | 30 | Proxmox UI, switch, `pve0` admin NIC, OPNsense GUI | Admin laptop and NetBird only |
| IoT | 40 | Plugs, sensors, cameras | Nothing — may only reach the MQTT broker |
| DMZ | 50 | Anything exposed to the internet | Tunnel only; may reach its own dataset |
| Uplink | 60 | The nodes' onboard 1G ports, and their vPro/AMT engines | Management only — outbound to the internet, nowhere else |

The rule behind the zones: **traffic is filtered where a decision is needed and switched where only throughput is needed.** Cluster-to-cluster and cluster-to-storage traffic stays inside a VLAN and never touches the router; anything crossing a trust boundary goes through OPNsense. Details and firewall rules live in [`design.md`](./design.md).

---

## Core Switch: MikroTik CRS310-8G+2S+IN

The central switch for the whole cluster. Bought new, because this switch brings real features that actually matter for Kubernetes.

| Part | Details |        Price | Where to find it |
|---|---|-------------:|---|
| MikroTik CRS310-8G+2S+IN | 8× 2.5G ports + 2× SFP+ |      ~ 180 € | [MikroTik official](https://mikrotik.com/product/crs310_8g_2s_in) · [Amazon](https://www.amazon.de/s?k=MikroTik+CRS310-8G%2B2S%2BIN) |

### Why this switch and not a cheap unmanaged 2.5G switch?

Kubernetes is not just about port speed. The nodes constantly talk to each other — for pod networking, Longhorn replication, databases and message brokers. If all that cluster traffic has to travel through your home router (in my case just a simple noob router with 1Gbit/s traffic per port), you lose all the benefits of 2.5G immediately. The MikroTik solves this with **Layer 3 routing**: it routes IP traffic directly between the nodes without a single packet ever leaving the switch to hit the router.

Specially for k8s its biggest advantage is its Marvell-Switch-Chip which enables the routing (also inbetween VLAN or subnets) directly on hardware level. This keeps the speed up
and avoids the CPU running hot with such easy tasks. So the communication ping of the mini-pcs stays extremely low so we can reach nearly real 2.5 Gbit/S per port without package loss.

RouterOS 7 comes with a GUI, CLI and REST API. That means you can build traffic dashboards, set alerts, manage the entire network config as code and experiment with VLANs for cleaner network separation. The two SFP+ ports also leave room to grow: a faster uplink, a NAS connection or a second switch can be added later without replacing the core hardware.

According to best practices in networking, at least for the internal traffic the home router shouldn't been abused for handling the traffic inside also then 
If you already have a fast router with Layer 3 features you could use a cheaper unmanaged switch instead — but then all of the above goes away.

### The Hidden Danger: Why Your Home Router Shouldn't Touch Cluster Traffic

Following enterprise networking best practices, a Kubernetes infrastructure should always leverage **Tier-2 Networking (Distribution Layer)**. By isolating your heavy cluster traffic on its own dedicated distribution layer, you ensure maximum internal performance while keeping your daily home life stable. 

Forcing dense internal cluster traffic through a standard home router or ISP box can have severe consequences for your entire household:
1. **Severe Bufferbloat & Ping Spikes:** When storage solutions like Longhorn replicate gigabytes of data across nodes, your home router's CPU will instantly redline. This results in massive latency spikes, causing online games to lag, Netflix streams to buffer, and web pages to load quälend langsam.
2. **NAT Table Overflows & Crashes:** Kubernetes pods, databases, and brokers spin up thousands of concurrent connections. Simple home routers have tiny session tables. When these overflow, the router freezes entirely, dropping the internet connection for everyone in the house.

Even if you own a high-end Layer 3 router, pairing it with a cheap unmanaged switch is a mistake. Inter-VLAN traffic would still have to travel up to the router and back (**Hairpinning**), destroying your low latencies and bottlenecking your cluster.

> **Update — how this reads with [OPNsense](./router) in the picture:**
> The warning above is about *ISP boxes*, and it stays true: consumer routers must never carry cluster traffic. It is not an argument that Layer 3 has to live on the switch. A properly sized firewall on a 10G trunk routes between VLANs comfortably, and this project starts exactly there: **OPNsense routes everything, the switch stays pure Layer 2.** The switch's Layer 3 capability is held in reserve for two cases — if inter-VLAN traffic ever measurably strains the firewall, and as a rescue path that does not run through the hypervisor hosting the router.
>
> **Neither device replaces the other.** OPNsense is needed no matter how much the switch can route: a switch does stateless port filtering at best, while the trust model in [`design.md`](./design.md) — home may not reach management, IoT may reach nothing but the MQTT broker, an exposed app stays caged in its DMZ — requires a **stateful firewall**, and DHCP, DNS and the internet edge live there too. The switch's job is the opposite one: keeping bulk traffic away from the firewall. That matters more now that the MS-01 hangs on the same switch — NAS transfers, cluster backups and VM traffic all cross it, and every one of those flows that stays Layer 2 is a flow the router never has to touch. Firewall where decisions are needed, switch where only throughput is needed.

### Port Plan — Current Target (3 nodes + MS-01)

**The internet does not enter the switch.** The ISP router connects with a single cable directly into one of the MS-01's own 2.5G ports, where OPNsense terminates it as its WAN interface. Everything else — cluster data, management and all Proxmox guests — travels over one **SFP+ trunk** carrying every VLAN tagged.

```text
                         ISP router (internet)
                                  │  🟡
                                  │  ← WAN, straight into pve0 (2.5G #1)
                                  ▼
[  node0   ]──  2.5G M.2  ──┐  [ pve0 (MS-01) ]
[  node0   ]── 1G onboard ──┤        │      │
[  node1   ]──  2.5G M.2  ──┤    🔵  │      │  🔴 2.5G #2 — management
[  node1   ]── 1G onboard ──┼── MikroTik CRS310 ──┘   VLAN 10/20/30/40/50 tagged
[  node2   ]──  2.5G M.2  ──┤        10G SFP+ trunk
[  node2   ]── 1G onboard ──┘
   🔵 2.5G = homelab data      🟡 1G = internet uplink
```

**Why the WAN bypasses the switch.** Untrusted internet traffic never becomes a VLAN on the switch at all, which removes an entire class of mistakes: no WAN VLAN to misconfigure, no chance of a tagging error putting the raw internet next to the cluster. The MS-01 has two spare RJ45 ports, so it costs nothing — and it frees a switch port as a side effect.

The only price is a physical dependency: the cable from the ISP router has to reach the MS-01. Since both live next to each other, that is not a real constraint.

### Port Assignment — Every Port On The CRS310

This is the full target wiring once [OPNsense](./router) is the router. `Untagged` means the connected device knows nothing about VLANs and the switch attaches the tag; `tagged` means the device speaks 802.1Q itself and several VLANs share the cable.

| Port | Connected to | Mode | VLAN | Speed | Cable |
|---|---|---|---|---|---|
| **1** | `node0` — 2.5G M.2 adapter | untagged, PVID 10 | 10 — k8s | 2.5G | 🔵 blue |
| **2** | `node1` — 2.5G M.2 adapter | untagged, PVID 10 | 10 — k8s | 2.5G | 🔵 blue |
| **3** | `node2` — 2.5G M.2 adapter | untagged, PVID 10 | 10 — k8s | 2.5G | 🔵 blue |
| **4** | `node0` — onboard NIC | untagged, PVID 60 | 60 — uplink | 1G | 🟡 yellow |
| **5** | `node1` — onboard NIC | untagged, PVID 60 | 60 — uplink | 1G | 🟡 yellow |
| **6** | `node2` — onboard NIC | untagged, PVID 60 | 60 — uplink | 1G | 🟡 yellow |
| **7** | `pve0` — 2.5G RJ45 #2 | untagged, PVID 30 | 30 — management | 2.5G | 🔴 red |
| **8** | WiFi access point | **tagged** | 1 (home), 40 (IoT) — one SSID per VLAN | 2.5G | ⚪ white |
| **SFP+ 1** | `pve0` (MS-01) | **tagged trunk** | 10, 20, 30, 40, 50 — all zones | 10G | 🩵 OM3 fibre |
| **SFP+ 2** | *free* | — | reserve: second trunk (LACP), dedicated NAS link, second switch | 10G | — |
| *(none)* | ISP router / modem | — | **not on the switch** — goes directly into `pve0` 2.5G RJ45 #1 as WAN | — | 🟡 yellow |

Four things are worth reading out of that table:

- **The two tagged ports carry the whole design.** SFP+ 1 is what lets OPNsense have a leg in every zone over one cable, and port 8 is what lets one access point serve the family WLAN and a separate IoT WLAN as genuinely different networks.

> ⚠️ **Port 8 dictates what kind of access point can be bought.** Serving two zones from one device requires an AP that supports **multiple SSIDs with a VLAN tag per SSID** (802.1Q). A cheap repeater or a consumer router in bridge mode cannot do this — it would put every wireless device into a single network, and the IoT zone would exist on paper only. Devices that can: TP-Link Omada EAP series (~50–70 €), Ubiquiti UniFi (~100 €+), or any OpenWrt-capable router used as an AP. This is a planned purchase, not something already owned — and a **phase 2 purchase only**: while the interim setup runs, the Fritz!Box's own WLAN serves the house and port 8 stays empty. The phase table and the decision to stay interim are documented in the [router](./router/README.md#where-the-house-wifi-comes-from-in-each-phase) folder.
- **Node cabling is split by plane, not by speed.** The fast M.2 adapters carry homelab traffic in VLAN 10; the onboard ports carry nothing but internet uplink in VLAN 60. Both are untagged, so a node never sees a VLAN tag and never needs a VLAN-aware bridge. Node administration rides the blue leg together with the rest of the lab — details and the reasoning in [`cabling.md`](./cabling.md).
- **`pve0` gets a management port of its own** (port 7, red). Without it, the machine hosting OPNsense could only be reached through OPNsense. This is the one port the previous plan did not have, and it is what a fourth node now costs.
- **The switch itself lives in VLAN 30.** Its management IP belongs in the same zone as `pve0`'s admin NIC and the Proxmox web UI — reachable from the admin laptop and through NetBird, from nowhere else.

> ⚠️ **VLAN 60 is not an internet zone, despite the name on the cable.** The Tinys' vPro/AMT engine is bound to the onboard NIC, so out-of-band management sits in VLAN 60 whether that is convenient or not. It has to be firewalled as a management zone: outbound to the internet, reachable inbound from VLAN 30 only, and never merged into the home VLAN.

Interim state, before OPNsense exists: everything runs untagged in one flat network and the ISP router remains the gateway. The port assignment above only becomes real when the router does.

### Maxed Switch Setup

**The switch is already full at three nodes.** 3× data + 3× uplink + `pve0` management + access point = exactly 8 RJ45 ports. Neither the MS-01's trunk (SFP+) nor the internet uplink (direct into the MS-01) competes for them, but there is no reserve left either.

```text
[  node0   ]──  2.5G M.2  ──┐  🔵
[  node0   ]── 1G onboard ──┤  🟡
[  node1   ]──  2.5G M.2  ──┤  🔵
[  node1   ]── 1G onboard ──┤  🟡 ── MikroTik CRS310 ──┬── SFP+ 1: pve0 (trunk)
[  node2   ]──  2.5G M.2  ──┤  🔵                      └── SFP+ 2: free
[  node2   ]── 1G onboard ──┤  🟡
[   pve0   ]── 2.5G  mgmt ──┤  🔴
[  WiFi AP ]── tagged 1+40 ─┘  ⚪
```

A fourth node needs two ports that do not exist. The way out is the [Netgear GS308](#uplink-extension-netgear-gs308-when-scaling-horizontally) below, taking over the **yellow uplink plane** — the 1G ports were never going to saturate a cheap switch anyway, and moving them frees three CRS310 ports at once.

The older version of this plan reached four nodes on the same eight ports. The port that was traded away is `pve0`'s management NIC — an admin path into the hypervisor that does not depend on the router VM it hosts. That is worth more than a node slot the project does not need yet.

---
 
## Patch Panel: 10" 12-Port Keystone, **Feed-Through**

Every device in this design lives in the same rack, and every cable is a short patch cable. That decides the panel type: it must accept a **plugged patch cable on the back and another on the front** — a *feed-through* panel (German: *Durchgangs-Patchpanel*), fitted with RJ45 coupler keystones that are a socket on both sides.

**This is the one detail that is easy to get wrong when ordering.** Most 10" panels ship with **LSA / punch-down** keystones (*Anlegetechnik*), which terminate solid installation cable with a punch tool and have no rear socket at all. They are the right module for a run that comes out of a wall, and the wrong one for a rack where the other end of every cable is three centimetres away.

✅ = bought (August 2026)

| | Part | Details | Price |
|:--:|---|---|---:|
| ✅ | **GeeekPi 10" 12-port keystone panel**, unbestückt | **0.5U**, empty frame, DeskPi RackMate compatible | **12,99 €** |
| ✅ | **deleyCON Cat.6a RJ45 feed-through keystone**, 12-pack | Socket/socket coupler, tool-less clip-in, **shielded** | **28,99 €** (2,42 €/ea) |
| ✅ | **ROLINE LC/LC duplex OM3 keystone** | Fibre coupler, black, for the [10G trunk on port 10](./cabling.md#why-the-fibre-goes-through-the-panel-after-all) | **4,29 €** |

Buying the frame empty and the modules separately landed at **46,27 €** — near enough to the ~36 € estimated that the conclusion holds: no money is saved by a panel with punch-down keystones included, and its modules would go straight into a drawer. The frame itself is agnostic; any keystone panel takes any keystone.

**The panel that was bought is 0.5U, not 1HE.** That is better than planned rather than a compromise — it is half the rack height for the same twelve ports, and it is dimensioned for the DeskPi RackMate the rest of the rack is built around. The consequence is purely geometric and it matters for cable lengths: twelve ports sit in **one row across the full width**, while the CRS310 clusters its eight ports in **two rows on the left half**. See [the switch has two port rows, the panel has one](./cabling.md#the-switch-has-two-port-rows-the-panel-has-one).

The 10" format matches the 3D-printed 1U rack mount used for the Tiny nodes. Twelve ports covers the current build — 6 node cables, `pve0`'s management port, and the drops that enter the rack from outside (WAN cable from the Fritz!Box, the access point, an admin laptop jack) — with two spare.

### What the panel is actually worth here

Worth being honest, because a feed-through panel does not *terminate* anything: it inserts two extra mated connector pairs into every link and buys organisation, not electrical function. At Cat.6a over well under 5 m that insertion loss is irrelevant, so the question is only whether the organisation is worth ~36 €. Two things say yes in this specific rack:

- **The switch side stops being touched.** Servicing or swapping a Tiny node means unplugging at the back of the panel; the front face and the switch ports keep their layout and their labels. Without a panel, every node move is a hand behind the switch.
- **It is what makes the colour scheme readable.** A fixed, labelled front row of eight coloured cables in port order is the thing you can read at a glance. A bundle running directly from three PCs into a switch is not, no matter what colour it is.

**The 10G fibre link to `pve0` now lives on this panel too** — port 10, via an LC-duplex keystone. This page originally argued the opposite, and the reversal is a direct consequence of the keystone format: converting a port to LC-duplex turned out to be a 4,29 € part rather than a future project, and the same argument that justifies the panel for copper (*the switch side stops being touched*) applies with more force to the one link whose transceivers are the most delicate parts in the rack. The measured cost is ~0.3 dB out of a 2.9 dB budget. Reasoning in [`cabling.md`](./cabling.md#why-the-fibre-goes-through-the-panel-after-all).

> ⚠️ **Check rack depth before ordering.** A feed-through port has a patch cable plugged in on *both* sides, so it needs the plug plus its strain-relief boot sticking out the back — roughly 4–5 cm with a normal boot. In a shallow 10" rack that competes with the switch behind it. Slim cables with short boots help, and **90° angled plugs on the rear side** save another 3–4 cm if it gets tight.

> ⚠️ **The keystones that were bought are shielded — the patch cables must stay UTP.** This page asked for unshielded keystones, and the deleyCON 12-pack is Cat.6a **geschirmt**. The reasoning behind the original rule still stands: a shield only helps if it is grounded, and a 3D-printed 10" rack has no earthed rail to bond it to, so a *connected* floating shield can act as an antenna rather than a screen.
>
> What makes the purchase harmless is that a shield needs a continuous path to do anything at all. **With UTP patch cables on both sides, the keystone's shield is connected to nothing and is simply inert metal** — no antenna, no ground loop, no difference to the unshielded part. The rule therefore changes rather than disappears:
>
> - **Buy UTP patch cables.** This is no longer a preference but the thing that keeps the shielded keystones neutral. An STP patch cable would bond the shield to a device chassis at one end and leave it floating at the other — the exact configuration the original warning was about.
> - **Do not bond the panel frame to anything.** There is nothing to bond it to, and a partial earth is worse than none.
>
> At these lengths the whole question is academic either way. It is written down because the parts on the shelf now contradict the sentence that was here, and a reader comparing the two would otherwise assume one of them is a mistake.
 
---
 
## Patch Cables — Two Per Link

A feed-through panel has a patch cable on both sides, so every connection is **two** cables: one from the device to the rear of the panel, one from the front of the panel to the switch beside it. Keeping the front ones as short as possible is what makes the dual-cable layout look intentional rather than chaotic.

> ⬜ **This is the only part of the rack still unbought**, and it is unbought for a reason worth writing down: the two constraints below rule out most of what a search returns.

| Part | Details | Price | Status |
|---|---|---:|---|
| Cat.6/6a patch, front side, panel → switch | **Mixed lengths**, see below | ~ 1–2,50 € | ⬜ measure first |
| 0.5 m patch, rear side, device → panel | Uniform length, follows shelf position | ~ 2–3 € | ⬜ |

For the current 3-node build: **8 front-side cables** (6 node links, `pve0`'s management port, the WiFi access point) and **6 rear-side cables** for the node links. Buying two or three spares per colour is worth it — when one fails, the alternative is a wrong-coloured cable in the rack, which quietly destroys the whole convention.

**Buy them colour-coded on both sides.** Because nothing is punched down, the [colour scheme](./cabling.md) runs unbroken from the node to the switch port: 3× blue and 3× yellow in each length, plus 1× red and 1× white on the front. The panel is where a cable stops being a run and becomes a labelled, colour-coded port — it no longer has to be where the colour stops.

### The two constraints that make this harder than it looks

**1. No single front-side length works.** The panel puts twelve ports in one row across the full width; the CRS310 clusters eight ports in two rows on the left half. The runs therefore range from a few centimetres to over twenty, and the uniform 0.25 m this page used to specify only fits the middle of the panel. Full geometry in [`cabling.md`](./cabling.md#the-switch-has-two-port-rows-the-panel-has-one) — **mount both parts and measure before ordering.**

Do not go below 0.2 m for any run. An RJ45 latch is not built for axial load; a cable under permanent tension slowly works the plug out of full seating, and the result is an intermittent link that appears and disappears when someone walks past the rack. That is the most expensive fault class to diagnose and it is bought for ten cents of saved cable.

**2. Colour and "UTP" together are the binding constraint.** Two traps, both easy to walk into:

- **Most short Cat.6a cables are S/FTP.** Anything with `SFTP`, `S/FTP` or `PiMF` in the title bonds a shield the rack cannot ground — see the keystone warning above. Cat.6a in **28 AWG slim UTP** does exist and is ideal here (thin, flexible, short boots, transparent plugs that leave the port LED visible), but the shielding is often only discoverable in the reviews rather than the spec.
- **The good slim lines are colourless.** The widely sold 28 AWG Cat.6a slim series on Amazon (Ercielook and its relabels) comes in **black and white only** — no blue, yellow or red, which makes it unusable for this rack. Its **white** variant is, by coincidence, exactly right for the single white AP cable.

Where colour is actually available:

| Source | What it gives | Note |
|---|---|---|
| **1aTTack.de** (Amazon) | Cat.6 UTP, per-colour multipacks, 0.25 m from ~1,05 €/ea | Not slim — normal jacket with kink protection. Fine for the front side |
| **patchkabel.de** | Free combination of length **and** colour, guaranteed UTP | The reliable answer when Amazon has the wrong colour in the right length |

Slim pays off mainly on the **rear** side, where the plug plus boot competes with rack depth. On the front there is nothing behind the cable, so a normal jacket is no disadvantage.

---

## Uplink Extension: Netgear GS308 *(When scaling horizontally)*

Not purchased yet — planned for the moment a fourth node is added, because that is when the CRS310 runs out of ports.

| Part | Details | Price | Where to find it |
|---|---|---:|---|
| Netgear GS308 | 8× 1G unmanaged | current market price | [Amazon](https://www.amazon.de/NETGEAR-GS308-300PES-Netgear-neu/dp/B07PTTX7MX) |

The GS308 would serve as a simple 1G extension switch carrying the **yellow uplink plane**: the onboard 1G ports of the Tiny nodes, whose only job is reaching the internet (and, unavoidably, carrying vPro/AMT). No routing or VLAN features needed from it — it hangs off a single untagged VLAN 60 access port on the MikroTik and acts as a dumb port expander for that one zone.

### Maxed Dual Switch Setup

The uplink plane moves to the Netgear GS308, freeing three CRS310 ports at once. With the MS-01 on SFP+, its management on port 7 and the WAN going directly into it, this scales to **six nodes**.

```text
Ports 1–6 (2.5G)  🔵  [ node0 … node5 ]── 2.5G M.2 ──┐
Port  7    (2.5G)  🔴  [ pve0 ]── management ────────┤
Port  8    (2.5G)  ⚪  [ WiFi AP ]── tagged 1 + 40 ──┤── MikroTik CRS310
                                                     │      SFP+ 1 ── pve0, trunk: all VLANs
                       [ Netgear GS308 ]─────────────┘      SFP+ 2 ── free
                              │  🟡 one untagged VLAN 60 access port
[ node0 … node5 ]── 1G onboard ┘
```

Beyond six nodes the access point has to move to a wireless-capable uplink or the CRS310 has to be replaced — but at that size a second 2.5G switch is the cheaper answer anyway.

The MS-01 keeps its second SFP+ port free throughout — reserve for a bonded second trunk link (LACP) if storage traffic ever justifies it, or for a direct link to a future dedicated NAS.
The 2.5G blue links handle all high-throughput Kubernetes and storage traffic on the MikroTik. The 1G yellow links handle nothing but internet egress and out-of-band AMT, via the cheap Netgear switch.

**Why this unmanaged switch does NOT cause Hairpinning:**
Unlike using a cheap switch for the main cluster data, using it purely for the 1G uplink plane is perfectly fine. The Netgear hangs off a single untagged VLAN 60 access port, so it is one isolated broadcast domain and nothing else. No cluster traffic ever enters it, which means no cluster traffic can travel back up through it to find a destination. It is a dumb port expander for one zone, leaving the MikroTik's premium 2.5G ports entirely free for heavy Kubernetes data.

---

## "Wait — Three Routers?"

Count the devices in the target design that can route IP traffic, and the result looks absurd for a home network:

| Device | Can route? | What it actually is here |
|---|---|---|
| Fritz!Box 7490 | yes | **The modem.** Routing the home network is a side job it does for free |
| OPNsense VM | yes | **The actual router** of the homelab — the only one enforcing zones |
| MikroTik CRS310 | yes (RouterOS 7) | **The switch.** Layer 3 is a capability it happens to have |

Nobody needs three routers. What is being bought is **one modem and one switch** — both of which happen to be able to route, because that is how such devices are built today. The only real router is OPNsense, and it costs nothing because it runs on hardware that already exists.

### Why the Fritz!Box is bought anyway

Two reasons, and neither is "another router":

1. **The DSL line needs a modem, and a modem alone is more expensive.** A standalone VDSL modem (Draytek Vigor 165, Zyxel VMG series) costs 60–100 €. A used Fritz!Box 7490 costs **20–40 €** — and includes the modem, a router, WiFi and a telephone system. Buying the cheaper device and ignoring half its features is the rational choice.
2. **The family should not depend on the hypervisor.** Since the Fritz!Box is there anyway, it keeps serving the home network: phones, TVs and laptops route through it, not through OPNsense. That means `pve0` can be rebooted, upgraded or broken at 22:00 without anyone losing Netflix. The lab pays for its own outages; the household does not.

The interim benefit on top: static routes and a configurable DNS handout, [neither of which the Speedport offers](./router#the-isp-router-problem).

### Could the switch be cheaper — or unmanaged?

This is the decision worth taking seriously, because the switch is the single most expensive part of the network.

| Setup | Cost | What you get | What you give up |
|---|--:|---|---|
| **Unmanaged 2.5G switch** + OPNsense | ~ 40–60 € | Full 2.5G cluster speed, working cluster, apps reachable | **No VLANs at all.** One flat network — the IoT plug sits next to the NAS, no management zone, no DMZ. OPNsense can route nothing because there is nothing to route between |
| **Cheap managed 2.5G switch** (with SFP+) + OPNsense | ~ 100–130 € | Everything the design needs: VLANs, zones, a 10G trunk | RouterOS: no REST API for Terraform, weaker build quality, no Layer 3 in reserve |
| **MikroTik CRS310** + OPNsense *(chosen)* | ~ 180 € | The above, plus RouterOS 7 with a REST API, two SFP+ ports, hardware L3 as reserve | ~ 50–80 € more than the cheap managed option |

The one thing that is **not** negotiable is `managed`. VLAN tags are attached by the switch — OPNsense can route between zones, but it cannot create them. An unmanaged switch means one flat network no matter how capable the firewall is, and with it the entire zone model, the IoT cage and the DMZ disappear. That is not a budget version of this design; it is a different design.

What the extra ~50–80 € for the CRS310 actually buys, honestly:

- **A 10G SFP+ trunk.** Every VLAN, all NAS traffic, all family apps and all cluster backups share this one link to the MS-01. At 2.5G that single cable would be the bottleneck of the entire Proxmox world at once; at 10G the question never comes up again.
- **The REST API.** This project wants network configuration as code — RouterOS makes that possible with Terraform, cheap managed switches usually offer a web UI and nothing else.
- **Layer 3 in reserve**, which is also the rescue path when the hypervisor hosting OPNsense is the thing that failed.

### The cheapest sensible build

For anyone rebuilding this without the premium parts — full function, no luxury, a little comfort:

| Part | Cost |
|---|--:|
| Used Fritz!Box 7490 (modem + home network during the transition) | ~ 25 € |
| Managed 2.5G switch, 8 ports, with SFP+ | ~ 110 € |
| VLAN-capable WiFi access point | ~ 50 € |
| OPNsense on existing hardware | 0 € |
| **Total** | **~ 185 €** |

The access point can be skipped at first — as long as the Fritz!Box still routes the home network, its own WiFi does the job. It becomes necessary at the moment OPNsense takes over as the gateway, because the Fritz!Box then sits in front of the firewall and its WiFi with it.

That delivers roughly 90 % of the documented design: real VLANs, real firewall zones, 2.5G to every node and a fast trunk. What is missing is network-as-code and the reserve capacity — worth the surcharge in this project because both are explicit learning goals, and not worth it if they are not.

---

## Alternative Paths (Without OPNsense)

If a separate firewall is not on the table at all, these two paths keep the home network from collapsing under cluster traffic:

### Alternative A: The "Old Router" Trick (0 €)
If you have an old, unused router (e.g., an old Fritz!Box or TP-Link) gathering dust in your basement, you can repurpose it as a dedicated Tier-2 gateway for your Kubernetes nodes.
* **The Setup:** Connect all your mini-PCs directly to the LAN ports of the old router. Then, connect the WAN or LAN1 port of this old router to your main home router. 
* **The Benefit:** The old router handles DHCP and local routing exclusively for the cluster. The heavy Kubernetes communication stays completely trapped inside the old hardware. Your main home router never sees this traffic, keeping your family's internet running smoothly. 
* **The Trade-off:** You will be limited to 1 Gbit/s node-to-node speeds, but your primary network remains entirely safe.

### Alternative B: Cheap Unmanaged 2.5G Switch + Single Subnet (~ 30 € – 50 €)

*This is the same option listed as the first row in the cost comparison above — fast and cheap, but it rules out the entire zone model.*
You can purchase an affordable, unmanaged 2.5G switch (such as a budget YuanLey or MokerLink) to get high-speed networking on a budget.
* **The Golden Rule:** You **must** keep all mini-PCs in the exact same IP subnet and completely avoid using VLANs or cross-subnet routing on the cluster nodes.
* **Why it works:** Because all nodes reside within the same Layer 2 broadcast domain, the unmanaged switch forwards all packets directly from MAC address to MAC address. The cluster traffic never leaves the switch to hit your home router. You get full 2.5G speeds for a fraction of the cost, and your home router stays perfectly relaxed.

> ⚠️ **Cybersecurity & Architecture Warning for Alternative B:**
> Running your Kubernetes cluster in the same flat subnet as your private devices comes with significant trade-offs:
> * **No Lateral Isolation (Security Risk):** If an attacker compromises a vulnerable app inside your cluster, they instantly gain direct access to your private laptops, phones, and NAS. Conversely, a hacked smart-home device can directly attack your K8s master nodes.
> * **Sniffing & Interception:** Internal cluster data (like database credentials or secrets) travels unencrypted over Layer 2 and could theoretically be intercepted by any other device in the same network.
> * **Broadcast Noise:** Your mini-PCs will waste CPU cycles processing background noise (like smart-TV discovery packets and Wi-Fi phone traffic) from your entire household, which can introduce micro-latencies.

---

## Upgrade Path

**Short term**
- ⬜ **Mount panel and switch, then measure the front-side runs** — this is now the gate on the last purchase, see [the two constraints](#the-two-constraints-that-make-this-harder-than-it-looks)
- ⬜ Buy the [colour-coded patch cables](./cabling.md#what-this-costs) and cable the rack to the target plan — the colours are worth applying now, while the network is still flat and nothing has to be re-pulled later
- ~~Buy the optics for the SFP+ trunk~~ — **done (August 2026)**: 2× Intel-coded 10Gtek SR, OM3 cords 0.5 m + 0.3 m, LC-duplex keystone. The link now [runs through panel port 10](./cabling.md#why-the-fibre-goes-through-the-panel-after-all)
- ⬜ Connect the MS-01 to the first SFP+ port as a tagged trunk — the modules fail *at first light-up or not at all*, so this is worth testing before the rack is closed up
- ⬜ Connect `pve0`'s second 2.5G RJ45 to port 7 as the management path
- ~~Replace the ISP router with a [Fritz!Box 7490](./router#the-isp-router-problem) so the interim setup gets static routes and a configurable DNS handout~~ — **done (August 2026)**; the house runs on `192.168.178.0/24` and `pve0` on [`.250`](./router#addressing-after-the-swap)

**Mid term**
- Connect all onboard 1G ports to create the full dual-path setup
- Purchase and set up the Netgear GS308 when a fourth node is added — the CRS310 is full at three

**Long term**
- Use the second SFP+ port for a bonded MS-01 link or a dedicated NAS connection
- Add a second 2.5G switch when expanding beyond six nodes