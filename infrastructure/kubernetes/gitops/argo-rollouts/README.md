# Argo Rollouts

[← Back to GitOps](../README.md)

Argo Rollouts adds **progressive delivery** to Kubernetes: blue/green and canary deployments, with automated analysis and rollback. It comes from the same project family as [Argo CD](../argocd) and is designed to be used alongside it.

It is **planned for later** — after the cluster runs, after Argo CD syncs it, and after there is at least one service where a failed release would actually hurt.

---

## What Problem It Solves

A standard Kubernetes `Deployment` offers exactly one update strategy worth using: rolling update. Pods are replaced gradually, and if the new version is broken, it is rolled out to everyone anyway — Kubernetes only checks that containers start, not that they behave.

Argo Rollouts replaces the `Deployment` object with a `Rollout` object that understands release *strategies*:

- **Blue/green** — the new version runs fully alongside the old one, receives no user traffic, gets verified, and then traffic switches over in one step. Rollback is switching back.
- **Canary** — the new version receives a small share of traffic (5%, then 25%, then 50%…), with pauses in between, either manual or gated by metrics.
- **Automated analysis** — during those pauses, Rollouts queries [Prometheus](../../../platform/observability/metrics/prometheus) and aborts the release automatically if error rate or latency degrades.

That last point is what makes it more than a deployment gimmick: the release decision becomes data-driven instead of "it seemed fine when I looked".

---

## Why It Is Documented Now

This project explicitly aims at how companies deploy software, and progressive delivery is the standard answer there. Documenting it early prevents a common homelab mistake: hand-building blue/green with two Services and a manually edited selector. That works, teaches the concept once, and then becomes a fragile thing to maintain. The proper tool exists, is small, and is the same tool used at work.

---

## Why Not Immediately

- Nothing is deployed yet — a rollout strategy for zero services is theatre.
- Canary analysis needs metrics, so [Prometheus](../../../platform/observability/metrics/prometheus) has to exist first.
- Traffic-splitting canaries want an ingress that supports weighted routing; [Traefik](../../../platform/ingress/traefik) can do it, but that is one more thing to configure correctly.
- For most homelab services, a rolling update is genuinely enough. Jellyfin does not need a canary.

The right first candidate is a custom service from [`services`](../../../../services) with real users — exactly where a bad release is noticed and a rollback matters.

---

## Runtime Status

`⚫ Inactive` — planned after Argo CD, Prometheus and the first custom service exist.

---

## Documentation

- [Argo Rollouts documentation](https://argo-rollouts.readthedocs.io/)
- [Argo Rollouts concepts](https://argo-rollouts.readthedocs.io/en/stable/concepts/)
- [Wikipedia: Blue-green deployment](https://en.wikipedia.org/wiki/Blue-green_deployment)
- [Wikipedia: Canary release](https://en.wikipedia.org/wiki/Feature_toggle#Canary_release)
