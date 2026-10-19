"""Build local terminal, toolkit, and phone artwork from the profile's vectors."""
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from profile_theme import apply_theme, animate_project, PROJECT_MOTION
from profile_art import header_art, art_style, visitor_pass, orbit_divider
from vendor_tool_icons import ICONS
from profile_motion import animate_profile
from build_readme_art import assets as readme_assets

OUT = Path(__file__).resolve().parents[1] / "profile"
TEXT, MUTED, BORDER = "#EFF4FC", "#A7B6CE", "#29364B"
TOOLS = (
    ("01", "Code & scripts", "#43E6C5", ("Python", "Bash", "C++")),
    ("02", "Security & detection", "#A995FF", ("Splunk", "Cortex XDR", "Kibana", "F5 BIG-IP")),
    ("03", "Automation & infrastructure", "#F36BAA", ("Docker", "Ansible", "Raspberry Pi")),
    ("04", "Observability", "#69B9FF", ("Grafana", "InfluxDB", "MQTT")),
)


def text(x, y, value, size=20, color=TEXT, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(value)}</text>'


def toolkit(mobile=False):
    width, height = (600, 653) if mobile else (1000, 348)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
         '<title id="title">Operator toolkit</title><desc id="desc">Code: Python, Bash, C++. Security: Splunk, Cortex XDR, Kibana, F5 BIG-IP. Infrastructure: Docker, Ansible, Raspberry Pi. Observability: Grafana, InfluxDB, MQTT.</desc>',
         '<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs><style>.tool-led{animation:equipped 12s ease-in-out infinite}@keyframes equipped{0%,16%,100%{opacity:.3}8%{opacity:1}}@media(prefers-reduced-motion:reduce){.tool-led{animation:none;opacity:1}}</style>',
         f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="22" fill="url(#surface)" stroke="{BORDER}"/>',
         text(28, 34, "OPERATOR TOOLKIT / EQUIPPED TO BUILD", 18 if mobile else 13, "#43E6C5", 'font-weight="600" letter-spacing="1.3" font-family="Consolas,monospace"')]
    y=70
    for i, (number, label, color, tools) in enumerate(TOOLS):
        p += [f'<circle class="tool-led" cx="{width-32}" cy="{y+10}" r="3" fill="{color}" style="animation-delay:{i*3}s"/>']
        p += [text(28, y+17, number, 18 if mobile else 13, color, 'font-family="monospace"'),
              text(64, y+17, label, 21 if mobile else 18, TEXT, 'font-weight="600"')]
        x, chip_y = (28, y+36) if mobile else (370, y-6)
        wrapped=False
        for tool in tools:
            chip_width = round(len(tool) * (10.8 if mobile else 10) + 60)
            if mobile and x+chip_width>width-28:
                x=28;chip_y+=47;wrapped=True
            icon_tree=ET.parse(OUT/'icons'/(ICONS[tool]+'.svg'))
            paths=''.join(ET.tostring(node,encoding='unicode') for node in icon_tree.getroot() if node.tag.endswith('}path'))
            if tool=='Splunk':
                paths=f'<path d="M7 4L18 12L7 20" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            p += [f'<rect x="{x}" y="{chip_y}" width="{chip_width}" height="37" rx="9" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".3"/>',
                  f'<g transform="translate({x+13} {chip_y+9.5}) scale(.75)" fill="{color}" aria-hidden="true">{paths}</g>',
                  text(x+43, chip_y+25, tool, 20 if mobile else 18, color, 'font-weight="500"')]
            x += chip_width + 10
        if i < 3:
            p += [f'<path d="M28 {y+(104+(47 if wrapped else 0) if mobile else 47)}H{width-28}" stroke="{BORDER}" stroke-opacity=".6"/>']
        y+=(130+(47 if wrapped else 0)) if mobile else 67
    p += [text(28, height-24, "FAVOURITE SHORTCUT: AUTOMATE THE BORING BITS.", 18 if mobile else 12, MUTED, 'letter-spacing="1" font-family="Consolas,monospace"'), '</g></svg>\n']
    return '\n'.join(p)


