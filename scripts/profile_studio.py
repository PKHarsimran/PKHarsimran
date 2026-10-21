"""A shared art direction for the profile hero and featured project covers."""
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from profile_art import art_style, visitor_pass
from profile_theme import PROJECT_MOTION
from profile_cinematics import project_scene

OUT=Path(__file__).resolve().parents[1]/'profile'
SVG='http://www.w3.org/2000/svg'
TEXT,MUTED,MINT,VIOLET,PINK='#EFF4FC','#B8C6DB','#43E6C5','#A995FF','#F36BAA'
PROJECTS=(
    ('swiftioc','01','SwiftIOC','Threat intelligence','Follow the indicator. Keep the evidence.','PYTHON / THREAT INTEL / ANALYST WORKFLOWS',MINT),
    ('inspector','02','IOC Inspector','Document triage','Suspicious documents. Useful answers.','PYTHON / STATIC ANALYSIS / REPORTS',VIOLET),
    ('downloader','03','Website Downloader','Web archiving','A little piece of the web, offline.','PYTHON / WEB ARCHIVING / PLAYWRIGHT',PINK),
)


def text(x,y,label,size=18,color=TEXT,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(label)}</text>'


NAME_STYLE = '''<style>
.name-glyph{animation:name-glyph .72s ease-out both;animation-delay:var(--glyph-delay)}
.name-slice-one,.name-slice-two{opacity:0}
.name-slice-one{animation:name-slice-one 16s steps(1,end) infinite}
.name-slice-two{animation:name-slice-two 16s steps(1,end) infinite}
.name-sweep{animation:name-sweep 16s cubic-bezier(.4,0,.2,1) infinite}
.name-cursor{opacity:.3;transform-box:fill-box;transform-origin:left center;animation:name-cursor 16s ease-in-out infinite}
.name-slice-one,.name-slice-two,.name-sweep,.name-cursor{animation-delay:var(--phase)}
@keyframes name-glyph{from{opacity:.6;fill:#43E6C5}to{opacity:1;fill:#EFF4FC}}
@keyframes name-sweep{0%,4%{transform:translateX(0)}19%,100%{transform:translateX(var(--travel))}}
@keyframes name-slice-one{0%,19%,20.4%,100%{opacity:0;transform:translateX(0)}19.2%{opacity:.65;transform:translateX(-4px)}19.6%{opacity:.35;transform:translateX(2px)}20%{opacity:.5;transform:translateX(-1px)}}
@keyframes name-slice-two{0%,19.4%,20.6%,100%{opacity:0;transform:translateX(0)}19.5%{opacity:.5;transform:translateX(4px)}19.8%{opacity:.55;transform:translateX(-2px)}20.2%{opacity:.3;transform:translateX(1px)}}
@keyframes name-cursor{0%,19%,43%,68%,93%,100%{opacity:.3;transform:scaleX(.72)}22%,27%{opacity:1;transform:scaleX(1)}55%,80%{opacity:.75;transform:scaleX(.92)}}
@media(prefers-reduced-motion:reduce){.name-glyph,.name-slice-one,.name-slice-two,.name-sweep,.name-cursor{animation:none}.name-slice-one,.name-slice-two,.name-sheen{display:none}.name-cursor{opacity:.7;transform:none}}
</style>'''


def identity_line(x, y, value, size):
    """Letter illumination and a sweep fitted to the bundled name font's advances."""
    ident = 'name-'+value.lower()
    phase = .26 if value == 'SIDHU' else 0
    # Em advances from the committed Chakra Petch subset, plus letter spacing.
    advance = {'HARSIMRAN':5.751, 'SIDHU':2.999}[value]*size + .4*(len(value)-1)
    beam = advance*.16
    extra = 'font-family="ProfileName,Consolas,monospace" letter-spacing=".4"'
    glyphs = ''.join(f'<tspan class="name-glyph" style="--glyph-delay:{phase+i*.055:.3f}s">{char}</tspan>' for i,char in enumerate(value))
    base = text(0,0,value,size,TEXT,700,extra).replace('>'+value+'</text>', '>'+glyphs+'</text>')
    p = [f'<g transform="translate({x} {y})" style="--phase:{phase}s;--travel:{advance+beam*2:.1f}px">',
         '<defs>',
         f'<clipPath id="{ident}-upper"><rect x="-5" y="{-size*.69:.1f}" width="{advance+10:.1f}" height="{size*.08:.1f}"/></clipPath>',
         f'<clipPath id="{ident}-lower"><rect x="-5" y="{-size*.27:.1f}" width="{advance+10:.1f}" height="{size*.05:.1f}"/></clipPath>',
         f'<linearGradient id="{ident}-light"><stop stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>',
         f'<mask id="{ident}-sweep" maskUnits="userSpaceOnUse" x="-8" y="{-size}" width="{advance+16:.1f}" height="{size+12}"><rect class="name-sweep" x="{-beam:.1f}" y="{-size}" width="{beam:.1f}" height="{size+12}" fill="url(#{ident}-light)"/></mask>',
         '</defs>', base,
         f'<g class="name-sheen" mask="url(#{ident}-sweep)" aria-hidden="true">',text(0,0,value,size,MINT,700,extra),'</g>']
    for name, color, clip in (('one',MINT,'upper'), ('two',PINK,'lower')):
        p += [f'<g clip-path="url(#{ident}-{clip})" aria-hidden="true"><g class="name-slice-{name}">',
              text(0,0,value,size,color,700,extra), '</g></g>']
    if value == 'SIDHU':
        p += [f'<rect class="name-cursor" x="{advance+size*.12:.1f}" y="{-size*.13:.1f}" width="{size*.20:.1f}" height="{size*.13:.1f}" fill="{MINT}" aria-hidden="true"/>']
    return ''.join(p+['</g>'])


