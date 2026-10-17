"""Run released CLIs on owned fixtures; record verified output and provenance."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from functools import partial
import hashlib
from html import escape
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from threading import Thread
from urllib.parse import unquote, urlsplit
import venv

from generate_profile_lab import surface, txt, TEXT, MUTED, BORDER

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'profile'
WORK=ROOT/'.demo-work'


def python_for(name):
    return WORK/(name+'-env')/('Scripts/python.exe' if os.name=='nt' else 'bin/python')


def clean_env():
    env=os.environ.copy()
    for name in ('GH_TOKEN','GITHUB_TOKEN','VT_API_KEY','ABUSEIPDB_API_KEY'):
        env[name]=''
    env.update(PYTHONUTF8='1',NO_COLOR='1',PYTHONIOENCODING='utf-8')
    return env


def run(args,**kwargs):
    return subprocess.run([str(a) for a in args],check=True,env=clean_env(),**kwargs)


def save(name,data):
    target=OUT/name
    content=json.dumps(data,indent=2,ensure_ascii=False)+'\n' if not isinstance(data,str) else data
    target.write_text(content,encoding='utf-8')


def plan():
    return json.loads((ROOT/'.demo-plan.json').read_text())


def prepare():
    WORK.mkdir(exist_ok=True)
    for name,source in plan()['sources'].items():
        if name not in ('inspector','downloader') or source['repo'] not in ('IOC-Inspector','website-downloader') or not re.fullmatch('[0-9a-f]{40}',source['sha']):
            raise ValueError('Invalid public demo source')
        directory=WORK/name
        run(['git','init',directory])
        run(['git','-C',directory,'remote','add','origin','https://github.com/PKHarsimran/'+source['repo']+'.git'])
        run(['git','-C',directory,'fetch','--depth','1','origin',source['sha']])
        run(['git','-C',directory,'checkout','--detach','FETCH_HEAD'])
        actual=subprocess.check_output(['git','-C',str(directory),'rev-parse','HEAD'],text=True).strip()
        if actual!=source['sha']: raise ValueError('Source checkout did not match the release commit')
        venv.EnvBuilder(with_pip=True).create(WORK/(name+'-env'))
        if name=='inspector':
            run([python_for(name),'-m','pip','install','-r',directory/'requirements.txt','Pillow==11.3.0'])
        else:
            run([python_for(name),'-m','pip','install',directory])
    # Use the parser's installed PDF library to make inert, owned fixtures.
    run([python_for('inspector'),__file__,'fixture'])


def fixture():
    import fitz
    cases=json.loads((ROOT/'demos/cases.json').read_text())
    index=int(plan()['week'].split('W')[1])%len(cases)
    case=cases[index]
    path=WORK/(case['slug']+'.pdf')
    document=fitz.open()
    page=document.new_page()
    lines=['IOC INSPECTOR / OWNED TRAINING FIXTURE',case['title'],'No macros. No scripts. No real incident data.','',*case['urls'],'','Support details (an ordinary hyperlink)']
    page.insert_text((42,52),'\n'.join(lines),fontsize=12)
    if case['hidden']:
        page.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(42,180,350,204),'uri':case['hidden']})
    document.set_metadata({'title':case['title'],'author':'Public profile demo'})
    document.save(path)
    document.close()
    (WORK/'case.json').write_text(json.dumps({**case,'file':path.name}),encoding='utf-8')


def inspector():
    case=json.loads((WORK/'case.json').read_text())
    source=plan()['sources']['inspector']
    command=[python_for('inspector'),'main.py','--file',WORK/case['file'],'--report','--json']
    print(f'IOC Inspector {source["tag"]} / {plan()["week"]}',flush=True)
    print('Owned PDF / static analysis / reputation keys absent',flush=True)
    print(f'$ python main.py --file {case["file"]} --report --json',flush=True)
    result=run(command,cwd=WORK/'inspector',capture_output=True,text=True,encoding='utf-8',timeout=90)
    raw=json.loads((WORK/'inspector/reports'/(Path(case['file']).stem+'_report.json')).read_text())
    expected=set(case['urls'])|({case['hidden']} if case['hidden'] else set())
    if set(raw['urls'])!=expected or raw.get('url_rep') or raw.get('ip_rep') or raw['embedded_files']!=0 or raw['js_count']!=0:
        raise ValueError('The released parser did not produce the expected static findings')
    ips={urlsplit(u).hostname for u in expected if re.fullmatch(r'\d+\.\d+\.\d+\.\d+',urlsplit(u).hostname or '')}
    if set(raw['ips'])!=ips: raise ValueError('Extracted IPs did not match fixture')
    record={'week':plan()['week'],'title':case['title'],'prompt':case['prompt'],'fixture':case['file'],'fixture_sha256':hashlib.sha256((WORK/case['file']).read_bytes()).hexdigest(),'source':source,'findings':raw,'scope':'Owned harmless training PDF. Static analysis; external reputation lookups disabled. The tool verdict is not a security guarantee.'}
    save('case-report.json',record)
    print(f'Extracted: {len(raw["urls"])} unique URLs / {len(raw["ips"])} IPs',flush=True)
    for url in raw['urls']: print('  '+url.replace('http','hxxp').replace('.','[.]'),flush=True)
    print(f'Actual heuristic output: score={raw["score"]} / verdict={raw["verdict"]}',flush=True)
    print('JSON + Markdown reports generated. CASE VERIFIED',flush=True)


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src') and value: self.refs.append(value)


def verify_mirror(directory):
    htmls=list(directory.rglob('*.html'))
    if len(htmls)!=3 or not list(directory.rglob('*.css')) or not list(directory.rglob('*.svg')):
        raise ValueError('Incomplete offline mirror')
    checked=0
    for path in htmls:
        parser=Links(); parser.feed(path.read_text(encoding='utf-8'))
        for ref in parser.refs:
            parts=urlsplit(ref)
            if parts.scheme or parts.netloc or parts.path.startswith('/'):
                raise ValueError('A mirrored fixture link still needs the source server')
            target=(path.parent/unquote(parts.path)).resolve()
            if not target.is_relative_to(directory.resolve()) or not target.is_file():
                raise ValueError('Broken or escaping offline link')
            checked+=1
    return checked


def downloader():
    site=WORK/'site'; site.mkdir(exist_ok=True)
    (site/'style.css').write_text('body{background:#0d1117;color:#43e6c5;font:22px sans-serif}main{margin:48px}a{color:#a995ff}',encoding='utf-8')
    (site/'mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect width="64" height="64" rx="12" fill="#43e6c5"/></svg>')
    for name,title in [('index.html','A little piece of the web.'),('guide.html','The field guide.'),('about.html','Built for this demo.')]:
        (site/name).write_text(f'<!doctype html><html><meta charset="utf-8"><title>{title}</title><link rel="stylesheet" href="style.css"><main><img src="mark.svg" alt="Fixture mark"><h1>{title}</h1><p>Owned local fixture. Three pages, CSS, SVG.</p><a href="index.html">Home</a> <a href="guide.html">Guide</a> <a href="about.html">About</a></main></html>',encoding='utf-8')
    (site/'robots.txt').write_text('User-agent: *\nAllow: /\n')
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(site)))
    Thread(target=server.serve_forever,daemon=True).start()
    target=WORK/'mirror'
    # Every invocation uses a fresh destination; the tape never displays cached results.
    target=target/str(os.getpid())
    command=[python_for('downloader'),'-m','website_downloader','--url',f'http://127.0.0.1:{server.server_port}/index.html','--destination',target,'--max-pages','3','--respect-robots']
    source=plan()['sources']['downloader']
    print('Website Downloader '+source['tag']+' / owned local fixture',flush=True)
    print('$ website-downloader --url <local fixture> --destination mirror --max-pages 3 --respect-robots',flush=True)
    try:
        result=run(command,cwd=WORK/'downloader',capture_output=True,text=True,encoding='utf-8',timeout=90)
    finally:
        server.shutdown(); server.server_close()
    # Source is stopped before checking that every HTML dependency resolves locally.
    checked=verify_mirror(target)
    print('Downloaded: index.html / guide.html / about.html',flush=True)
    print('Assets: stylesheet + SVG / source server stopped',flush=True)
    print(f'Checked {checked} local references: all resolve inside the mirror',flush=True)
    print('OFFLINE MIRROR VERIFIED',flush=True)
    save('downloader-demo.json',{'source':source,'html_pages':3,'assets':['CSS','SVG'],'local_references_checked':checked,'source_server_stopped_before_validation':True,'scope':'Released CLI run against an owned localhost fixture, not a crawl of an external website.'})


def case_art(record,mobile=False,findings=False):
    w,h=(600,370) if mobile else (1000,270)
    if findings: w,h=600,400
    p=surface(w,h,'IOC Inspector / '+record['week'],record['scope'])
    p += ['<style>.scan{animation:scan 4s ease-in-out infinite}@keyframes scan{50%{opacity:.25}}@media(prefers-reduced-motion:reduce){.scan{animation:none}}</style>',txt(28,34,'IOC INSPECTOR / '+record['week'],15,'#A995FF',600)]
    if findings:
        raw=record['findings']
        p += [txt(28,80,f'{len(raw["urls"])} unique URLs / {len(raw["ips"])} IPs',26,TEXT,600)]
        for i,url in enumerate(raw['urls']):
            p += [txt(28,121+i*32,url.replace('http','hxxp').replace('.','[.]'),18,'#43E6C5')]
        p += [txt(28,253,f'Actual tool output: {raw["verdict"]} / score {raw["score"]}',20,'#A995FF',600),txt(28,290,'0 embedded files / 0 JavaScript objects',18,MUTED),txt(28,335,'Static result on a known harmless fixture.',18,MUTED),txt(28,368,'A heuristic verdict is not a security guarantee.',16,MUTED)]
    else:
        p += [txt(28,83,'A small document. A few clues.',28,TEXT,600),txt(28,126,record['title'],21,MUTED),txt(28,170 if not mobile else 176,record['prompt'],20,'#43E6C5'),txt(28,h-30,'EXPAND “REVEAL THE FINDINGS” BELOW',14,'#A995FF',600),f'<path class="scan" d="M28 {h-76}H{w-28}" stroke="#A995FF" stroke-width="2" stroke-dasharray="8 10"/>']
    return '\n'.join(p+['</g></svg>\n'])


def finish():
    from PIL import Image
    for name in ('inspector','downloader'):
        gif=OUT/(name+'-demo.gif')
        with Image.open(gif) as img:
            duration=sum(frame.info.get('duration',0) for frame in __import__('PIL.ImageSequence',fromlist=['Iterator']).Iterator(img))
            if img.n_frames<2 or gif.stat().st_size>4_000_000 or not 1_000<duration<60_000:
                raise ValueError('Invalid or oversized demo reel')
            img.seek(max(0,img.n_frames-2))
            img.convert('RGB').save(OUT/(name+'-demo.webp'),'WEBP',lossless=True,method=6)
    record=json.loads((OUT/'case-report.json').read_text())
    save('case-file.svg',case_art(record))
    save('case-file-mobile.svg',case_art(record,True))
    save('case-findings.svg',case_art(record,findings=True))
    raw=record['findings']
    md=f'# IOC Inspector case file / {record["week"]}\n\n{record["title"]}\n\n{record["scope"]}\n\n'
    md+=f'Released source: [{record["source"]["tag"]}](https://github.com/PKHarsimran/IOC-Inspector/tree/{record["source"]["sha"]}). Fixture SHA-256: `{record["fixture_sha256"]}`.\n\n'
    md+=f'Actual tool verdict: **{raw["verdict"]}**, score **{raw["score"]}**. {len(raw["urls"])} unique URLs and {len(raw["ips"])} IPs.\n\n'
    md+='\n'.join('- `'+u.replace('http','hxxp').replace('.','[.]')+'`' for u in raw['urls'])+'\n\n[Raw findings](./case-report.json) · [Reproducible fixture recipe](../demos/cases.json)\n'
    save('case-report.md',md)
    save('demo-provenance.json',{**plan(),'recorded_at':datetime.now(timezone.utc).isoformat(),'method':'VHS recorded executions of released CLIs on owned fixtures; assertions passed.','reels':{name:hashlib.sha256((OUT/(name+'-demo.gif')).read_bytes()).hexdigest() for name in ('inspector','downloader')}})
    print('Demo reels, static posters, case findings, and source provenance verified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','fixture','inspector','downloader','finish'])
    globals()[parser.parse_args().command]()
