# Nextcloud Multi-User And Family Setup

[<- Back to Nextcloud](./README.md)

This guide describes how one Nextcloud instance serves a whole family: individual accounts through [Keycloak](../../infrastructure/platform/security/rights-management/keycloak), private data per person, and deliberate sharing of files and calendars between members.

The goal is the same experience families get from iCloud Family Sharing or a Microsoft 365 Family plan — private spaces by default, shared spaces on purpose — but on hardware the family owns.

---

## Identity: One Login Per Person, Managed In Keycloak

Nextcloud has local user management, but this homelab centralizes identity in Keycloak (OIDC). Every family member gets **one Keycloak account** that works across all user-facing apps — Nextcloud, [Immich](../immich), and whatever comes later. One password (plus MFA) per person, for everything.

Setup outline:

1. Create the `homelab` realm in Keycloak with one user per member, in a `family` group.
2. Create subgroups such as `parents`, `kids`, `admins`.
3. Install the Nextcloud OIDC app (`user_oidc`) and register Nextcloud as a Keycloak client.
4. Map Keycloak groups into Nextcloud groups so permissions follow the identity.
5. Disable local Nextcloud **registration** — but keep one local admin account, see below.

### Keycloak lives in the other world — and that is handled

Nextcloud runs as an LXC on [`pve0`](../../setup/compute/proxmox-cluster); Keycloak is a cluster workload. Left alone, that would mean a cluster rebuild locks the family out of their own files — the exact dependency the [two-world split](../../setup/compute/README.md) exists to prevent.

It is resolved by [anchoring](../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds): Keycloak keeps one replica pinned to a Proxmox-hosted cluster node, and its database is a container on `pve0` outside cluster storage. Logins survive the cluster being wiped.

### Break-glass: keep one local admin

**Do not disable local login entirely**, even though "Keycloak is the only door" is the cleaner-sounding rule. Keep exactly one local admin account, unused for daily work, with its password in [Vaultwarden](../../infrastructure/platform/security/password-manager/bitwarden) on `pve0`.

The reason is circular dependency: if Keycloak is misconfigured or down, the person who must fix it needs to get into Nextcloud to diagnose it — and an OIDC-only Nextcloud will not let them. This is the single most common way a homelab SSO rollout turns a two-hour problem into a weekend.

[Jellyfin](../jellyfin) sits outside this model entirely and keeps local accounts for everyone, because its OIDC support is a third-party plugin not worth depending on.

What each member gets automatically:

- their own files, calendars and contacts — private by default
- their own [sync setup](./synchronization.md) on their devices with per-device app passwords
- optional storage quota (e.g. kids get 50 GB)
- group-based access: apps or folders visible only to `parents`, admin rights only for `admins`

---

## Sharing Files Within The Family

Nextcloud sharing is opt-in per file or folder:

- **Share with a user or group**: a "Family Documents" folder shared with the `family` group appears in everyone's file view and syncs to their devices like any other folder.
- **Group folders app**: admin-defined shared folders (e.g. `Family`, `Household`, `Taxes`) that exist for all members without anyone personally owning them — closer to a shared drive.
- **Public links**: password-protected, expiring links for people without accounts.

A practical family layout:

```text
Personal space (private, per user)
Family/            ← group folder, everyone
Household/         ← group folder, parents only
Media-Inbox/       ← upload-only share for scans, receipts
```

---

## Shared Calendars And Contacts

Calendars are individually shareable, which maps well onto family life:

- each person keeps a private calendar
- a shared **Family** calendar (appointments, holidays, school events) is shared write-access with everyone; it shows up automatically in Apple Calendar on every device through the existing CalDAV account
- read-only sharing works too, e.g. parents see kids' calendars
- a shared address book (via group sharing or the Contacts app) keeps family-wide contacts consistent

Because sync runs over CalDAV/CardDAV, a shared calendar entry created on one phone appears on every family device natively — no extra app needed. This is exactly the iCloud Family calendar experience, self-hosted.

---

## Photos: Handled By Immich

Photos deliberately live in [Immich](../immich), not Nextcloud — same Keycloak accounts, same model (private libraries, shared albums, partner sharing), but a much better photo experience. See the [Immich family model](../immich/README.md#family-and-multi-user-model).

---

## Roles And Guardrails

Suggested minimal role model:

| Keycloak group | Nextcloud effect |
|---|---|
| `admins` | Nextcloud admin group — settings, apps, users |
| `parents` | Access to `Household/`, larger/no quota |
| `kids` | Quota, no admin apps, restricted sharing if desired |
| `family` | Everyone — receives the shared `Family/` folder and calendar |

Guardrails worth configuring:

- default share permissions (e.g. disable resharing)
- storage quotas per group — and a matching ZFS quota on `tank/nextcloud`, so one account cannot fill the pool that [Immich](../immich) also lives on
- MFA enforced in Keycloak, at least for admin accounts

---

## Rollout Order

1. Get single-user Nextcloud stable first ([README checklist](./README.md#hands-on-start)).
2. **Prove `vzdump` and a restore** before any second person is involved.
3. Add Keycloak OIDC login; verify your own account works end to end, and verify the local break-glass admin still works too.
4. Prove [device sync](./synchronization.md) for yourself for a few weeks.
5. Create family accounts and the shared folder/calendar structure.
6. Onboard one family member as pilot — their devices, their sync.
7. Onboard the rest only when backups and restores are boring routine.

Step 7 is the real threshold. From that point the homelab has **users who did not choose it**, and every outage becomes someone else's problem rather than a learning opportunity. That change is worth making deliberately rather than drifting into it.

---

## Documentation

- [Nextcloud user management](https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_configuration.html)
- [Nextcloud OIDC app (user_oidc)](https://github.com/nextcloud/user_oidc)
- [Nextcloud Group folders app](https://github.com/nextcloud/groupfolders)
- [Nextcloud calendar sharing](https://docs.nextcloud.com/server/latest/user_manual/en/groupware/calendar.html)
- [Keycloak documentation](https://www.keycloak.org/documentation)
