"""Decorative SVG motion: steady text, local paths, and static reduced-motion fallbacks."""
import xml.etree.ElementTree as ET

SVG='http://www.w3.org/2000/svg'
N='{'+SVG+'}'
MINT,VIOLET,PINK='#43E6C5','#A995FF','#F36BAA'
ET.register_namespace('',SVG)

CSS='''
.motion-echo{opacity:0;animation:echo 8s ease-out infinite;transform-origin:0 0}
.motion-frame{animation:frame-travel 28s linear infinite}
.motion-scan{opacity:0;animation:document-scan 7s ease-in-out infinite}
.motion-result{opacity:.2;animation:clue 7s ease-in-out infinite}
.motion-parcel{opacity:0;animation:parcel 7s linear infinite}
.motion-eyes{transform-box:fill-box;transform-origin:center;animation:eye-rest 7.4s linear infinite}
.motion-radio{opacity:0;animation:radio 8s ease-out infinite}
.motion-stage{opacity:.08;animation:handoff 12s ease-in-out infinite}
@keyframes echo{0%,15%{opacity:0;transform:scale(.72)}25%{opacity:.22}70%,100%{opacity:0;transform:scale(1.28)}}
@keyframes frame-travel{to{stroke-dashoffset:-1000}}
@keyframes document-scan{0%,12%{opacity:0;transform:translateY(-25px)}22%{opacity:.8}65%{opacity:.8;transform:translateY(24px)}78%,100%{opacity:0;transform:translateY(24px)}}
@keyframes clue{0%,30%,100%{opacity:.15}48%,68%{opacity:.9}}
@keyframes parcel{0%,8%,100%{opacity:0}18%,78%{opacity:.9}94%{opacity:0}}
@keyframes eye-rest{0%,43%,47%,100%{transform:scaleY(1)}45%{transform:scaleY(.12)}}
@keyframes radio{0%,60%,100%{opacity:0}68%{opacity:.65;transform:translateY(0)}85%{opacity:0;transform:translateY(-5px)}}
@keyframes handoff{0%,22%,100%{opacity:.08}7%,14%{opacity:.7}}
@media(prefers-reduced-motion:reduce){.motion-only{display:none!important}.motion-eyes{animation:none!important}}
'''


def node(parent,tag,**attrs):
    return ET.SubElement(parent,N+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})


def prepare(source,role):
    root=ET.fromstring(source)
    # The composition can be rerun without stacking duplicate animation layers.
    for parent in list(root.iter()):
        for child in list(parent):
            if child.get('id') in ('profile-motion-style','profile-motion-overlay','profile-motion-defs','profile-motion-icon'):
                parent.remove(child)
    style=node(root,'style',id='profile-motion-style');style.text=CSS
    root.set('data-motion-role',role)
    return root,node(root,'g',id='profile-motion-overlay',aria_hidden='true')


def traveller(parent,path,color,duration=12,begin=0,parcel=False,trail=12):
    attrs={'class':'motion-only'+(' motion-parcel' if parcel else ''),'data-motion':'traveller','fill':color,'stroke':'none'}
    if parcel:attrs['style']=f'animation-delay:{begin}s'
    g=ET.SubElement(parent,N+'g',attrs)
    if parcel:
        node(g,'rect',x=-4,y=-5.5,width=8,height=11,rx=1.5,fill='#121A26',stroke=color,stroke_width=1.3)
        node(g,'path',d='M-1-2H2M-1 1H2',fill='none',stroke=color,stroke_width=1)
    else:
        if trail:node(g,'path',d=f'M-{trail} 0H-3',stroke=color,stroke_width=1.6,stroke_opacity='.35',stroke_linecap='round')
        node(g,'circle',r=2.4,fill=color)
    node(g,'animateMotion',dur=f'{duration}s',begin=f'{begin}s',repeatCount='indefinite',rotate='auto',path=path)
    return g


def orbit(parent,cx,cy,scale=1,angle=-20,small=False):
    center=node(parent,'g',transform=f'translate({cx} {cy}) scale({scale})')
    plane=node(center,'g',transform=f'rotate({angle})')
    rx,ry=(105,33) if small else (124,82)
    route=f'M-{rx} 0A{rx} {ry} 0 1 1 {rx} 0A{rx} {ry} 0 1 1 -{rx} 0'
    traveller(plane,route,MINT,24 if small else 20,trail=10 if small else 18)
    if not small:
        traveller(plane,route,PINK,30,-12,trail=10)
        for delay in (0,4):
            node(center,'circle',r=96,fill='none',stroke=MINT,stroke_width='.8',**{'class':'motion-only motion-echo','style':f'animation-delay:{delay}s'})


