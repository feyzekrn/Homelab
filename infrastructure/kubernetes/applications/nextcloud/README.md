# Nextcloud

[<- Back to User-Facing Applications](../README.md)

Nextcloud is a self-hosted file sync, sharing and productivity platform.

In this homelab, Nextcloud is the **chosen personal cloud**: it will replace iCloud and OneDrive as the source of truth for files, calendars and contacts, serving the whole family through [Keycloak](../../security/rights-management/keycloak) accounts. It was chosen over [ownCloud](../owncloud) because everything needed is open source without an enterprise tier or paywall.

It belongs under `applications` because it is not required for the cluster itself. It is a user-facing app that consumes infrastructure: storage, database, ingress, TLS, backups and identity.

Nextcloud is often described as a self-hosted personal cloud. It can store files, sync them between devices, share links, manage calendars and contacts and integrate with office/collaboration features depending on installed apps.

From a platform perspective, Nextcloud is valuable because it is a real stateful application. It needs persistent storage, a database, caching, web ingress, TLS, background jobs and backups. That makes it a practical test of whether the homelab can run software people actually rely on.

---

## Detailed Guides

The README stays at overview level. The operational details live in dedicated guides:

| Guide | Covers |
|---|---|
| [Synchronization](./synchronization.md) | Replacing iCloud/OneDrive: CalDAV/CardDAV/WebDAV sync with Apple and Windows devices, app passwords, migration checklist |
| [Multi-User And Family Setup](./multi-user-family.md) | Keycloak SSO, one account per family member, shared folders, shared calendars, roles and quotas |

Photos are deliberately **not** Nextcloud's job in this homelab — see [Immich](../immich) for the family photo cloud.

---

## Why It Fits

Nextcloud is a good homelab application because it exercises many real platform concerns without being artificial:

- persistent storage
- database reliability
- object storage integration
- ingress and TLS
- user login and SSO
- backups and restore testing
- mobile and desktop clients

It is useful both as a personal tool and as a practical test of whether the cluster can run stateful web applications.

---

## Used For

- file sync across Apple, Windows and Linux devices ([guide](./synchronization.md))
- calendar and contact sync as the source of truth instead of iCloud/OneDrive
- file sharing inside and outside the family
- personal cloud storage
- family accounts and shared data through Keycloak SSO ([guide](./multi-user-family.md))
- document collaboration experiments
- testing S3-compatible storage with MinIO

---

## Strengths

- Real user-facing workload with practical value.
- Exercises many platform layers at once.
- Strong ecosystem of clients and plugins.
- Useful for testing SSO, backups and object storage.
- Good example of why stateful Kubernetes operation matters.

---

## Weaknesses

- Heavier than a simple file browser.
- Needs careful backup and restore planning.
- Performance depends on database, cache and storage choices.
- Plugins can increase maintenance and security surface.
- Object storage mode and filesystem mode have different tradeoffs.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../databases/postgresql`](../../databases/postgresql) | Recommended primary database |
| [`../../databases/redis`](../../databases/redis) | Cache and file locking |
| [`../../storage/longhorn`](../../storage/longhorn) | Persistent application and data volumes |
| [`../../storage/minio`](../../storage/minio) | Optional S3-compatible object storage |
| [`../../networking/traefik`](../../networking/traefik) | HTTP(S) ingress |
| [`../../networking/cert-manager`](../../networking/cert-manager) | TLS certificates |
| [`../../security/rights-management/keycloak`](../../security/rights-management/keycloak) | Optional SSO/OIDC provider |
| [`../../backup/velero`](../../backup/velero) | Backup and restore orchestration |

---

## Application Examples

- Sync files between laptop, phone and homelab.
- Share files with temporary links.
- Store documents in a self-hosted personal cloud.
- Test Keycloak login with a real user-facing app.
- Use MinIO as external object storage for larger file data.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Nextcloud | Broad personal cloud and collaboration features | Heavier than simple file servers |
| [ownCloud](../owncloud) | Lean, fast file sync (oCIS rewrite in Go) | Narrower scope, open-core model |
| Seafile | Efficient file sync | Narrower ecosystem |
| Syncthing | Peer-to-peer file sync | Not a web-based cloud platform |
| File Browser | Simple web file access | Much smaller feature set |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Deploy PostgreSQL and Redis first.
2. Decide whether files live on Longhorn volumes or MinIO object storage.
3. Expose Nextcloud through Traefik.
4. Add TLS through cert-manager.
5. Test login, file upload, sync client and restore from backup.
6. Add Keycloak SSO only after the basic setup is stable.
7. Then follow the [synchronization guide](./synchronization.md) to move devices over, and the [family setup guide](./multi-user-family.md) before onboarding other users.

---

## Runtime Status

Nextcloud is currently `⚫ Inactive`. Add it after core storage, ingress, database and backup workflows are understood.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/applications/nextcloud/
```

---

## Documentation

- [Nextcloud documentation](https://docs.nextcloud.com/)
- [Nextcloud administration manual](https://docs.nextcloud.com/server/latest/admin_manual/)
- [Wikipedia: Nextcloud](https://en.wikipedia.org/wiki/Nextcloud)
- [Wikipedia: File synchronization](https://en.wikipedia.org/wiki/File_synchronization)
