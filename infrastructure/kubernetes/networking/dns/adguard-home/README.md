# AdGuard Home

[<- Back to DNS](../README.md)

AdGuard Home is a network-wide DNS resolver with built-in ad, tracker and malware-domain blocking, configured through a modern web UI.

In this homelab, AdGuard Home is the **chosen LAN-facing resolver**: the DNS server that all household devices receive via DHCP. It filters unwanted domains, caches answers, forwards internal homelab zones to CoreDNS and sends everything else to an encrypted public upstream.

It works at the DNS level: when a device asks for a known ad or tracking domain, AdGuard Home answers with a blocked response instead of the real IP. Every device on the network benefits — phones, TVs, consoles — without installing anything on them.

---

## Why It Fits

AdGuard Home was chosen over Pi-hole for this project because:

- encrypted upstreams (DNS-over-HTTPS/TLS/QUIC) are built in, no extra sidecar needed
- it can also *serve* encrypted DNS to clients, useful for phones outside the LAN
- per-client settings and parental controls fit the multi-user family goal
- DNS rewrites for internal names are a first-class UI feature
- single Go binary, easy to run in Kubernetes
- configuration lives in one YAML file, which suits a GitOps mindset

It is also a genuinely useful always-on service: the first component where the family notices the homelab exists — in a good way.

---

## Used For

- network-wide ad and tracker blocking
- the default DNS resolver handed out by DHCP
- forwarding internal zones to CoreDNS
- encrypted DNS upstreams (DoH/DoT)
- per-device filtering rules and safe search for kids' devices
- DNS query statistics and debugging

---

## Strengths

- Modern UI with per-client configuration.
- Native encrypted DNS on both the client and upstream side.
- Built-in DNS rewrites for internal homelab names.
- Single binary with one config file; container-friendly.
- Actively developed by the AdGuard team.

---

## Weaknesses

- Smaller community than Pi-hole; fewer third-party guides.
- DNS-level blocking cannot remove ads served from first-party domains (e.g. YouTube).
- Becomes household-critical: outages affect everyone immediately.
- Statistics/query log grow and should be bounded on small volumes.
- Backed by a company with commercial products (the Home component itself is open source).

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../metallb`](../../metallb) | Stable LAN IP — DNS clients need a fixed address, not ingress |
| [`../coredns`](../coredns) | Upstream for internal homelab zones |
| [`../../../storage/longhorn`](../../../storage/longhorn) | Persistence for config, filters and query log |
| [`../../../../network`](../../../../network) | MikroTik DHCP must hand out the AdGuard IP |
| [`../../traefik`](../../traefik) | Optional HTTPS exposure of the admin UI only |

---

## Application Examples

- Hand out AdGuard Home as primary DNS via MikroTik DHCP.
- Rewrite `*.home.example.com` to the Traefik LoadBalancer IP.
- Give a child's tablet a stricter filtering profile than adult devices.
- Use the query log to find which device is phoning home at 3 a.m.
- Forward everything else to a DoH upstream so the ISP sees no plain-text DNS.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| AdGuard Home | Modern UI, encrypted DNS, per-client rules | Smaller ecosystem than Pi-hole |
| [Pi-hole](../pihole) | Huge community, classic homelab standard | Encrypted upstreams need extra components |
| Blocky | Lightweight, config-file-only blocker | No UI at all |
| NextDNS | Managed cloud filtering | Not self-hosted, subscription limits |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Deploy with a persistent volume and a MetalLB service on TCP/UDP 53.
2. Point a single test device at it manually before touching DHCP.
3. Configure encrypted upstreams and enable the default blocklists.
4. Add DNS rewrites (or conditional forwarding to CoreDNS) for internal zones.
5. Verify blocking works, then update MikroTik DHCP for the whole LAN.
6. Configure a fallback DNS in DHCP before the family depends on it.

---

## Runtime Status

AdGuard Home is currently `⚫ Inactive`. It is planned as the household resolver once the cluster networking baseline (MetalLB, stable IPs) is in place.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/networking/dns/adguard-home/
```

---

## Documentation

- [AdGuard Home documentation](https://github.com/AdguardTeam/AdGuardHome/wiki)
- [AdGuard Home GitHub](https://github.com/AdguardTeam/AdGuardHome)
- [Wikipedia: AdGuard](https://en.wikipedia.org/wiki/AdGuard)
- [Wikipedia: DNS sinkhole](https://en.wikipedia.org/wiki/DNS_sinkhole)
