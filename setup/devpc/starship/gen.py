from fontmap import load
m=load()
def g(n,fb=None):
    if n in m: return chr(m[n])
    if fb and fb in m: return chr(m[fb])
    raise SystemExit("FEHLT: "+n)

# Powerline-Trenner
CAP_L = g('ple-left_half_circle_thick')    # E0B6  runde Kappe links
CAP_R = g('ple-right_half_circle_thick')   # E0B4  runde Kappe rechts
SEP_R = g('pl-left_hard_divider')          # E0B0  Pfeil nach rechts
SEP_L = g('pl-right_hard_divider')         # E0B2  Pfeil nach links
LINE  = "─"                            # ─  Verbindungslinie

I = dict(
  # Material-Design-Glyphen: groesser gezeichnet als die fa-/dev-Varianten
  mac=g('md-apple'), linux=g('md-linux'), debian=g('md-debian'),
  ubuntu=g('md-ubuntu'), rpi=g('md-raspberry_pi'), alpine=g('linux-alpine'),
  arch=g('md-arch'), fedora=g('md-fedora'), redhat=g('md-redhat'),
  windows=g('md-microsoft_windows'), unknown=g('md-server'),
  proxmox=g('dev-proxmox'), k8s=g('md-kubernetes'), docker=g('md-docker'),
  branch=g('md-source_branch'), node=g('md-nodejs'), python=g('md-language_python'),
  java=g('md-language_java'), dotnet=g('md-language_csharp'), go=g('md-language_go'),
  rust=g('md-language_rust'), terraform=g('md-terraform'), lock=g('md-lock'),
  clock=g('md-clock_outline'), timer=g('md-timer_outline'),
  check=g('md-check_bold'), cross=g('md-close_thick'),
)

# ── Farbschemata ────────────────────────────────────────────────────────
# Pro Palette nur die vier Segmentfarben, der Prompt-Pfeil und die Linie.
# Schriftfarbe je Segment sowie Gruen/Rot fuer Haekchen und Kreuz werden
# unten automatisch nach Kontrast (mindestens 5:1) berechnet.
import colorsys

PALETTES = {
 "nord":       dict(seg=["#6487b0","#81a1c1","#88c0d0","#8fbcbb"], accent="#88c0d0", line="#3b4252"),
 "ice":        dict(seg=["#7aa2f7","#6545ba","#2ac3de","#7dcfff"], accent="#2ac3de", line="#2c3347"),
 "tokyo":      dict(seg=["#7aa2f7","#bb9af7","#7dcfff","#9ece6a"], accent="#7dcfff", line="#2f3549"),
 "dracula":    dict(seg=["#bd93f9","#ff79c6","#8be9fd","#50fa7b"], accent="#8be9fd", line="#44475a"),
 "catppuccin": dict(seg=["#cba6f7","#f5c2e7","#94e2d5","#89dceb"], accent="#94e2d5", line="#3d3f56"),
 "rosepine":   dict(seg=["#eb6f92","#c4a7e7","#9ccfd8","#f6c177"], accent="#9ccfd8", line="#403d52"),
 "sunset":     dict(seg=["#f7768e","#5e3468","#e0af68","#ff9e64"], accent="#ff9e64", line="#43303a"),
 "gruvbox":    dict(seg=["#d79921","#689d6a","#db5f0e","#9e4c73"], accent="#fabd2f", line="#4a4038"),
 "forest":     dict(seg=["#a7c080","#7fbbb3","#dbbc7f","#e69875"], accent="#a7c080", line="#3d4642"),
 "slate":      dict(seg=["#323a4d","#272e3d","#2f4a45","#2b3446"], accent="#4fd6be", line="#333a4a"),
 "carbon":     dict(seg=["#4a4f5a","#3a3e47","#2f333b","#3a3e47"], accent="#00d4aa", line="#3a3e47"),
}

PALETTE = "nord"
SPACE_ABOVE = 1         # Leerzeilen ueber dem Balken
SPACE_IN_BLOCK = 1      # Leerzeilen zwischen Balken und Eingabepfeil