def group(name,original,replacement):
    root=ET.parse(OUT/name)
    node=root.find('.//{'+SVG+'}g[@transform="'+original+'"]')
    if node is None:raise ValueError('Missing source illustration: '+name)
    node.set('transform',replacement)
    return ET.tostring(node,encoding='unicode')


def panel(w,h,title,desc):
    return [f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            '<defs><linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#141C29"/><stop offset="1" stop-color="#0B0F16"/></linearGradient></defs>',
            f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#surface)" stroke="#29364B"/>']


def hero(mobile=False):
    w,h=(600,460) if mobile else (1000,374)
    source=(OUT/'mission-banner-orbital.svg').read_text(encoding='utf-8')
    motion=re.search(r'<style>.*?</style>',source,re.S).group()
    p=panel(w,h,'Harsimran Sidhu / Security instincts. Builder energy.','Cybersecurity, open source and self-hosting. Hacker-inspired letters illuminate in sequence, catch fitted cyan sweeps and settle through fine chromatic cuts into a softly breathing cursor. Orbital line art surrounds cute Hacker Bender with a tiny laptop. Reduced-motion preferences keep the design still.')
    p += [motion,art_style(),NAME_STYLE,f'<path d="M25 1H{210 if mobile else 310}" stroke="{MINT}" stroke-width="2"/>',
          group('mission-banner-orbital.svg','translate(620 55)','translate(383 68) scale(.58)' if mobile else 'translate(617 46)'),
          group('mission-banner-orbital.svg','translate(801 164)','translate(487 171) scale(.66)' if mobile else 'translate(809 163) scale(.9)')]
    if mobile:
        p += [text(28,36,'PKHARSIMRAN / SECURITY + CODE',18,MINT,500,'font-family="Consolas,monospace"'),
              identity_line(28,124,'HARSIMRAN',64),identity_line(28,201,'SIDHU',64),
              text(30,262,'Security instincts.',27,MUTED),text(30,300,'Builder energy.',27,MINT),
              '<path d="M28 339H572" stroke="#29364B"/>',
              text(28,378,'CYBERSECURITY / OPEN SOURCE',18,MUTED,500,'font-family="Consolas,monospace"'),text(28,408,'SELF-HOSTING / ALWAYS LEARNING',18,MUTED,500,'font-family="Consolas,monospace"'),
              text(28,440,'CURIOUS BY DESIGN.',18,VIOLET,500,'font-family="Consolas,monospace"')]
    else:
        p += [text(40,36,'PKHARSIMRAN / SECURITY + CODE',13,MINT,500),
              identity_line(40,139,'HARSIMRAN',94),identity_line(40,231,'SIDHU',94),
              text(44,283,'Security instincts. Builder energy.',26,MINT),
              '<path d="M40 319H960" stroke="#29364B"/>',
              text(40,349,'CYBERSECURITY / OPEN SOURCE / SELF-HOSTING',13,MUTED,500),
              text(746,349,'ALWAYS LEARNING ↗',13,VIOLET,500)]
    return ''.join(p+['</g></svg>\n'])


def project(item,mobile=False):
    kind,number,name,area,tagline,tags,color=item
    w,h=(600,312) if mobile else (1000,194)
    p=panel(w,h,name,tagline+' '+tags)
    p += [PROJECT_MOTION,f'<path class="edge-breathe" d="M24 1H{w*.34:.0f}" stroke="{color}" stroke-width="2"/>']
    if not mobile:
        p += ['<path d="M724 28V166" stroke="#29364B"/>',
              '<g transform="translate(746 14)">'+project_scene(kind)+'</g>',
              text(30,32,number+' / '+area.upper(),12,color,500),
              text(28,91,name,43,TEXT,700),text(30,125,tagline,20,MUTED),text(30,169,tags,12,color,500),
              f'<circle cx="955" cy="163" r="15" fill="{color}" fill-opacity=".05" stroke="{color}" stroke-opacity=".22"/>',
              text(947,170,'↗',22,color)]
    else:
        p += [text(28,36,number+' / '+area.upper(),18,color,500,'font-family="Consolas,monospace"'),
              f'<circle cx="555" cy="30" r="17" fill="{color}" fill-opacity=".05" stroke="{color}" stroke-opacity=".22"/>',
              text(548,38,'↗',24,color),
              text(26,98,name,42,TEXT,700),text(28,143,tagline,24,MUTED),
              '<g transform="translate(28 163)">'+project_scene(kind,True)+'</g>',
              text(28,286,tags,18,color,500,'font-family="Consolas,monospace"')]
    return ''.join(p+['</g></svg>\n'])


def outro(mobile=False):
    root=ET.fromstring(visitor_pass(mobile))
    replacements={
        'Hey, curious human. Welcome to the lab.':'Thanks for exploring the lab.',
        'VISITOR ARRIVALS / WELCOME TO THE LAB':'GUESTBOOK / THANKS FOR DROPPING IN',
        'Hey, curious human.':'Still curious?',
        'Welcome to my corner of the internet.':'There’s always another rabbit hole to explore.',
        'Hey, curious':'Stay', 'human.':'curious.',
        'Welcome to my corner':'Come back for the tools.',
        'of the internet.':'Stay for the side quests.',
    }
    for node in root.iter():
        if node.text in replacements:node.text=replacements[node.text]
    return ET.tostring(root,encoding='unicode')+'\n'
