# OpenBao

[← Back to Security](../README.md)

OpenBao is an open-source fork of HashiCorp Vault, maintained under the Linux Foundation. It was created in late 2023 after HashiCorp relicensed Vault from the Mozilla Public License to the Business Source License (BUSL), and it continues the last open-licensed version under the original terms.

It is documented as the **main alternative** to the chosen [Secret Store (Vault)](../secret-store) — and unusually for an alternative, it is a near drop-in one.

---

## Why It Is Documented

- **The API is the same.** OpenBao kept Vault's HTTP API, CLI ergonomics and storage layout. Tooling that speaks Vault — including the [External Secrets Operator](../external-secrets) and most Helm charts — works against OpenBao with a changed endpoint.
- **The licence question is real.** BUSL forbids offering the software as a competing service. That has no consequence for a homelab, but it is the kind of shift worth understanding rather than shrugging at, because it has already changed how teams pick infrastructure tooling.
- **Vendor-neutral governance.** Linux Foundation stewardship means the licence cannot be changed under it again in the same way.
- **It is a genuine escape hatch.** If Vault's direction ever becomes uncomfortable, the migration is a configuration change rather than a redesign — which is exactly what makes documenting it worth the page.

---

## Why It Is Not Chosen

- **Vault is what the industry runs.** This homelab exists partly to build skills that transfer to work, and job postings, tutorials, integration guides and colleagues all say Vault.
- **Ecosystem maturity.** Vault's integrations, secret engines and documentation have a decade of accumulation behind them; OpenBao is catching up but is younger.
- **The licence does not bite here.** BUSL restricts commercial hosting of Vault as a service — irrelevant for a private homelab.

The honest summary: OpenBao is the ideologically cleaner choice, Vault the professionally more useful one. This project takes the second and keeps the first documented, because switching later costs little.

---

## Comparison Notes

| System | Best at | Trade-off |
|---|---|---|
| [Vault](../secret-store) | Industry standard, largest ecosystem, transferable skills (chosen here) | BUSL licence, heavier than the homelab needs |
| OpenBao | Truly open licence, API-compatible, neutral governance | Younger, smaller ecosystem |
| Infisical | Modern UI, developer-friendly, simple setup | Less enterprise-shaped, fewer secret engines |
| [Sealed Secrets](../sealed-secrets) | No server to run at all | Encrypted values only — no rotation, no audit, no dynamic credentials |

---

## Runtime Status

`⚫ Inactive` and not planned. [Vault](../secret-store) is the chosen secret store; this page exists for comparison and as the documented migration target.

---

## Documentation

- [OpenBao documentation](https://openbao.org/docs/)
- [OpenBao GitHub](https://github.com/openbao/openbao)
- [Wikipedia: HashiCorp Vault](https://en.wikipedia.org/wiki/HashiCorp#Vault)
