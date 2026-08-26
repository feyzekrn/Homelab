# 🪟 Windows

[← Back to Dev PC](../README.md)

> 🔜 **Planned.** No Windows dev machine exists for this homelab, so nothing here is tested.

This folder exists to keep the structure honest: three operating systems are conceivable, one is actually supported.

---

## The Likely Shape

Windows is the one platform where the setup would genuinely differ, because the answer is probably **not to set up Windows at all**.

**WSL2** gives a real Ubuntu userspace. The shell configuration and the prompt would then be the Linux problem, not a Windows one — [`starship.toml`](../starship/starship.toml) works unchanged, and [servers/bootstrap.sh](../servers/bootstrap.sh) is close to what a WSL2 setup would need. Windows Terminal handles Nerd Fonts and renders the Powerline glyphs correctly.

**Native PowerShell** is the other route. Starship supports it — `Invoke-Expression (&starship init powershell)` — and the same config file applies, since the prompt modules are shell-agnostic. What is lost is everything the `zshrc` provides: the history behaviour, the completion styling, the `json` helper. Those would need PowerShell equivalents rather than a translation.

| | WSL2 | Native PowerShell |
|---|---|---|
| `starship.toml` | ✅ unchanged | ✅ unchanged |
| Shell config | ✅ reuse the Linux one | ❌ rewrite as a PowerShell profile |
| Package manager | `apt` inside WSL | `winget` or `scoop` |
| Terminal | Windows Terminal | Windows Terminal |
| Font | Install on the Windows side — WSL does not render anything | same |

The font point is the same one that applies to the servers: glyphs are rendered by the terminal, so the font belongs on the Windows side even when the shell runs in WSL.

---

If a Windows machine ever joins, WSL2 is the path. It collapses this folder into the Linux one and leaves only the font and the terminal profile as genuinely Windows-specific.
