# Immich

[<- Back to User-Facing Applications](../README.md)

Immich is a self-hosted photo and video management platform designed as a direct replacement for Google Photos and iCloud Photos.

In this homelab, Immich is the **chosen family photo cloud**, running as an **LXC container on [`pve0`](../../setup/compute/proxmox-cluster)** (`lxc`). Its mobile apps automatically back up photos and videos from iOS and Android in the background, the web UI provides timeline, search, albums and sharing, and machine-learning features (face recognition, object search) run entirely locally.

Immich is deliberately opinionated about one job: photos. Nextcloud can also store photos, but Immich's mobile backup, timeline performance and ML-powered search are in a different league — which is why this homelab runs both, with a clear split: [Nextcloud](../nextcloud) for files, calendars and contacts; Immich for the photo library.

---

## Why It Fits

Immich fits the "replace iCloud" goal precisely where it hurts most — photos:

- automatic background upload from every family phone, like iCloud Photos
- each user gets a private library; albums can be shared within the family
- partner sharing, shared albums and public links cover the family workflows
- face and object search without sending images to any cloud provider
- OAuth/OIDC login means [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) accounts work here too

It is also an excellent platform test: Immich is a multi-service deployment (server, machine-learning service, PostgreSQL with vector extension, Redis) with real storage growth — much closer to a production application than a single-container app.

---

## Why It Runs On `pve0`

**It is the most storage-hungry application in the homelab, and the least replaceable.** Photo originals live on the `tank/immich` dataset of the [ZFS pool](../../infrastructure/platform/storage/zfs-nas) by **bind-mount** — a local path, not a network share. The cluster's ~250 GB of Longhorn capacity is not a photo library, and it never will be.

**The machine learning wants the right hardware.** Face recognition and semantic search want real CPU and 2–4 GB of RAM. The MS-01's i9-12900H has it; the Tiny nodes have four Skylake cores that the cluster components already share. Later, when a GPU goes into the MS-01's PCIe slot, Immich's ML is one of its first consumers — and it is already on that machine.

**And it holds the data the family would actually miss.** Photos are the least replaceable thing in this homelab. They belong where cluster experiments cannot reach them.

**Its database runs inside the container.** PostgreSQL with the vector extension and Redis both live in the Immich LXC rather than in the cluster. That keeps it one self-contained `vzdump` and avoids a cross-world dependency for a service the family uses daily.

---

## Prerequisites

| Requirement | Why |
|---|---|
| **Disks in `pve0`** → [ZFS pool](../../infrastructure/platform/storage/zfs-nas) | `tank/immich` holds the originals — the hard blocker |
| PostgreSQL **with the vector extension** | Not stock PostgreSQL; Immich needs `pgvecto.rs` or equivalent for search |
| Redis in the container | Job queue — and this one needs persistence, or queued work is lost on restart |
| RAM headroom (2–4 GB for ML) | Budget it against the 32 GB on `pve0`, alongside ZFS ARC and the other guests |
| [Caddy](../../infrastructure/platform/ingress/caddy) | HTTPS with a real certificate |
| [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel) | **Not optional here** — background upload from mobile data is the entire point |
| [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) | Family SSO via native OIDC |
| `vzdump` + `zfs send` off-box | Two layers, because these photos have no other copy once iCloud is cancelled |

**The backup requirement is the strict one.** Every other application here can be rebuilt from documentation. A lost photo library cannot, and the ZFS mirror does not help against a deletion that replicates instantly to both disks.

---

## Family And Multi-User Model

The intended setup mirrors the Nextcloud family model documented in [Nextcloud: Multi-User And Family Setup](../nextcloud/multi-user-family.md):

- every family member gets their own Keycloak identity and logs into Immich with it
- each user has a **private photo area** — uploads from their phone land only in their library
- **shared albums** collect vacations, birthdays and kids' photos across users
- **partner sharing** can expose one user's full timeline to another, like iCloud family features
- public share links (optionally with password/expiry) work for relatives without accounts

The phones keep using their native camera apps. The Immich app syncs the camera roll to the homelab in the background; photos are then viewable on every device through app or browser. External access for uploads on the go runs through [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel).

---

## Used For

