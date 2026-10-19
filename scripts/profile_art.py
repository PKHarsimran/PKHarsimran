"""Original orbital line art and a decorative visitor arrival pass. Standard library."""
from html import escape
import random
import xml.etree.ElementTree as ET
from profile_mascot import hacker_bender

SVG='http://www.w3.org/2000/svg'
MINT,VIOLET,PINK='#43E6C5','#A995FF','#F36BAA'


def art_style():
    return '<style id="orbital-art-style">.art-twinkle{animation:art-twinkle 9s ease-in-out infinite}.art-orbit{animation:art-orbit 36s linear infinite}.visitor-float{animation:visitor-float 5s ease-in-out infinite}.visitor-wave{transform-box:fill-box;transform-origin:bottom left;animation:visitor-wave 8s ease-in-out infinite}@keyframes art-twinkle{0%,100%{opacity:.25}50%{opacity:.8}}@keyframes art-orbit{to{transform:rotate(360deg)}}@keyframes visitor-float{50%{transform:translateY(-4px)}}@keyframes visitor-wave{0%,65%,100%{transform:rotate(0)}70%,80%{transform:rotate(-18deg)}75%,85%{transform:rotate(8deg)}}@media(prefers-reduced-motion:reduce){.art-twinkle,.art-orbit,.visitor-float,.visitor-wave{animation:none}}</style>'


def sparkle(x,y,color,size=6):
    return f'<path transform="translate({x} {y})" d="M0-{size}Q0 0 {size} 0Q0 0 0 {size}Q0 0-{size} 0Q0 0 0-{size}Z" fill="{color}"/>'


def header_art(source):
    root=ET.fromstring(source)
    for node in list(root):
        if node.get('id')=='orbital-art-style':root.remove(node)
    main=root.find('{'+SVG+'}g')
    for node in list(main):
        if node.get('id')=='mission-art':main.remove(node)
    p=['<g xmlns="'+SVG+'" id="mission-art" transform="translate(620 55)" fill="none">']
    # Offset contours, halftone and registration marks evoke a small screen print.
    for i in range(6):
        p.append(f'<path d="M{15+i*7} {12+i*8}C{125+i*5} {-25+i*11} {315-i*5} {48+i*6} {331-i*7} {150+i*5}S{111+i*12} {269-i*6} {36+i*5} {226-i*4}" stroke="{VIOLET if i%2 else MINT}" stroke-opacity="{.06+i*.012:.3f}" stroke-width=".8"/>')
    rng=random.Random(41)
    for _ in range(110):
        x,y=rng.uniform(15,334),rng.uniform(3,225)
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.choice((.6,.9,1.2))}" fill="{VIOLET}" opacity=".14"/>')
    p += ['<g class="art-twinkle">',sparkle(8,45,PINK,7),sparkle(322,4,MINT,5),sparkle(42,210,VIOLET,4),'</g>',
          f'<path d="M-14 10H-2M-8 4V16M322 232H334M328 226V238" stroke="{PINK}" stroke-opacity=".4"/>',
          f'<text x="8" y="238" font-family="monospace" font-size="10" fill="{VIOLET}" opacity=".65" transform="rotate(-5 8 238)">CURIOUS BY DESIGN</text>','</g>']
    main.insert(2,ET.fromstring(''.join(p)))
    root.insert(0,ET.fromstring(art_style().replace('<style ','<style xmlns="'+SVG+'" ',1)))
    return ET.tostring(root,encoding='unicode')+'\n'


def t(x,y,value,size=18,color='#B8C6DB',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>'


def visitor_pass(mobile=False):
    w,h=(600,270) if mobile else (1000,164)
    x,y,scale=(482,117,.82) if mobile else (849,86,1)
    p=[f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">Hey, curious human. Welcome to the lab.</title><desc id="desc">A cute waving Hacker Bender in a charcoal hoodie and an orbital arrival stamp. Decorative animation; the separate live badge below counts page hits, not unique visitors or identities.</desc>',art_style(),
       '<defs><linearGradient id="arrival" x2="1" y2="1"><stop stop-color="#192137"/><stop offset="1" stop-color="#0D1117"/></linearGradient><pattern id="ink" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="#A995FF" opacity=".1"/></pattern></defs>',
       f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="url(#arrival)" stroke="#34445C"/><rect x="2" y="2" width="{w-4}" height="{h-4}" rx="19" fill="url(#ink)"/>',
       f'<path d="M2 26V{h-26}" stroke="{PINK}" stroke-width="3"/>',
       t(28,33,'VISITOR ARRIVALS / WELCOME TO THE LAB',13,MINT,600)]
    if mobile:
        p += [t(28,94,'Hey, curious',39,'#EFF4FC',700),t(28,140,'human.',39,'#EFF4FC',700),t(28,195,'Welcome to my corner',23),t(28,230,'of the internet.',23)]
    else:
        p += [t(28,87,'Hey, curious human.',36,'#EFF4FC',700),t(30,128,'Welcome to my corner of the internet.',20),f'<path d="M704 20V144" stroke="{VIOLET}" stroke-opacity=".25" stroke-dasharray="3 7"/>']
    p += [f'<g transform="translate({x} {y}) scale({scale})">',
          f'<ellipse rx="106" ry="35" transform="rotate(-20)" fill="none" stroke="{MINT}" stroke-opacity=".28"/>',
          f'<circle r="55" fill="#121A26" stroke="{VIOLET}" stroke-opacity=".4"/><circle r="65" fill="none" stroke="{VIOLET}" stroke-opacity=".3" stroke-dasharray="1 6"/>',
          f'<g class="art-orbit"><circle cx="65" r="3" fill="{PINK}"/><path d="M60-5L70 5M60 5L70-5" stroke="{PINK}" stroke-opacity=".4"/></g>',
          hacker_bender(scale=.72,key='guestbook'),
          t(-46,65,'HELLO, WORLD',10,MINT,500),'<g class="art-twinkle">',sparkle(-82,-46,PINK,5),sparkle(88,32,MINT,7),'</g></g></g></svg>\n']
    return ''.join(p)


def orbit_divider():
    p=[f'<svg xmlns="{SVG}" width="1000" height="48" viewBox="0 0 1000 48" role="img" aria-label="Orbital constellation divider">',art_style(),
       '<defs><linearGradient id="ink"><stop stop-color="#43E6C5" stop-opacity="0"/><stop offset=".3" stop-color="#43E6C5" stop-opacity=".35"/><stop offset=".5" stop-color="#A995FF"/><stop offset=".7" stop-color="#F36BAA" stop-opacity=".35"/><stop offset="1" stop-color="#F36BAA" stop-opacity="0"/></linearGradient></defs>',
       '<path d="M0 24C160 9 322 38 467 24M533 24C678 10 843 39 1000 24" fill="none" stroke="url(#ink)"/><path d="M0 29C189 39 335 6 465 26M535 26C682 40 820 5 1000 20" fill="none" stroke="url(#ink)" stroke-opacity=".35"/>',
       '<g transform="translate(500 24)"><ellipse rx="28" ry="10" transform="rotate(-20)" fill="none" stroke="#A995FF" stroke-opacity=".6"/><g class="art-orbit"><circle cx="28" r="2" fill="#43E6C5"/></g>',sparkle(0,0,PINK,7),'</g><g class="art-twinkle">',sparkle(277,24,MINT,3),sparkle(735,24,VIOLET,3),'</g></svg>\n']
    return ''.join(p)
