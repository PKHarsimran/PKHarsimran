"""Small, self-contained SVG stories for the GitHub README. No runtime services."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

from profile_theme import apply_theme
from profile_mascot import hacker_bender

ROOT = Path(__file__).resolve().parents[1]
SVG = 'http://www.w3.org/2000/svg'
N = '{' + SVG + '}'
TEXT, MUTED, MINT, VIOLET, PINK = '#EFF4FC', '#B8C6DB', '#43E6C5', '#A995FF', '#F36BAA'

STYLE = '''
.cinema-ring{transform-box:fill-box;transform-origin:center;animation:cinema-ring 24s linear infinite}
.cinema-scan{animation:cinema-scan 8s ease-in-out infinite}
.cinema-ink{animation:cinema-ink 8s ease-in-out infinite}
.cinema-comet{opacity:0;animation:cinema-comet 18s ease-out infinite}
.cinema-confetti{opacity:0;animation:cinema-confetti 18s ease-out infinite}
.console-frame{opacity:0;animation:console-frame 18s linear infinite}
.console-two{animation-delay:6s}.console-three{animation-delay:12s}
.console-reveal{animation:console-type 6s steps(14,end) infinite}
.portal-patch{animation:portal-patch 18s ease-in-out infinite}
.cinema-ambient{animation:cinema-ambient 32s ease-in-out infinite}
.cinema-border{animation:cinema-border 28s linear infinite}
.cinema-flow-one{opacity:0;animation:cinema-flow-one 12s linear infinite}
.cinema-flow-two{opacity:0;animation:cinema-flow-two 12s linear infinite}
@keyframes cinema-ring{to{transform:rotate(360deg)}}
@keyframes cinema-scan{0%,12%,100%{opacity:0;transform:translateY(-15px)}25%,65%{opacity:.8}78%{opacity:0;transform:translateY(18px)}}
@keyframes cinema-ink{0%,20%,100%{opacity:.35}45%,78%{opacity:1}}
@keyframes cinema-comet{0%,70%,100%{opacity:0;transform:translate(0,0)}74%{opacity:.8}82%{opacity:0;transform:translate(38px,20px)}}
@keyframes cinema-confetti{0%,33%,67%,100%{opacity:0;transform:translateY(-8px)}38%,53%{opacity:.9}64%{opacity:0;transform:translateY(30px)}}
@keyframes console-frame{0%,32%{opacity:1}33.333%,100%{opacity:0}}
@keyframes console-type{0%{width:0}28%,94%{width:var(--line-width)}100%{width:0}}
@keyframes portal-patch{0%,65%,100%{opacity:.45}76%,91%{opacity:1}}
@keyframes cinema-ambient{50%{transform:translate(-14px,10px);opacity:.65}}
@keyframes cinema-border{to{stroke-dashoffset:-1000}}
@keyframes cinema-flow-one{0%,6%,44%,100%{opacity:0}10%,40%{opacity:1}}
@keyframes cinema-flow-two{0%,44%,84%,100%{opacity:0}48%,80%{opacity:1}}
@media(prefers-reduced-motion:reduce){
 .cinema-moving{display:none!important}
 .cinema-ring,.cinema-scan,.cinema-ink,.portal-patch,.cinema-ambient{animation:none!important}
 .cinema-scan{opacity:.5}.cinema-ink,.portal-patch{opacity:1}
 .console-frame{animation:none;opacity:0}.console-one{opacity:1}
 .console-reveal{animation:none;width:var(--line-width)}
}
'''

SEQUENCE_STYLE = '''
.sequence-intake{animation:sequence-intake 12s ease-in-out infinite}
.sequence-lens{animation:sequence-lens 12s ease-in-out infinite}
.sequence-store{animation:sequence-store 12s ease-in-out infinite}
.sequence-input{animation:sequence-input 12s ease-in-out infinite}
.sequence-process{animation:sequence-process 12s ease-in-out infinite}
.sequence-output{animation:sequence-output 12s ease-in-out infinite}
.sequence-progress{stroke-dasharray:100;stroke-dashoffset:100;animation:sequence-progress 12s linear infinite}
.sequence-check{stroke-dasharray:100;stroke-dashoffset:100;animation:sequence-check 12s ease-in-out infinite}
@keyframes sequence-intake{0%,20%,100%{transform:translateY(0)}7%{transform:translateY(-3px)}13%{transform:translateY(1px)}}
@keyframes sequence-lens{0%,34%,68%,100%{transform:translate(0,0)}44%{transform:translate(3px,-2px)}56%{transform:translate(-2px,2px)}}
@keyframes sequence-store{0%,42%,68%,100%{transform:translateY(0)}50%,60%{transform:translateY(3px)}55%{transform:translateY(-1px)}}
@keyframes sequence-input{0%,22%,100%{opacity:.06}6%,13%{opacity:.55}}
@keyframes sequence-process{0%,32%,66%,100%{opacity:.06}42%,54%{opacity:.55}}
@keyframes sequence-output{0%,75%,100%{opacity:.06}84%,95%{opacity:.55}}
@keyframes sequence-progress{0%,5%{stroke-dashoffset:100;opacity:.7}90%,96%{stroke-dashoffset:0;opacity:.7}99%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes sequence-check{0%,76%{stroke-dashoffset:100;opacity:0}80%{opacity:1}91%,97%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
@media(prefers-reduced-motion:reduce){
 .sequence-intake,.sequence-lens,.sequence-store{animation:none}
 .sequence-input,.sequence-process,.sequence-output{animation:none;opacity:.18}
 .sequence-progress{animation:none;stroke-dashoffset:0;opacity:.3}
 .sequence-check{animation:none;stroke-dashoffset:0;opacity:1}
}
'''

HERO_STYLE = '''
.hero-contact{animation:hero-contact 18s ease-out infinite}
.hero-return{opacity:0;transform-box:fill-box;transform-origin:center;animation:hero-return 18s ease-out infinite}
@keyframes hero-contact{0%,16%,100%{opacity:.4}2%,5%{opacity:1}}
@keyframes hero-return{0%{opacity:0;transform:scale(.65)}2%{opacity:.7}13%,100%{opacity:0;transform:scale(2.1)}}
@media(prefers-reduced-motion:reduce){.hero-contact,.hero-return{animation:none}.hero-contact{opacity:.8}.hero-return{display:none}}
'''


def label(x, y, value, size=12, color=MUTED, weight=500, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def packet(path, color, delay=0, duration=8):
    return (f'<g class="cinema-moving" aria-hidden="true"><circle r="2.4" fill="{color}"/>'
            f'<animateMotion dur="{duration}s" begin="{delay}s" repeatCount="indefinite" path="{path}"/></g>')


def staged_packet(path, color, second=False):
    times = '0;0.44;0.84;1' if second else '0;0.06;0.44;1'
    return (f'<g class="cinema-moving cinema-flow-{"two" if second else "one"}" aria-hidden="true">'
            f'<circle r="6" fill="{color}" fill-opacity=".08"/><circle r="2.4" fill="{color}"/>'
            f'<animateMotion dur="12s" repeatCount="indefinite" path="{path}" keyPoints="0;0;1;1" keyTimes="{times}" calcMode="linear"/></g>')


def project_scene(kind, mobile=False):
    """Three process illustrations; the labels remain readable without animation."""
    width = 544 if mobile else 224
    points = (42, 272, 502) if mobile else (30, 112, 194)
    y = 31 if mobile else 65
    color = {'swiftioc': MINT, 'inspector': VIOLET, 'downloader': PINK}[kind]
    labels = {'swiftioc': ('FEEDS', 'IOCs', 'CONTEXT'),
              'inspector': ('FILE', 'TRIAGE', 'REPORT'),
              'downloader': ('PAGE', 'SAVE', 'OFFLINE')}[kind]
    p = [f'<g data-cinematic="{kind}" aria-hidden="true">', f'<style>{STYLE+SEQUENCE_STYLE}</style>',
         f'<rect x="0" y="{0 if mobile else 9}" width="{width}" height="{88 if mobile else 143}" rx="14" fill="{color}" fill-opacity=".025" stroke="{color}" stroke-opacity=".12"/>',
         f'<rect class="cinema-moving cinema-border" x="0" y="{0 if mobile else 9}" width="{width}" height="{88 if mobile else 143}" rx="14" fill="none" stroke="{color}" stroke-opacity=".4" pathLength="1000" stroke-dasharray="22 978"/>']
    for start, end in zip(points, points[1:]):
        route = f'M{start+23} {y}H{end-23}'
        p += [f'<path d="{route}" fill="none" stroke="{color}" stroke-opacity=".25" stroke-dasharray="2 5"/>',
              staged_packet(route, color, second=start != points[0])]
    for index, x in enumerate(points):
        phase = ('input', 'process', 'output')[index]
        motion = 'sequence-intake' if index == 0 else 'sequence-lens' if kind == 'inspector' and index == 1 else 'sequence-store' if kind == 'downloader' and index == 1 else ''
        p += [f'<g transform="translate({x} {y})" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">',
              f'<circle class="sequence-{phase}" r="27" fill="{color}" fill-opacity=".035" stroke-opacity=".5" stroke-width="1"/>',
              f'<g class="{motion}">']
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
                    p += ['<path d="M-6 10L-1 15L8 5" stroke="#43E6C5" stroke-opacity=".3" stroke-width="2"/>',
                          '<path class="sequence-check" pathLength="100" d="M-6 10L-1 15L8 5" stroke="#43E6C5" stroke-width="2"/>']
            else:
                p += ['<circle r="15" fill="#121A26"/><circle r="9" opacity=".3"/><path d="M11 11L22 22M-4 0H4M0-4V4"/>']
        else:
            if index == 0:
                p += ['<rect x="-19" y="-17" width="38" height="32" rx="4" fill="#121A26"/><path d="M-19-7H19M-12-12H-11M-7-12H-6M-12 0H1M-12 6H9"/>']
            elif index == 1:
                p += ['<path d="M-20-12H-4L1-6H20V18H-20Z" fill="#121A26"/><path class="cinema-ink" d="M0-2V11M-5 6L0 11L5 6" stroke="#43E6C5"/>']
            else:
                p += ['<rect x="-18" y="-19" width="36" height="38" rx="4" fill="#121A26"/><path d="M-10-10H10M-10-3V10H-3M-10 2H6M-3 10H7"/><circle cx="11" cy="10" r="6" fill="#121A26" stroke="#43E6C5"/><path d="M8 10L10 12L14 7" stroke="#43E6C5" stroke-opacity=".3"/><path class="sequence-check" pathLength="100" d="M8 10L10 12L14 7" stroke="#43E6C5"/>']
        p += ['</g></g>', label(x, 76 if mobile else 122, labels[index], 18 if mobile else 12, color, extra='text-anchor="middle" font-family="Consolas,monospace"')]
    if not mobile:
        p += [f'<path d="M16 139H{width-16}" stroke="{color}" stroke-opacity=".1" stroke-linecap="round"/>',
              f'<path class="sequence-progress" pathLength="100" d="M16 139H{width-16}" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>']
    return ''.join(p + ['</g>'])


def hero_finish(source, mobile=False):
    root = ET.fromstring(source)
    for parent in root.iter():
        for child in list(parent):
            if child.tag == N+'text' and child.text == 'CURIOUS BY DESIGN':
                parent.remove(child)
    style = ET.SubElement(root, N+'style', {'id': 'cinematic-style'})
    style.text = STYLE + HERO_STYLE + '.motion-frame{animation-duration:48s}'
    defs = ET.SubElement(root, N+'defs')
    for name, color in (('mint',MINT),('violet',VIOLET)):
        gradient = ET.SubElement(defs, N+'radialGradient', {'id':'cinema-ambient-'+name})
        ET.SubElement(gradient, N+'stop', {'stop-color':color,'stop-opacity':'.09'})
        ET.SubElement(gradient, N+'stop', {'offset':'1','stop-color':color,'stop-opacity':'0'})
    main = root.find(N+'g')
    radar_transform = 'translate(487 171) scale(.66)' if mobile else 'translate(809 163) scale(.9)'
    radar = root.find('.//'+N+'g[@transform="'+radar_transform+'"]')
    if radar is None: raise ValueError('Missing hero radar')
    # The selected mascot leads the orbital artwork; the shield remains in the
    # smaller security/code/infrastructure route underneath it.
    shield_paths = ('M0-32L29-21V4C29 25 0 40 0 40S-29 25-29 4V-21Z',
                    'M-12 2L-3 11L15-10')
    for child in list(radar):
        if child.tag == N+'path' and child.get('d') in shield_paths:
            radar.remove(child)
    radar.append(ET.fromstring(hacker_bender(0,4,.98,pose='laptop',key='hero').replace('<g ',f'<g xmlns="{SVG}" ',1)))
    contacts = list(radar.findall(N+'circle[@class="pulse"]'))
    if len(contacts) != 3: raise ValueError('Expected three hero radar contacts')
    for contact, delay in zip(contacts, (10.7, 6.4, .7)):
        contact.set('class', 'hero-contact')
        contact.set('style', f'animation-delay:{delay}s')
        ring = ET.SubElement(radar, N+'g', {'transform': f'translate({contact.get("cx")} {contact.get("cy")})'})
        ET.SubElement(ring, N+'circle', {'class': 'hero-return', 'r': '7', 'fill': 'none',
                      'stroke': contact.get('fill'), 'stroke-width': '1', 'style': f'animation-delay:{delay}s'})
    cx, cy = (487,171) if mobile else (809,163)
    glow = f'<g xmlns="{SVG}" class="cinema-ambient" aria-hidden="true"><ellipse cx="{cx}" cy="{cy}" rx="{180 if mobile else 240}" ry="160" fill="url(#cinema-ambient-mint)"/><ellipse cx="{cx+45}" cy="{cy+64}" rx="155" ry="125" fill="url(#cinema-ambient-violet)"/></g>'
    main.insert(1, ET.fromstring(glow))
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
    px, py = (510, 109) if mobile else (438, 134)
    p = [f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
         '<title id="title">Psst. There’s a secret terminal.</title>',
         '<desc id="desc">Hacker Bender holds a tiny laptop beside an animated invitation to the live lab. Preview commands help, party and patches. Click the card to enter the actual terminal, solve tiny cases and earn five mission patches. The README illustration is not a terminal input. Reduced motion shows a complete still preview.</desc>',
         f'<style>{STYLE}</style>',
         '<defs><linearGradient id="portal-surface" x2="1" y2="1"><stop stop-color="#17223A"/><stop offset="1" stop-color="#0B121C"/></linearGradient><radialGradient id="portal-glow"><stop stop-color="#A995FF" stop-opacity=".13"/><stop offset="1" stop-color="#A995FF" stop-opacity="0"/></radialGradient></defs>',
         f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#portal-surface)" stroke="#34445C"/>',
         f'<ellipse cx="{px}" cy="{py}" rx="104" ry="92" fill="url(#portal-glow)"/>',
         f'<path d="M25 1H{224 if mobile else 310}" stroke="{MINT}" stroke-width="2"/>',
         label(28, 34, 'BONUS AREA / BENDER’S COMMAND DECK', 18 if mobile else 12, MINT, extra='font-family="Consolas,monospace"'),
         label(26, 92 if mobile else 95, 'Psst. There’s a', 42 if mobile else 41, TEXT, 700),
         label(26, 142 if mobile else 146, 'secret terminal.', 42 if mobile else 41, TEXT, 700),
         label(28, 178 if mobile else 187, 'TINY CASES / FIVE PATCHES / BENDER', 18 if mobile else 12, MUTED, extra='font-family="Consolas,monospace"'),
         hacker_bender(px, py, .75 if mobile else .92,pose='laptop',key='portal')]
    for i, (dx, dy, color) in enumerate(((-39,-39,MINT),(27,-58,PINK),(45,-20,VIOLET),(-27,-61,PINK),(52,-48,MINT))):
        p += [f'<g transform="translate({px+dx} {py+dy})"><path class="cinema-moving cinema-confetti" style="animation-delay:{i*.18}s" d="M0 0L3 5" stroke="{color}" stroke-width="2.5"/></g>']
    p += [f'<rect x="{tx}" y="{ty}" width="{tw}" height="168" rx="14" fill="#0A1019" stroke="#34445C"/>',
          f'<path d="M{tx} {ty+34}H{tx+tw}" stroke="#29364B"/>']
    for i, color in enumerate((PINK, VIOLET, MINT)):
        p += [f'<circle cx="{tx+18+i*13}" cy="{ty+17}" r="3" fill="{color}" fill-opacity=".7"/>']
    p += [label(tx+tw-16, ty+22, 'LAB / TOY TERMINAL', 18 if mobile else 12, MUTED, extra='text-anchor="end" font-family="Consolas,monospace"')]
    frames = (('one', 'help', 'A route, a hint, or a terrible joke.', 'Try hint. Curiosity is welcome.'),
              ('two', 'party', 'Confetti mode: enthusiastically on.', 'A little chaos. Nicely contained.'),
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
