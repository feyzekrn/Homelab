import struct
import glob, os, sys

# Wo der Nerd Font liegen kann - erster Treffer gewinnt.
FONT_CANDIDATES = [
    "~/Library/Fonts/JetBrainsMonoNerdFont-Regular.ttf",          # macOS, manuell
    "/Library/Fonts/JetBrainsMonoNerdFont-Regular.ttf",           # macOS, systemweit
    "~/Library/Fonts/JetBrainsMono*NerdFont-Regular.ttf",         # macOS, Homebrew-Cask
    "~/.local/share/fonts/JetBrainsMono*NerdFont-Regular.ttf",    # Linux, User
    "/usr/share/fonts/**/JetBrainsMono*NerdFont-Regular.ttf",     # Linux, systemweit
]

def find_font():
    for pat in FONT_CANDIDATES:
        hits = sorted(glob.glob(os.path.expanduser(pat), recursive=True))
        if hits:
            return hits[0]
    sys.exit(
        "Nerd Font nicht gefunden. Erwartet wird JetBrainsMono Nerd Font.\n"
        "  macOS:  brew install --cask font-jetbrains-mono-nerd-font\n"
        "  Linux:  Release von github.com/ryanoasis/nerd-fonts nach ~/.local/share/fonts/"
    )

def load(path=None):
    path = path or find_font()
    f=open(path,'rb').read()
    num=struct.unpack('>H',f[4:6])[0]; tabs={}
    for i in range(num):
        off=12+16*i; tag=f[off:off+4].decode('latin1')
        o,l=struct.unpack('>II',f[off+8:off+16]); tabs[tag]=(o,l)
    co,_=tabs['cmap']; n=struct.unpack('>H',f[co+2:co+4])[0]; best=None
    for i in range(n):
        pid,eid,off=struct.unpack('>HHI',f[co+4+8*i:co+12+8*i])
        fmt=struct.unpack('>H',f[co+off:co+off+2])[0]
        if fmt==12: best=(co+off,12)
        elif fmt==4 and best is None: best=(co+off,4)
    cm={}; so,fmt=best
    if fmt==12:
        ng=struct.unpack('>I',f[so+12:so+16])[0]
        for i in range(ng):
            s,e,g=struct.unpack('>III',f[so+16+12*i:so+28+12*i])
            for c in range(s,e+1): cm[c]=g+(c-s)
    po,pl=tabs['post']; names={}
    if struct.unpack('>I',f[po:po+4])[0]==0x20000:
        ng=struct.unpack('>H',f[po+32:po+34])[0]
        idx=struct.unpack('>%dH'%ng,f[po+34:po+34+2*ng])
        p=po+34+2*ng; extra=[]
        while p<po+pl:
            ln=f[p]; extra.append(f[p+1:p+1+ln].decode('latin1')); p+=1+ln
        for g in range(ng):
            i=idx[g]
            if i>=258 and i-258<len(extra): names[g]=extra[i-258]
    rev={g:c for c,g in cm.items()}
    return {nm:rev[g] for g,nm in names.items() if g in rev}
