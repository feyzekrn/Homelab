# Jellyfin

[<- Back to User-Facing Applications](../README.md)

Jellyfin is a fully open-source, self-hosted media server for organizing and streaming movies, shows and music.

In this homelab, Jellyfin is the **chosen media server**, running as an **LXC container on [`pve0`](../../setup/compute/proxmox-cluster)** (`lxc`). [Plex](../plex) remains documented for comparison, but the deployment plan is Jellyfin: it is completely free software, has no account requirement, no paywalled features and no phone-home dependency — which matches the self-hosting philosophy of this whole repository.

Jellyfin scans media libraries, fetches metadata and streams to clients on TVs, phones, browsers and media boxes. It is a community-driven fork of Emby and shares the same infrastructure profile as Plex: persistent metadata, large media volumes, LAN exposure and optional hardware transcoding.

---

## Why It Fits

Jellyfin fits this homelab for the same platform reasons as any media server, plus philosophical ones:

- large media libraries test storage layout decisions
- persistent metadata tests backup separation — config is small and precious, media is huge and replaceable
- hardware transcoding tests device passthrough into an unprivileged container
- no external account: the server works fully offline and stays under local control
- every feature is free — remote access, hardware transcoding, all clients

The decision against Plex is not about quality. Plex has the more polished ecosystem; Jellyfin has no strings attached. For a repository built around open, self-controlled infrastructure, Jellyfin is the consistent choice.

---

## Why It Runs On `pve0`, Not The Cluster

Three reasons, in order of weight:

**The media lives there.** The library is on the `tank/media` dataset of the [ZFS pool](../../infrastructure/platform/storage/zfs-nas), which is a local filesystem on `pve0`. As a container on the same host, Jellyfin reads it through a **bind-mount** — no NFS, no CSI driver, no network hop for every thumbnail and seek. Running it on the cluster would mean exporting terabytes over the network to reach data sitting on the disk next door.

**Transcoding wants the right GPU.** The MS-01's i9-12900H has a 12th-generation iGPU that handles HEVC 10-bit and AV1 in hardware. The Tiny nodes have Skylake-era i5-6500T graphics, which fall back to CPU on exactly the modern codecs a current library is full of — four cores without hyper-threading produce a stuttering stream. The hardware that can transcode is in the Proxmox host, and passing `/dev/dri` into an LXC is a two-line config change rather than a Kubernetes device-plugin exercise.

**The family should not notice cluster experiments.** A rebuild of the three Tiny nodes must not interrupt film night. This is the [availability rule](../../setup/compute/README.md) that produced the two-world split in the first place.

---

## Accounts: Local, Deliberately

Jellyfin is the **one family app that does not use [Keycloak](../../infrastructure/platform/security/rights-management/keycloak) SSO**, and that is a decision rather than an omission.

Jellyfin has no first-class OIDC support. Single sign-on requires a third-party plugin that has a history of breaking across releases — and the failure mode lands on a TV in the living room, at the worst possible moment, in front of people who did not ask for a homelab. The blast radius of a broken login plugin is much larger than the convenience it buys.

The trade is acceptable because of what Jellyfin actually stores: watch state, favourites and per-user library visibility. No documents, no photos, no calendar. One local account per family member, with the credentials in [Vaultwarden](../../infrastructure/platform/security/password-manager/bitwarden), is proportionate to that.

If Jellyfin ever gains native OIDC, this decision is worth revisiting — the accounts already exist in Keycloak for [Nextcloud](../nextcloud) and [Immich](../immich).

---

## Used For

- media library management
- local streaming to TVs, phones and browsers
- remote streaming through the chosen access path
- testing large persistent media volumes and the ZFS dataset model
- testing hardware transcoding (Intel Quick Sync) through container device passthrough
- learning firewall zoning: an exposed service that still reads local storage

---

## Strengths

- 100% free and open source; no accounts, subscriptions or feature gates.
- Hardware transcoding without a paid pass.
- No external dependency: works fully offline.
- Active community and steady release cadence.
- Same learning value as Plex for storage and placement decisions.

---

## Weaknesses

- Client apps on some platforms are less polished than Plex's.
- Metadata matching sometimes needs more manual care.
- No managed relay for remote access — external exposure is your own responsibility (see [Cloudflare Tunnel](../../infrastructure/platform/ingress/cloudflare-tunnel)).
- No native OIDC, so it stays outside the SSO story documented above.

---

## Prerequisites

| Requirement | Why |
|---|---|
| **Disks in `pve0`** → [ZFS pool](../../infrastructure/platform/storage/zfs-nas) | `tank/media` is the library — the hard blocker |
| [Caddy](../../infrastructure/platform/ingress/caddy) | HTTPS under a real hostname |
| [AdGuard Home](../../infrastructure/platform/dns/adguard-home) | Split DNS for the internal name |
| `/dev/dri` passthrough configured | Only for hardware transcoding — start without it |
| DMZ VLAN (50) | Optional but recommended; needs the switch and OPNsense |