- automatic photo/video backup from iOS and Android
- family photo library with private per-user areas
- shared albums and partner sharing
- face recognition and semantic search, fully local
- replacing iCloud Photos / Google Photos storage plans

---

## Strengths

- Best-in-class mobile backup experience among self-hosted options.
- Local ML: face grouping and object search without cloud services.
- True multi-user design with private libraries, sharing and quotas.
- OIDC support for Keycloak SSO.
- Very active development and large community.

---

## Weaknesses

- Fast-moving project: breaking changes between releases happen; read release notes before upgrading.
- Multi-service architecture is heavier to operate than single-container apps.
- ML features want real CPU (or GPU) and RAM.
- Photo storage grows forever — capacity and backup planning is mandatory.
- Deleting the app from a phone does not delete photos there; the mental model (what lives where) must be explained to the family.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`zfs-nas`](../../infrastructure/platform/storage/zfs-nas) | `tank/immich` bind-mounted read-write — the originals |
| [`postgresql`](../../infrastructure/platform/databases/postgresql) | Metadata database with the vector extension, **inside the container** |
| [`redis`](../../infrastructure/platform/databases/redis) | Job queue, **inside the container**, with persistence enabled |
| [`caddy`](../../infrastructure/platform/ingress/caddy) | HTTPS reverse proxy with automatic certificates |
| [`adguard-home`](../../infrastructure/platform/dns/adguard-home) | Split DNS for the internal hostname |
| [`cloudflare-tunnel`](../../infrastructure/platform/ingress/cloudflare-tunnel) | Mobile upload from outside the LAN |
| [`keycloak`](../../infrastructure/platform/security/rights-management/keycloak) | Family SSO via OIDC |
| `vzdump` + `zfs send` | Backups — the least replaceable data in the homelab |
| [`bitwarden`](../../infrastructure/platform/security/password-manager/bitwarden) | Holds the break-glass admin credential |

---

## Application Examples

- Every family phone backs up its camera roll automatically over night.
- A shared "Vacation 2026" album collects photos from all four family members.
- Search "beach" or a person's face and find photos instantly, all locally.
- Grandparents receive a public link to the newest album, no account needed.
- Cancel the iCloud storage plan once a restore test has proven the backups.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Immich | Google-Photos-class experience, self-hosted | Fast-moving, heavier stack |
| Nextcloud Photos/Memories | Photos inside the existing Nextcloud | Weaker mobile backup and search |
| PhotoPrism | Powerful indexing and search of existing folders | Multi-user and mobile backup are weaker |
| LibrePhotos | Open source ML photo management | Smaller community, rougher edges |

---

## Hands-On Start

There is **no Helm chart** — Immich is a Proxmox guest and follows the `docs` · `config` pattern.

First evaluation checklist:

1. Create the container; install PostgreSQL **with the vector extension** and Redis inside it.
2. Bind-mount `tank/immich` and deploy the Immich server plus the ML service.
3. Create one test user, install the mobile app, verify background backup on the LAN.
4. Add Keycloak OIDC login and one account per family member, keeping a local admin as break-glass.
5. Test shared albums and partner sharing between two users.
6. Enable remote upload through Cloudflare Tunnel — without it, backup only happens at home.
7. **Restore a full `vzdump` into a fresh container and confirm the library is intact.**
8. Only then cancel the iCloud storage plan.

**Read the release notes before every upgrade.** Immich moves fast and has shipped breaking changes between minor versions. Pinning a version and upgrading deliberately is the correct posture for the one application whose data cannot be re-created.

---

## Runtime Status

Immich is currently `⚫ Inactive`, blocked on **disks in `pve0`** — there is no `tank/immich` yet.

It is deliberately the **last** of the three family apps to build. Not because it is hardest, but because it is the one where a mistake is permanent: it should go live only after the backup path has been proven by restoring [Nextcloud](../nextcloud) at least once. Photos are the data with no second copy once iCloud is switched off, and step 8 above exists for that reason.

## Documentation

- [Immich documentation](https://immich.app/docs/overview/introduction)
- [Immich GitHub](https://github.com/immich-app/immich)
- [Immich OAuth/OIDC setup](https://immich.app/docs/administration/oauth)
- [Wikipedia: Google Photos](https://en.wikipedia.org/wiki/Google_Photos) (the product being replaced)