def animate_profile(source,role,mobile=False):
    root,overlay=prepare(source,role)
    if role=='hero':
        orbit(overlay,487 if mobile else 809,171 if mobile else 163,.66 if mobile else .9)
        w,h=(600,460) if mobile else (1000,374)
        node(overlay,'rect',x=1,y=1,width=w-2,height=h-2,rx=24,fill='none',stroke=MINT,stroke_width=1.3,stroke_opacity='.5',pathLength=1000,stroke_dasharray='22 978',**{'class':'motion-only motion-frame'})
    elif role in ('swiftioc','inspector','downloader'):
        if root.find('.//'+N+'g[@data-cinematic="'+role+'"]') is not None:
            return ET.tostring(root,encoding='unicode')+'\n'
        transform='translate(548 37) scale(.35)' if mobile else 'translate(890 93) scale(.92)'
        icon=root.find('.//'+N+'g[@transform="'+transform+'"]')
        if icon is None:raise ValueError('Missing project illustration for '+role)
        extra=node(icon,'g',id='profile-motion-icon',aria_hidden='true')
        if role=='swiftioc':
            route='M-29 22L-17-25L28-12L18 31L-29 22'
            traveller(extra,route,MINT,8,trail=0)
            traveller(extra,route,VIOLET,8,-4,trail=0)
            traveller(extra,'M-29 22L28-12L-17-25L18 31',PINK,11,-2,trail=0)
        elif role=='inspector':
            defs=node(root,'defs',id='profile-motion-defs')
            clip=node(defs,'clipPath',id='profile-document-clip')
            node(clip,'path',d='M-25-34H8L24-18V31H-25Z')
            clipped=node(extra,'g',clip_path='url(#profile-document-clip)')
            node(clipped,'path',d='M-26 0H25',fill='none',stroke=MINT,stroke_width=2,**{'class':'motion-only motion-scan'})
            for i,(x,y) in enumerate(((-15,-7),(-15,5),(8,-7))):
                node(extra,'circle',cx=x,cy=y,r=2,fill=MINT,stroke='none',**{'class':'motion-only motion-result','style':f'animation-delay:{i*.6}s'})
        else:
            traveller(extra,'M-35-39Q-50-10-31 13Q-15 33 0 44',PINK,7,parcel=True)
            traveller(extra,'M34-40Q49-9 30 14Q15 34 0 44',VIOLET,7,-3.5,parcel=True)
    elif role=='outro':
        x,y,s=(482,117,.82) if mobile else (849,86,1)
        orbit(overlay,x,y,s,small=True)
        for eye in root.iter(N+'path'):
            if eye.get('d')=='M-9-11H-3V-5H-9ZM3-11H9V-5H3Z':eye.set('class','motion-eyes')
        radio=node(overlay,'g',transform=f'translate({x} {y}) scale({s})',fill='none',stroke=VIOLET,stroke_width=1.2)
        for i,d in enumerate(('M-9-42Q0-49 9-42','M-15-49Q0-61 15-49')):
            node(radio,'path',d=d,**{'class':'motion-only motion-radio','style':f'animation-delay:{i*.6}s'})
    elif role=='divider':
        traveller(overlay,'M35 24C160 9 322 38 467 24Q500 18 533 24C678 10 843 39 965 24',MINT,18,trail=16)
    else:raise ValueError('Unknown motion role: '+role)
    return ET.tostring(root,encoding='unicode')+'\n'


def animate_lab(source):
    root,overlay=prepare(source,'homelab')
    for i,card in enumerate(root.findall('.//'+N+'rect[@rx="14"]')):
        attrs={key:card.get(key) for key in ('x','y','width','height','rx')}
        attrs.update({'class':'motion-only motion-stage','fill':'none','stroke':(MINT,VIOLET,PINK,'#69B9FF')[i%4],'stroke-width':'2','style':f'animation-delay:{i*2.8}s'})
        ET.SubElement(overlay,N+'rect',attrs)
    return ET.tostring(root,encoding='unicode')+'\n'
