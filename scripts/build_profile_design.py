"""Build repository-owned navigation and action buttons, then update their README slots."""
from html import escape
import argparse
from pathlib import Path
import re
from profile_theme import apply_theme

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'profile/buttons'
MINT,VIOLET,PINK,BLUE='#43E6C5','#A995FF','#F36BAA','#69B9FF'

# label, width, accent, treatment, icon
BUTTONS={
    'website':('Visit website',140,MINT,'primary','globe'),
    'linkedin':('LinkedIn',124,VIOLET,'secondary','chat'),
    'contact':("Let's connect",160,VIOLET,'primary','chat'),
    'projects-tab':('Projects',86,MINT,'nav','01'),
    'homelab-tab':('Homelab',90,VIOLET,'nav','02'),
    'arcade-tab':('Arcade',78,BLUE,'nav','03'),
    'dashboard':('Open dashboard',166,MINT,'primary','play'),
    'quick-start':('Quick start',150,VIOLET,'primary','bolt'),
    'field-guide':('Field guide',150,PINK,'primary','book'),
    'source':('View source',140,MINT,'secondary','code'),
    'source-inspector':('View source',140,VIOLET,'secondary','code'),
    'source-downloader':('View source',140,PINK,'secondary','code'),
    'snapshot':('Read snapshot',160,MINT,'secondary','report'),
    'workflow':('Workflow',138,VIOLET,'secondary','flow'),
    'docker':('Container images',188,BLUE,'secondary','cube'),
    'live-lab':('Enter live lab',176,MINT,'primary','play'),
    'back-top-tab':('Back to top',126,MINT,'nav','up'),
    'spin-pixel':('Spin Pixel',144,VIOLET,'primary','cube'),
}
GROUPS={
    'hero':[('website','https://harsim.ca'),('linkedin','https://www.linkedin.com/in/harsimransidhu/')],
    'navigation':[('projects-tab','#user-content-selected-builds'),('homelab-tab','#user-content-homelab'),('arcade-tab','#user-content-arcade')],
    'swift':[('dashboard','https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/'),('source','https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector')],
    'inspector':[('quick-start','https://github.com/PKHarsimran/IOC-Inspector#-quick-start'),('source-inspector','https://github.com/PKHarsimran/IOC-Inspector')],
    'downloader':[('field-guide','https://github.com/PKHarsimran/website-downloader/wiki'),('source-downloader','https://github.com/PKHarsimran/website-downloader')],
    'containers':[('docker','https://hub.docker.com/u/pkvirus')],
    'live-lab':[('live-lab','https://harsim.ca/lab/')],
    'radar':[('snapshot','./profile/public-pulse.md'),('workflow','https://github.com/PKHarsimran/PKHarsimran/actions/workflows/profile-lab.yml')],
    'footer':[('contact','https://www.linkedin.com/in/harsimransidhu/')],
    'return':[('back-top-tab','#user-content-mission-control')],
    'pocket':[('spin-pixel','./profile/pixel-pocket.stl')],
}
ICONS={
    'globe':'<circle cx="0" cy="0" r="8"/><ellipse cx="0" cy="0" rx="3.5" ry="8"/><path d="M-7-3H7M-7 3H7"/>',
    'chat':'<path d="M-8-7H8V5H-2L-7 9V5H-8Z"/><path d="M-4-2H4M-4 1H2"/>',
    'play':'<path d="M-5-8L8 0L-5 8Z"/>',
    'bolt':'<path d="M2-9L-6 2H0L-2 9L7-3H1Z"/>',
    'book':'<path d="M0-6C-4-9-8-8-9-7V7C-5 5-2 6 0 8C2 6 5 5 9 7V-7C5-9 2-8 0-6ZM0-6V8"/>',
    'code':'<path d="M-4-6L-10 0L-4 6M4-6L10 0L4 6M2-8L-2 8"/>',
    'report':'<path d="M-6-9H3L7-5V9H-6ZM3-9V-5H7M-3-1H3M-3 3H3M-3 6H1"/>',
    'flow':'<rect x="-3" y="-9" width="6" height="5" rx="1"/><rect x="-10" y="4" width="6" height="5" rx="1"/><rect x="4" y="4" width="6" height="5" rx="1"/><path d="M0-4V0M-7 4V0H7V4"/>',
    'cube':'<path d="M0-9L8-4V5L0 10L-8 5V-4ZM-8-4L0 1L8-4M0 1V10M-4-6L4-1"/>',
    'up':'<path d="M-6 0L0-6L6 0M0-6V7"/>',
}


