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
.name-intro{animation:name-resolve .9s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--phase)}
.name-slice-one,.name-slice-two{opacity:0}
.name-slice-one{animation:name-slice-one 16s linear infinite}
.name-slice-two{animation:name-slice-two 16s linear infinite}
.name-sweep{animation:name-sweep 16s cubic-bezier(.4,0,.2,1) infinite}
.name-slice-one,.name-slice-two,.name-sweep{animation-delay:var(--phase)}
.name-cursor{animation:name-cursor 3.2s steps(1,end) infinite}
@keyframes name-resolve{from{opacity:.45;transform:translateX(-5px)}to{opacity:1;transform:translateX(0)}}
@keyframes name-sweep{0%,2%{transform:translateX(-100px)}14%,100%{transform:translateX(580px)}}
@keyframes name-slice-one{0%,13%,15%,100%{opacity:0;transform:translateX(0)}13.4%{opacity:.7;transform:translateX(-3px)}13.8%{opacity:.45;transform:translateX(2px)}14.2%{opacity:.6;transform:translateX(-1px)}}
@keyframes name-slice-two{0%,13%,15%,100%{opacity:0;transform:translateX(0)}13.6%{opacity:.55;transform:translateX(3px)}14%{opacity:.6;transform:translateX(-2px)}14.4%{opacity:.3;transform:translateX(1px)}}
@keyframes name-cursor{0%,56%,100%{opacity:.85}57%,99%{opacity:.22}}
@media(prefers-reduced-motion:reduce){.name-intro,.name-slice-one,.name-slice-two,.name-sweep,.name-cursor{animation:none}.name-slice-one,.name-slice-two,.name-sheen{display:none}.name-cursor{opacity:.7}}
</style>'''


def identity_line(x, y, value, size):
    """A soft entrance, a masked light sweep, then a short signal-lock glitch."""
    ident = 'name-'+value.lower()
    extra = 'font-family="ProfileName,Consolas,monospace" letter-spacing=".4"'
    p = [f'<g transform="translate({x} {y})" style="--phase:{".24s" if value == "SIDHU" else "0s"}">',
         '<defs>',
         f'<clipPath id="{ident}-upper"><rect x="-5" y="{-size*.69:.1f}" width="580" height="{size*.10:.1f}"/></clipPath>',
         f'<clipPath id="{ident}-lower"><rect x="-5" y="{-size*.27:.1f}" width="580" height="{size*.07:.1f}"/></clipPath>',
         f'<linearGradient id="{ident}-light"><stop stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>',
         f'<mask id="{ident}-sweep" maskUnits="userSpaceOnUse" x="-8" y="{-size}" width="588" height="{size+12}"><rect class="name-sweep" x="0" y="{-size}" width="{size*.9:.1f}" height="{size+12}" fill="url(#{ident}-light)"/></mask>',
         '</defs>', '<g class="name-intro">', text(0,0,value,size,TEXT,700,extra), '</g>',
         f'<g class="name-sheen" mask="url(#{ident}-sweep)" aria-hidden="true">',text(0,0,value,size,MINT,700,extra),'</g>']
    for name, color, clip in (('one',MINT,'upper'), ('two',PINK,'lower')):
        p += [f'<g clip-path="url(#{ident}-{clip})" aria-hidden="true"><g class="name-slice-{name}">',
              text(0,0,value,size,color,700,extra), '</g></g>']
    if value == 'SIDHU':
        p += [f'<rect class="name-cursor" x="{size*3.02+10:.1f}" y="{-size*.13:.1f}" width="{size*.20:.1f}" height="{size*.13:.1f}" fill="{MINT}" aria-hidden="true"/>']
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
    p=panel(w,h,'Harsimran Sidhu / Security instincts. Builder energy.','Cybersecurity, open source and self-hosting. Angular hacker-inspired name lettering settles in, catches a soft cyan light sweep and briefly splits into chromatic slices. Orbital line art surrounds cute Hacker Bender with a tiny laptop. Reduced-motion preferences keep the design still.')
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