INK_D, INK_L, MIN_RATIO = "#12101a", "#f4f1fa", 5.0

def _lum(h):
    h=h.lstrip("#"); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]

def _ratio(a,b):
    l1,l2=sorted((_lum(a),_lum(b)),reverse=True); return (l1+.05)/(l2+.05)

def _hex(h,l,s):
    r,g,b=colorsys.hls_to_rgb(h,l,s); return "#%02x%02x%02x"%(round(r*255),round(g*255),round(b*255))

def _ink(bg):
    return INK_D if _ratio(INK_D,bg) >= _ratio(INK_L,bg) else INK_L

def _accent(hue,bg,sat=.80):
    """Farbigste Variante des Farbtons, die MIN_RATIO gegen bg noch schafft."""
    dark = _lum(bg) <= .25
    best=None
    for i in (range(50,99) if dark else range(48,2,-1)):
        c=_hex(hue,i/100,sat); r=_ratio(c,bg)
        if r>=MIN_RATIO: return c
        if best is None or r>best[1]: best=(c,r)
    return best[0]


def _chevron(bg, target=2.0):
    """Sichtbar abgesetzter Ton auf gleichem Grund - fuer Doppel-Trennzeichen."""
    h=bg.lstrip("#"); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    hh,ll,ss=colorsys.rgb_to_hls(r,g,b)
    down = _lum(bg) > .22
    best=None
    for i in range(1,90):
        l2 = ll-(i/100) if down else ll+(i/100)
        if not 0.02 < l2 < 0.98: break
        c=_hex(hh,l2,ss)
        if _ratio(c,bg) >= target: return c
        best=c
    return best or bg


def _sibling(bg, sep=1.3, min_ink=5.0):
    """Nachbarton fuer ein eigenes Segment: sichtbar anders als bg,
    aber die Schrift darauf muss weiter lesbar bleiben."""
    h=bg.lstrip("#"); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    hh,ll,ss=colorsys.rgb_to_hls(r,g,b)
    for direction in ((-1, 1) if _lum(bg) > .22 else (1, -1)):
        for i in range(1, 90):
            l2 = ll + direction*(i/100)
            if not 0.02 < l2 < 0.98: break
            c=_hex(hh,l2,ss)
            if _ratio(c,bg) >= sep and _ratio(_ink(c), c) >= min_ink:
                return c
    return bg

_p = PALETTES[PALETTE]
C = dict(accent=_p["accent"], line=_p["line"])
for _i,_bg in enumerate(_p["seg"], 1):
    C[f"s{_i}"]  = _bg
    C[f"ink{_i}"] = _ink(_bg)
C["m23"]  = _chevron(C["s3"], 1.9)   # leeres Tab zwischen Pfad und Branch
C["m4"]   = _chevron(C["s4"], 1.9)   # leeres Tab zwischen Runtime und Zeiten
C["s4b"]  = _sibling(C["s4"], 1.3)   # eigenes Segment fuer die Uhr
C["ink4b"] = _ink(C["s4b"])
C["ok"]  = _accent(142/360, C["s4"])
C["err"] = _accent(356/360, C["s4"])

_worst = min([_ratio(C[f"ink{i}"], C[f"s{i}"]) for i in (1,2,3,4)]
             + [_ratio(C["ok"], C["s4"]), _ratio(C["err"], C["s4"]),
                _ratio(C["ink4b"], C["s4b"])])
print(f"  leere Tabs: {C['m23']} (links) / {C['m4']} (rechts), Uhr-Tab {C['s4b']}")
print(f"Palette '{PALETTE}': schwaechster Kontrast {_worst:.1f}:1"
      + ("" if _worst >= MIN_RATIO else "   << unter dem Ziel!"))

d = dict(C); d.update(I)
d.update(cap_l=CAP_L, cap_r=CAP_R, sep_r=SEP_R, sep_l=SEP_L, line_ch=LINE)

