# Password Manager

[<- Back to Security](../README.md)

This directory documents human password management: the vault where people store login credentials, passkeys, recovery codes and shared family secrets.

This is deliberately separate from the rest of the security stack. The [Secret Store](../secret-store) holds **application** secrets — database passwords, API tokens, service credentials that workloads read at runtime. A password manager holds **human** secrets — the things a person types or autofills. Collapsing these into one system mixes very different threat models and access patterns.

A self-hosted password manager is one of the highest-value homelab services: every family member benefits daily, and the data is small, precious and perfectly suited to practicing serious backup discipline.

---

## Why This Matters

Passwords are the keys to everything else. Browser-saved passwords, reused passwords and sticky notes are how personal accounts get compromised. A password manager generates unique credentials per site and autofills them on every device.

Self-hosting it adds control: the encrypted vault lives on homelab hardware instead of a vendor's cloud. Because vaults are end-to-end encrypted client-side, the server only ever sees ciphertext — which also means self-hosting it is *less* risky than it sounds, but **losing the server without backups means losing every password**.

In companies, the same split exists: a workforce password manager for humans, and Vault-style systems for machines. Knowing which secret belongs where is a professional skill this repository wants to teach.

---

## What You Can Do With It

- unique, generated passwords for every account
- autofill on iOS, Android, macOS, Windows and all browsers
- passkeys, TOTP codes and secure notes in one place
- shared collections for family credentials (WiFi, streaming, banking access for partners)
- developer-friendly access: CLI and API for scripts and dotfiles
- emergency access and recovery workflows

---

## Component Catalog

| Name | Path | Status | Recommendation | Purpose |
|---|---|---|---|---|
| Bitwarden (Vaultwarden) | [docs](./bitwarden) · [chart](../../../../helm-charts/infrastructure/platform/security/password-manager/bitwarden) · [config](./bitwarden/terraform) | ⚫ Inactive | Chosen password manager (via Vaultwarden server) | Family password vault with clients on every platform |

---

## Naming Note

Not to be confused with **BitLocker**, Microsoft's full-disk encryption for Windows. BitLocker encrypts a drive against physical theft; Bitwarden manages login credentials. The names are similar, the jobs are unrelated.

---

## Learning Links

- [Wikipedia: Password manager](https://en.wikipedia.org/wiki/Password_manager)
- [Wikipedia: End-to-end encryption](https://en.wikipedia.org/wiki/End-to-end_encryption)
- [Wikipedia: WebAuthn](https://en.wikipedia.org/wiki/WebAuthn)
