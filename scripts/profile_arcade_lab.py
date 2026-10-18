"""A reproducible README puzzle, snapshot rewind, and collectible public-data sprite."""
from datetime import datetime
from hashlib import sha256
from html import escape
import json
import re

from contribution_arcade import calendar_summary
from profile_theme import apply_theme

PROJECTS = {
    'SwiftIOC-Automated-Threat-Intelligence-Collector': 'SwiftIOC',
    'IOC-Inspector': 'IOC Inspector',
    'website-downloader': 'Website Downloader',
}
COLORS = ('#43E6C5', '#A995FF', '#F36BAA')
FIELDS = ('release', 'ci', 'stars', 'latest_commit_at')
CREATURES = ('Cache Goblin','Packet Pixie','Log Sprite','Port Nomad','Byte Moth','Patch Imp','Signal Sprout','Null Navigator')
START, END = '<!-- arcade-lab:start -->', '<!-- arcade-lab:end -->'
RECIPE = 'signal-heist-v1'


class Picker:
    """Recipe-owned selection stays stable across Python runtime upgrades."""
    def __init__(self, seed):
        self.seed, self.counter = seed, 0

    def index(self, length):
        value = sha256(f'{self.seed}:{self.counter}'.encode()).digest()
        self.counter += 1
        return int.from_bytes(value, 'big') % length

    def choice(self, values):
        return values[self.index(len(values))]

    def shuffle(self, values):
        for i in range(len(values)-1,0,-1):
            j = self.index(i+1)
            values[i],values[j] = values[j],values[i]


def observation(snapshot):
    projects = snapshot['projects']
    if len(projects) != 3 or {p['repo'] for p in projects} != set(PROJECTS):
        raise ValueError('Arcade inputs must be exactly the three selected public repositories')
    datetime.fromisoformat(snapshot['generated_at'].replace('Z', '+00:00'))
    result = []
    for repo in PROJECTS:
        item = next(p for p in projects if p['repo'] == repo)
        if type(item['stars']) is not int or item['stars'] < 0:
            raise ValueError('Invalid public star count')
        result.append({'repo': repo, **{key: item[key] for key in FIELDS}})
    return {'generated_at': snapshot['generated_at'], 'projects': result}