def button(name):
    label,width,color,variant,icon=BUTTONS[name]
    height=44
    fill=color if variant=='primary' else '#121A26'
    foreground='#0D1117' if variant=='primary' else '#EFF4FC'
    border=color if variant=='primary' else '#34445C'
    icon_color=foreground if variant=='primary' else color
    icon_x=16 if variant=='nav' else 22
    label_x=32 if variant=='nav' else 43
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">',f'<title>{escape(label)}</title><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="{9 if variant=="nav" else 11}" fill="{fill}" stroke="{border}"/>']
    if variant=='primary':
        p += ['<style>.cta-icon{animation:invite 9s ease-in-out infinite}@keyframes invite{0%,75%,100%{transform:translateX(0)}82%,91%{transform:translateX(2px)}86%{transform:translateX(0)}}@media(prefers-reduced-motion:reduce){.cta-icon{animation:none}}</style>']
        p += [f'<path d="M13 2H{width-13}" stroke="#FFFFFF" stroke-opacity=".35"/>']
    if icon in ('01','02','03'):
        p += [f'<text x="10" y="26" font-family="Consolas,monospace" font-size="11" fill="{icon_color}">{icon}</text>']
    else:
        p += [f'<g class="{"cta-icon" if variant=="primary" else "icon"}"><g transform="translate({icon_x} {height/2}) scale({.75 if variant=="nav" else .8})" fill="none" stroke="{icon_color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g></g>']
    p += [f'<text x="{label_x}" y="{height/2+5}" font-family="Segoe UI,Arial,sans-serif" font-size="{13 if variant=="nav" else 15}" font-weight="600" fill="{foreground}">{escape(label)}</text>','</svg>\n']
    return apply_theme(''.join(p),'button')


def group(name):
    align='center' if name in ('hero','navigation','footer') else 'left'
    links=[]
    for asset,url in GROUPS[name]:
        label,width,_,variant,_=BUTTONS[asset]
        height=44
        links.append(f'  <a href="{escape(url,quote=True)}"><img src="./profile/buttons/{asset}.svg" alt="{escape(label)}" width="{width}" height="{height}" /></a>')
    return '<p align="'+align+'">\n'+'\n'.join(links)+'\n</p>'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if not args.check:OUT.mkdir(exist_ok=True)
    for name in BUTTONS:
        path=OUT/(name+'.svg')
        content=button(name)
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=content:
                parser.exit(1,'Rebuild with python scripts/build_profile_design.py: '+name+'\n')
        else:path.write_text(content,encoding='utf-8')
    path=ROOT/'README.md'
    original=path.read_text(encoding='utf-8')
    source=original
    for name in GROUPS:
        pattern=rf'<!-- buttons:{name}:start -->.*?<!-- buttons:{name}:end -->'
        source,count=re.subn(pattern,f'<!-- buttons:{name}:start -->\n'+group(name)+f'\n<!-- buttons:{name}:end -->',source,flags=re.S)
        if count<1: raise ValueError('Missing README button slot: '+name)
    if args.check:
        if source!=original:parser.exit(1,'Rebuild README button slots with python scripts/build_profile_design.py\n')
    else:path.write_text(source,encoding='utf-8')
    print(('Verified' if args.check else 'Built')+f' {len(BUTTONS)} action buttons and their README slots.')
