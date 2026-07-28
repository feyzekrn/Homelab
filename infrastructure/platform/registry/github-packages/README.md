# GitHub Packages

[← Back to Registry](../README.md)

GitHub Packages is the registry built into GitHub itself. Every repository can publish and consume npm, Maven, NuGet, RubyGems and container images through it, authenticated with the same tokens already used for the repository — and inside GitHub Actions, that token exists automatically.

It is **not planned as homelab infrastructure**, but it is the pragmatic bridge for one specific gap: private npm packages, which the chosen registry cannot serve.

---

## Why It Is In This Catalog

[Harbor](../harbor) is an OCI registry. It stores container images, Helm charts and other OCI artifacts — but it does **not** speak the npm protocol, so `npm publish` has no target in this homelab until [Nexus](../artifact-repository) is deployed.

GitHub Packages closes that gap at zero cost and zero operational effort:

- private npm packages under the personal scope, within the free plan's allowance (500 MB storage, 1 GB monthly transfer — far beyond what a handful of packages consume)
- unlimited for public packages
- publishing from GitHub Actions needs no secret setup: `GITHUB_TOKEN` is injected into every workflow run
- consuming is a two-line `.npmrc` change

It is also worth using once simply to understand the mechanics — scopes, registry routing in `.npmrc`, token permissions — because those concepts transfer directly to Nexus, Artifactory and every other package registry.

---

## Why It Is Not The Long-Term Answer

**It does not run here.** The point of this homelab is to operate the things it depends on: to see how a registry stores artifacts, how retention and access control work, how a supply chain is secured. A hosted registry teaches none of that, and the packages live on someone else's infrastructure.

There is also a coupling argument: artifacts, repositories and CI all sitting with one provider is convenient right up to the moment that provider is unavailable, changes its plans or its quotas.

---

## Comparison Notes

| Option | Best at | Trade-off |
|---|---|---|
| [Harbor](../harbor) | Container images and Helm charts, scanning, RBAC (chosen here) | No npm, Maven or NuGet support |
| GitHub Packages | Zero setup, free for private npm, native in Actions | Not self-hosted, quota-limited, nothing learned about operating a registry |
| [Nexus](../artifact-repository) | Every package format in one place, proxy caching (planned later) | 1.5–2.5 GB RAM, dated interface |
| [Forgejo](../forgejo) | Light multi-format registry alongside a Git server | Its main feature — self-hosted Git — is not needed here |

---

## Runtime Status

`⚫ Inactive` — nothing to deploy. Used opportunistically for private npm packages until [Nexus](../artifact-repository) exists, and worth trying once for the experience of publishing to a real registry.

---

## Documentation

- [GitHub Packages documentation](https://docs.github.com/en/packages)
- [Working with the npm registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry)
