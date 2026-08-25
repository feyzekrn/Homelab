# 🎨 Cabling — One Colour Per Plane

[← Back to Networking](./README.md)

Every cable in this rack belongs to exactly one of three **planes**, and the colour of the cable says which one. Not "which VLAN", not "which speed" — which *job*. Once the three colours are learned, the rack can be read without a label and without opening a wiki page: pull a yellow cable and a machine loses the internet, pull a blue one and it leaves the homelab, pull the red one and only the admin lock-out gets worse.

The colours are not freely chosen. They are the same hues the [diagram palette](../schematics/README.md) already assigns to these layers, so a yellow line in a diagram and a yellow cable in the rack mean the same thing.

---

## The Three Planes

| Colour | Plane | What runs on it | Palette slot |
|---|---|---|---|
| 🔵 **Blue** | **Data** — homelab east-west | Cluster traffic, Longhorn replication, etcd, node ↔ `pve0`, NAS and storage paths, MetalLB service IPs | network fabric `#2a78d6` |
| 🟡 **Yellow** | **Uplink** — north-south | Everything whose destination is the internet: image pulls, updates, the WAN cable itself | edge / untrusted `#eda100` |
| 🔴 **Red** | **Management** — out-of-band | Getting *onto* a machine when its normal path is gone: `pve0` admin NIC, admin laptop drop | security boundary `#e34948` |

A fourth colour appears exactly once and means something different in kind:

| ⚪ **White** | **Tagged trunk** — more than one VLAN on the wire | The WiFi access point (home + IoT) | — |

White is deliberately not one of the three plane colours: it marks a wire where you **cannot** tell from the cable what is inside it. Only two links in the whole design are tagged — the access point and the MS-01 trunk — and knowing which ones at a glance is the point. The trunk is the exception that proves it: it is tagged too, but it is a fibre in standard OM3 aqua, and nothing else in the rack looks remotely like it.

---

## Why Split The Planes Physically At All

The direct reason is the one that decided this design: **the fast NICs should carry nothing but homelab traffic.** A cluster node pulling a 2 GB container image should not be sharing the wire that Longhorn is replicating over, and an admin should not lose SSH because a storage experiment saturated the link.

The argument that tagging costs CPU is worth being precise about, because it is only half true here. Modern NICs — the I226-V in the Tinys and the X710 in the MS-01 — do 802.1Q insertion and stripping in hardware; the tag itself is close to free. What is *not* free is what a trunk implies on the host: a VLAN-aware Linux bridge, one virtual interface per zone, and every packet passing the host's software bridge instead of going straight from NIC to socket. On a 14-core MS-01 that is noise. On an i5-6500T that is also running kubelet, Cilium and Longhorn, keeping the data path as a plain untagged interface is genuinely the simpler and faster arrangement — and it removes a class of misconfiguration from the nodes entirely.

So: **the Tinys never see a VLAN tag.** Two untagged NICs, two planes, and the switch attaches the tags. The MS-01 keeps one tagged trunk, because OPNsense must have a leg in every zone and there is no way around that — but it gets its uplink and its management on their own untagged ports, so neither depends on the trunk or on the router VM being healthy.

---

## Per-Device Port Assignment

### `node0`, `node1`, `node2` — Lenovo M910q Tiny

| Physical port | Plane | Colour | VLAN (set by switch) | Gateway? |
|---|---|---|---|---|
| 2.5G M.2 adapter (I226-V) | Data | 🔵 blue | 10 — k8s, untagged | **no** |
| 1G onboard (I219-LM) | Uplink | 🟡 yellow | 60 — uplink, untagged | **yes — default route** |

The Tinys have two NICs and three planes, so one plane has to be shared. Management shares the **blue** leg: SSH, `kubectl`, monitoring and the Proxmox/Talos API all live in VLAN 10 with the rest of the homelab. That is the right one to merge — a node is the lab; there is nothing to protect it from that is not already in VLAN 10.

### `pve0` — Minisforum MS-01

| Physical port | Plane | Colour | VLAN | Goes to |
|---|---|---|---|---|
| SFP+ 1 (X710, 10G) | Data | 🩵 aqua *(OM3 fibre — see below)* | **tagged** 10, 20, 30, 40, 50 | CRS310 SFP+ 1 |
| SFP+ 2 (X710, 10G) | — | — | free | reserve: LACP second trunk, dedicated NAS link |
| 2.5G RJ45 #1 (I226) | Uplink | 🟡 yellow | WAN — **off-switch** | Fritz!Box LAN port |
| 2.5G RJ45 #2 (I226) | Management | 🔴 red | 30 — management, untagged | CRS310 port 7 |

