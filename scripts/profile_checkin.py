"""A decorative check-in desk beside the README's independently hosted hit badge."""
from html import escape

from profile_mascot import hacker_bender

MINT, VIOLET, TEXT, MUTED = '#43E6C5', '#A995FF', '#EFF4FC', '#B8C6DB'

STYLE = '''
.checkin-type{animation:checkin-type 14s steps(8,end) infinite}
.checkin-cursor{animation:checkin-travel 14s steps(8,end) infinite,checkin-blink 3.6s ease-in-out infinite}
.checkin-scan{opacity:0;animation:checkin-scan 14s ease-in-out infinite}
@keyframes checkin-type{0%,4%{width:0}12%,100%{width:var(--command-width)}}
@keyframes checkin-travel{0%,4%{transform:translateX(0)}12%,100%{transform:translateX(var(--command-width))}}
@keyframes checkin-blink{0%,55%,100%{opacity:.8}75%{opacity:.2}}
@keyframes checkin-scan{0%,10%{opacity:0;transform:translateY(0)}18%,65%{opacity:.14}80%,100%{opacity:0;transform:translateY(var(--scan-distance))}}
@media(prefers-reduced-motion:reduce){.checkin-type,.checkin-cursor,.checkin-scan{animation:none}.checkin-type{width:var(--command-width)}.checkin-cursor{transform:translateX(var(--command-width));opacity:.7}.checkin-scan{display:none}}
'''


def label(x, y, value, size=18, color=MUTED, weight=400, mono=False, extra=''):
    family = 'Consolas,monospace' if mono else 'Segoe UI,Arial,sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def checkin_desk(mobile=False):
    w, h = (600, 348) if mobile else (1000, 226)
    tx, ty, tw, th = (24, 174, 552, 126) if mobile else (270, 54, 704, 136)
    bx, by, scale = (486, 105, .63) if mobile else (128, 133, .84)
    size = 22 if mobile else 20
    line_x, line_y = tx+22, ty+(59 if mobile else 57)
    command_x = line_x+12*size*.6
    command_width = 8*size*.6
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
         '<title id="title">Bender\'s check-in desk / Welcome, curious human.</title>',
         '<desc id="desc">A waving Hacker Bender hosts a decorative terminal with a typing check-in command, a soft screen sweep and antenna pings. The separate badge below shows today and lifetime page hits for the existing counter. Open the arrival log for statistics. Reduced motion keeps the artwork still.</desc>',
         f'<style>{STYLE}</style>',
         '<defs><linearGradient id="checkin-surface" x2="1" y2="1"><stop stop-color="#172232"/><stop offset="1" stop-color="#0D1117"/></linearGradient>',
         '<radialGradient id="checkin-glow"><stop stop-color="#43E6C5" stop-opacity=".1"/><stop offset="1" stop-color="#43E6C5" stop-opacity="0"/></radialGradient>',
         f'<clipPath id="checkin-screen"><rect x="{tx+1}" y="{ty+28}" width="{tw-2}" height="{th-29}"/></clipPath>',
         f'<clipPath id="checkin-command"><rect class="checkin-type" x="0" y="{-size}" width="{command_width:.1f}" height="{size+7}" style="--command-width:{command_width:.1f}px"/></clipPath></defs>',
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="url(#checkin-surface)" stroke="#34445C"/>',
         f'<path d="M24 1H{250 if mobile else 322}" stroke="{MINT}" stroke-width="2"/>',
         label(24, 32, "LAB ARRIVALS / BENDER'S CHECK-IN", 17 if mobile else 13, MINT, mono=True),
         f'<ellipse cx="{bx}" cy="{by-5}" rx="{94 if mobile else 112}" ry="86" fill="url(#checkin-glow)"/>',
         f'<circle cx="{bx}" cy="{by-4}" r="{59 if mobile else 76}" fill="none" stroke="{VIOLET}" stroke-opacity=".15" stroke-dasharray="2 8"/>',
         hacker_bender(bx, by, scale, key='checkin')]
    if mobile:
        p += [label(26, 91, 'Hey, curious', 34, TEXT, 700), label(26, 132, 'human.', 34, TEXT, 700)]
    else:
        p += [label(972, 32, 'THE DOOR IS ALWAYS OPEN', 12, VIOLET, mono=True, extra='text-anchor="end"'),
              f'<path d="M242 54V199" stroke="#34445C" stroke-dasharray="2 7"/>']
    p += [f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="#0A1019" stroke="#34445C"/>',
          f'<path d="M{tx} {ty+28}H{tx+tw}" stroke="#263247"/>']
    for i, color in enumerate(('#F36BAA', '#A995FF', '#43E6C5')):
        p.append(f'<circle cx="{tx+18+i*12}" cy="{ty+14}" r="2.6" fill="{color}" fill-opacity=".6"/>')
    p += [label(tx+tw-18, ty+19, 'ARRIVAL LOG / CHECK-IN', 14 if mobile else 11, MUTED, mono=True, extra='text-anchor="end"'),
          label(line_x, line_y, 'guest@lab > ', size, VIOLET, mono=True),
          f'<g transform="translate({command_x:.1f} {line_y})" style="--command-width:{command_width:.1f}px"><g clip-path="url(#checkin-command)">',
          label(0, 0, 'check-in', size, MINT, mono=True), '</g>',
          f'<rect class="checkin-cursor" x="3" y="{-size*.75:.1f}" width="2" height="{size*.9:.1f}" fill="{MINT}"/></g>']
    if mobile:
        p += [label(line_x, ty+100, 'Bender saved you a seat.', 24, TEXT, 500),
              label(26, h-20, 'PAGE HITS / TODAY + LIFETIME', 18, MINT, mono=True)]
    else:
        p += [label(line_x, ty+95, 'Welcome, curious human.', 28, TEXT, 700),
              label(line_x, ty+120, 'Bender saved you a seat.', 17),
              label(tx, h-14, 'PAGE HITS / TODAY + LIFETIME', 12, MINT, mono=True)]
    p += [f'<g clip-path="url(#checkin-screen)"><rect class="checkin-scan" x="{tx+1}" y="{ty+29}" width="{tw-2}" height="1" fill="{MINT}" style="--scan-distance:{th-32}px"/></g>', '</svg>\n']
    return ''.join(p)
