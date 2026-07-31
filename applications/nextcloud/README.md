# Nextcloud

[<- Back to User-Facing Applications](../README.md)

Nextcloud is a self-hosted file sync, sharing and productivity platform.

In this homelab, Nextcloud is the **chosen personal cloud**, running as an **LXC container on [`pve0`](../../setup/compute/proxmox-cluster)** (`lxc`). It will replace iCloud and OneDrive as the source of truth for files, calendars and contacts, serving the whole family through [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) accounts. It was chosen over [ownCloud](../owncloud) because everything needed is open source without an enterprise tier or paywall.

It belongs under `applications` because it is not required for the platform itself. It is a user-facing app that consumes infrastructure: storage, database, ingress, TLS, backups and identity.

---

## Why It Runs On `pve0`

**The data is the reason.** Nextcloud holds the family's documents on the `tank/nextcloud` dataset of the [ZFS pool](../../infrastructure/platform/storage/zfs-nas), reached by **bind-mount** — a local filesystem path, no network storage, no CSI driver. The cluster's 250 GB of Longhorn capacity could not hold it, and exporting it over the network to reach a disk on the same machine would be a detour with no benefit.

**And the availability class is different.** This is the household's source of truth for calendars and contacts. It must not go offline because a Kubernetes experiment went sideways — which is precisely the [two-world split](../../setup/compute/README.md).

**Its database lives in the same container.** PostgreSQL and Redis run inside the Nextcloud LXC rather than in the cluster or in a shared database container. That keeps the whole application one self-contained `vzdump`, with no cross-world dependency and no shared outage that could take Nextcloud and Immich down together.

The one deliberate exception is **identity** — see below.

---

## Identity: The One Cluster Dependency

Nextcloud authenticates against [Keycloak](../../infrastructure/platform/security/rights-management/keycloak), which is a cluster workload. On paper that reintroduces exactly the dependency this placement avoids.

It is resolved by [anchoring](../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds): Keycloak keeps one replica pinned to a Proxmox-hosted cluster node, and its database is an LXC on `pve0` outside cluster storage. A cluster rebuild therefore does not lock the family out.

Two safeguards belong in the deployment regardless:

- **Keep one local admin account**, disabled for daily use but not deleted. Disabling local login entirely means a Keycloak problem locks out the person who has to fix it.
- **Store that credential in [Vaultwarden](../../infrastructure/platform/security/password-manager/bitwarden)** — on `pve0`, reachable when the cluster is not.

---

## Prerequisites

| Requirement | Why |
|---|---|
| **Disks in `pve0`** → [ZFS pool](../../infrastructure/platform/storage/zfs-nas) | `tank/nextcloud` is the data directory — the hard blocker |
| [Caddy](../../infrastructure/platform/ingress/caddy) | HTTPS with a real certificate; clients refuse anything less |
| An own domain | Sync clients need a stable, valid hostname |
| [AdGuard Home](../../infrastructure/platform/dns/adguard-home) | Split DNS so the hostname resolves to Caddy inside the LAN |
| PostgreSQL + Redis in the container | Database and file locking |
| [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) | Family SSO — see above |
| [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel) | Access from outside; without it CalDAV/CardDAV sync only works at home |
| `vzdump` + [PBS](../../infrastructure/platform/backup/proxmox-backup-server) | This holds irreplaceable data from day one |

**Backups are not a later step here.** The moment a phone's calendar is pointed at this server, iCloud stops being the copy — and the migration checklist in the [synchronization guide](./synchronization.md) explicitly says to prove restores before switching anything off.

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
- proving the backup and restore path on data that actually matters

---

## Strengths

- Real user-facing workload with practical value.
- Exercises many platform layers at once: storage, TLS, identity, backup.
- Strong ecosystem of clients and plugins.
- The first honest test of whether SSO and backups actually work.
- Self-contained as an LXC — one container, one backup, one restore.

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
| [`zfs-nas`](../../infrastructure/platform/storage/zfs-nas) | `tank/nextcloud` bind-mounted — the file data |
| [`postgresql`](../../infrastructure/platform/databases/postgresql) | Primary database, **inside the container** |
| [`redis`](../../infrastructure/platform/databases/redis) | Cache and file locking, **inside the container** |
| [`caddy`](../../infrastructure/platform/ingress/caddy) | HTTPS reverse proxy with automatic certificates |
| [`adguard-home`](../../infrastructure/platform/dns/adguard-home) | Split DNS for the internal hostname |
| [`keycloak`](../../infrastructure/platform/security/rights-management/keycloak) | Family SSO via the `user_oidc` app |
| [`cloudflare-tunnel`](../../infrastructure/platform/ingress/cloudflare-tunnel) | Sync from outside the LAN |
| `vzdump` → [`proxmox-backup-server`](../../infrastructure/platform/backup/proxmox-backup-server) | Backup of container and data |
| [`bitwarden`](../../infrastructure/platform/security/password-manager/bitwarden) | Holds the break-glass admin credential |

---

## Application Examples

- Sync files between laptop, phone and homelab at local disk speed.
- Share files with temporary links, with or without an expiry.
- Replace iCloud as the calendar and contact source of truth for every family device.
- Test Keycloak login with the first real user-facing app.
- Restore the whole application from a single `vzdump` and verify nothing was lost.

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

There is **no Helm chart** — Nextcloud is a Proxmox guest and follows the `docs` · `config` pattern.

First evaluation checklist:

1. Create the container; install PostgreSQL and Redis inside it.
2. Bind-mount `tank/nextcloud` as the data directory.
3. Put [Caddy](../../infrastructure/platform/ingress/caddy) in front and confirm a valid certificate on the LAN.
4. Create one local admin account and test upload, sync client and share links.
5. **Set up `vzdump` and restore it once** — before any real data goes in.
6. Add Keycloak SSO only after the basic setup is stable, keeping the local admin as break-glass.
7. Add [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel), because DAV sync is useless if it only works at home.
8. Then follow the [synchronization guide](./synchronization.md) to move devices over, and the [family setup guide](./multi-user-family.md) before onboarding other users.

**Configure the background job runner properly.** Nextcloud's cron drives sync, notifications and cleanup; left on the default AJAX mode it degrades quietly and the symptoms look like unrelated sync bugs.

---

## Runtime Status

Nextcloud is currently `⚫ Inactive`, blocked on the same thing as the other data-heavy apps: **`pve0` needs disks.** There is no `tank/nextcloud` to bind-mount yet.

Once the pool exists it is the first of the three family apps to build, because it is the one with the most demanding migration — calendars and contacts have to move off iCloud device by device, and that is easier to do early than alongside two other new services.

---

## Configuration Link

```text
applications/nextcloud/terraform/
```

---

## Documentation

- [Nextcloud documentation](https://docs.nextcloud.com/)
- [Nextcloud administration manual](https://docs.nextcloud.com/server/latest/admin_manual/)
- [Wikipedia: Nextcloud](https://en.wikipedia.org/wiki/Nextcloud)
- [Wikipedia: File synchronization](https://en.wikipedia.org/wiki/File_synchronization)
