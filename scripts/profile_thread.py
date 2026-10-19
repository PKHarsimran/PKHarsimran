"""An illustrated, opt-in reading route through four independent public builds."""
from html import escape

from profile_theme import apply_theme

MINT, VIOLET, PINK, BLUE = '#43E6C5', '#A995FF', '#F36BAA', '#69B9FF'
CHAPTERS = (
    ('COLLECT', 'SwiftIOC', 'Keep the sources.', 'Keep the context.', MINT),
    ('INVESTIGATE', 'IOC Inspector', 'Read the clues.', 'Make them legible.', VIOLET),
    ('PRESERVE', 'Website Downloader', 'Keep a useful page.', 'Take it offline.', PINK),
    ('CONNECT', 'Zima homelab', 'Make tools a habit.', 'Keep learning.', BLUE),
)
ICONS = (
    '<path d="M-18 9L-5-13L19-4L8 18Z"/><circle cx="-18" cy="9" r="3"/><circle cx="-5" cy="-13" r="3"/><circle cx="19" cy="-4" r="3"/><circle cx="8" cy="18" r="3"/>',
    '<path d="M-16-21H4L15-10V1M4-21V-10H15M-16-21V20H-3M-9-5H0"/><circle cx="9" cy="11" r="10"/><path d="M16 18L24 26"/>',
    '<rect x="-22" y="-18" width="44" height="35" rx="4"/><path d="M-22-7H22M-15-12H-13M-8-12H-6M0-1V11M-5 6L0 11L5 6"/>',
    '<rect x="-22" y="-21" width="44" height="17" rx="4"/><rect x="-22" y="5" width="44" height="17" rx="4"/><path d="M-14-13H-11M-14 13H-11M3-13H14M3 13H14"/>',
)
STYLE = '''
.thread-spotlight{opacity:0;animation:thread-spotlight 20s linear infinite}
.thread-lamp{animation:thread-lamp 20s linear infinite;opacity:.3}
.thread-runner{animation:thread-runner 20s linear infinite;opacity:0}
.thread-orbit{transform-box:fill-box;transform-origin:center;animation:thread-orbit 40s linear infinite}
@keyframes thread-spotlight{0%,22%{opacity:.65}25%,100%{opacity:0}}
@keyframes thread-lamp{0%,22%{opacity:1}25%,100%{opacity:.3}}
@keyframes thread-runner{0%,2%,98%,100%{opacity:0}5%,94%{opacity:1}}
@keyframes thread-orbit{to{transform:rotate(360deg)}}
@media(prefers-reduced-motion:reduce){.thread-runner{display:none}.thread-spotlight{animation:none;opacity:.25}.thread-lamp{animation:none;opacity:1}.thread-orbit{animation:none}}
'''


def text(x, y, value, size, color='#B8C6DB', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def thread_story(mobile=False):
    w, h = (600, 660) if mobile else (1000, 400)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
         '<title id="title">Pull the thread: curiosity, carried through.</title>',
         '<desc id="desc">A thematic tour of four independent builds: SwiftIOC collects sources and context; IOC Inspector reads document clues; Website Downloader preserves pages offline; the Zima homelab turns tools into everyday habits. A small light follows the illustrated route. These are thematic connections, not a live or integrated pipeline. All chapters remain readable without animation.</desc>',
         f'<style>{STYLE}</style>',
         '<defs><linearGradient id="thread-surface" x2="1" y2="1"><stop stop-color="#141E2F"/><stop offset="1" stop-color="#0C111A"/></linearGradient></defs>',
         f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#thread-surface)" stroke="#29364B"/>',
         text(28, 35, 'FIELD GUIDE / PULL THE THREAD', 18 if mobile else 13, MINT, 500, 'font-family="Consolas,monospace"'),
         text(26, 88, 'Curiosity, carried through.', 38 if mobile else 40, '#EFF4FC', 700),
         text(28, 122, 'Notice a signal. Make something useful.', 22 if mobile else 20)]
    positions = [(28+(i%2)*284, 150+(i//2)*238) for i in range(4)] if mobile else [(28+i*242, 148) for i in range(4)]
    cw, ch = (260, 214) if mobile else (220, 196)
    centers = [(x+cw/2, y+75) for x, y in positions]
    if mobile:
        route = f'M{centers[0][0]} {centers[0][1]}H{centers[1][0]}Q586 {centers[1][1]} 586 344Q586 376 300 376Q14 376 14 426Q14 {centers[2][1]} {centers[2][0]} {centers[2][1]}H{centers[3][0]}'
    else:
        route = 'M138 223H864'
    p += [f'<path d="{route}" fill="none" stroke="#53637D" stroke-opacity=".3" stroke-width="1.3"/>']
    for i, ((x,y), chapter) in enumerate(zip(positions, CHAPTERS)):
        action, name, line, foot, color = chapter
        delay = i*5
        cx, cy = centers[i]
        p += [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="#111A27" stroke="#29364B"/>',
              f'<rect class="thread-spotlight" style="animation-delay:{delay}s" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{color}" fill-opacity=".025" stroke="{color}" stroke-opacity=".55"/>',
              text(x+16, y+27, f'0{i+1} / {action}', 18 if mobile else 12, color, 500, 'font-family="Consolas,monospace"'),
              f'<g transform="translate({cx} {cy})" aria-hidden="true" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">',
              '<g class="thread-orbit"><circle r="31" stroke-opacity=".2" stroke-dasharray="2 9"/></g>', ICONS[i], '</g>',
              text(x+16, y+132, name, 22 if mobile else 19, '#EFF4FC', 700, 'font-family="ProfileDisplay,Segoe UI,Arial,sans-serif"'),
              text(x+16, y+164, line, 20 if mobile else 16),
              text(x+16, y+190 if mobile else y+163+22, foot, 20 if mobile else 16)]
        p += [f'<circle class="thread-lamp" style="animation-delay:{delay}s" cx="{x+cw-17}" cy="{y+23}" r="2.5" fill="{color}"/>']
    p += [f'<g class="thread-runner" aria-hidden="true"><circle r="8" fill="{MINT}" fill-opacity=".07"/><circle r="2.6" fill="{MINT}"/><animateMotion dur="20s" repeatCount="indefinite" path="{route}" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/></g>',
          text(28, h-23, 'FOUR INDEPENDENT BUILDS / ONE CURIOUS MIND', 18 if mobile else 12, '#B8C6DB', 500, 'font-family="Consolas,monospace"'), '</g></svg>']
    return apply_theme(''.join(p))
