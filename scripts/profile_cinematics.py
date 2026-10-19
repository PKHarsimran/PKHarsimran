"""Small, self-contained SVG stories for the GitHub README. No runtime services."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

from profile_theme import apply_theme

ROOT = Path(__file__).resolve().parents[1]
SVG = 'http://www.w3.org/2000/svg'
N = '{' + SVG + '}'
TEXT, MUTED, MINT, VIOLET, PINK = '#EFF4FC', '#B8C6DB', '#43E6C5', '#A995FF', '#F36BAA'

STYLE = '''
.cinema-ring{transform-box:fill-box;transform-origin:center;animation:cinema-ring 24s linear infinite}
.cinema-scan{animation:cinema-scan 8s ease-in-out infinite}
.cinema-ink{animation:cinema-ink 8s ease-in-out infinite}
.cinema-blink{transform-box:fill-box;transform-origin:center;animation:cinema-blink 7s linear infinite}
.cinema-float{animation:cinema-float 6s ease-in-out infinite}
.cinema-comet{opacity:0;animation:cinema-comet 18s ease-out infinite}
.cinema-confetti{opacity:0;animation:cinema-confetti 18s ease-out infinite}
.cinema-wave{transform-box:fill-box;transform-origin:bottom left;animation:cinema-wave 18s ease-in-out infinite}
.console-frame{opacity:0;animation:console-frame 18s linear infinite}
.console-two{animation-delay:6s}.console-three{animation-delay:12s}
.console-reveal{animation:console-type 6s steps(14,end) infinite}
.portal-patch{animation:portal-patch 18s ease-in-out infinite}
@keyframes cinema-ring{to{transform:rotate(360deg)}}
@keyframes cinema-scan{0%,12%,100%{opacity:0;transform:translateY(-15px)}25%,65%{opacity:.8}78%{opacity:0;transform:translateY(18px)}}
@keyframes cinema-ink{0%,20%,100%{opacity:.35}45%,78%{opacity:1}}
@keyframes cinema-blink{0%,44%,48%,100%{transform:scaleY(1)}46%{transform:scaleY(.15)}}
@keyframes cinema-float{50%{transform:translateY(-5px)}}
@keyframes cinema-comet{0%,70%,100%{opacity:0;transform:translate(0,0)}74%{opacity:.8}82%{opacity:0;transform:translate(38px,20px)}}
@keyframes cinema-confetti{0%,33%,67%,100%{opacity:0;transform:translateY(-8px)}38%,53%{opacity:.9}64%{opacity:0;transform:translateY(30px)}}
@keyframes cinema-wave{0%,35%,65%,100%{transform:rotate(0)}42%,52%{transform:rotate(-20deg)}47%,57%{transform:rotate(9deg)}}
@keyframes console-frame{0%,32%{opacity:1}33.333%,100%{opacity:0}}
@keyframes console-type{0%{width:0}28%,94%{width:var(--line-width)}100%{width:0}}
@keyframes portal-patch{0%,65%,100%{opacity:.45}76%,91%{opacity:1}}
@media(prefers-reduced-motion:reduce){
 .cinema-moving{display:none!important}
 .cinema-ring,.cinema-scan,.cinema-ink,.cinema-blink,.cinema-float,.cinema-wave,.portal-patch{animation:none!important}
 .cinema-scan{opacity:.5}.cinema-ink,.portal-patch{opacity:1}
 .console-frame{animation:none;opacity:0}.console-one{opacity:1}
 .console-reveal{animation:none;width:var(--line-width)}
}
'''


def label(x, y, value, size=12, color=MUTED, weight=500, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def pixel(x, y, scale=1):
    return f'''<g transform="translate({x} {y}) scale({scale})" aria-hidden="true">
      <ellipse cy="45" rx="33" ry="5" fill="{VIOLET}" fill-opacity=".12"/>
      <g class="cinema-float" shape-rendering="crispEdges">
       <path d="M-2-37H2V-26H-2ZM-22-25H22V12H-22ZM-15 12H-5V28H-15ZM5 12H15V28H5Z" fill="{VIOLET}"/>
       <path d="M-4-42H4V-36H-4Z" fill="{PINK}"/>
       <path d="M-16-16H16V1H-16Z" fill="#0B121C"/>
       <g class="cinema-blink"><path d="M-10-11H-4V-5H-10ZM4-11H10V-5H4Z" fill="{MINT}"/></g>
       <path d="M-4 5H4V8H-4Z" fill="#0B121C"/>
       <path d="M-30-8H-22V6H-30Z" fill="{VIOLET}"/>
       <path class="cinema-wave" d="M22-12H30V-28H38V-4H22Z" fill="{PINK}"/>
      </g>
     </g>'''


def packet(path, color, delay=0, duration=8):
    return (f'<g class="cinema-moving" aria-hidden="true"><circle r="2.4" fill="{color}"/>'
            f'<animateMotion dur="{duration}s" begin="{delay}s" repeatCount="indefinite" path="{path}"/></g>')


def project_scene(kind, mobile=False):
    """Three process illustrations; the labels remain readable without animation."""
    width = 544 if mobile else 224
    points = (42, 272, 502) if mobile else (30, 112, 194)
    y = 31 if mobile else 65
    color = {'swiftioc': MINT, 'inspector': VIOLET, 'downloader': PINK}[kind]
    labels = {'swiftioc': ('FEEDS', 'IOCs', 'CONTEXT'),
              'inspector': ('FILE', 'TRIAGE', 'REPORT'),
              'downloader': ('PAGE', 'SAVE', 'OFFLINE')}[kind]
    p = [f'<g data-cinematic="{kind}" aria-hidden="true">', f'<style>{STYLE}</style>',
         f'<rect x="0" y="{0 if mobile else 9}" width="{width}" height="{88 if mobile else 143}" rx="14" fill="{color}" fill-opacity=".035" stroke="{color}" stroke-opacity=".12"/>']
    for start, end in zip(points, points[1:]):
        route = f'M{start+23} {y}H{end-23}'
        p += [f'<path d="{route}" fill="none" stroke="{color}" stroke-opacity=".25" stroke-dasharray="2 5"/>',
              packet(route, color, -2 if start == points[0] else -6)]
    for index, x in enumerate(points):
        p += [f'<g transform="translate({x} {y})" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">']
        if kind == 'swiftioc':
            if index == 0:
                p += ['<rect x="-16" y="-20" width="27" height="31" rx="3" opacity=".35"/><rect x="-10" y="-13" width="27" height="31" rx="3" fill="#121A26"/><path d="M-4-5H11M-4 1H6M-4 7H10"/>']
            elif index == 1:
                p += ['<g class="cinema-ring"><circle r="23" stroke-dasharray="2 8" opacity=".4"/></g>', '<path d="M0-15L15 0L0 15L-15 0Z" fill="#121A26"/><path d="M-5 0L-1 4L6-5"/>']
            else:
                p += ['<path d="M-16-11L0-19L16-8L8 15L-13 17Z" opacity=".5"/><path d="M-16-11L8 15M0-19L-13 17M16-8L-13 17" opacity=".3"/>']
                for px, py in ((-16,-11),(0,-19),(16,-8),(8,15),(-13,17)):
                    p += [f'<circle class="cinema-ink" cx="{px}" cy="{py}" r="3" fill="{color}" stroke="none"/>']
        elif kind == 'inspector':
            if index in (0, 2):
                p += ['<path d="M-14-20H4L14-10V20H-14Z" fill="#121A26"/><path d="M4-20V-10H14M-7-4H7M-7 2H3"/>']
                if index == 0:
                    p += ['<path class="cinema-scan" d="M-18 0H18" stroke="#43E6C5" stroke-width="2"/>']
                else:
                    p += ['<path class="cinema-ink" d="M-6 10L-1 15L8 5" stroke="#43E6C5" stroke-width="2"/>']
            else:
                p += ['<circle r="15" fill="#121A26"/><circle r="9" opacity=".3"/><path d="M11 11L22 22M-4 0H4M0-4V4"/>']
        else:
            if index == 0:
                p += ['<rect x="-19" y="-17" width="38" height="32" rx="4" fill="#121A26"/><path d="M-19-7H19M-12-12H-11M-7-12H-6M-12 0H1M-12 6H9"/>']
            elif index == 1:
                p += ['<path d="M-20-12H-4L1-6H20V18H-20Z" fill="#121A26"/><path class="cinema-ink" d="M0-2V11M-5 6L0 11L5 6" stroke="#43E6C5"/>']
            else:
                p += ['<rect x="-18" y="-19" width="36" height="38" rx="4" fill="#121A26"/><path d="M-10-10H10M-10-3V10H-3M-10 2H6M-3 10H7"/><circle cx="11" cy="10" r="6" fill="#121A26" stroke="#43E6C5"/><path d="M8 10L10 12L14 7" stroke="#43E6C5"/>']
        p += ['</g>', label(x, 76 if mobile else 122, labels[index], 18 if mobile else 12, color, extra='text-anchor="middle" font-family="Consolas,monospace"')]
    return ''.join(p + ['</g>'])


def hero_finish(source, mobile=False):
    root = ET.fromstring(source)
    for parent in root.iter():
        for child in list(parent):
            if child.tag == N+'text' and child.text == 'CURIOUS BY DESIGN':
                parent.remove(child)
    style = ET.SubElement(root, N+'style', {'id': 'cinematic-style'})
    style.text = STYLE
    x, y = (406, 39) if mobile else (666, 59)
    ornaments = f'''<g xmlns="{SVG}" aria-hidden="true">
      <g transform="translate({x} {y})"><g class="cinema-moving cinema-comet">
       <path d="M-30-16L0 0" stroke="{PINK}" stroke-opacity=".2"/>
       <path d="M-11-6L0 0" stroke="{PINK}" stroke-width="1.5"/>
       <circle r="2" fill="{PINK}"/>
      </g></g>
     </g>'''
    root.append(ET.fromstring(ornaments))
    points = ((418,258),(482,279),(553,259)) if mobile else ((652,270),(735,288),(824,267))
    route = f'M{points[0][0]} {points[0][1]}Q{points[1][0]-10} {points[1][1]+22} {points[1][0]} {points[1][1]}T{points[2][0]} {points[2][1]}'
    p = [f'<g xmlns="{SVG}" aria-hidden="true">',
         f'<path d="{route}" fill="none" stroke="{VIOLET}" stroke-opacity=".25" stroke-dasharray="2 5"/>',
         packet(route, MINT, duration=14)]
    icons = ('<path d="M0-7L6-4V1Q6 5 0 8Q-6 5-6 1V-4Z"/>',
             '<path d="M-3-4L-7 0L-3 4M3-4L7 0L3 4M1-6L-1 6"/>',
             '<path d="M0-7L6-3V4L0 8L-6 4V-3ZM-6-3L0 1L6-3M0 1V8"/>')
    for (cx, cy), icon, color in zip(points, icons, (MINT,VIOLET,PINK)):
        p += [f'<g transform="translate({cx} {cy})" fill="none" stroke="{color}" stroke-width="1.1"><circle r="14" fill="#121A26" stroke-opacity=".4"/>{icon}</g>']
    root.append(ET.fromstring(''.join(p+['</g>'])))
    return ET.tostring(root, encoding='unicode')+'\n'


def portal(mobile=False):
    w, h = (600, 428) if mobile else (1000, 276)
    tx, ty, tw = (28, 205, 544) if mobile else (520, 40, 448)
    px, py = (518, 98) if mobile else (447, 128)
    p = [f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
         '<title id="title">Psst. There’s a secret terminal.</title>',
         '<desc id="desc">An animated invitation to Pixel’s interactive lab. Preview commands help, party and patches. Click the card to enter the actual terminal, solve tiny cases and earn five mission patches. The README illustration is not a terminal input. Reduced motion shows a complete still preview.</desc>',
         f'<style>{STYLE}</style>',
         '<defs><linearGradient id="portal-surface" x2="1" y2="1"><stop stop-color="#17223A"/><stop offset="1" stop-color="#0B121C"/></linearGradient><radialGradient id="portal-glow"><stop stop-color="#A995FF" stop-opacity=".13"/><stop offset="1" stop-color="#A995FF" stop-opacity="0"/></radialGradient></defs>',
         f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#portal-surface)" stroke="#34445C"/>',
         f'<ellipse cx="{px}" cy="{py}" rx="104" ry="92" fill="url(#portal-glow)"/>',
         f'<path d="M25 1H{224 if mobile else 310}" stroke="{MINT}" stroke-width="2"/>',
         label(28, 34, 'BONUS AREA / PIXEL’S COMMAND DECK', 18 if mobile else 12, MINT, extra='font-family="Consolas,monospace"'),
         label(26, 92 if mobile else 95, 'Psst. There’s a', 42 if mobile else 41, TEXT, 700),
         label(26, 142 if mobile else 146, 'secret terminal.', 42 if mobile else 41, TEXT, 700),
         label(28, 178 if mobile else 187, 'TINY CASES / FIVE PATCHES / PIXEL', 18 if mobile else 12, MUTED, extra='font-family="Consolas,monospace"'),
         pixel(px, py, .78 if mobile else .88)]
    for i, (dx, dy, color) in enumerate(((-39,-39,MINT),(27,-58,PINK),(45,-20,VIOLET),(-27,-61,PINK),(52,-48,MINT))):
        p += [f'<g transform="translate({px+dx} {py+dy})"><path class="cinema-moving cinema-confetti" style="animation-delay:{i*.18}s" d="M0 0L3 5" stroke="{color}" stroke-width="2.5"/></g>']
    p += [f'<rect x="{tx}" y="{ty}" width="{tw}" height="168" rx="14" fill="#0A1019" stroke="#34445C"/>',
          f'<path d="M{tx} {ty+34}H{tx+tw}" stroke="#29364B"/>']
    for i, color in enumerate((PINK, VIOLET, MINT)):
        p += [f'<circle cx="{tx+18+i*13}" cy="{ty+17}" r="3" fill="{color}" fill-opacity=".7"/>']
    p += [label(tx+tw-16, ty+22, 'PIXEL / TOY TERMINAL', 18 if mobile else 12, MUTED, extra='text-anchor="end" font-family="Consolas,monospace"')]
    frames = (('one', 'help', 'A route, a hint, or a terrible joke.', 'Try hint. Pixel won’t judge.'),
              ('two', 'party', 'Confetti mode: enthusiastically on.', 'Pixel takes fun very seriously.'),
              ('three', 'patches', 'Five tiny reasons to keep exploring.', 'Earn a little proof of curiosity.'))
    for index, (name, command, line, foot) in enumerate(frames):
        extent = len(command)*10.8
        p += [f'<defs><clipPath id="console-clip-{index}"><rect class="console-reveal" width="{extent}" height="30" style="--line-width:{extent}px"/></clipPath></defs>',
              f'<g class="console-frame console-{name}">',
              label(tx+20, ty+70, 'visitor@lab >', 17, VIOLET, extra='font-family="Consolas,monospace"'),
              f'<g transform="translate({tx+182} {ty+49})" clip-path="url(#console-clip-{index})">',
              label(0, 21, command, 18, MINT, extra='font-family="Consolas,monospace"'), '</g>',
              label(tx+20, ty+108, line, 20 if mobile else 17, TEXT),
              label(tx+20, ty+139, foot, 18 if mobile else 16, MUTED), '</g>']
    for i, color in enumerate((MINT, VIOLET, PINK, MINT, VIOLET)):
        x, y = (40+i*31, 399) if mobile else (532+i*28, 239)
        p += [f'<g transform="translate({x} {y})"><g class="portal-patch" style="animation-delay:{i*.35}s"><path d="M0-10L9-5V5L0 10L-9 5V-5Z" fill="{color}" fill-opacity=".08" stroke="{color}"/><path d="M-3 0L-1 2L4-3" fill="none" stroke="{color}" stroke-width="1.4"/></g></g>']
    if mobile:
        p += [label(572, 404, 'ENTER THE LIVE LAB ↗', 18, MINT, extra='text-anchor="end"')]
    else:
        p += [label(28, 240, 'ENTER THE LIVE LAB ↗', 16, MINT),
              label(686, 244, 'FIVE PATCHES. ONE SIDE QUEST AT A TIME.', 11, MUTED)]
    return apply_theme(''.join(p + ['</g></svg>']))


def build():
    for mobile in (False, True):
        name = 'pixel-portal' + ('-mobile' if mobile else '') + '.svg'
        (ROOT/'profile'/name).write_text(portal(mobile), encoding='utf-8')


if __name__ == '__main__':
    build()