**The lightest of the three family apps.** No database, no SSO, no external identity — a container, a read-only bind-mount and a Caddyfile entry. Once the pool exists it is the fastest of them to bring up, which makes it a good first test of the whole `pve0` application pattern before [Nextcloud](../nextcloud) and [Immich](../immich) raise the stakes.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`zfs-nas`](../../infrastructure/platform/storage/zfs-nas) | `tank/media` bind-mounted **read-only** — the library itself |
| Local container volume | Metadata, artwork and watch state — small, and the only part that needs backing up |
| [`caddy`](../../infrastructure/platform/ingress/caddy) | HTTPS reverse proxy for the Proxmox world, with automatic certificates |
| [`adguard-home`](../../infrastructure/platform/dns/adguard-home) | Split DNS: resolves the hostname to Caddy inside the LAN |
| `/dev/dri` passthrough | Intel Quick Sync on the MS-01 iGPU for hardware transcoding |
| [`cloudflare-tunnel`](../../infrastructure/platform/ingress/cloudflare-tunnel) | Optional remote streaming without port forwarding |
| `vzdump` → [`proxmox-backup-server`](../../infrastructure/platform/backup/proxmox-backup-server) | Container backup; the media dataset follows its own strategy |

**Read-only is the point of the first row.** Jellyfin never needs to write to the library — it only reads. Mounting the dataset read-only means a compromised media server, which is the most exposed application in this homelab, cannot encrypt or delete the collection.

---

## Application Examples

- Stream the local media library inside the LAN at full disk speed, no network storage involved.
- Keep metadata and watch state in the container, backed up nightly with `vzdump`.
- Enable Quick Sync transcoding by passing `/dev/dri` into the container.
- Create separate local users for family members with their own watch state and library visibility.
- Cage the container in the DMZ VLAN while it still reads the library locally.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Jellyfin | Fully open source, all features free | Some clients less polished |
| [Plex](../plex) | Polished ecosystem and client coverage | Account required, key features paywalled |
| Emby | Middle ground, commercial | Licensing model, closed components |

---

## Container Notes

Two things are genuinely fiddly about Jellyfin in an LXC, and both are worth knowing before starting:

**GPU passthrough into an unprivileged container.** Quick Sync needs `/dev/dri/renderD128` visible inside the container, which means a device entry in the container config plus matching group ownership — the `render` group ID on the host and inside the container have to line up. This is easier than the Kubernetes equivalent (no device plugin, no node labels), but it is not zero-configuration.

**Network placement versus storage placement.** Jellyfin is the most exposed application here, so it belongs in the **DMZ VLAN (50)** where the firewall keeps it away from everything else. That costs nothing in storage performance precisely because the library arrives by bind-mount rather than over the network — the firewall zone and the data path are independent. This is the concrete payoff of the [ZFS-on-host decision](../../infrastructure/platform/storage/zfs-nas#how-each-consumer-reaches-it).

**Backups split in two.** The container (config, metadata, watch state) is a few hundred megabytes and gets a nightly `vzdump`. The media dataset is terabytes, is mostly re-acquirable, and gets ZFS snapshots plus whatever off-site strategy its value justifies. Treating them as one backup job wastes space; treating the metadata as disposable loses years of watch history.

---

## Hands-On Start

There is **no Helm chart** — Jellyfin is a Proxmox guest, so it follows the `docs` · `config` pattern rather than `docs` · `chart` · `config`.

First evaluation checklist:

1. Create the container and bind-mount a small test directory from `tank/media`, read-only.
2. Start without hardware transcoding and confirm direct play works.
3. Expose it on the LAN only, through [Caddy](../../infrastructure/platform/ingress/caddy) with a real hostname and certificate.
4. Create the family's local accounts.
5. Add `/dev/dri` and verify Quick Sync actually engages — check the transcode logs, do not assume.
6. Move the container into the DMZ VLAN and confirm the bind-mount is unaffected.
7. Consider remote streaming through Cloudflare Tunnel last, and read their terms on media streaming before relying on it.

---

## Runtime Status

Jellyfin is currently `⚫ Inactive`. It is blocked on one thing only: **the ZFS pool needs disks.** `pve0` currently holds a single NVMe carrying the hypervisor, so there is no `tank/media` to mount yet. Once the pool exists, Jellyfin is one of the quickest wins in this repository — a container, a bind-mount and a Caddyfile entry.

---

## Configuration Link

```text
applications/jellyfin/terraform/
```

---

## Documentation

- [Jellyfin documentation](https://jellyfin.org/docs/)
- [Jellyfin GitHub](https://github.com/jellyfin/jellyfin)
- [Wikipedia: Jellyfin](https://en.wikipedia.org/wiki/Jellyfin)
- [Wikipedia: Media server](https://en.wikipedia.org/wiki/Media_server)