Three notes on this row set:

- **The WAN port's speed is irrelevant and that is fine.** A 2.5G port terminating a DSL line that delivers a fraction of that is not waste — the port is spent on *physical separation*, not on bandwidth. Untrusted traffic never becomes a VLAN on the switch, so there is no WAN VLAN to mistag.
- **The red port is the whole reason this plan differs from the old one.** Today, if the OPNsense VM breaks or the trunk is misconfigured, the machine hosting the router is reached through the router. The red port breaks that loop: an untagged management NIC in VLAN 30, plugged into a switch that is pure Layer 2 and does not need OPNsense to forward a frame.
- **VLAN tagging on the trunk is not a contradiction.** The X710 offloads it, and OPNsense genuinely needs a leg in five zones. What matters is that the trunk is no longer the *only* way in.

---

## The Full Cable List

```text
                    ┌─────────────────────┐
     Internet ──────┤  Fritz!Box 7490     │
                    └──────────┬──────────┘
                               │ 🟡 WAN — the only internet cable
                               ▼
   ┌───────────────────────────────────────────────┐
   │  pve0 — MS-01                                 │
   │   2.5G #1  🟡 uplink / WAN   (from Fritz!Box) │
   │   2.5G #2  🔴 management     ──────────────┐  │
   │   SFP+ 1   🩵 data, tagged trunk (fibre) ┐  │  │
   └─────────────────────────────────────────┼──┼──┘
                                             │  │
   ┌─────────────────────────────────────────▼──▼──┐
   │  MikroTik CRS310  —  pure Layer 2             │
   │  1 2 3   4 5 6      7        8    SFP+1 SFP+2 │
   └──┬─┬─┬───┬─┬─┬──────┬────────┬────────────────┘
      🔵🔵🔵  🟡🟡🟡     🔴       ⚪
      │ │ │   │ │ │      │        │
      │ │ │   │ │ │   pve0 mgmt   WiFi AP (phase 2)
      │ │ │   └─┴─┴── node0-2, 1G onboard
      └─┴─┴────────── node0-2, 2.5G M.2
```

Every link through the panel is two cables — rear (device → panel) and front (panel → switch):

| Panel port | Link | Colour | Rear cable | Front cable |
|---|---|---|---|---|
| **1–3** | `node0-2` 2.5G M.2 → CRS310 1–3 | 🔵 blue | 0.5 m Cat.6 | 0.25 m slim |
| **4–6** | `node0-2` 1G onboard → CRS310 4–6 | 🟡 yellow | 0.5 m Cat.6 | 0.25 m slim |
| **7** | *(phase 2)* WiFi AP → CRS310 8 | ⚪ white | to AP position | 0.25 m slim |
| **8** | Fritz!Box LAN → `pve0` 2.5G #1 (WAN) | 🟡 yellow | 2–3 m, leaves the rack | 0.5 m to `pve0` |
| **9** | *(optional)* admin laptop jack | 🔴 red | as needed | 0.25 m slim |
| 10–12 | *reserve* | — | — | — |

Direct links, no panel — both ends are adjacent devices:

| Link | Colour | Type | Length |
|---|---|---|---|
| `pve0` 2.5G #2 → CRS310 port 7 | 🔴 red | Cat.6 patch | ~0.5 m |
| `pve0` SFP+ 1 → CRS310 SFP+ 1 | 🩵 aqua *(OM3 standard)* | OM3 LC-LC duplex + 2× SFP+ SR | 1 m |

The WAN cable is worth a second look in that first table: it is the one run that genuinely *enters* the rack from outside, and it terminates on the panel and then hops to `pve0` — even though it never touches the switch. That is exactly what a panel is for, and it means the long cable from the Fritz!Box can be unplugged, replaced or rerouted without ever reaching behind the MS-01.

### The colour runs through the panel, front and back

