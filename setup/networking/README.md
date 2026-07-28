# 🔌 Networking — Switches & Physical Topology

[← Back to Setup Overview](../README.md)

**In this folder:** [`design.md`](./design.md) — VLANs, DHCP, firewall zones and addressing · [`mikrotik`](./mikrotik) — switch configuration docs and Terraform · [`router`](./router) — the gateway layer: OPNsense as router and firewall.

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
        └──┬────────┬────────┬────────┬───────┬────────┬───┘
           │1,2,3   │4,5,6   │  7     │  8    │ SFP+2  │
           ▼        ▼        ▼        ▼       ▼        
      node0–2   node0–2   WiFi AP   free    free
      (2.5G)    (1G mgmt) (tagged)
      VLAN 10   VLAN 30   VLAN 1+40
         │
         └── bare-metal Kubernetes: apps, Home Assistant, Longhorn, Traefik
```

| Zone | VLAN | Who lives there | Reachable from |
|---|---|---|---|
| Home | 1 (untagged) | Family phones, laptops, TVs | Internet; apps via 80/443 only |
| Kubernetes | 10 | The three nodes, MetalLB range | Home (apps), management |
| Services | 20 | NAS shares, family app containers | Home (apps), k8s (storage paths) |
| Management | 30 | Proxmox UI, switch, vPro, OPNsense GUI | Admin laptop and NetBird only |
| IoT | 40 | Plugs, sensors, cameras | Nothing — may only reach the MQTT broker |
| DMZ | 50 | Anything exposed to the internet | Tunnel only; may reach its own dataset |

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
                                  │
                                  │  ← WAN, straight into pve0
                                  ▼
[  node0   ]──  2.5G M.2  ──┐  [ pve0 (MS-01) ]
[  node0   ]── 1G onboard ──┤          │
[  node1   ]──  2.5G M.2  ──┤          │ 10G SFP+ trunk
[  node1   ]── 1G onboard ──┼── MikroTik CRS310 ──┘   VLAN 10/20/30/40/50 tagged
[  node2   ]──  2.5G M.2  ──┤
[  node2   ]── 1G onboard ──┘
```

**Why the WAN bypasses the switch.** Untrusted internet traffic never becomes a VLAN on the switch at all, which removes an entire class of mistakes: no WAN VLAN to misconfigure, no chance of a tagging error putting the raw internet next to the cluster. The MS-01 has two spare RJ45 ports, so it costs nothing — and it frees a switch port as a side effect.

The only price is a physical dependency: the cable from the ISP router has to reach the MS-01. Since both live next to each other, that is not a real constraint.

### Port Assignment — Every Port On The CRS310

This is the full target wiring once [OPNsense](./router) is the router. `Untagged` means the connected device knows nothing about VLANs and the switch attaches the tag; `tagged` means the device speaks 802.1Q itself and several VLANs share the cable.

| Port | Connected to | Mode | VLAN | Speed |
|---|---|---|---|---|
| **1** | `node0` — 2.5G M.2 adapter | untagged, PVID 10 | 10 — k8s | 2.5G |
| **2** | `node1` — 2.5G M.2 adapter | untagged, PVID 10 | 10 — k8s | 2.5G |
| **3** | `node2` — 2.5G M.2 adapter | untagged, PVID 10 | 10 — k8s | 2.5G |
| **4** | `node0` — onboard NIC | untagged, PVID 30 | 30 — management | 1G |
| **5** | `node1` — onboard NIC | untagged, PVID 30 | 30 — management | 1G |
| **6** | `node2` — onboard NIC | untagged, PVID 30 | 30 — management | 1G |
| **7** | WiFi access point | **tagged** | 1 (home), 40 (IoT) — one SSID per VLAN | 2.5G |
| **8** | *free* | — | reserve: `node3` data, or a wired device in any zone | 2.5G |
| **SFP+ 1** | `pve0` (MS-01) | **tagged trunk** | 10, 20, 30, 40, 50 — all zones | 10G |
| **SFP+ 2** | *free* | — | reserve: second trunk (LACP), dedicated NAS link, second switch | 10G |
| *(none)* | ISP router / modem | — | **not on the switch** — goes directly into a `pve0` RJ45 port as WAN | — |

Three things are worth reading out of that table:

- **The two tagged ports carry the whole design.** SFP+ 1 is what lets OPNsense have a leg in every zone over one cable, and port 7 is what lets one access point serve the family WLAN and a separate IoT WLAN as genuinely different networks.

> ⚠️ **Port 7 dictates what kind of access point can be bought.** Serving two zones from one device requires an AP that supports **multiple SSIDs with a VLAN tag per SSID** (802.1Q). A cheap repeater or a consumer router in bridge mode cannot do this — it would put every wireless device into a single network, and the IoT zone would exist on paper only. Devices that can: TP-Link Omada EAP series (~50–70 €), Ubiquiti UniFi (~100 €+), or any OpenWrt-capable router used as an AP. This is a planned purchase, not something already owned.
- **Node cabling is split by purpose, not by speed.** The fast M.2 adapters carry cluster traffic in VLAN 10; the onboard ports carry management in VLAN 30. If a cluster experiment saturates the data path, SSH and monitoring still work.
- **The switch itself lives in VLAN 30.** Its management IP belongs in the same zone as the node management ports and the Proxmox web UI — reachable from the admin laptop and through NetBird, from nowhere else.

Interim state, before OPNsense exists: everything runs untagged in one flat network and the ISP router remains the gateway. The port assignment above only becomes real when the router does.

### Maxed Switch Setup

Without a management switch, the RJ45 ports run out at four nodes: 8 ports = 4× data + 4× management. Neither the MS-01 (SFP+) nor the internet uplink (direct into the MS-01) competes for them.

