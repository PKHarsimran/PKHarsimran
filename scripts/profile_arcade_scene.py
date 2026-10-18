"""A decorative evidence-run diorama. It never modifies contribution data."""
from html import escape

MINT, VIOLET, PINK = '#43E6C5', '#A995FF', '#F36BAA'
SCENE_REDUCED = '.quest-motion{display:none}.quest-static{display:inline}.quest-gate,.quest-foot-a,.quest-foot-b{animation:none}'
SCENE_CSS = '''
.quest-static{display:none}
.quest-runner{opacity:0;animation:quest-arrival 24s linear infinite}
.quest-foot-a{animation:quest-step .48s steps(2,end) infinite}
.quest-foot-b{animation:quest-step .48s steps(2,end) -.24s infinite}
.quest-loot-first{animation:quest-loot-first 24s linear infinite}
.quest-loot-second{animation:quest-loot-second 24s linear infinite}
.quest-scan{opacity:0;animation:quest-scan 24s ease-in-out infinite}
.quest-gate{animation:quest-gate 24s ease-in-out infinite;opacity:.45}
.quest-delivery{opacity:0;animation:quest-delivery 24s ease-out infinite}
@keyframes quest-arrival{0%,100%{opacity:0}4%,93%{opacity:1}98%{opacity:0}}
@keyframes quest-step{50%{transform:translateX(3px)}}
@keyframes quest-loot-first{0%,24%,100%{opacity:1}29%,98%{opacity:0}}
@keyframes quest-loot-second{0%,65%,100%{opacity:1}71%,98%{opacity:0}}
@keyframes quest-scan{0%,43%,59%,100%{opacity:0;transform:translateY(-10px)}48%{opacity:.7}55%{opacity:.7;transform:translateY(10px)}}
@keyframes quest-gate{0%,75%,100%{opacity:.45}88%,95%{opacity:.95}}
@keyframes quest-delivery{0%,84%,99%,100%{opacity:0;transform:translateY(0)}89%{opacity:.8}97%{opacity:0;transform:translateY(-12px)}}
''' + '@media(prefers-reduced-motion:reduce){' + SCENE_REDUCED + '}\n'


def label(x, y, value, size=12, color='#B8C6DB', anchor='start', weight=500):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>'


def runner():
    return f'''<g shape-rendering="crispEdges">
      <path d="M-6-15H6V-11H11V3H6V8H-6V3H-11V-11H-6Z" fill="{VIOLET}"/>
      <path d="M-7-8H7V-1H-7Z" fill="#0B121C"/>
      <path d="M-4-6H-1V-3H-4ZM2-6H5V-3H2Z" fill="{MINT}"/>
      <path d="M-2-20H1V-15H-2Z" fill="{VIOLET}"/><path d="M-3-23H2V-19H-3Z" fill="{PINK}"/>
      <g class="quest-foot-a"><path d="M-8 7H-2V13H-10V10H-8Z" fill="{VIOLET}"/></g>
      <g class="quest-foot-b"><path d="M3 7H9V10H11V13H3Z" fill="{VIOLET}"/></g>
      <path d="M10-4H22V9H10Z" fill="{PINK}"/><path d="M15-4H18V1H15Z" fill="#EFF4FC" fill-opacity=".75"/>
      <path d="M-13-6H-9V3H-13Z" fill="{MINT}"/>
    </g>'''


def token(x, y, kind):
    shape = f'<path d="M-5-9H5L10-4V4L5 9H-5L-10 4V-4Z" fill="#172236" stroke="{PINK}"/><path d="M0-5L1.5-1.5L5 0L1.5 1.5L0 5L-1.5 1.5L-5 0L-1.5-1.5Z" fill="{PINK}"/>'
    return f'<g transform="translate({x} {y})" aria-hidden="true"><g class="quest-motion quest-loot-{kind}">{shape}</g><g class="quest-static">{shape}</g></g>'


def side_quest(quote, y, mobile=False):
    width, height = (544,184) if mobile else (944,174)
    span = width-44
    floor = y+148
    cy = floor-13
    left = 50
    p = [f'<rect x="28" y="{y}" width="{width}" height="{height}" rx="16" fill="#101925" stroke="#29364B"/>',
         label(50,y+27,'BONUS LOOP / THE EVIDENCE RUN',15 if mobile else 12,VIOLET),
         label(50,y+55,quote,22,'#EFF4FC',weight=600)]
    for ratio, title, color, anchor in ((0,'01 / COLLECT',MINT,'start'),(.5,'02 / INSPECT',VIOLET,'middle'),(1,'03 / DELIVER',PINK,'end')):
        p += [label(left+span*ratio,y+83,title,15 if mobile else 12,color,anchor)]
    # The track is artwork, separate from the real calendar above it.
    p += [f'<path d="M{left} {floor}H{left+span}" stroke="#34445C"/>',
          f'<path d="M{left+14} {floor+8}H{left+span-14}" stroke="#29364B" stroke-dasharray="2 14"/>']
    for ratio in (.245,.685):
        x = left+span*ratio-6
        p += [f'<path d="M{x} {floor}V{floor-8}H{x+12}V{floor}" fill="#192639" stroke="#34445C"/>']
    p += [f'<g transform="translate({left+13} {floor-20})" aria-hidden="true"><rect x="-12" y="-17" width="24" height="30" rx="3" fill="#14232D" stroke="{MINT}" stroke-opacity=".55"/><path d="M-6-9H6M-6-3H3M-6 3H6" stroke="{MINT}" stroke-opacity=".6"/><path d="M-6 17H6M0 13V17" stroke="{MINT}" stroke-opacity=".5"/></g>']
    mid = left+span*.5
    p += [f'<g transform="translate({mid} {floor-23})" aria-hidden="true"><path d="M-13-16H4L13-7V15H-13Z" fill="#14202D" stroke="{VIOLET}" stroke-opacity=".6"/><path d="M4-16V-7H13M-7-2H6M-7 4H3" fill="none" stroke="{VIOLET}" stroke-opacity=".55"/><path class="quest-motion quest-scan" d="M-16 0H17" stroke="{MINT}" stroke-width="2"/></g>']
    gate = left+span*.95
    p += [f'<g transform="translate({gate} {floor-22})" aria-hidden="true"><g class="quest-gate"><ellipse rx="18" ry="28" fill="{VIOLET}" fill-opacity=".05" stroke="{VIOLET}"/><ellipse rx="12" ry="22" fill="none" stroke="{MINT}" stroke-opacity=".4"/><path d="M-23 28H23" stroke="{VIOLET}"/></g><g class="quest-motion quest-delivery"><path d="M-15-27L-18-33M13-30L17-36M-3-32V-40" stroke="{PINK}" stroke-width="2"/><path d="M-5-9L-1-5L6-13" fill="none" stroke="{MINT}" stroke-width="2"/></g></g>']
    p += [token(left+span*.245,cy-34,'first'),token(left+span*.685,cy-34,'second')]
    route = f'M{left+span*.035:g} {cy}L{left+span*.18:g} {cy}Q{left+span*.245:g} {cy-68} {left+span*.31:g} {cy}L{left+span*.62:g} {cy}Q{left+span*.685:g} {cy-68} {left+span*.75:g} {cy}L{gate:g} {cy}'
    p += [f'<g class="quest-motion quest-runner" aria-hidden="true">{runner()}<animateMotion dur="24s" repeatCount="indefinite" path="{route}"/></g>',
          f'<g class="quest-static" transform="translate({left+span*.1} {cy})" aria-hidden="true">{runner()}</g>']
    return '\n'.join(p)
