# Plex

[<- Back to User-Facing Applications](../README.md)

Plex is a self-hosted media server for organizing and streaming movies, shows, music and other media.

In this homelab, Plex is documented as the **main alternative** to [Jellyfin](../jellyfin), which is the chosen media server. Plex has the more polished client ecosystem, but key features require a Plex account and paid pass — Jellyfin's fully open model fits this repository better. This page stays because Plex vs. Jellyfin is one of the classic homelab decisions.

It belongs under `applications` because it is a user-facing workload. It is not required for the platform itself, but it is a useful real-world app for testing storage, networking and hardware capabilities.

Plex scans a media library, organizes metadata and streams media to clients such as TVs, phones, browsers and media boxes. It is not a database, ingress controller or storage system; it is an application that uses those platform services.

If it were deployed here it would take exactly the same place as [Jellyfin](../jellyfin): an **LXC container on [`pve0`](../../setup/compute/proxmox-cluster)** with the media library bind-mounted from the ZFS pool. The infrastructure profile is identical — the software and the licensing model are what differ.

---

## Why It Fits

Plex is a good homelab workload because it stresses different parts of the platform than typical web apps:

- large media libraries
- persistent metadata, separate from the media itself
- reverse-proxy exposure and firewall zoning
- storage layout and dataset design
- optional hardware transcoding

It also forces a practical decision that shaped this whole repository: **some workloads are easier to run beside Kubernetes than on it.** Media paths, iGPU access and terabyte-scale storage all point at a container on the machine that holds the disks — which is exactly the conclusion the [compute split](../../setup/compute/README.md) reached.

---

## Used For

- media library management
- local streaming
- remote streaming experiments
- testing large persistent media volumes
- testing hardware transcoding support
- learning workload placement: which apps belong beside the cluster rather than on it

---

## Strengths

- Real workload with visible user value.
- Tests storage layout and LAN service exposure.
- Good case study for hardware access and container device passthrough.
- Mature client ecosystem, still the best-in-class TV apps.
- Useful comparison between cluster-hosted and host-hosted deployment models.

---

## Weaknesses

- Requires a Plex account even for a fully local server — the thing this repository is built to avoid.
- Hardware transcoding sits behind Plex Pass, a paid subscription.
- Network discovery and remote access can be more awkward than normal web apps.
- The server phones home; a local-only setup is not the default path.
- It is optional and should not block core platform work.

---

## Infrastructure Dependencies

If it were deployed, the profile would match [Jellyfin](../jellyfin) exactly:

| Dependency | Purpose |
|---|---|
| [`zfs-nas`](../../infrastructure/platform/storage/zfs-nas) | `tank/media` bind-mounted read-only — the library |
| Local container volume | Metadata and watch state |
| [`caddy`](../../infrastructure/platform/ingress/caddy) | HTTPS reverse proxy for the Proxmox world |
| `/dev/dri` passthrough | Intel Quick Sync — but only with a paid Plex Pass |
| `vzdump` | Container backup, separate from the media dataset |

---

## Application Examples

- Stream local media inside the LAN through a bind-mounted library.
- Keep Plex metadata in the container, backed up separately from the media.
- Cage the container in the DMZ VLAN while it still reads storage locally.
- Compare the polished client apps directly against Jellyfin's on the same library.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Plex | Polished media server ecosystem and clients | Some features depend on Plex account or paid plan |
| [Jellyfin](../jellyfin) | Fully open-source media server (chosen for this homelab) | Less polished client ecosystem for some devices |
| Emby | Media server with commercial features | Licensing model differs |

---

## Why Jellyfin Won

The comparison is genuinely close on quality, and pretending otherwise would be dishonest — Plex has better client apps, especially on TVs, and a more forgiving setup experience.

It lost on **ownership**, which is the criterion this repository weights above polish:

| Question | Plex | Jellyfin |
|---|---|---|
| Works with no external account? | No | Yes |
| Hardware transcoding included? | Paid (Plex Pass) | Free |
| Server usable if the vendor disappears? | Uncertain | Yes |
| Can the vendor change the terms? | Yes | No vendor to do so |

A media server that requires an account to play files from a disk two metres away contradicts the premise of the whole project. That is the entire argument — not quality, not features.

---

## Runtime Status

Plex is `⚫ Inactive` and there is **no plan to deploy it**. [Jellyfin](../jellyfin) is the chosen media server; this page exists for comparison and decision documentation, because Plex vs. Jellyfin is one of the classic homelab decisions and the reasoning deserves to be written down rather than assumed.

---

## Documentation

- [Plex Support](https://support.plex.tv/)
- [Plex Docker image](https://hub.docker.com/r/plexinc/pms-docker)
- [Wikipedia: Plex](https://en.wikipedia.org/wiki/Plex_(software))
- [Wikipedia: Media server](https://en.wikipedia.org/wiki/Media_server)
