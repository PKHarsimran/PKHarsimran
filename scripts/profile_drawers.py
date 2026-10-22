"""Small, responsive drawer labels that keep GitHub's native disclosure controls."""
from html import escape
from pathlib import Path

from profile_theme import apply_theme

ROOT = Path(__file__).resolve().parents[1]
DRAWERS = {
    'thread': ('Pull the thread', 'One curiosity. Four builds. Follow the connections.', '#43E6C5'),
    'evidence': ('Evidence desk', 'Real feed snapshot + a 12-second walkthrough', '#43E6C5'),
    'case': ('Case desk', 'Weekly case + a three-chapter CLI replay', '#A995FF'),
    'offline': ('Offline field trip', 'One site. No server. A real CLI demo.', '#F36BAA'),
    'crew': ('Meet the service crew', 'Media, libraries, dashboards & monitoring', '#A995FF'),
    'heist': ("Today's Signal Heist", 'Three clues. One code. A creature to uncover.', '#43E6C5'),
    'snake': ('Release the snake', 'A bonus lap around the contribution grid', '#43E6C5'),
    'radar': ('Project radar', 'Build checks, releases & collectible patches', '#69B9FF'),
    'backstage': ('Behind the curtain', 'The workflows that keep this profile moving', '#A995FF'),
}
MOBILE_HINTS = {
    'thread': 'One curiosity. Four builds.',
    'evidence': 'Feed snapshot + dashboard replay',
    'case': 'Weekly case + CLI replay',
    'offline': 'Save a site. Unplug. Explore.',
    'crew': 'Media, libraries + monitoring',
    'heist': 'Crack the code. Meet a creature.',
    'snake': 'A bonus lap around the grid',
    'radar': 'Checks, releases + patches',
    'backstage': 'Meet the profile workflows',
}
ICONS = {
    'thread': '<path d="M-11 7Q-4-12 2 0T12-7"/><circle cx="-11" cy="7" r="2"/><circle cx="2" cy="0" r="2"/><circle cx="12" cy="-7" r="2"/>',
    'evidence': '<path d="M-9 4L0-8L10 1L3 10Z"/><circle cx="-9" cy="4" r="2"/><circle cx="0" cy="-8" r="2"/><circle cx="10" cy="1" r="2"/><circle cx="3" cy="10" r="2"/>',
    'case': '<path d="M-9-11H3L8-6V-1M3-11V-6H8M-9-11V10H-3"/><circle cx="3" cy="3" r="6"/><path d="M7 7L12 12"/>',
    'offline': '<path d="M-11-9H-2L0-6H11V10H-11ZM0-2V6M-4 2L0 6L4 2"/>',
    'crew': '<rect x="-11" y="-10" width="22" height="8" rx="2"/><rect x="-11" y="3" width="22" height="8" rx="2"/><path d="M-7-6H-5M-7 7H-5M3-6H7M3 7H7"/>',
    'heist': '<rect x="-11" y="-11" width="22" height="22" rx="5"/><circle cx="-5" cy="-5" r="1"/><circle cx="5" cy="-5" r="1"/><circle cx="0" cy="0" r="1"/><circle cx="-5" cy="5" r="1"/><circle cx="5" cy="5" r="1"/>',
    'snake': '<path d="M-11 8H3V1H-5V-7H11"/><rect x="5" y="-11" width="9" height="8" rx="2"/><path d="M10-8V-7"/>',
    'radar': '<circle r="11"/><circle r="5"/><path d="M0-13V-8M0 8V13M-13 0H-8M8 0H13M0 0L8-8"/>',
    'backstage': '<rect x="-4" y="-12" width="8" height="7" rx="1"/><rect x="-12" y="5" width="8" height="7" rx="1"/><rect x="4" y="5" width="8" height="7" rx="1"/><path d="M0-5V0M-8 5V0H8V5"/>',
}


def summary(name):
    title, hint, _ = DRAWERS[name]
    version = '?v=drawer-polish-3'
    # Keep whitespace out of the inline picture so the native marker has room.
    return ('<summary><picture>'
            f'<source media="(max-width: 600px)" srcset="./profile/drawers/{name}-mobile.svg{version}">'
            f'<img src="./profile/drawers/{name}.svg{version}" alt="{escape(title+": "+hint, quote=True)}" width="92%" align="middle">'
            '</picture></summary>\n<br>')


def render(name, mobile=False):
    title, hint, color = DRAWERS[name]
    w, h = (600, 100) if mobile else (1000, 80)
    cy, tx = h // 2, 80
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="drawer-title" font-family="Segoe UI,Arial,sans-serif">',
         f'<title id="drawer-title">{escape(title+": "+hint)}</title>',
         '<defs><linearGradient id="drawer-surface" x2="1" y2="1"><stop stop-color="#172232"/><stop offset="1" stop-color="#101722"/></linearGradient></defs>',
         '<style>.drawer-orbit{transform-box:fill-box;transform-origin:center;animation:drawer-orbit 18s linear infinite}.drawer-cue{animation:drawer-cue 12s ease-in-out infinite}@keyframes drawer-orbit{to{transform:rotate(360deg)}}@keyframes drawer-cue{0%,66%,100%{opacity:.3}78%,86%{opacity:.8}}@media(prefers-reduced-motion:reduce){.drawer-orbit,.drawer-cue{animation:none}.drawer-cue{opacity:.6}}</style>',
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="url(#drawer-surface)" stroke="#34445C"/>',
         f'<path d="M18 2H{w-18}" stroke="{color}" stroke-opacity=".12" stroke-linecap="round"/>',
         f'<path d="M2 20V{h-20}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>',
         f'<circle cx="40" cy="{cy}" r="24" fill="{color}" fill-opacity=".08"/>',
         f'<g transform="translate(40 {cy})"><circle class="drawer-orbit" r="20" fill="none" stroke="{color}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="13 113"/></g>',
         f'<g transform="translate(40 {cy})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>',
         f'<text x="{tx}" y="{40 if mobile else 34}" font-size="{30 if mobile else 24}" font-weight="700" fill="#EFF4FC">{escape(title)}</text>']
    p.append(f'<text x="{tx}" y="{78 if mobile else 60}" font-size="{24 if mobile else 18}" fill="#B8C6DB">{escape(MOBILE_HINTS[name] if mobile else hint)}</text>')
    p += [f'<g class="drawer-cue" fill="{color}">',
          ''.join(f'<circle cx="{w-30+offset}" cy="{cy}" r="1.8"/>' for offset in (-7,0,7)), '</g></svg>']
    return apply_theme('\n'.join(p))


if __name__ == '__main__':
    out = ROOT / 'profile/drawers'
    out.mkdir(exist_ok=True)
    for name in DRAWERS:
        for mobile in (False, True):
            (out / (name+('-mobile' if mobile else '')+'.svg')).write_text(render(name, mobile), encoding='utf-8')
