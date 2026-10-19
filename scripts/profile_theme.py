"""Self-contained SVG type system. No remote fonts or runtime dependencies."""
from base64 import b64encode
from functools import lru_cache
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SVG='http://www.w3.org/2000/svg'
ET.register_namespace('',SVG)


@lru_cache(maxsize=4)
def font(name):
    data=(ROOT/'fonts'/name).read_bytes()
    if data[:4]!=b'wOF2': raise ValueError('Invalid bundled WOFF2 font')
    return 'data:font/woff2;base64,'+b64encode(data).decode('ascii')


def face(name,file,weight):
    return f'@font-face{{font-family:{name};font-style:normal;font-weight:{weight};src:url("{font(file)}") format("woff2");font-display:block}}'


def apply_theme(source,kind='panel'):
    root=ET.fromstring(source)
    for style in list(root):
        if style.get('id')=='profile-type': root.remove(style)
    if kind=='button':
        css=face('ProfileButton','space-grotesk-buttons-600.woff2',600)
    elif kind=='terminal':
        css=face('ProfileMono','ibm-plex-mono-500.woff2',500)
    else:
        css=face('ProfileDisplay','space-grotesk-700.woff2',700)+face('ProfileMono','ibm-plex-mono-500.woff2',500)
    if any(node.get('font-family','').startswith('ProfileName') for node in root.iter('{'+SVG+'}text')):
        css+=face('ProfileName','chakra-petch-name-700.woff2',700)
    for node in root.iter('{'+SVG+'}text'):
        size=float(node.get('font-size','18'))
        weight=float(node.get('font-weight','400'))
        family=node.get('font-family','')
        if kind=='button':
            node.set('font-family','ProfileButton,Segoe UI,Arial,sans-serif')
            node.set('font-weight','600')
        elif family.startswith('ProfileName'):
            node.set('font-weight','700')
        elif kind=='terminal' or size<=15 or 'mono' in family.lower() or 'consolas' in family.lower():
            node.set('font-family','ProfileMono,Consolas,monospace')
            node.set('font-weight','500')
            if kind!='terminal' and node.get('letter-spacing'):
                node.set('letter-spacing',str(min(float(node.get('letter-spacing')),.8)))
        elif size>=22 and weight>=600:
            node.set('font-family','ProfileDisplay,Segoe UI,Arial,sans-serif')
            node.set('font-weight','700')
            node.set('letter-spacing','-.7' if size>=36 else '-.3')
        if node.get('fill')=='#A7B6CE': node.set('fill','#B8C6DB')
    style=ET.Element('{'+SVG+'}style',{'id':'profile-type'})
    style.text=css
    root.insert(0,style)
    return ET.tostring(root,encoding='unicode')+'\n'


PROJECT_MOTION='''<style>.signal-node{animation:signal 4.8s ease-in-out infinite}.signal-ring{animation:ring 18s linear infinite}.inspect-scan{animation:inspect 7s ease-in-out infinite}.download-packet{opacity:0;animation:download 4.5s ease-in-out infinite}.edge-breathe{animation:edge 8s ease-in-out infinite}@keyframes signal{0%,70%,100%{opacity:.5}22%{opacity:1}}@keyframes ring{to{stroke-dashoffset:-138}}@keyframes inspect{0%,65%,100%{transform:translate(0,0)}25%,40%{transform:translate(-5px,-3px)}}@keyframes download{0%,15%,100%{opacity:0;transform:translateY(-15px)}25%{opacity:.8}70%{opacity:.8;transform:translateY(39px)}85%{opacity:0;transform:translateY(44px)}}@keyframes edge{50%{opacity:.45}}@media(prefers-reduced-motion:reduce){.signal-node,.signal-ring,.inspect-scan,.download-packet,.edge-breathe{animation:none}.download-packet{display:none}}</style>'''


def animate_project(source,kind):
    root=ET.fromstring(source)
    icon=root.find('.//{'+SVG+'}g[@transform="translate(891 101)"]')
    if icon is None: raise ValueError('Missing project illustration')
    if icon.get('data-motion')=='v1': return source
    icon.set('data-motion','v1')
    style=ET.fromstring(PROJECT_MOTION)
    root.insert(0,style)
    bar=root.find('.//{'+SVG+'}rect[@width="4"]')
    if bar is not None: bar.set('class','edge-breathe')
    if kind=='swiftioc':
        for i,node in enumerate(icon.findall('{'+SVG+'}circle')):
            if node.get('r')=='49': node.set('class','signal-ring')
            else:
                node.set('class','signal-node')
                node.set('style',f'animation-delay:{i*.6}s')
    elif kind=='inspector':
        group=ET.SubElement(icon,'{'+SVG+'}g',{'class':'inspect-scan'})
        for node in list(icon):
            if node.tag=='{'+SVG+'}circle' or node.get('d')=='M29 31L41 43':
                icon.remove(node); group.append(node)
    elif kind=='downloader':
        group=ET.SubElement(icon,'{'+SVG+'}g',{'class':'download-packet'})
        ET.SubElement(group,'{'+SVG+'}rect',{'x':'-3','y':'-8','width':'6','height':'8','rx':'1','fill':'#F36BAA','stroke':'none'})
    return ET.tostring(root,encoding='unicode')+'\n'