def typing():
    phrases = ("Follow the evidence.", "Automate the boring bits.", "Always one more thing to build.")
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="780" height="44" viewBox="0 0 780 44" role="img" aria-labelledby="title desc">',
         '<title id="title">Follow the evidence. Automate the boring bits. Always one more thing to build.</title>',
         '<desc id="desc">Three rotating terminal lines. Reduced motion shows the first line.</desc>',
         '<style>.line{opacity:0;animation:line 15s linear infinite}.second{animation-delay:5s}.third{animation-delay:10s}.reveal{animation:type 5s steps(31,end) infinite}.caret{animation:travel 5s steps(31,end) infinite}.blink{animation:blink 1s steps(2,end) infinite}@keyframes line{0%,32%{opacity:1}33.333%,100%{opacity:0}}@keyframes type{0%{width:0}55%,88%{width:var(--extent)}100%{width:0}}@keyframes travel{0%{transform:translateX(0)}55%,88%{transform:translateX(var(--extent))}100%{transform:translateX(0)}}@keyframes blink{50%{opacity:0}}@media(prefers-reduced-motion:reduce){.line,.reveal,.caret,.blink{animation:none}.first{opacity:1}.reveal{width:var(--extent)}.caret{display:none}}</style>',
         '<g fill="#43E6C5" font-family="Consolas,monospace" font-size="22">']
    for i, (cls, phrase) in enumerate(zip(("first", "second", "third"), phrases)):
        extent = round(len(phrase)*13.2, 1)
        x = round((780-extent-36)/2, 1)
        p += [f'<defs><clipPath id="reveal{i}"><rect class="reveal" width="{extent}" height="44" style="--extent:{extent}px"/></clipPath></defs>',
              f'<g class="line {cls}" transform="translate({x} 0)">', text(0,29,">",22,"#A995FF"),
              f'<g transform="translate(30 0)" style="--extent:{extent}px"><g clip-path="url(#reveal{i})">',
              text(0,29,phrase,22,"#43E6C5",f'textLength="{extent}" lengthAdjust="spacingAndGlyphs"'),
              '</g><g class="caret"><path class="blink" d="M4 11V32" stroke="#A995FF" stroke-width="2"/></g></g></g>']
    p += ['</g></svg>\n']
    return '\n'.join(p)


def panel(width, height, title, description):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '<defs><linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#A7B6CE" stroke-opacity=".055"/></pattern></defs>',
            f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="22" fill="url(#surface)" stroke="{BORDER}"/><rect x="2" y="2" width="{width-4}" height="{height-4}" rx="21" fill="url(#grid)"/>']


def artwork_group(name, transform, replacement):
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    tree = ET.parse(OUT/name)
    group = tree.find(f'.//{{http://www.w3.org/2000/svg}}g[@transform="{transform}"]')
    if group is None:
        raise ValueError(f'Missing source artwork in {name}: {transform}')
    group.set('transform', replacement)
    return ET.tostring(group, encoding='unicode')