```text
[  node0   ]──  2.5G M.2  ──┐
[  node0   ]── 1G onboard ──┤
[  node1   ]──  2.5G M.2  ──┤
[  node1   ]── 1G onboard ──┤── MikroTik CRS310 ──┬── SFP+ 1: pve0 (trunk)
[  node2   ]──  2.5G M.2  ──┤                     └── SFP+ 2: free
[  node2   ]── 1G onboard ──┤
[  node3   ]──  2.5G M.2  ──┤
[  node3   ]── 1G onboard ──┘
```

All eight RJ45 ports are then taken by nodes — which means the WiFi access point has to move to SFP+ 2 (via a media converter or an AP with an SFP+ uplink) or the management network has to move to its own switch. Beyond four nodes, the second option is the only sensible one.

---
 
## Patch Panel: HB-Digital 12-Port Cat.6a 10" 1HE
 
A clean build needs a clean cable termination point. Instead of plugging patch cables directly into the switch, all node cables terminate at the patch panel first. From there, short 0.25m slim patch cables run to the switch ports — keeping the cable routing tidy and making it easy to move, relabel or replace connections without touching the longer runs.
 
| Part | Details | Price | Where to find it |
|---|---|---:|---|
| HB-Digital 12-Port Patchpanel Cat.6a | 10" 1HE, STP, schwarz, 12× Cat.6a Keystone included | 35.90 € | [hb-digital.de](https://www.hb-digital.de/Patchpanel-12-Port-mit-Cat6a-RJ45-Keystone-Module-10-Patchfeld-1HE-schwarz) |
 
The 10" format matches the 3D-printed 1U rack mount used for the Tiny nodes. The Cat.6a Keystone modules are included and clip in tool-less via LSA snap-in — no crimping needed. With 12 ports there is enough room for the current 3-node dual-cable setup (6 ports used) and space to grow.
 
---
 
## Patch Cables — 0.25m Slim
 
Short slim patch cables connect the patch panel front to the switch ports directly beside it. Keeping these as short as possible is what makes the dual-cable layout look intentional rather than chaotic.
 
| Part | Details | Price | Where to find it |
|---|---|---:|---|
| 0.25m Slim Patch Cable Cat.6 | Short run from patch panel to switch, per cable | ~ 1.50–2.50 € | [Amazon](https://www.amazon.de/s?k=0.25m+patchkabel+slim+cat6) |
 
For the current 3-node setup with dual cables: 6 node connections, plus one for the WiFi access point = **7 cables minimum**. The internet uplink is not among them — it goes straight into the MS-01, not through the patch panel. Buying 10 leaves a few spares for future nodes or replacements.

---

## Management Extension: Netgear GS308 *(When scaling horizontally)*

Not purchased yet — planned for a later stage when a dedicated management network becomes necessary.

| Part | Details | Price | Where to find it |
|---|---|---:|---|
| Netgear GS308 | 8× 1G unmanaged | current market price | [Amazon](https://www.amazon.de/NETGEAR-GS308-300PES-Netgear-neu/dp/B07PTTX7MX) |

The GS308 would serve as a simple 1G extension switch. Its only job is to connect the onboard 1G ports of the Tiny nodes, providing a dedicated path for SSH, monitoring and fallback traffic. No routing or management features needed from it — the MikroTik handles all of that. The GS308 just extends the number of available 1G ports.

### Maxed Dual Switch Setup

Management traffic moves to a dedicated Netgear GS308, freeing all 8× 2.5G ports on the MikroTik for cluster data. With the MS-01 on SFP+ and the WAN going directly into it, this scales to **8 nodes** with a dedicated management path.

```text
Ports 1–8 (2.5G)                      SFP+ 1 ── pve0 (MS-01), trunk: all VLANs
[  node0 … node7  ]──  2.5G M.2 ──── MikroTik CRS310
                                      SFP+ 2 ── Netgear GS308 (VLAN 30 trunk)
                                                      │
[  node0 … node7  ]── 1G onboard ─────────────────────┘
[ MikroTik CRS310 ]── 1G onboard ─────────────────────┘
```

The MS-01 keeps its second SFP+ port free throughout — reserve for a bonded second trunk link (LACP) if storage traffic ever justifies it, or for a direct link to a future dedicated NAS.
The 2.5G link handles all high-throughput Kubernetes and storage traffic directly on the MikroTik's L3 hardware. The 1G link handles management, SSH, monitoring and fallback via the cheap Netgear switch. 

**Why this unmanaged switch does NOT cause Hairpinning:**
Unlike using a cheap switch for the main cluster data, using it purely for the 1G management plane is perfectly fine. The Netgear switch connects to the MikroTik via a dedicated VLAN trunk. Since the MikroTik handles all inter-VLAN routing *before* pushing the packets down to the Netgear, no cluster traffic ever has to travel back up to find its destination. The Netgear simply acts as a dumb port-expander for a single, isolated management network, leaving the MikroTik's premium 2.5G ports entirely free for heavy Kubernetes data.

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
- Connect the MS-01 to the first SFP+ port as a tagged trunk (needs an SFP+ module or DAC cable — not included with either device)
- Replace the ISP router with a [Fritz!Box 7490](./router#the-isp-router-problem) so the interim setup gets static routes and a configurable DNS handout

**Mid term**
- Purchase and set up the Netgear GS308 once the management network separation becomes relevant
- Connect all onboard 1G ports to create the full dual-path setup

**Long term**
- Use the second SFP+ port for a bonded MS-01 link, a WiFi AP or a dedicated NAS connection
- Add a second switch when expanding beyond 8 nodes