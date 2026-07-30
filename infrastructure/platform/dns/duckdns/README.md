# DuckDNS

[<- Back to DNS](../README.md)

DuckDNS is a free dynamic DNS service: it gives you a public subdomain (`yourname.duckdns.org`) that always points at your home IP address, even when the ISP changes it.

In this homelab, DuckDNS is **documented but dropped from the plan**. It answers one question — "how does the outside world find my changing home IP?" — and the chosen architecture never asks it: [Cloudflare Tunnel](../../ingress/cloudflare-tunnel) publishes apps through outbound connections, [NetBird](../../ingress/netbird) provides private access through its managed control plane, and certificates are issued over the Cloudflare API on an owned domain. Nothing needs to know the home IP, so nothing needs to track it.

The page stays because dynamic DNS remains the correct answer for a different architecture — one that exposes services directly through a port forward — and because that is the setup most readers arrive with.

Dynamic DNS exists because most home connections have changing IP addresses. A small updater — a cron job or Kubernetes CronJob calling the DuckDNS token API — reports the current IP every few minutes, and the DNS record follows. Combined with a router port forward, services become reachable at a stable name; combined with a DNS-01 webhook, even Let's Encrypt certificates work without any open port.

---

## Why It Is Documented Anyway

DuckDNS earns a page despite not being deployed:

- it is the classic zero-cost answer to "how do I reach my homelab from outside?" and the first thing most readers try
- it teaches the dynamic-DNS concept that also underlies paid DynDNS offerings
- cert-manager can issue real TLS certificates for `*.duckdns.org` names via a community DNS-01 webhook — free valid HTTPS without owning a domain
- it is the honest fallback if the Cloudflare dependency ever becomes unwelcome

**What replaced it.** The decision was not "DuckDNS is bad" but "this architecture has no inbound path at all". A dynamic-DNS name is only useful when something outside is supposed to connect *to* the home IP. Here every external path is outbound-initiated — the tunnel connector dials Cloudflare, the NetBird peer dials its control plane — which removes the port forward, the open firewall rule and the need for a public name in one move. That is a security property first and a convenience second.

For a reader who owns no domain and wants remote access on a budget, DuckDNS plus a port forward remains the shortest path. It is simply a different trade: an open port and a public IP in exchange for owning nothing.

---

## Used For

- a stable public name for a changing home IP
- first remote access experiments with router port forwarding
- Let's Encrypt certificates via DNS-01 webhook (no open ports needed)
- learning how dynamic DNS updaters work (a one-line cron job)

---

## Strengths

- Completely free, up to five subdomains per account.
- Dead-simple token API; the updater is a single `curl` call.
- Community cert-manager webhook enables DNS-01 challenges.
- No client software required — any device that can run cron works.

---

## Weaknesses

- Free community service: no SLA, occasional slowness or outages.
- Only subdomains of `duckdns.org` — no own domain, no vanity names.
- Used with port forwarding, it exposes the home IP directly (the opposite of the tunnel/mesh approach this homelab targets).
- Single-purpose: no zone management, no mail records, no delegation.

---

## Infrastructure Dependencies

The planned shape here (and the typical homelab shape):

| Dependency | Purpose |
|---|---|
| Kubernetes CronJob (or router feature) | Periodic IP update against the DuckDNS API |
| [`cert-manager`](../../ingress/cert-manager) | TLS via the community DuckDNS DNS-01 webhook |
| [`networking`](../../../../setup/networking) | Router port forward, if direct exposure is intended |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| DuckDNS | Free, instant, zero setup | Subdomain only, no guarantees |
| Own domain + Cloudflare | Full control, tunnel support, real DNS | Costs a domain (~10 €/year) |
| dynv6 / deSEC | Free dynamic DNS with more DNS features | Smaller communities |
| No-IP / DynDNS | Long-established commercial DynDNS | Free tiers with renewal nagging |

The short version: DuckDNS for free plumbing names and as the everything-for-zero-cost entry path; the owned Cloudflare domain for user-facing app names. This repository uses both, each for its layer.

---

## Runtime Status

DuckDNS is `⚫ Inactive` and **dropped from the plan**. It answers the question "how does the outside world find my changing home IP" — and in this architecture nothing needs to: [Cloudflare Tunnel](../../ingress/cloudflare-tunnel) publishes apps through outbound connections, [NetBird](../../ingress/netbird) provides private access, and certificates are issued through the Cloudflare API on an own domain. The page stays because dynamic DNS remains the right answer for anyone exposing services directly.

---

## Future Deployment Link

The updater CronJob will live at:

```text
../../../../helm-charts/infrastructure/platform/dns/duckdns/
```

---

## Documentation

- [DuckDNS](https://www.duckdns.org/)
- [DuckDNS install/updater examples](https://www.duckdns.org/install.jsp)
- [cert-manager webhook for DuckDNS (community)](https://github.com/ebrianne/cert-manager-webhook-duckdns)
- [Wikipedia: Dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS)