def build_lab(snapshot, calendar, previous=None):
    current = observation(snapshot)
    summary = calendar_summary(calendar)
    day = snapshot['generated_at'][:10]
    canonical = {'recipe':RECIPE, 'day': day, 'projects': current['projects'], 'days': calendar['days']}
    fingerprint = sha256(json.dumps(canonical, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    asset_id = fingerprint[:16]
    rng = Picker(fingerprint)
    project = rng.choice(current['projects'])
    version = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)(?:[-+].+)?', str(project['release']))
    if version:
        part = rng.choice((1, 2))
        a = {'id': 'A', 'label': 'RELEASE', 'source': PROJECTS[project['repo']], 'display': str(project['release']), 'hint': 'Minor version: ones digit.' if part == 1 else 'Patch version: ones digit.', 'value': int(version[part+1])}
    else:
        a = {'id': 'A', 'label': 'PROJECT STARS', 'source': PROJECTS[project['repo']], 'display': str(project['stars']), 'hint': 'Stars: take the ones digit.', 'value': project['stars']}
    recent = summary['recent'] is not None and rng.choice((True, False))
    b_value = summary['recent'] if recent else summary['active']
    b = {'id': 'B', 'label': 'CALENDAR', 'source': 'Last 30 days / contributions' if recent else 'Days with activity', 'display': f'{b_value:,}', 'hint': 'Take the ones digit.', 'value': b_value}
    passing = rng.choice((True, False))
    c_value = sum(p['ci'] == 'PASSING' for p in current['projects']) if passing else sum(p['stars'] for p in current['projects'])
    c = {'id': 'C', 'label': 'BUILD RADAR', 'source': 'Passing checks / selected 3' if passing else 'Stars / selected 3 projects', 'display': f'{c_value:,}', 'hint': 'Take the ones digit.', 'value': c_value}
    gates = [a, b, c]
    for gate in gates:
        gate['digit'] = gate['value'] % 10
    route = list('ABC')
    rng.shuffle(route)
    digits = {g['id']: g['digit'] for g in gates}
    solution = ''.join(str(digits[key]) for key in route)
    choices = [solution, f'{(int(solution)+137)%1000:03}', f'{(int(solution)+463)%1000:03}']
    rng.shuffle(choices)
    before = observation(previous) if previous else None
    changes = []
    if before:
        old = {p['repo']: p for p in before['projects']}
        for item in current['projects']:
            for field in FIELDS:
                if old[item['repo']][field] != item[field]:
                    changes.append({'project': PROJECTS[item['repo']], 'field': field, 'before': old[item['repo']][field], 'after': item[field]})
    return {'schema': 1, 'recipe':RECIPE, 'generated_at': snapshot['generated_at'], 'calendar_observed_at': calendar['generated_at'], 'fingerprint': fingerprint,
            'serial': fingerprint[:8].upper(), 'asset_id':asset_id, 'retained':[asset_id],
            'assets':{'heist':f'arcade/heist-{asset_id}.svg','mobile':f'arcade/heist-{asset_id}-mobile.svg','relic':f'arcade/relic-{asset_id}.svg'},
            'relic_name':CREATURES[int(fingerprint[14:16],16)%len(CREATURES)], 'gates': gates, 'route': route, 'solution': solution, 'choices': choices,
            'tool_url': 'https://github.com/PKHarsimran/'+project['repo'], 'tool_name': PROJECTS[project['repo']],
            'rewind': {'previous': before, 'current': current, 'changes': changes},
            'sources': ['public-pulse.json', 'contribution-calendar.json']}


def text(x, y, value, size=18, color='#EFF4FC', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>'


def panel(w, h, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="lab-title"><title id="lab-title">{escape(title)}</title>',
            '<defs><linearGradient id="lab-bg" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs>',
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#lab-bg)" stroke="#29364B"/><g font-family="Segoe UI,Arial,sans-serif">']


def clue_description(lab):
    return 'Signal Heist. Route: '+', then '.join(lab['route'])+'. '+'. '.join(f"Gate {g['id']}: {g['source']}, {g['display']}. {g['hint'].rstrip('.')}" for g in lab['gates'])+'. Choose a three-digit code below.'


def render_heist(lab, mobile=False):
    w,h = (600,815) if mobile else (1000,410)
    p = panel(w,h,clue_description(lab))
    p += [text(28,34,'SIGNAL HEIST / '+lab['serial'],15 if mobile else 12,COLORS[0],600),
          text(28,82,'Three clues. One route.',34 if mobile else 40,weight=700),
          text(28,116,'Take the ones digit from each clue.',20,'#B8C6DB'),
          text(28,151,'ROUTE / '+' → '.join(lab['route']),24,COLORS[1],600)]
    for i,gate in enumerate(lab['gates']):
        x,y,cw = (28,174+i*190,544) if mobile else (28+i*322,174,300)
        color = COLORS[i]
        p += [f'<rect x="{x}" y="{y}" width="{cw}" height="170" rx="15" fill="#101925" stroke="#29364B"/><path d="M{x+1} {y+24}V{y+146}" stroke="{color}" stroke-width="3"/>',
              text(x+20,y+28,'GATE '+gate['id']+' / '+gate['label'],16 if mobile else 12,color,600),
              text(x+20,y+60,gate['source'],20 if mobile else 16,'#B8C6DB'),
              text(x+20,y+107,gate['display'][:23],36,color,700),
              text(x+20,y+143,gate['hint'],21 if mobile else 17)]
    p += [text(28,773 if mobile else 378,'Try a code below. Open its hatch to check.',18 if mobile else 16,'#B8C6DB'),
          text(28,799 if mobile else 399,'SNAPSHOT / '+lab['generated_at'][:10],14 if mobile else 11,'#B8C6DB'),'</g></svg>\n']
    return apply_theme('\n'.join(p))


def render_relic(lab):
    digest = bytes.fromhex(lab['fingerprint'])
    name = lab['relic_name']
    p = panel(600,268,'Snapshot relic '+lab['serial']+': '+name+'. A deterministic pixel creature drawn from the public snapshot fingerprint.')
    p += ['<style>.relic-float{animation:relic-float 8s ease-in-out infinite}@keyframes relic-float{50%{transform:translateY(-.5px)}}@media(prefers-reduced-motion:reduce){.relic-float{animation:none}}</style>',
          text(28,34,'SNAPSHOT RELIC / SIGNAL HEIST',14,COLORS[0],600),
          '<circle cx="112" cy="139" r="67" fill="#A995FF" fill-opacity=".035" stroke="#A995FF" stroke-opacity=".2"/>',
          '<g transform="translate(72 99) scale(9)"><g class="relic-float" shape-rendering="crispEdges">']
    for row in range(9):
        for col in range(5):
            bit = row*5+col
            active = bool(digest[bit//8] & (1 << (bit%8))) or (2 <= row <= 6 and 2 <= col <= 3)
            if active:
                color = COLORS[(digest[(row+col)%32]+row)%3]
                for mirrored in sorted({col,8-col}):
                    p.append(f'<rect x="{mirrored}" y="{row}" width="1" height="1" fill="{color}"/>')
    p += ['<path d="M2 3H4V5H2ZM5 3H7V5H5Z" fill="#0D1117"/><path d="M2.5 3.5H3.5V4.5H2.5ZM5.5 3.5H6.5V4.5H5.5Z" fill="#43E6C5"/></g></g>',
          text(218,109,name,32,weight=700),text(220,147,'RELIC / '+lab['serial'],15,COLORS[1],600),
          text(220,183,'A tiny creature from public signals.',18,'#B8C6DB'),
          text(28,242,'SNAPSHOT / '+lab['generated_at'][:10]+' / KEEP TINKERING',13,'#B8C6DB'),'</g></svg>\n']
    return apply_theme('\n'.join(p))


def md(value):
    return str(value if value is not None else 'not recorded').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('|','\\|').replace('`','&#96;').replace('\n',' ')


def readme_slot(lab):
    p = ['<details>',"<summary><strong>🎲 Enter today's Signal Heist</strong></summary>",'',
         '<picture>','  <source media="(max-width: 600px)" srcset="./profile/'+lab['assets']['mobile']+'">',
         '  <img src="./profile/'+lab['assets']['heist']+'" alt="'+escape(clue_description(lab),quote=True)+'" width="100%">','</picture>','',
         '**Read the clues, follow the route, pick a hatch.** A correct code unlocks today’s snapshot creature.','']
    for choice in lab['choices']:
        p += ['<details>',f'<summary><strong>Try code {choice}</strong></summary>','']
        if choice == lab['solution']:
            p += [f"🔓 **Signal recovered.** {' → '.join(lab['route'])} gives **{choice}**.",'', '| Gate | Clue | Digit |','| --- | --- | ---: |']
            p += [f"| {g['id']} | {md(g['source'])}: {md(g['display'])} · {md(g['hint'])} | {g['digit']} |" for g in lab['gates']]
            p += ['',f"**Next side quest:** [Explore {lab['tool_name']}]({lab['tool_url']}) — the real tool behind gate A.",'',
                  '<img src="./profile/'+lab['assets']['relic']+'" alt="Snapshot relic '+lab['serial']+': '+lab['relic_name']+', a symmetric pixel creature drawn from this public snapshot." width="600">','',
                  '[Open today’s relic](./profile/'+lab['assets']['relic']+') · [Read its snapshot fingerprint](./profile/arcade-lab.json)','']
        else:
            p += ['↺ **Decoy hatch.** Take each clue’s ones digit, then arrange the digits in the printed route order. Try another hatch.','']
        p += ['</details>','']
    rewind = lab['rewind']
    p += ['<details>','<summary><strong>⏪ Rewind the previous snapshot</strong></summary>','']
    if rewind['previous']:
        p += [f"Compared **{md(rewind['previous']['generated_at'])}** → **{md(lab['generated_at'])}** (UTC). These are observed snapshots of the three selected public repositories.",'']
        if rewind['changes']:
            p += ['| Project | Signal | Before | Now |','| --- | --- | --- | --- |']
            p += [f"| {md(c['project'])} | {md(c['field'].replace('_',' '))} | {md(c['before'])} | {md(c['after'])} |" for c in rewind['changes']]
        else:
            p += ['**Quiet checkpoint.** Release tags, CI states, star counts and latest commit timestamps match the previous snapshot.']
    else:
        p += ['**First checkpoint saved.** The next refresh can compare the selected public project signals.']
    p += ['', '</details>', '', '<sub>Clues and creatures rotate with the daily public snapshot. [Open the fingerprint and source data](./profile/arcade-lab.json).</sub>', '', '</details>']
    return '\n'.join(p)


def update_readme(source, lab):
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError('Expected exactly one arcade README slot')
    before, tail = source.split(START)
    _, after = tail.split(END)
    return before+START+'\n'+readme_slot(lab)+'\n'+END+after


def retained_editions(previous, current):
    values = previous.get('retained', []) if previous else []
    if not isinstance(values,list) or any(not isinstance(v,str) or not re.fullmatch('[0-9a-f]{16}',v) for v in values):
        raise ValueError('Invalid arcade asset history')
    return [value for value in dict.fromkeys(values) if value != current][-13:]+[current]


def prune_editions(directory, retained):
    """Only remove obsolete generator-owned SVG names in its dedicated directory."""
    directory = directory.resolve()
    for path in directory.glob('*.svg'):
        match = re.fullmatch(r'(?:heist|relic)-([0-9a-f]{16})(?:-mobile)?\.svg',path.name)
        if match and match[1] not in retained:
            if path.resolve().parent != directory:
                raise ValueError('Arcade output escaped its dedicated directory')
            path.unlink()
