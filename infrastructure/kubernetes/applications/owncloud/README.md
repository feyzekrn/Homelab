# ownCloud

[<- Back to User-Facing Applications](../README.md)

ownCloud is a self-hosted file sync and share platform — and the project Nextcloud was forked from in 2016.

In this homelab, ownCloud is documented as the **main alternative** to [Nextcloud](../nextcloud), which is the chosen personal cloud. Anyone evaluating a self-hosted cloud will meet both names immediately, so the comparison belongs in this catalog even though only one will be deployed.

There are effectively two ownClouds today:

- **ownCloud Server (classic)**: the original PHP application, feature-frozen in favor of the rewrite.
- **ownCloud Infinite Scale (oCIS)**: a complete rewrite in Go with no PHP and no database requirement, focused on performance and file handling.

oCIS is technically interesting — a single Go binary with built-in identity management is a very different operational profile than the PHP stack. But its feature set is narrower than Nextcloud's (files first; calendar/contacts ecosystems are not the focus), and parts of the ownCloud commercial model gate enterprise features behind subscriptions.

---

## Why It Is Documented

ownCloud earns a page even though it is not the chosen tool:

- the Nextcloud-vs-ownCloud question is unavoidable when researching self-hosted clouds
- the fork history explains *why* Nextcloud's ecosystem looks the way it does
- oCIS shows what a ground-up Go rewrite of this problem looks like
- comparing the licensing models (fully open vs. open core) is exactly the kind of decision this repository wants to teach

This project chose Nextcloud because everything needed — calendar, contacts, file sync, SSO — is open source without an enterprise tier, and because the replace-iCloud/OneDrive goal needs the broad app ecosystem, not only file sync.

---

## Used For

- self-hosted file sync and sharing (its core strength)
- evaluating oCIS as a lightweight, files-focused alternative
- understanding the trade-off between "does everything" and "does files fast"

---

## Strengths

- oCIS: single Go binary, no PHP, no external database, strong file performance.
- Long history and mature sync clients.
- Cleaner scope: files first, less plugin sprawl than Nextcloud.
- Classic server is well understood with years of documentation.

---

## Weaknesses

- Open-core model: some features target paying enterprise customers.
- Smaller self-hosting community than Nextcloud since the fork.
- oCIS covers fewer use cases: the calendar/contacts/groupware story is much weaker.
- Two parallel product lines (classic vs. oCIS) make research confusing.
- For this project's goal (full iCloud/OneDrive replacement) it simply covers less.

---

## Infrastructure Dependencies

If it were deployed, the profile matches Nextcloud's:

| Dependency | Purpose |
|---|---|
| [`../../storage/longhorn`](../../storage/longhorn) | Persistent data volumes |
| [`../../databases/postgresql`](../../databases/postgresql) | Database (classic server only; oCIS needs none) |
| [`../../networking/traefik`](../../networking/traefik) | HTTP(S) ingress |
| [`../../networking/cert-manager`](../../networking/cert-manager) | TLS certificates |
| [`../../security/rights-management/keycloak`](../../security/rights-management/keycloak) | External OIDC identity (oCIS integrates natively) |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| [Nextcloud](../nextcloud) | Full personal cloud: files, calendar, contacts, apps | Heavier, more moving parts |
| ownCloud oCIS | Fast, lean file sync in one Go binary | Narrow scope, open-core model |
| ownCloud classic | Proven PHP file platform | Feature-frozen, superseded by oCIS |
| Seafile | Very efficient sync engine | Niche ecosystem, core features split by edition |

The short version: choose Nextcloud to replace iCloud/OneDrive entirely; consider oCIS when the only requirement is fast file sync and everything else is handled elsewhere.

---

## Runtime Status

ownCloud is `⚫ Inactive` and there is no plan to deploy it. [Nextcloud](../nextcloud) is the chosen personal cloud; this page exists for comparison and decision documentation.

---

## Future Deployment Link

If it were deployed, the location would be:

```text
../../../../helm-charts/applications/owncloud/
```

---

## Documentation

- [ownCloud documentation](https://doc.owncloud.com/)
- [ownCloud Infinite Scale GitHub](https://github.com/owncloud/ocis)
- [Wikipedia: ownCloud](https://en.wikipedia.org/wiki/OwnCloud)
- [Wikipedia: Nextcloud](https://en.wikipedia.org/wiki/Nextcloud) (covers the fork history)
