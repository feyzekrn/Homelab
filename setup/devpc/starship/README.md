# Starship — Config, Generator And Shell

[← Back to Dev PC](../README.md)

The shared artefacts. These four files are what the setup scripts install, on the Mac and on the servers alike.

| File | What it is |
|---|---|
| [`starship.toml`](./starship.toml) | The prompt. **Generated — do not edit.** |
| [`gen.py`](./gen.py) | Generates `starship.toml`. Palette, spacing and icons are configured here |
| [`fontmap.py`](./fontmap.py) | Reads the Nerd Font and resolves icons by glyph name |
| [`zshrc`](./zshrc) | Becomes `~/.zshrc` on the Mac |

---

## Why generated

Nerd Font icons live in the Unicode Private Use Area, and those characters do not survive ordinary text editing reliably — they get silently stripped to empty strings, which is invisible in an editor and only shows up in a hex dump. The generator never types a glyph; it looks each one up **by name** in the font's own tables:

```python
mac     = g('md-apple')          # -> U+F0035
proxmox = g('dev-proxmox')       # -> U+E937
```

The full reasoning, including the code point that is widely documented as the Proxmox logo and is not, is in [terminal-designs.md](../terminal-designs.md#why-the-config-is-generated).

## Using the generator

```bash
python3 gen.py                    # writes starship.toml next to the script
python3 gen.py ~/.config/starship.toml   # or straight to a destination
```

It needs Python 3 and the JetBrains Mono Nerd Font installed — `fontmap.py` searches the usual macOS and Linux font directories and tells you how to install it if it finds nothing.

Every run prints the palette's worst contrast ratio. Below 5:1 it says so.

```text
  empty tabs: #3f899f (left) / #528988 (right), clock tab #6ca7a6
Palette 'nord': weakest contrast 5.0:1
-> …/setup/devpc/starship/starship.toml
```

## The knobs

At the top of `gen.py`:

```python
PALETTE        = "nord"   # one of eleven, see terminal-designs.md
SPACE_ABOVE    = 1        # blank lines above the bar
SPACE_IN_BLOCK = 1        # blank lines between the bar and the ❯
```

A palette declares only four background colours, an accent and a line colour. Text colours, the ✔/✘ greens and reds, the empty-tab shades and the clock segment are all computed from those against a 5:1 contrast target — so a new palette cannot accidentally produce unreadable text.