def mobile_banner():
    source = (OUT/'mission-banner-orbital.svg').read_text(encoding='utf-8')
    p = panel(600,440,'Harsimran Sidhu — mission control','Cybersecurity, threat intelligence, automation. A radar and floating pixel robot decorate the panel. Animation respects reduced motion.')
    p += [art_style(),artwork_group('mission-banner-orbital.svg','translate(620 55)','translate(389 104) scale(.55)'),re.search(r'<style>.*?</style>',source,re.S).group(),
          text(28,34,'PKHARSIMRAN / MISSION CONTROL',15,MUTED,'font-weight="600" letter-spacing="1.2"'),
          text(28,116,'HARSIMRAN',56,TEXT,'font-weight="750" textLength="343" lengthAdjust="spacingAndGlyphs"'),
          text(28,181,'SIDHU',56,TEXT,'font-weight="750"'),
          text(30,238,'Turning curiosity',27,'#43E6C5','font-weight="500"'),
          text(30,273,'into automation.',27,'#43E6C5','font-weight="500"'),
          artwork_group('mission-banner-orbital.svg','translate(801 164)','translate(479 218) scale(.76)'),
          artwork_group('mission-banner-orbital.svg','translate(916 258)','translate(518 365) scale(1.05)')]
    for x,label,color,width in [(30,'SECURITY','#43E6C5',125),(165,'THREAT INTEL','#A995FF',167),(342,'AUTOMATION','#F36BAA',159)]:
        p += [f'<rect x="{x}" y="316" width="{width}" height="34" rx="17" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".3"/>', text(x+13,339,label,15,color,'font-weight="600"')]
    p += [text(30,400,'BUILD / INVESTIGATE / LEARN / REPEAT',14,MUTED,'letter-spacing="1"'),'</g></svg>\n']
    return '\n'.join(p)


def mobile_project(kind, number, name, tagline, tags, color):
    p = panel(600,264,name,tagline+' '+tags)
    p += [PROJECT_MOTION, f'<path class="edge-breathe" d="M2 28V234" stroke="{color}" stroke-width="4"/>',
          text(28,37,f'PROJECT / {number}',15,color,'font-weight="600" letter-spacing="1.5"'),
          artwork_group(f'mission-{kind}.svg','translate(891 101)','translate(545 43) scale(.38)'),
          text(28,104,name,39,TEXT,'font-weight="700" letter-spacing="-1"'),
          text(30,149,tagline,23,MUTED),text(30,215,tags,15,color,'font-weight="600"'),
          text(543,235,'↗',25,color),'</g></svg>\n']
    return '\n'.join(p)


def mobile_now():
    p=panel(600,414,'Now building — the Compose starter kit','In development: modular home-server services and guided setup. Next checkpoint: independent fresh-install validation using the documentation.')
    p += ['<style>.rack-led{animation:rack 5s ease-in-out infinite}@keyframes rack{0%,70%,100%{opacity:.35}25%{opacity:1}}@media(prefers-reduced-motion:reduce){.rack-led{animation:none}}</style>',
          text(28,36,'NOW BUILDING / IN DEVELOPMENT',15,'#F36BAA','font-weight="600"'),
          text(28,100,'The Compose',37,TEXT,'font-weight="700"'),
          text(28,145,'starter kit',37,TEXT,'font-weight="700"'),
          artwork_group('mission-now.svg','translate(822 70)','translate(456 76) scale(.64)'),
          text(28,199,'Modular services. Guided setup.',23,MUTED),
          text(28,233,'Connections included.',23,MUTED),
          f'<path d="M28 264H572" stroke="{BORDER}"/>',
          text(28,300,'NEXT CHECKPOINT',15,'#A995FF','font-weight="600"'),
          text(28,343,'An independent fresh install,',23,'#43E6C5'),
          text(28,377,'using only the docs.',23,'#43E6C5'),'</g></svg>\n']
    return '\n'.join(p)