tpl = r'''"$schema" = 'https://starship.rs/config-schema.json'

# Powerline-Prompt. Farbschema und Abstaende siehe Kopf von gen.py.
# Links : [OS Host Rolle] > [Verzeichnis] > [Git]  ---Linie---  [Kontext Uhr]
# Zeile 2: Eingabe
#
# Erzeugt von ~/.config/starship-tools/gen.py — nicht direkt editieren,
# sonst gehen beim naechsten Lauf die Aenderungen verloren.
# Diese Datei geht 1:1 auch auf die Homelab-Hosts: ~/bin/starship-deploy

format = """\
[{cap_l}](fg:{s1})\
[$os$username$hostname${{custom.proxmox}}${{custom.k8snode}}$container](bg:{s1} fg:{ink1})\
[{sep_r}](fg:{s1} bg:{s2})\
[ $directory ](bg:{s2} fg:{ink2})\
$git_branch$git_status${{custom.gitend}}${{custom.nogitend}}\
$fill\
[{sep_l}](fg:{s4})\
[$kubernetes$nodejs$python$java$dotnet$golang$rust$terraform$cmd_duration](bg:{s4} fg:{ink4})\
$character\
[{sep_r}](fg:{s4} bg:{s4b})\
[$time](bg:{s4b} fg:{ink4b})\
[{cap_r}](fg:{s4b}){below}
[❯](bold fg:{accent}) """

add_newline = true

# Die durchgehende Linie zwischen linker und rechter Seite (wie p10k-Frame)
[fill]
symbol = "{line_ch}"
style = "fg:{line}"

# == Linke Seite ===========================================================

[os]
disabled = false
format = "[ $symbol ]($style)"
style = "bg:{s1} fg:{ink1}"

[os.symbols]
Macos = "{mac}"
Linux = "{linux}"
Debian = "{debian}"
Ubuntu = "{ubuntu}"
Raspbian = "{rpi}"
Alpine = "{alpine}"
Arch = "{arch}"
Fedora = "{fedora}"
Redhat = "{redhat}"
RedHatEnterprise = "{redhat}"
Windows = "{windows}"
Unknown = "{unknown}"

[username]
show_always = false
style_user = "bg:{s1} fg:{ink1}"
style_root = "bg:{s1} fg:{err}"
format = "[$user@]($style)"

[hostname]
ssh_only = false
ssh_symbol = ""
style = "bg:{s1} fg:{ink1}"
format = "[$hostname ]($style)"

# Rollen-Icons leben im selben Segment -> kein Stummel wenn sie fehlen
[custom.proxmox]
description = "Proxmox VE Host"
when = "test -d /etc/pve"
command = ""
symbol = "{proxmox}"
style = "bg:{s1} fg:{ink1}"
format = "[$symbol ]($style)"

[custom.k8snode]
description = "Kubernetes Node"
when = "test -d /var/lib/kubelet || test -d /var/lib/rancher/k3s || test -d /var/lib/rancher/rke2"
command = ""
symbol = "{k8s}"
style = "bg:{s1} fg:{ink1}"
format = "[$symbol ]($style)"

[container]
symbol = "{docker}"
style = "bg:{s1} fg:{ink1}"
format = "[$symbol $name ]($style)"

[directory]
style = "bg:{s2} fg:{ink2}"
format = "[$path]($style)[$read_only]($read_only_style)"
read_only = " {lock}"
read_only_style = "bg:{s2} fg:{ink2}"
truncation_length = 3
truncate_to_repo = true
truncation_symbol = "…/"

# Git bekommt ein eigenes Segment. Der Eingangs-Trenner steckt IM Modul,
# damit ausserhalb eines Repos nichts uebrig bleibt.
[git_branch]
symbol = "{branch}"
style = "bg:{s3} fg:{ink3}"
format = "[{sep_r}](fg:{s2} bg:{m23})[{sep_r}](fg:{m23} bg:{s3})[ $symbol $branch]($style)"

[git_status]
style = "bg:{s3} fg:{ink3}"
format = "[( $all_status$ahead_behind)]($style)"
conflicted = "="
ahead = "^${{count}}"
behind = "v${{count}}"
diverged = "^${{ahead_count}}v${{behind_count}}"
untracked = "?${{count}}"
stashed = "*${{count}}"
modified = "!${{count}}"
staged = "+${{count}}"
renamed = "r${{count}}"
deleted = "x${{count}}"

# Abschluss-Pfeil der linken Gruppe: Farbe haengt davon ab, ob Git da ist.
[custom.gitend]
description = "Abschluss wenn im Git-Repo"
when = 'd=$PWD; while [ -n "$d" ]; do [ -e "$d/.git" ] && exit 0; d=${{d%/*}}; done; exit 1'
command = ""
symbol = "{sep_r}"
style = "fg:{s3}"
format = "[ ](bg:{s3})[$symbol]($style)"

[custom.nogitend]
description = "Abschluss wenn kein Git-Repo"
when = 'd=$PWD; while [ -n "$d" ]; do [ -e "$d/.git" ] && exit 1; d=${{d%/*}}; done; exit 0'
command = ""
symbol = "{sep_r}"
style = "fg:{s2}"
format = "[$symbol]($style)"

# == Rechte Seite (ein Segment, damit nie ein leerer Stummel entsteht) =====

[time]
disabled = false
time_format = "%H:%M"
style = "bg:{s4b} fg:{ink4b}"
format = "[ {clock} $time ]($style)"

[cmd_duration]
min_time = 0
show_milliseconds = false
style = "bg:{s4} fg:{ink4}"
format = "[ {timer} $duration]($style)"

[kubernetes]
disabled = false
symbol = "{k8s}"
style = "bg:{s4} fg:{ink4}"
format = '[ $symbol $context(\({{$namespace}}\))]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})'

[nodejs]
symbol = "{node}"
style = "bg:{s4} fg:{ink4}"
format = "[ $symbol $version]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})"

[python]
symbol = "{python}"
style = "bg:{s4} fg:{ink4}"
format = '[ $symbol $version]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})'

[java]
symbol = "{java}"
style = "bg:{s4} fg:{ink4}"
format = "[ $symbol $version]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})"

[dotnet]
symbol = "{dotnet}"
style = "bg:{s4} fg:{ink4}"
format = "[ $symbol $tfm]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})"

[golang]
symbol = "{go}"
style = "bg:{s4} fg:{ink4}"
format = "[ $symbol $version]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})"

[rust]
symbol = "{rust}"
style = "bg:{s4} fg:{ink4}"
format = "[ $symbol $version]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})"

[terraform]
symbol = "{terraform}"
style = "bg:{s4} fg:{ink4}"
format = "[ $symbol $workspace]($style)[{sep_r}](fg:{s4} bg:{m4})[{sep_r}](fg:{m4} bg:{s4})"

# == Eingabezeile ==========================================================

[character]
format = "$symbol"
success_symbol = "[ {check} ](bold fg:{ok} bg:{s4})"
error_symbol = "[ {cross} ](bold fg:{err} bg:{s4})"
vimcmd_symbol = "[ ❮ ](bold fg:{err} bg:{s4})"
'''

d["below"] = "\n" * SPACE_IN_BLOCK
out = tpl.format(**d)
if SPACE_ABOVE > 1:
    out = out.replace('format = """\\\n', 'format = """\\\n' + "\\n" * (SPACE_ABOVE - 1), 1)
import pathlib, sys
_dest = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 \
        else pathlib.Path(__file__).resolve().parent / "starship.toml"
_dest.parent.mkdir(parents=True, exist_ok=True)
_dest.write_text(out, encoding="utf-8")
print(f"-> {_dest}")
print("geschrieben:", len(out.encode()), "bytes")
print("Trenner:", " ".join(f"U+{ord(c):04X}" for c in (CAP_L,SEP_R,SEP_L,CAP_R)))