Because the [patch panel is a feed-through type](./README.md#patch-panel-10-12-port-keystone-feed-through) — a socket on the rear and a socket on the front, no punch-down — **every cable in this rack is a patch cable, and every one of them is colour-coded.** There is no hidden segment where the colour stops.

That is a better outcome than a punch-down panel would have given, and it comes for free:

```text
        rear                    panel                   front
   node0  2.5G ──🔵── [ port 1  feed-through ] ──🔵── CRS310 port 1
   node0  1G   ──🟡── [ port 4  feed-through ] ──🟡── CRS310 port 4
```

Each link is therefore **two** patch cables, not one:

- **Rear side** (device → panel): length follows where the machine sits on the shelf, typically 0.5 m. Same colour as the front.
- **Front side** (panel → switch): 0.25 m slim, standing directly beside the switch ports.

The practical consequence is that the cable count doubles — six node links become twelve short cables — but nothing has to be crimped, punched down or bought as a 50 m ring of solid installation cable in three colours, which was the ugly part of the punch-down variant. Twelve slim patch cables at ~2 € are cheaper than one ring of Verlegekabel.

**The links that skip the panel entirely** are the ones between adjacent devices: `pve0`'s red management cable straight into switch port 7, and the 10G fibre. Those are single cables, coloured the same way.

### The 10G link: fibre, and why it does not touch the panel

**The SFP+ link between the CRS310 and `pve0` never goes through the patch panel.** A panel exists to terminate runs that go *somewhere* — through a wall, into another room, out of the rack. This link is one metre between two devices standing next to each other. Patching it through a panel would add two more connector pairs, two more mating losses and two more things to unplug by accident, for no benefit at all. It gets plugged straight in, transceiver to transceiver.

So the panel choice is unaffected by this link. What the link does need is a decision between **DAC** and **fibre**, and for this particular pair of devices fibre wins:

| | DAC (passive twinax) | **Fibre — OM3 + 2× SFP+ SR** | 10GBASE-T module |
|---|---|---|---|
| Cost | ~15 € | ~30 € | ~80 € |
| Heat in the cage | ~0 W | ~0.7 W per end | **2.5 W per end** |
| Cable handling | 24 AWG, stiff, ~5 cm bend radius | 2 mm, flexible | normal Cat.6a |
| Vendor coding | **one cable, both ends coded** — must satisfy MikroTik *and* Intel at once | **one module per end** — buy each coded for its own switch | per end |

The decisive one is the third row. `pve0`'s SFP+ ports are an **Intel X710**, which is the pickiest end of this link; the CRS310 running RouterOS does not enforce vendor coding at all. A DAC is a single part that has to please both vendors simultaneously. Two separate transceivers decompose that problem: one coded for MikroTik (or generic — RouterOS does not care), one coded for Intel. If one end is wrong, one 12 € module gets replaced instead of the whole cable.

The stiffness matters more than it sounds, too. A 1 m DAC in a 10" rack full of 0.25 m slim patch cables behaves like a garden hose and forces the MS-01 to sit where the cable allows. An LC duplex patch is 2 mm and disappears.

**Take multimode OM3, not singlemode OS2**, for two reasons that both apply specifically at this distance:

- **Singlemode LR optics can overdrive the receiver over one metre.** LR is built to survive 10 km of attenuation; with none of it, transmit power can land above the receiver's overload threshold and the link goes unstable in a way that looks like a bad cable. Fixing it needs an inline attenuator. SR is designed for exactly this short in-rack case.
- **OS2 patch cords are yellow by standard** — and yellow already means *internet uplink* in this rack. OM3's standard **aqua** collides with nothing.

That aqua is a fifth colour in a three-colour scheme, and that is fine: it is a different *medium*, not a different plane. Nobody will ever mistake a 2 mm fibre for a copper patch cable. It gets the `pve0-TRUNK` label like everything else.

> ⚠️ Keep the dust caps on until the moment of plugging in, and do not buy the SFP+ modules from a source that will not take a return — module compatibility is the one part of this link that can genuinely fail, and it fails at first light-up or not at all.

---

## Labelling

Colour says *which plane*. A label says *which device*, and both ends get one:

```text
node0-DATA    node1-DATA    node2-DATA      🔵
node0-UP      node1-UP      node2-UP        🟡
pve0-MGMT     pve0-WAN      pve0-TRUNK      🔴 🟡 🔵
```

Panel ports carry the same string on the front strip. The rule for reading the rack then becomes: *colour tells you what breaks, label tells you whose it is.*

---

## What This Costs

| Item | Qty | Unit | Total |
|---|--:|--:|--:|
| 10" 12-port keystone panel, empty frame | 1 | ~12 € | ~12 € |
| Cat.6a UTP **feed-through** keystone (socket/socket) | 12 | ~2 € | ~24 € |
| 0.25 m Cat.6 slim patch, front side — 3 blue, 3 yellow, 1 red, 1 white | 8 | ~2 € | ~16 € |
| 0.5 m Cat.6 patch, rear side — 3 blue, 3 yellow | 6 | ~2.50 € | ~15 € |
| 0.5 m Cat.6 patch, red (`pve0` mgmt, direct) | 1 | ~3 € | ~3 € |
| 2–3 m Cat.6 patch, yellow (WAN, into the rack) | 1 | ~5 € | ~5 € |
| SFP+ SR transceiver (1× MikroTik-coded, 1× Intel-coded) | 2 | ~12 € | ~24 € |
| OM3 LC-LC duplex patch, 1 m | 1 | ~6 € | ~6 € |
| Label tape + Velcro ties | — | — | ~8 € |
| | | **Total** | **~ 113 €** |

Buying a few spare 0.25 m cables per colour is worth it — they are ~2 € and the alternative when one fails is a rack with a wrong-coloured cable in it, which quietly destroys the entire convention.

Roughly 36 € of that total is the panel and its modules, and it buys organisation rather than function — see [what the panel is actually worth](./README.md#what-the-panel-is-actually-worth-here). The other ~77 € is cable and optics that have to be bought either way.

---

## What This Plan Changes — And What It Costs

Three consequences follow from the split, and none of them are cosmetic.

### 1. VLAN 60 — a new zone for the uplink plane

The Tinys' 1G ports were previously planned as VLAN 30 (management). They cannot stay there now that their job is internet access, because VLAN 30 also holds the switch's admin IP, the Proxmox web UI and the OPNsense GUI — a compromised pod would be one hop from all three.

So the uplink plane gets its own zone:

| Zone | VLAN | Members | Rules |
|---|---|---|---|
| **Uplink** | **60** | `node0-2` onboard 1G | → internet: **allow** (NAT) · → any other zone: **deny** · ← from management: **allow** |

This is the zone the [zone table](./README.md#the-whole-picture) needs to gain, and it is the only structural change to the network design.

### 2. Intel AMT now lives on the yellow cable

The M910q's vPro/AMT engine is bound to the **onboard** NIC — the yellow one. It is not a choice; the management engine sits behind that specific PHY. That means the out-of-band channel that the [cross-watchdog concept](../compute/README.md) depends on is in VLAN 60, on the cable labelled "uplink".

That is acceptable, but only with the rule written above: **VLAN 60 must be treated as management-grade, not internet-grade.** AMT listens on 16992–16995 and authenticates with a password set in MEBx. Reachable from VLAN 30 and nothing else; never routed to the internet; never merged into the home VLAN.

It is also the strongest argument against the tempting shortcut of plugging the Tinys' 1G ports straight into the Fritz!Box: that would put three out-of-band management engines into the family LAN next to the phones.

### 3. The switch now caps at three nodes

Counting ports: 3 data + 3 uplink + 1 `pve0` management + 1 access point = **8 of 8**. The CRS310 is full, and a fourth node needs two ports that do not exist.

The already-planned [Netgear GS308](./README.md#uplink-extension-netgear-gs308-when-scaling-horizontally) resolves this, with one change of purpose: it becomes the **uplink-plane switch**, not the management switch. The three yellow 1G cables move off the CRS310 onto the GS308, the GS308 links back on a single VLAN 60 access port, and the CRS310 recovers two net ports.

```text
Ports 1–6 (2.5G)  🔵  node0 … node5 data          SFP+ 1 ── pve0, tagged trunk
Port  7      (2.5G)  🔴  pve0 management           SFP+ 2 ── free
Port  8      (2.5G)  ⚪  WiFi AP (tagged 1 + 40)
Port  x → GS308      🟡  VLAN 60 access port
                          └── node0 … node7, 1G onboard
```

The honest trade: the old plan reached four nodes on eight ports, this one reaches three. The port bought back is `pve0`'s management NIC — an admin path that survives a dead router VM, which is worth more than a node slot the project does not need yet.

---

## Interim State

None of this is live yet. While the [interim setup](./router/README.md#where-the-house-wifi-comes-from-in-each-phase) runs, everything is one flat untagged network behind the Fritz!Box and there are no VLANs to separate.

The colours can and should be bought and used **now** anyway. Physical cabling is the part that is expensive to change later — pulling and relabelling cables in a populated rack is exactly the work nobody does. The plane a cable belongs to is already decided; only the tags the switch attaches are still missing.

---

## Learning Links

- [Wikipedia: TIA-606](https://en.wikipedia.org/wiki/TIA-606) — the standard behind colour-coded structured cabling
- [Wikipedia: IEEE 802.1Q](https://en.wikipedia.org/wiki/IEEE_802.1Q) — VLAN tagging
- [Wikipedia: Intel Active Management Technology](https://en.wikipedia.org/wiki/Intel_Active_Management_Technology)
- [Wikipedia: Direct attach copper cable](https://en.wikipedia.org/wiki/Direct_attach_copper_cable)
