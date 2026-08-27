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
| **1–3** | `node0-2` 2.5G M.2 → CRS310 1–3 | 🔵 blue | 0.5 m Cat.6 | 0.25–0.5 m † |
| **4–6** | `node0-2` 1G onboard → CRS310 4–6 | 🟡 yellow | 0.5 m Cat.6 | 0.25–0.5 m † |
| **7** | *(phase 2)* WiFi AP → CRS310 8 | ⚪ white | to AP position | 0.25–0.5 m † |
| **8** | Fritz!Box LAN → `pve0` 2.5G #1 (WAN) | 🟡 yellow | 2–3 m, leaves the rack | 0.5 m to `pve0` |
| **9** | *(optional)* admin laptop jack | 🔴 red | as needed | 0.25–0.5 m † |
| **10** | `pve0` SFP+ 1 → CRS310 SFP+ 1 | 🩵 aqua | 0.5 m OM3 LC-LC | 0.3 m OM3 LC-LC |
| 11–12 | *reserve* | — | — | — |

† **The front-side length is not uniform** and cannot be decided from this table — the panel's port pitch and the switch's do not match. See [the switch has two port rows, the panel has one](#the-switch-has-two-port-rows-the-panel-has-one).

Direct links, no panel — both ends are adjacent devices:

| Link | Colour | Type | Length |
|---|---|---|---|
| `pve0` 2.5G #2 → CRS310 port 7 | 🔴 red | Cat.6 patch | ~0.5 m |

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
- **Front side** (panel → switch): as short as the geometry allows, **0.25 m for the middle ports and 0.5 m for the outer ones** — not one uniform length, [and here is why](#the-switch-has-two-port-rows-the-panel-has-one).

The practical consequence is that the cable count doubles — six node links become twelve short cables — but nothing has to be crimped, punched down or bought as a 50 m ring of solid installation cable in three colours, which was the ugly part of the punch-down variant. Twelve slim patch cables at ~2 € are cheaper than one ring of Verlegekabel.

**The link that skips the panel entirely** is `pve0`'s red management cable, straight into switch port 7 — a single cable, coloured the same way.

### The switch has two port rows, the panel has one

This is the geometry problem that decides the front-side cable order, and it is invisible until both parts are mounted:

```text
   panel  0.5U   [1][2][3][4][5][6][7][8][9][10][11][12]   ~200 mm, one row, ~17 mm pitch
                  └──────────── spread out ────────────┘

   switch 1U      [1][2][3][4]  ┌──────┐                   ~70 mm of RJ45,
                  [5][6][7][8]  │SFP+ 1│                   two rows, clustered left
                                │SFP+ 2│
                                └──────┘
```

The CRS310 is 200 × 206 × 44 mm and puts its eight 2.5G ports in **two rows of four**, clustered on the left half of the face with the SFP+ cages beside them. The panel spreads twelve ports across the full width. So the two faces have **completely different port pitch**, and the distance from panel port *n* to switch port *m* is not constant — it ranges from a few centimetres for the aligned middle ports to well over 20 cm for the outer ones.

Three consequences:

- **One cable length is the wrong answer.** The originally planned uniform 0.25 m works for the middle of the panel and comes up short at the edges. Plan on **a mix of 0.25 m and 0.5 m**, and buy the exact split only after both parts are screwed into the rack and the real distances can be measured.
- **The two rows differ by about one RJ45 height** (~15 mm) in vertical distance. That is inside the tolerance of a single length — it is the *horizontal* spread that forces the mix, not the two rows.
- **Port assignment is now a design choice, not bookkeeping.** Nothing requires panel port 1 to land on switch port 1. Mapping the panel's outer ports to the switch's *near* row — and keeping the panel's middle ports for the far row — cuts the longest run substantially. The [labels](#labelling) carry the meaning; the numbers do not have to line up.

> ⬜ **Measure before ordering the front-side cables.** This is the one item on the [cost table](#what-this-costs) that should not be bought from a plan. Mount the panel and the switch, then measure the longest and the shortest run.

### The 10G link: fibre, and why it now *does* touch the panel

> ✅ **Bought (August 2026):** 2× 10Gtek SFP+ SR Intel-coded (**33,99 €**), 1× ROLINE LC/LC duplex OM3 keystone (**4,29 €**), 1× OM3 LC-LC 0.5 m rear (**7,19 €**), 1× OM3 LC-LC 0.3 m front (**7,99 €**). Total **53,45 €**.
>
> This **reverses** what this section originally argued — the fibre now runs through panel port 10 like every copper link. Reasoning in [why the panel won after all](#why-the-fibre-goes-through-the-panel-after-all).

The first decision this link needed was between **DAC** and **fibre**, and for this particular pair of devices fibre wins:

| | DAC (passive twinax) | **Fibre — OM3 + 2× SFP+ SR** | 10GBASE-T module |
|---|---|---|---|
| Cost | ~15 € | ~30 € | ~80 € |
| Heat in the cage | ~0 W | ~0.7 W per end | **2.5 W per end** |
| Cable handling | 24 AWG, stiff, ~5 cm bend radius | 2 mm, flexible | normal Cat.6a |
| Vendor coding | **one cable, both ends coded** — must satisfy MikroTik *and* Intel at once | **one module per end**, coded independently | per end |

The decisive one is the third row. `pve0`'s SFP+ ports are an **Intel X710**, which is the pickiest end of this link: the `i40e` driver compares the module's vendor OUI against a whitelist and disables Rx/Tx on a miss (*"an unsupported SFP+ module type was detected"*). The CRS310 running RouterOS does not enforce vendor coding at all. A DAC is a single part that has to please both vendors simultaneously; two separate transceivers decompose that problem.

**And decomposing it produces a simplification worth stating plainly: because RouterOS is indifferent, the module that satisfies Intel satisfies both ends.** So this link does not need one MikroTik-coded and one Intel-coded module — it needs **two identical Intel-coded modules**. That is what was bought, and it is strictly better than the split: one spare part covers both ends, and swapping the two modules is a free diagnostic that separates a bad module from a bad port.

> ⚠️ **Known quirk of this pairing:** a 10Gtek SR module in an X710 occasionally fails to link when both devices power on at the same instant. Reseating the transceiver fixes it. Worth knowing before it gets diagnosed as a bad module or a bad fibre.

The stiffness matters more than it sounds, too. A 1 m DAC in a 10" rack full of 0.25 m slim patch cables behaves like a garden hose and forces the MS-01 to sit where the cable allows. An LC duplex patch is 2 mm and disappears.

**Take multimode OM3, not singlemode OS2**, for two reasons that both apply specifically at this distance:

- **Singlemode LR optics can overdrive the receiver over one metre.** LR is built to survive 10 km of attenuation; with none of it, transmit power can land above the receiver's overload threshold and the link goes unstable in a way that looks like a bad cable. Fixing it needs an inline attenuator. SR is designed for exactly this short in-rack case.
- **OS2 patch cords are yellow by standard** — and yellow already means *internet uplink* in this rack. OM3's standard **aqua** collides with nothing.

That aqua is a fifth colour in a three-colour scheme, and that is fine: it is a different *medium*, not a different plane. Nobody will ever mistake a 2 mm fibre for a copper patch cable. It gets the `pve0-TRUNK` label like everything else.

> ⬜ **The colour breaks at the panel.** The keystone that was bought is a ROLINE LC/LC duplex **in black**, not aqua — it was the OM3 module actually available. The two patch cords either side of it are aqua, so the medium is still unmistakable in the cable run; only the 2 cm of coupler in the panel face is the wrong colour. If an aqua LC-duplex keystone (e.g. Delock 86720) turns up later, swapping it is a 4 € fix and closes the last gap in the convention.

#### Why the fibre goes through the panel after all

This section originally argued the opposite, and the argument was sound for the assumption it made: *a panel exists to terminate runs that go somewhere, and this link is one metre between two adjacent devices.* Two things changed that conclusion.

**The cost is smaller than it looked.** Routing through the panel adds one mated pair — two endfaces, roughly 0.3 dB by the keystone's own spec. 10GBASE-SR over OM3 has a ~2.9 dB budget for 300 m; this link spends about 0.5 dB in total over 0.8 m. There is no scenario in which the loss matters.

**The benefit is the same one the panel buys for copper**, and it was already written down two sections above: *the switch side stops being touched.* Servicing `pve0` means unplugging at the rear of the panel; the front face and the SFP+ cage keep their layout and their label. Without the panel, every MS-01 move is a hand behind the switch, on the one link whose transceivers are the most delicate parts in the rack.

The real cost is neither of those — it is **two extra endfaces that can get dirty**, on a medium where a fingerprint is a link fault. That is a maintenance rule, not a design objection:

> ⚠️ Dust caps stay on until the moment of plugging in, at all four connector ends. A **1.25 mm LC cleaning pen** (~10 €) belongs in the rack drawer — with two mated pairs in this link, contamination is now the single most likely fault on it, ahead of the modules.

The modules themselves are bought and Intel-coded, so the original *"buy from a source that takes returns"* caution has done its job. What remains true is the failure timing: **module compatibility fails at first light-up or not at all.** If the link comes up, it stays up.

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

✅ = bought · ⬜ = still needed

| | Item | Qty | Unit | Total |
|:--:|---|--:|--:|--:|
| ✅ | GeeekPi 10" **0.5U** 12-port keystone panel, empty frame | 1 | 12,99 € | **12,99 €** |
| ✅ | deleyCON Cat.6a **feed-through** keystone (12-pack, shielded) | 12 | 2,42 € | **28,99 €** |
| ✅ | ROLINE LC/LC duplex OM3 keystone — fibre, panel port 10 | 1 | 4,29 € | **4,29 €** |
| ✅ | 10Gtek SFP+ SR, **Intel-coded** (2-pack) | 2 | 17,00 € | **33,99 €** |
| ✅ | OM3 LC-LC duplex 0.5 m, rear side | 1 | 7,19 € | **7,19 €** |
| ✅ | OM3 LC-LC duplex 0.3 m, front side | 1 | 7,99 € | **7,99 €** |
| ⬜ | Cat.6 patch, front side — [mixed lengths](#the-switch-has-two-port-rows-the-panel-has-one), 3 blue · 3 yellow · 1 red · 1 white | 8 | ~2 € | ~16 € |
| ⬜ | 0.5 m Cat.6 patch, rear side — 3 blue, 3 yellow | 6 | ~2.50 € | ~15 € |
| ⬜ | 0.5 m Cat.6 patch, red (`pve0` mgmt, direct) | 1 | ~3 € | ~3 € |
| ⬜ | 2–3 m Cat.6 patch, yellow (WAN, into the rack) | 1 | ~5 € | ~5 € |
| ⬜ | LC cleaning pen, 1.25 mm | 1 | ~10 € | ~10 € |
| ⬜ | Label tape + Velcro ties | — | — | ~8 € |
| | | | **Bought** | **95,44 €** |
| | | | **Projected total** | **~ 152 €** |

Buying a few spare front-side cables per colour is worth it — they are ~2 € and the alternative when one fails is a rack with a wrong-coloured cable in it, which quietly destroys the entire convention.

**~46 € of that is the panel and its three kinds of keystone**, and it buys organisation rather than function — see [what the panel is actually worth](./README.md#what-the-panel-is-actually-worth-here). The other ~106 € is cable and optics that have to be bought either way.

The estimate this table replaced was ~113 €. The gap is not overspending: the fibre gained a keystone and a second patch cord when it [moved onto the panel](#why-the-fibre-goes-through-the-panel-after-all), the modules cost 34 € rather than the 24 € guessed, and the cleaning pen was missing from the original list entirely.

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
