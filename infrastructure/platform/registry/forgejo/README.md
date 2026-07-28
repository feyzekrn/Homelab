# Forgejo / Gitea

[← Back to Registry](../README.md)

Forgejo is a self-hosted software forge — essentially a lightweight GitHub for the home: repositories, issues, pull requests, a CI engine that runs GitHub-Actions-compatible workflows, and a **built-in package registry** covering npm, Docker, Maven, PyPI, NuGet and a dozen other formats. All of it is a single Go binary using roughly 300 MB of RAM.

Forgejo is a fork of **Gitea**, created in 2022 after Gitea's development moved under a for-profit company; Forgejo continues under the non-profit Codeberg umbrella. Functionally the two remain close relatives — Forgejo is the choice for governance, Gitea for the larger ecosystem.

It is documented as an **alternative**, because it solves the registry problem from an angle the other candidates do not.

---

## Why It Is Documented

- **One process, many formats.** It does in 300 MB what [Nexus](../artifact-repository) needs 2 GB for, if the requirements stay modest.
- **Registry plus forge.** For anyone who wants their code *and* their artifacts off external services, this is the shortest path to both.
- **CI included.** Gitea/Forgejo Actions reuse GitHub Actions workflow syntax, so pipelines are largely portable in either direction.
- **It is a genuine escape route.** If GitHub ever became unattractive — pricing, policy, availability — this is the migration target that would not require rethinking the pipelines.

---

## Why It Is Not Chosen

**Its strongest argument does not apply here.** Repositories and CI live on GitHub deliberately: this project aims at industry-standard tooling, and GitHub Actions is what that means in practice. A self-hosted forge would either duplicate that or replace something working well.

That leaves only the package registry as a reason to run it — and there:

- for container images, [Harbor](../harbor) is clearly stronger (vulnerability scanning, RBAC, replication, retention policies)
- for npm in the short term, [GitHub Packages](../github-packages) costs nothing and needs no server
- for a serious multi-format registry later, [Nexus](../artifact-repository) is the industry reference with proxy caching

Running Forgejo purely as a registry means maintaining a Git server nobody pushes to.

---

## Comparison Notes

| Option | Best at | Trade-off |
|---|---|---|
| [Harbor](../harbor) | Images, charts, scanning, RBAC (chosen here) | Container formats only |
| [Nexus](../artifact-repository) | Every format, proxy caching, industry reference (planned later) | Heavy, dated UI |
| Forgejo / Gitea | Git + CI + registry in one light process | Duplicates GitHub; registry is a secondary feature |
| [GitHub Packages](../github-packages) | Zero effort, free private npm | Hosted, teaches nothing operationally |

---

## Runtime Status

`⚫ Inactive` and not planned.

---

## Documentation

- [Forgejo documentation](https://forgejo.org/docs/latest/)
- [Forgejo package registry](https://forgejo.org/docs/latest/user/packages/)
- [Gitea documentation](https://docs.gitea.com/)
