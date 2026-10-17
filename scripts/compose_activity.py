"""Lay out existing generated cards side by side, or stack them for phone readers."""
from copy import deepcopy
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SVG='http://www.w3.org/2000/svg'
ET.register_namespace('',SVG)


def card(path,prefix):
    node=ET.parse(path).getroot()
    identifiers={e.get('id') for e in node.iter() if e.get('id')}
    classes={c for e in node.iter() for c in e.get('class','').split()}
    xml=ET.tostring(node,encoding='unicode')
    for value in sorted(identifiers,key=len,reverse=True):
        xml=xml.replace('id="'+value+'"','id="'+prefix+value+'"').replace('url(#'+value+')','url(#'+prefix+value+')')
        xml=re.sub(r'(aria-labelledby|aria-describedby)="([^"]+)"',lambda m:m[1]+'="'+' '.join(prefix+x if x==value else x for x in m[2].split())+'"',xml)
    node=ET.fromstring(xml)
    for element in node.iter():
        if element.get('class'):
            element.set('class',' '.join(prefix+c for c in element.get('class').split()))
        if element.tag=='{'+SVG+'}style' and element.text:
            css=element.text
            for c in sorted(classes,key=len,reverse=True):
                css=re.sub(r'\.'+re.escape(c)+r'(?![\w-])','.'+prefix+c,css)
            names=re.findall(r'@keyframes\s+([\w-]+)',css)
            for name in set(names):
                css=re.sub(r'(?<![\w-])'+re.escape(name)+r'(?![\w-])',prefix+name,css)
            element.text=css
    width,height=map(float,node.get('viewBox').split()[2:])
    return node,width,height


def compose(mobile=False):
    cards=[card(ROOT/'profile/stats.svg','stats-'),card(ROOT/'profile/top-langs.svg','langs-')]
    gap=24
    if mobile:
        width=600
        placements=[(0,0,600,600/cards[0][1]*cards[0][2])]
        placements.append((0,placements[0][3]+gap,600,600/cards[1][1]*cards[1][2]))
        height=sum(p[3] for p in placements)+gap
    else:
        width=1000
        scale=(width-gap)/(cards[0][1]+cards[1][1])
        placements=[(0,0,cards[0][1]*scale,cards[0][2]*scale),(cards[0][1]*scale+gap,0,cards[1][1]*scale,cards[1][2]*scale)]
        height=max(p[3] for p in placements)
    result=ET.Element('{'+SVG+'}svg',{'width':str(width),'height':str(round(height,2)),'viewBox':f'0 0 {width} {height:.2f}','role':'img','aria-labelledby':'activity-title activity-desc'})
    ET.SubElement(result,'{'+SVG+'}title',{'id':'activity-title'}).text='GitHub activity and language mix'
    ET.SubElement(result,'{'+SVG+'}desc',{'id':'activity-desc'}).text='The current generated GitHub statistics and language cards, arranged for '+('phone' if mobile else 'desktop')+' reading.'
    ET.SubElement(result,'{'+SVG+'}style').text='@media(prefers-reduced-motion:reduce){*{animation-duration:.001ms!important;animation-delay:0ms!important;animation-iteration-count:1!important}}'
    for (node,_,_), (x,y,w,h) in zip(cards,placements):
        child=deepcopy(node)
        for key,value in {'x':x,'y':y,'width':w,'height':h}.items(): child.set(key,f'{value:.2f}')
        result.append(child)
    return ET.tostring(result,encoding='unicode')+'\n'


if __name__=='__main__':
    for mobile in (False,True):
        name='activity-summary'+('-mobile' if mobile else '')+'.svg'
        (ROOT/'profile'/name).write_text(compose(mobile),encoding='utf-8')
