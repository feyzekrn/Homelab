# Pi-hole

[<- Back to DNS](../README.md)

Pi-hole is the classic self-hosted DNS sinkhole: a network-wide ad and tracker blocker that acts as the DNS server for a LAN.

In this homelab, Pi-hole is documented as the **most popular alternative** to AdGuard Home. This project deploys [AdGuard Home](../adguard-home) as its LAN resolver, but Pi-hole is so widespread in the homelab world that any reader deciding between the two deserves the comparison.

Pi-hole started on the Raspberry Pi (hence the name) and became the default answer to "how do I block ads for my whole network?". It combines a filtering DNS forwarder (`pihole-FTL`, based on dnsmasq) with a web dashboard, blocklist management and optional DHCP server.

---

## Why It Is Documented

Pi-hole earns a page even though it is not the chosen tool:

- it is the de-facto standard; most homelab DNS tutorials assume it
- comparing it against AdGuard Home is a useful decision-making exercise
- its dnsmasq foundation teaches classic Linux DNS tooling
- an enormous community means nearly every problem is already answered
- if AdGuard Home ever disappoints, Pi-hole is the natural fallback

The choice between the two is close. This project prefers AdGuard Home mainly for built-in encrypted DNS and per-client controls — not because Pi-hole is bad.

---

## Used For

- network-wide ad and tracker blocking
- LAN DNS forwarding and caching
- optional DHCP for small networks
- query logging and network debugging
- the standard reference point when evaluating filtering resolvers

---

## Strengths

- Massive community, documentation and blocklist ecosystem.
- Long, proven track record on tiny hardware.
- Familiar dashboard many homelab users already know.
- Local DNS records and conditional forwarding supported.
- Can replace the router's DHCP if desired.

---

## Weaknesses

- Encrypted upstreams (DoH/DoT) require an extra component such as `cloudflared` or `unbound`.
- Per-client filtering is more limited than AdGuard Home's.
- Architecture (FTL + web + PHP) is heavier to containerize cleanly than a single Go binary.
- Same operational risk as any LAN resolver: when it is down, "the internet is down".

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../../kubernetes/metallb`](../../../kubernetes/metallb) | Stable LAN IP for DNS clients |
| [`../../storage/longhorn`](../../storage/longhorn) | Persistence for config and query database |
| [`../../../../setup/networking`](../../../../setup/networking) | DHCP must hand out the Pi-hole IP |
| Optional `unbound`/`cloudflared` | Encrypted or recursive upstream resolution |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Pi-hole | Community, maturity, familiarity | Encrypted upstreams need extra parts |
| [AdGuard Home](../adguard-home) | Built-in encrypted DNS, per-client rules | Smaller ecosystem |
| Blocky | Minimal GitOps-friendly blocker | No UI |
| Technitium | Full DNS server with blocking | Less common, fewer guides |

---

## Hands-On Start

If evaluating Pi-hole instead of (or against) AdGuard Home:

1. Deploy with a persistent volume and a MetalLB service on port 53.
2. Point one test device at it and verify blocking.
3. Add `unbound` or `cloudflared` if encrypted/recursive upstreams are wanted.
4. Configure local DNS records for internal homelab names.
5. Compare the admin experience directly against AdGuard Home before committing DHCP.

---

## Runtime Status

Pi-hole is `⚫ Inactive` and there is no plan to deploy it. [AdGuard Home](../adguard-home) is the chosen resolver; this page exists for comparison and as a documented fallback.

---

## Future Deployment Link

If it were deployed, the location would be:

```text
../../../../helm-charts/infrastructure/platform/dns/pihole/
```

---

## Documentation

- [Pi-hole documentation](https://docs.pi-hole.net/)
- [Pi-hole GitHub](https://github.com/pi-hole/pi-hole)
- [Wikipedia: Pi-hole](https://en.wikipedia.org/wiki/Pi-hole)
- [Wikipedia: DNS sinkhole](https://en.wikipedia.org/wiki/DNS_sinkhole)
