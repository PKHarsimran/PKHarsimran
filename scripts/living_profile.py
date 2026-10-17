"""Public-data artwork and release-pinned demo planning. Standard library only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html import escape
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

from generate_profile_lab import PROJECTS, OWNER, github_json, txt, surface, MUTED, TEXT, BORDER

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'profile'
SWIFT = 'https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/'
DEMO_REPOS = {'inspector': 'IOC-Inspector', 'downloader': 'website-downloader'}
COLORS = ['#43E6C5', '#A995FF', '#F36BAA', '#69B9FF']
STYLE = '<style>.packet{animation:packet 8s linear infinite}.scan{animation:scan 4s ease-in-out infinite}@keyframes packet{to{stroke-dashoffset:-96}}@keyframes scan{50%{opacity:.25}}@media(prefers-reduced-motion:reduce){.packet,.scan{animation:none}}</style>'


def write(name, value):
    OUT.mkdir(exist_ok=True)
    text = json.dumps(value, indent=2, ensure_ascii=False)+'\n' if not isinstance(value, str) else value
    target = OUT/name
    temporary = target.with_suffix(target.suffix+'.tmp')
    temporary.write_text(text, encoding='utf-8')
    temporary.replace(target)


def public_json(path):
    if path not in ('diagnostics/run.json', 'diagnostics/collection-attempt.json'):
        raise ValueError('Unapproved public diagnostics path')
    with urlopen(Request(SWIFT+path, headers={'User-Agent':'PKHarsimran-living-profile'}), timeout=25) as response:
        data = response.read(1_000_001)
    if len(data)>1_000_000:
        raise ValueError('Oversized diagnostics')
    return json.loads(data)


def count(value):
    if type(value) is not int or value < 0:
        raise ValueError('Invalid public count')
    return value


def intel_snapshot(run, attempt, now):
    stamp = datetime.fromisoformat(run['ts'].replace('Z','+00:00'))
    if stamp.tzinfo is None or stamp > now:
        raise ValueError('Invalid collection timestamp')
    c = run['collections']
    observables, vulnerabilities = count(c['observables']), count(c['vulnerabilities'])
    if observables+vulnerabilities != count(run['total']):
        raise ValueError('Collection counts do not reconcile')
    status = attempt.get('status','unknown')
    if status not in ('accepted','rejected','failed','unknown'):
        status='unknown'
    return {'observed_at':now.isoformat().replace('+00:00','Z'), 'collection_at':run['ts'], 'source':SWIFT+'diagnostics/run.json', 'observables':observables, 'vulnerabilities':vulnerabilities, 'duplicates_removed':count(run['duplicates_removed']), 'retained':count(run['total']), 'delta':{k:count(run['delta_counts'][k]) for k in ('added','updated','removed')}, 'latest_attempt':status, 'attempt_at':attempt.get('ts'), 'scope':'Retained snapshot and one collection interval; not threats detected or local incidents.'}


def stamp(value):
    return datetime.fromisoformat(value.replace('Z','+00:00')).strftime('%d %b %Y / %H:%M UTC')


def conveyor(data, mobile=False):
    w,h = (600,686) if mobile else (1000,390)
    p=surface(w,h,'SwiftIOC intelligence conveyor','Animated illustration of the collection pipeline. All counts come from the published diagnostics. '+data['scope'])
    p += [STYLE,txt(28,34,'SWIFTIOC / INTELLIGENCE CONVEYOR',14,COLORS[0],600),txt(28,74,'Follow the data. Keep the evidence.',26,TEXT,600)]
    stages=[('COLLECT','Public feeds','Retrieve source records'),('NORMALIZE',f'{data["duplicates_removed"]:,} duplicates','Removed during collection'),('PUBLISH',f'{data["retained"]:,} retained','Bounded snapshot'),('INVESTIGATE','Source-aware records','Open the analyst dashboard')]
    for i,(label,value,detail) in enumerate(stages):
        x,y = (28,98+i*104) if mobile else (28+i*242,108)
        cw,ch = (544,88) if mobile else (220,126)
        if i<3:
            path=f'M300 {y+88}V{y+104}' if mobile else f'M{x+220} {y+63}H{x+242}'
            p += [f'<path class="packet" d="{path}" stroke="{COLORS[i]}" stroke-width="3" stroke-dasharray="4 5"/>']
        p += [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="#121A26" stroke="{BORDER}"/>',txt(x+16,y+25,f'0{i+1} / {label}',13,COLORS[i],600),txt(x+16,y+53,value,22 if mobile else 19,TEXT,600),txt(x+16,y+76 if mobile else y+91,detail,16 if mobile else 13,MUTED)]
    y=538 if mobile else 272
    p += [txt(28,y,f'{data["observables"]:,} observables  /  {data["vulnerabilities"]:,} CVEs',21 if mobile else 20,COLORS[0],600),txt(28,y+30,f'Last interval: +{data["delta"]["added"]:,} added / {data["delta"]["updated"]:,} updated / {data["delta"]["removed"]:,} removed',17 if mobile else 15,MUTED),txt(28,y+62,'COLLECTION / '+stamp(data['collection_at']),14 if mobile else 12,MUTED),txt(28,h-22,'Retained records, not local detections. Open the snapshot for context.',14 if mobile else 12,MUTED),'</g></svg>\n']
    return '\n'.join(p)


def validate_lab(manifest):
    if set(manifest) != {'schema_version','label','scope','media_flow','libraries','operations','monitoring'}:
        raise ValueError('The public manifest accepts service labels only')
    if manifest['schema_version'] != 1 or manifest['label'] != 'Zima homelab' or len(manifest['media_flow']) != 4:
        raise ValueError('Unexpected public manifest structure')
    labels=[manifest['scope']]
    for stage in manifest['media_flow']:
        if set(stage) != {'title','services','detail'} or not 1<=len(stage['services'])<=4:
            raise ValueError('Unexpected service group')
        labels += [stage['title'],stage['detail'],*stage['services']]
    for name in ('libraries','operations','monitoring'):
        labels += manifest[name]
    for label in labels:
        if not isinstance(label,str) or len(label)>100 or re.search(r'https?://|\d+\.\d+\.\d+\.\d+|[\\/@=]',label):
            raise ValueError('Use public service labels, never configuration or addresses')
    return manifest


def lab_flow(data,mobile=False):
    w,h=(600,850) if mobile else (1000,426)
    p=surface(w,h,'Zima homelab flow theatre','Illustrative service handoffs, generated from the curated public service manifest. No live health or network topology is represented.')
    p += [STYLE,txt(28,34,'ZIMA HOMELAB / FLOW THEATRE',14,COLORS[0],600),txt(28,76,'From “can we watch this?” to play.',26,TEXT,600)]
    for i,s in enumerate(data['media_flow']):
        x,y=(64,102+i*124) if mobile else (28+i*242,108)
        cw,ch=(508,108) if mobile else (220,154)
        if i<3:
            path=f'M42 {y+54}V{y+178}' if mobile else f'M{x+220} {y+77}H{x+242}'
            p += [f'<path class="packet" d="{path}" stroke="{COLORS[i]}" stroke-width="3" stroke-dasharray="5 7"/>']
        if mobile:
            p += [f'<circle class="scan" cx="42" cy="{y+54}" r="6" fill="{COLORS[i]}"/>']
        services=s['services']
        lines=[' · '.join(services)] if mobile or len(services)<3 else [' · '.join(services[:2]),' · '.join(services[2:])]
        p += [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="#121A26" stroke="{BORDER}"/>',txt(x+16,y+27,f'0{i+1} / {s["title"].upper()}',15,COLORS[i],600)]
        for j,line in enumerate(lines):
            p += [txt(x+16,y+60+j*26,line,22 if mobile else 18,TEXT,600)]
        p += [txt(x+16,y+91 if mobile else y+130,s['detail'],17 if mobile else 13,MUTED)]
    y=634 if mobile else 305
    for i,(label,key) in enumerate([('LIBRARIES','libraries'),('OPERATIONS','operations'),('MONITORING','monitoring')]):
        text=' · '.join(data[key])
        p += [txt(28,y+i*(56 if mobile else 31),label,13,COLORS[i],600),txt(28 if mobile else 154,y+(24 if mobile else 0)+i*(56 if mobile else 31),text,17 if mobile else 16,MUTED)]
    p += [txt(28,h-22,'Illustrated handoffs / Curated service list / No live telemetry',14 if mobile else 12,MUTED),'</g></svg>\n']
    return '\n'.join(p)


def releases():
    result=[]
    for repo,name,_,color in PROJECTS:
        if github_json(repo).get('private') is not False:
            raise ValueError('Public repositories only')
        items=github_json(repo,'/releases?per_page=10')
        selected=[r for r in items if not r['draft'] and not r['prerelease']][:2]
        for r in selected:
            result.append({'repo':repo,'name':name,'color':color,'tag':r['tag_name'],'published_at':r['published_at'],'url':f'https://github.com/{OWNER}/{repo}/releases/tag/'+quote(r['tag_name'],safe='')})
    return result


def patches(data,mobile=False):
    cols=1 if mobile else 3
    rows=max(1,(len(data)+cols-1)//cols)
    w,h=(600,104+rows*184) if mobile else (1000,110+rows*218)
    p=surface(w,h,'Release mission patches','A patch for each of up to two recent stable releases per selected public project. Versions and dates are real published release metadata.')
    p += [txt(28,34,'MISSION PATCHES / PUBLIC RELEASES',14,COLORS[1],600),txt(28,73,'Small releases. Permanent souvenirs.',26,TEXT,600)]
    if not data:
        p += [txt(28,130,'No stable public releases found.',22,MUTED)]
    for i,r in enumerate(data):
        x,y=(28,96+i*184) if mobile else (28+(i%3)*324,96+(i//3)*218)
        if not mobile:
            row_count=min(3,len(data)-(i//3)*3)
            x=(1000-(row_count*296+(row_count-1)*28))//2+(i%3)*324
        cw,ch=(544,168) if mobile else (296,198)
        if r.get('repo')=='IOC-Inspector':
            emblem='<path d="M-16-20H4L14-10V8M4-20V-10H14M-16-20V18H-5M-8-2H2"/><rect x="0" y="2" width="16" height="16"/><path d="M16 18L22 24"/>'
        elif r.get('repo')=='website-downloader':
            emblem='<path d="M-4-21H4V-3H14L0 11L-14-3H-4Z"/><path d="M-19 16V23H19V16"/>'
        else:
            emblem='<path d="M-14-12L12-5L3 17Z" stroke-opacity=".5"/><g fill="'+r['color']+'" stroke="none"><rect x="-19" y="-17" width="10" height="10"/><rect x="7" y="-10" width="10" height="10"/><rect x="-2" y="12" width="10" height="10"/></g>'
        p += [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="#121A26" stroke="{BORDER}"/>',f'<g transform="translate({x+58} {y+62})" fill="none" stroke="{r["color"]}" stroke-width="2"><path d="M0-35L30-17V17L0 35L-30 17V-17Z"/>'+emblem+'<circle r="44" stroke-opacity=".2" stroke-dasharray="3 6"/></g>',txt(x+(122 if mobile else 118),y+47,r['name'],22 if mobile else 17,TEXT,600),txt(x+(122 if mobile else 118),y+78,r['tag'][:18],25 if mobile else 20,r['color'],650),txt(x+22,y+(132 if mobile else 145),'RELEASED / '+r['published_at'][:10],15 if mobile else 13,MUTED),txt(x+22,y+ch-17,'PUBLIC RELEASE / MISSION COMPLETE',12,r['color'],500)]
    p += ['</g></svg>\n']
    return '\n'.join(p)


def resolve_tag(repo,tag):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._+-]{0,79}',tag):
        raise ValueError('Unsupported demo release tag')
    obj=github_json(repo,'/git/ref/tags/'+quote(tag,safe=''))['object']
    for _ in range(5):
        if obj['type']=='commit' and re.fullmatch('[0-9a-f]{40}',obj['sha']):
            return obj['sha']
        if obj['type']!='tag': break
        obj=github_json(repo,'/git/tags/'+obj['sha'])['object']
    raise ValueError('Could not resolve a release to an immutable commit')


def demo_plan(release_data,now):
    sources={}
    for name,repo in DEMO_REPOS.items():
        release=next(r for r in release_data if r['repo']==repo)
        sources[name]={'repo':repo,'tag':release['tag'],'sha':resolve_tag(repo,release['tag'])}
    week=now.strftime('%G-W%V')
    recipes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'demos').rglob('*')) if p.is_file()}
    recipes['scripts/profile_demos.py']=hashlib.sha256((ROOT/'scripts/profile_demos.py').read_bytes()).hexdigest()
    signature={'week':week,'sources':sources,'recipes':recipes}
    fingerprint=hashlib.sha256(json.dumps(signature,sort_keys=True).encode()).hexdigest()
    return {**signature,'fingerprint':fingerprint}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan-only',action='store_true')
    args=parser.parse_args()
    now=datetime.now(timezone.utc).replace(microsecond=0)
    release_data=releases()
    plan=demo_plan(release_data,now)
    (ROOT/'.demo-plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    previous=json.loads((OUT/'demo-provenance.json').read_text()) if (OUT/'demo-provenance.json').exists() else {}
    required=['inspector-demo.gif','inspector-demo.webp','downloader-demo.gif','downloader-demo.webp','case-file.svg','case-file-mobile.svg','case-findings.svg','case-report.json','case-report.md']
    needs=previous.get('fingerprint')!=plan['fingerprint'] or any(not (OUT/f).is_file() for f in required)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a',encoding='utf-8') as f:
            f.write('needs_demos='+str(needs).lower()+'\n')
    if args.plan_only: return
    intel=intel_snapshot(public_json('diagnostics/run.json'),public_json('diagnostics/collection-attempt.json'),now)
    lab=validate_lab(json.loads((OUT/'lab-services.json').read_text()))
    # Validate every input before changing artwork; failures preserve the last good files.
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        write('intel-conveyor'+suffix+'.svg',conveyor(intel,mobile))
        write('homelab-flow'+suffix+'.svg',lab_flow(lab,mobile))
        write('release-patches'+suffix+'.svg',patches(release_data,mobile))
    write('intel-conveyor.json',intel)
    write('intel-conveyor.md',f'# SwiftIOC intelligence conveyor\n\nCollection: {intel["collection_at"]}. Observed: {intel["observed_at"]}.\n\n'+f'- Retained observables: {intel["observables"]:,}\n- Retained CVEs: {intel["vulnerabilities"]:,}\n- Duplicates removed in collection: {intel["duplicates_removed"]:,}\n- Last interval: {intel["delta"]}\n- Latest collection attempt: {intel["latest_attempt"]} at {intel["attempt_at"]}\n\n'+intel['scope']+' Removed means absent from the retained feed, not benign. Counts do not establish compromise. The conveyor is an illustration.\n\n'+f'[Published diagnostics]({intel["source"]}) · [Latest attempt]({SWIFT}diagnostics/collection-attempt.json)\n')
    write('release-patches.json',{'observed_at':now.isoformat(),'releases':release_data})
    write('release-patches.md','# Release mission patches\n\nUp to two recent stable releases per selected public project.\n\n'+'\n'.join(f'- [{r["name"]} {r["tag"]}]({r["url"]}) — published {r["published_at"][:10]}' for r in release_data)+'\n')
    print(f'Public artwork refreshed; demo refresh required: {needs}')


if __name__=='__main__': main()
