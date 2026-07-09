# DuckDNS

[<- Back to DNS](../README.md)

DuckDNS is a free dynamic DNS service: it gives you a public subdomain (`yourname.duckdns.org`) that always points at your home IP address, even when the ISP changes it.

In this homelab, DuckDNS is documented as the **free entry path** for readers who do not own a domain. This project itself plans a real domain managed at Cloudflare (see [Cloudflare Tunnel](../../ingress/cloudflare-tunnel)), so DuckDNS is not on the deployment plan — but for a first homelab, "reachable from outside without buying anything" is exactly the problem DuckDNS solves.

Dynamic DNS exists because most home connections have changing IP addresses. A small updater — a cron job or Kubernetes CronJob calling the DuckDNS token API — reports the current IP every few minutes, and the DNS record follows. Combined with a router port forward, services become reachable at a stable name; combined with a DNS-01 webhook, even Let's Encrypt certificates work without any open port.

---

## Why It Is Documented

DuckDNS earns a page even though it is not the chosen tool:

- it is the classic zero-cost answer to "how do I reach my homelab from outside?"
- it teaches the dynamic-DNS concept that also underlies paid DynDNS offerings
- cert-manager can issue real TLS certificates for `*.duckdns.org` names via a community DNS-01 webhook — free valid HTTPS without a domain
- it is the natural stepping stone before buying a domain and moving to Cloudflare or deSEC

The reason it is not chosen here: the target architecture avoids exposing the home IP at all (tunnel/mesh instead of port forwarding), uses an owned domain, and DuckDNS as a free service comes with no availability guarantees.

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

If a reader deploys it, the typical homelab shape is:

| Dependency | Purpose |
|---|---|
| Kubernetes CronJob (or router feature) | Periodic IP update against the DuckDNS API |
| [`../../ingress/cert-manager`](../../ingress/cert-manager) | TLS via the community DuckDNS DNS-01 webhook |
| [`../../../../setup/networking`](../../../../setup/networking) | Router port forward, if direct exposure is intended |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| DuckDNS | Free, instant, zero setup | Subdomain only, no guarantees |
| Own domain + Cloudflare | Full control, tunnel support, real DNS | Costs a domain (~10 €/year) |
| dynv6 / deSEC | Free dynamic DNS with more DNS features | Smaller communities |
| No-IP / DynDNS | Long-established commercial DynDNS | Free tiers with renewal nagging |

The short version: start with DuckDNS if you own nothing; buy a domain the moment the homelab becomes serious — everything in this repository's external-access design assumes an owned domain.

---

## Runtime Status

DuckDNS is `⚫ Inactive` and not planned for this homelab (an owned domain at Cloudflare is). This page exists as the documented free alternative for readers starting from zero.

---

## Future Deployment Link

If it were deployed, the updater CronJob would live at:

```text
../../../../helm-charts/infrastructure/platform/dns/duckdns/
```

---

## Documentation

- [DuckDNS](https://www.duckdns.org/)
- [DuckDNS install/updater examples](https://www.duckdns.org/install.jsp)
- [cert-manager webhook for DuckDNS (community)](https://github.com/ebrianne/cert-manager-webhook-duckdns)
- [Wikipedia: Dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS)
