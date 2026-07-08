# Nextcloud Multi-User And Family Setup

[<- Back to Nextcloud](./README.md)

This guide describes how one Nextcloud instance serves a whole family: individual accounts through [Keycloak](../../security/rights-management/keycloak), private data per person, and deliberate sharing of files and calendars between members.

The goal is the same experience families get from iCloud Family Sharing or a Microsoft 365 Family plan — private spaces by default, shared spaces on purpose — but on hardware the family owns.

---

## Identity: One Login Per Person, Managed In Keycloak

Nextcloud has local user management, but this homelab centralizes identity in Keycloak (OIDC). Every family member gets **one Keycloak account** that works across all user-facing apps — Nextcloud, [Immich](../immich), and whatever comes later. One password (plus MFA) per person, for everything.

Setup outline:

1. Create a realm (e.g. `family`) in Keycloak with one user per member.
2. Create Keycloak groups such as `parents`, `kids`, `admins`.
3. Install the Nextcloud OIDC app (`user_oidc`) and register Nextcloud as a Keycloak client.
4. Map Keycloak groups into Nextcloud groups so permissions follow the identity.
5. Disable local Nextcloud registration; Keycloak is the only door.

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
- storage quotas per group
- MFA enforced in Keycloak, at least for admin accounts

---

## Rollout Order

1. Get single-user Nextcloud stable first ([README checklist](./README.md#hands-on-start)).
2. Add Keycloak OIDC login; verify your own account works end to end.
3. Prove [device sync](./synchronization.md) for yourself for a few weeks.
4. Create family accounts and the shared folder/calendar structure.
5. Onboard one family member as pilot — their devices, their sync.
6. Onboard the rest only when backups and restores are boring routine. Family data raises the stakes: from that point on, the homelab has users who did not choose it.

---

## Documentation

- [Nextcloud user management](https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_configuration.html)
- [Nextcloud OIDC app (user_oidc)](https://github.com/nextcloud/user_oidc)
- [Nextcloud Group folders app](https://github.com/nextcloud/groupfolders)
- [Nextcloud calendar sharing](https://docs.nextcloud.com/server/latest/user_manual/en/groupware/calendar.html)
- [Keycloak documentation](https://www.keycloak.org/documentation)
