# Nextcloud

[<- Back to User-Facing Applications](../README.md)

Nextcloud is a self-hosted file sync, sharing and productivity platform.

In this homelab, it belongs under `applications` because it is not required for the cluster itself. It is a user-facing app that consumes infrastructure: storage, database, ingress, TLS, backups and identity.

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

- file sync
- file sharing
- personal cloud storage
- document collaboration experiments
- calendar and contacts experiments
- testing SSO with Keycloak
- testing S3-compatible storage with MinIO

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