def mobile_homelab():
    p=panel(600,856,'Zima homelab — connected by Compose','The same public service inventory as the desktop panel, arranged vertically for smaller screens. Animated connections are decorative; no network addresses or private configuration are included.')
    p += ['<style>.packet{animation:flow 6s linear infinite}@keyframes flow{to{stroke-dashoffset:-54}}@media(prefers-reduced-motion:reduce){.packet{animation:none}}</style>',
          text(28,36,'ZIMA HOMELAB / DOCKER COMPOSE',16,'#43E6C5','font-weight="600" letter-spacing="1"'),
          text(28,76,'One server. Connected services.',28,TEXT,'font-weight="600"'),
          '<path d="M42 119V779" stroke="#29364B" stroke-width="2"/><path class="packet" d="M42 119V779" stroke="#43E6C5" stroke-width="2" stroke-dasharray="5 22"/>']
    rows=[('MEDIA + AUTOMATION','Jellyfin · Jellyseerr','Radarr · Sonarr · Prowlarr · Bazarr','#43E6C5'),('DOWNLOADS','Transmission · Gluetun','VPN-routed downloads','#A995FF'),('PHOTOS','PhotoPrism','Photo library + indexing','#F36BAA'),('BOOKS + AUDIO','Shelfmark · Audiobookshelf','Reading + listening libraries','#43E6C5'),('OPERATIONS','Homepage · Portainer','Custom flow dashboards','#A995FF'),('MONITORING','Uptime Kuma · Glances','Dozzle logs + ntfy notifications','#F36BAA')]
    for i,(label,services,detail,color) in enumerate(rows):
        y=104+i*114
        p += [f'<circle cx="42" cy="{y+49}" r="6" fill="{color}"/><path d="M48 {y+49}H68" stroke="{color}" stroke-opacity=".4"/><rect x="68" y="{y}" width="504" height="100" rx="13" fill="#121A26" stroke="{BORDER}"/>',
              text(86,y+25,f'0{i+1} / {label}',15,color,'font-weight="600"'),
              text(86,y+55,services,23,TEXT,'font-weight="500"'),text(86,y+81,detail,19,MUTED)]
    p += [text(28,826,'SELF-HOSTING / WORKFLOWS / AUTOMATION',14,MUTED,'letter-spacing="1"'),'</g></svg>\n']
    return '\n'.join(p)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in ('mission-banner-orbital.svg','mission-now.svg','mission-swiftioc.svg','mission-inspector.svg','mission-downloader.svg'):
        path=OUT/name
        content=path.read_text(encoding='utf-8')
        if name=='mission-banner-orbital.svg':content=header_art(content)
        if name in ('mission-swiftioc.svg','mission-inspector.svg','mission-downloader.svg'):
            content=animate_project(content,name.removeprefix('mission-').removesuffix('.svg'))
        path.write_text(apply_theme(content),encoding='utf-8')
    terminal=typing()
    assets={"mission-typing.svg":terminal,"mission-typing-mobile.svg":terminal.replace('width="780" height="44" viewBox="0 0 780 44"','width="512" height="44" viewBox="134 0 512 44"'),"mission-toolkit-icons.svg":toolkit(),"mission-toolkit-icons-mobile.svg":toolkit(True),"mission-banner-orbital-mobile.svg":mobile_banner(),"mission-homelab-mobile.svg":mobile_homelab()}
    for kind,number,name,tagline,tags,color in [('swiftioc','01','SwiftIOC','Follow the indicator. Keep the evidence.','PYTHON / THREAT INTEL / ANALYST WORKFLOWS','#43E6C5'),('inspector','02','IOC Inspector','Suspicious documents. Useful answers.','PYTHON / STATIC ANALYSIS / REPORTS','#A995FF'),('downloader','03','Website Downloader','Take a little piece of the web offline.','PYTHON / WEB ARCHIVING / PLAYWRIGHT','#F36BAA')]:
        assets[f'mission-{kind}-mobile.svg']=mobile_project(kind,number,name,tagline,tags,color)
    assets['mission-now-mobile.svg']=mobile_now()
    assets['mission-visitors.svg']=visitor_pass()
    assets['mission-visitors-mobile.svg']=visitor_pass(True)
    assets['studio-signal-divider.svg']=animate_profile(orbit_divider(),'divider')
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        assets['studio-guestbook-motion'+suffix+'.svg']=animate_profile(profile_studio.outro(mobile),'outro',mobile)
    assets.update(readme_assets())
    for name, content in assets.items():
        (OUT / name).write_text(apply_theme(content,'terminal' if 'typing' in name else 'panel'), encoding="utf-8")
