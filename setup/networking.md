# 🔌 Networking — Switches & Physical Topology

[← Back to Setup Overview](./README.md)

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

Even if you own a high-end Layer 3 router, pairing it with a cheap unmanaged switch is a mistake. Inter-VLAN traffic would still have to travel up to the router and back (**Hairpinning**), destroying your low latencies and bottlenecking your cluster. For Kubernetes, the Layer 3 routing **must** happen directly on the switch hardware where the nodes are physically connected.

### Maxed Switch Setup
All traffic — data and management — runs through the MikroTik. Works up to 4 nodes before all 8× 2.5G RJ45 ports are occupied. The two SFP+ ports remain free for a WiFi AP and Node 5 without dual cable,
if a 5th Node is sat up then there is no room a NAS or future expansion.

```
[  Node 1  ]──  2.5G M.2  ──┐
[  Node 1  ]── 1G onboard ──┤
[  Node 2  ]──  2.5G M.2  ──┤
[  Node 2  ]── 1G onboard ──┤
[  Node 3  ]──  2.5G M.2  ──┤
[  Node 3  ]── 1G onboard ──┤── MikroTik CRS310 ──── Router (WAN only)
[  Node 4  ]──  2.5G M.2  ──┤
[  Node 4  ]── 1G onboard ──┤
[  Node 5  ]──   10G SFP+ ──┤
[   WiFi   ]──   10G SFP+ ──┘
```

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
 
For the current 3-node setup with dual cables: 6 node connections + 1 router uplink = **7 cables minimum**. Buying 10 leaves a few spares for future nodes or replacements.

---

## Management Extension: Netgear GS308 *(When scaling horizontally)*

Not purchased yet — planned for a later stage when a dedicated management network becomes necessary.

| Part | Details | Price | Where to find it |
|---|---|---:|---|
| Netgear GS308 | 8× 1G unmanaged | current market price | [Amazon](https://www.amazon.de/NETGEAR-GS308-300PES-Netgear-neu/dp/B07PTTX7MX) |

The GS308 would serve as a simple 1G extension switch. Its only job is to connect the onboard 1G ports of the Tiny nodes, providing a dedicated path for SSH, monitoring and fallback traffic. No routing or management features needed from it — the MikroTik handles all of that. The GS308 just extends the number of available 1G ports.

### Maxed Dual Switch Setup
Management traffic moves to a dedicated Netgear GS308, freeing all 8× 2.5G ports on the MikroTik for cluster data. Scales up to 7 nodes with a dedicated management path, plus Node 8 connecting via SFP+ for a faster dedicated link.

```
[       Node 1      ]──  2.5G M.2 ──┐
[       Node 2      ]──  2.5G M.2 ──┤
[       Node 3      ]──  2.5G M.2 ──┤
[       Node 4      ]──  2.5G M.2 ──┤
[       Node 5      ]──  2.5G M.2 ──┤
[       Node 6      ]──  2.5G M.2 ──┤── MikroTik CRS310 ──── Router (WAN only)
[       Node 7      ]──  2.5G M.2 ──┤
[       Node 8      ]──  2.5G M.2 ──┤
[   Netgear GS308   ]──  10G SFP+ ──┤
[        WiFi       ]──  10G SFP+ ──┘

[      Node 1     ]── 1G onboard ──┐
[      Node 2     ]── 1G onboard ──┤
[      Node 3     ]── 1G onboard ──┤
[      Node 4     ]── 1G onboard ──┤── Netgear GS308 ──── MikroTik (VLAN trunk)
[      Node 5     ]── 1G onboard ──┤
[      Node 6     ]── 1G onboard ──┤
[      Node 7     ]── 1G onboard ──┤
[ MikroTik CRS310 ]── 1G onboard ──┘
```
The 2.5G link handles all high-throughput Kubernetes and storage traffic directly on the MikroTik's L3 hardware. The 1G link handles management, SSH, monitoring and fallback via the cheap Netgear switch. 

**Why this unmanaged switch does NOT cause Hairpinning:**
Unlike using a cheap switch for the main cluster data, using it purely for the 1G management plane is perfectly fine. The Netgear switch connects to the MikroTik via a dedicated VLAN trunk. Since the MikroTik handles all inter-VLAN routing *before* pushing the packets down to the Netgear, no cluster traffic ever has to travel back up to find its destination. The Netgear simply acts as a dumb port-expander for a single, isolated management network, leaving the MikroTik's premium 2.5G ports entirely free for heavy Kubernetes data.

---

## Alternative Paths (For Budgets Under 200 €)

If you don't have the spare cash for a premium Layer 3 switch like the MikroTik CRS310, you can still protect your home network from collapsing. Here are two budget-friendly architecture alternatives:

### Alternative A: The "Old Router" Trick (0 €)
If you have an old, unused router (e.g., an old Fritz!Box or TP-Link) gathering dust in your basement, you can repurpose it as a dedicated Tier-2 gateway for your Kubernetes nodes.
* **The Setup:** Connect all your mini-PCs directly to the LAN ports of the old router. Then, connect the WAN or LAN1 port of this old router to your main home router. 
* **The Benefit:** The old router handles DHCP and local routing exclusively for the cluster. The heavy Kubernetes communication stays completely trapped inside the old hardware. Your main home router never sees this traffic, keeping your family's internet running smoothly. 
* **The Trade-off:** You will be limited to 1 Gbit/s node-to-node speeds, but your primary network remains entirely safe.

### Alternative B: Cheap Unmanaged 2.5G Switch + Single Subnet (~ 30 € – 50 €)
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

**Mid term**
- Purchase and set up the Netgear GS308 once the management network separation becomes relevant
- Connect all onboard 1G ports to create the full dual-path setup

**Long term**
- Use the SFP+ ports on the MikroTik for a faster uplink or a dedicated NAS connection
- Add a second switch when expanding beyond 7 nodes