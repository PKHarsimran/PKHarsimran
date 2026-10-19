"""Run released CLIs on owned fixtures; record verified output and provenance."""
from __future__ import annotations
from profile_theme import apply_theme
from demo_terminal import Terminal

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
    if name.endswith('.svg'): content=apply_theme(content)
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


def inspector(record=False, compact=False):
    case=json.loads((WORK/'case.json').read_text())
    source=plan()['sources']['inspector']
    command=[python_for('inspector'),'main.py','--file',WORK/case['file'],'--report','--json']
    terminal=Terminal(record,compact)
    terminal.page('IOC Inspector',source['tag'],'01 / FOLLOW THE CLUES')
    terminal.line('One PDF. What is hiding inside?')
    terminal.line('Owned fixture / static analysis','muted')
    terminal.line()
    terminal.pause(1)
    terminal.command(['$ python main.py \\',f'  --file ../{case["file"]} \\','  --report --json'])
    # Use precisely the relative file argument shown in the recording.
    command[3]=Path('..')/case['file']
    for extension in ('json','md'):
        (WORK/'inspector/reports'/(Path(case['file']).stem+'_report.'+extension)).unlink(missing_ok=True)
    terminal.perform(lambda:run(command,cwd=WORK/'inspector',capture_output=True,text=True,encoding='utf-8',timeout=90),'Reading the PDF')
    raw=json.loads((WORK/'inspector/reports'/(Path(case['file']).stem+'_report.json')).read_text())
    expected=set(case['urls'])|({case['hidden']} if case['hidden'] else set())
    if set(raw['urls'])!=expected or raw.get('url_rep') or raw.get('ip_rep') or raw['embedded_files']!=0 or raw['js_count']!=0:
        raise ValueError('The released parser did not produce the expected static findings')
    ips={urlsplit(u).hostname for u in expected if re.fullmatch(r'\d+\.\d+\.\d+\.\d+',urlsplit(u).hostname or '')}
    if set(raw['ips'])!=ips: raise ValueError('Extracted IPs did not match fixture')
    markdown=WORK/'inspector/reports'/(Path(case['file']).stem+'_report.md')
    if not markdown.is_file() or not markdown.stat().st_size:
        raise ValueError('The released CLI did not write its Markdown report')
    record={'week':plan()['week'],'title':case['title'],'prompt':case['prompt'],'fixture':case['file'],'fixture_sha256':hashlib.sha256((WORK/case['file']).read_bytes()).hexdigest(),'source':source,'findings':raw,'scope':'Owned harmless training PDF. Static analysis; external reputation lookups disabled. The tool verdict is not a security guarantee.'}
    save('case-report.json',record)
    ip_label='IP' if len(raw['ips'])==1 else 'IPs'
    terminal.pause(.6)
    terminal.page('IOC Inspector',source['tag'],'02 / READ THE FINDINGS')
    terminal.line(f'{len(raw["urls"])} UNIQUE URLs / {len(raw["ips"])} {ip_label}', 'mint',True)
    terminal.line()
    for url in sorted(raw['urls']):
        terminal.line(url.replace('http','hxxp').replace('.','[.]'))
        terminal.line()
        terminal.pause(.6)
    terminal.line('Links defanged for display.','muted')
    terminal.line('Read from the actual JSON report.','muted')
    terminal.pause(4)
    terminal.page('IOC Inspector',source['tag'],'03 / CLOSE THE CASE')
    terminal.line(f'[ok] {len(raw["urls"])} URLs / {len(raw["ips"])} {ip_label} verified','mint')
    terminal.line('[ok] 0 embedded / 0 JavaScript','mint')
    terminal.line('[ok] JSON + Markdown written','mint')
    terminal.line()
    terminal.line(f'Tool verdict: {raw["verdict"]}','violet',True)
    terminal.line(f'Heuristic score: {raw["score"]}','muted')
    terminal.line()
    terminal.line('Owned PDF. Reputation keys off.','muted')
    terminal.line('A verdict is not a guarantee.','muted')
    terminal.end('CASE VERIFIED')


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


def downloader(record=False, compact=False):
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
    url=f'http://127.0.0.1:{server.server_port}'
    command=[python_for('downloader'),'-m','website_downloader','--url',url,'--destination',target,'--max-pages','3','--respect-robots']
    source=plan()['sources']['downloader']
    terminal=Terminal(record,compact)
    terminal.page('Website Downloader',source['tag'],'01 / PACK A PIECE OF THE WEB')
    terminal.line('Three pages. Take them offline.')
    terminal.line('Owned localhost fixture','muted')
    terminal.line()
    terminal.pause(1)
    terminal.command(['$ python -m website_downloader \\','  --url \\',f'  {url} \\',f'  --destination mirror/{os.getpid()} \\','  --max-pages 3 --respect-robots'])
    command[6]=Path('mirror')/str(os.getpid())
    try:
        terminal.perform(lambda:run(command,cwd=WORK,capture_output=True,text=True,encoding='utf-8',timeout=90),'Saving the site')
    finally:
        server.shutdown(); server.server_close()
    # Source is stopped before checking that every HTML dependency resolves locally.
    terminal.page('Website Downloader',source['tag'],'02 / PULL THE PLUG')
    terminal.line('SOURCE SERVER: OFF','violet',True)
    terminal.line()
    terminal.line('The mirror has to stand alone.')
    terminal.line('No source server to fall back on.','muted')
    terminal.line()
    terminal.line('index.html / guide.html','mint')
    terminal.line('about.html / CSS / SVG','mint')
    terminal.pause(3)
    checked=verify_mirror(target)
    save('downloader-demo.json',{'source':source,'html_pages':3,'assets':['CSS','SVG'],'local_references_checked':checked,'source_server_stopped_before_validation':True,'scope':'Released CLI run against an owned localhost fixture, not a crawl of an external website.'})
    terminal.page('Website Downloader',source['tag'],'03 / THE OFFLINE PROOF')
    terminal.line('[ok] 3 HTML pages saved','mint')
    terminal.line('[ok] CSS + SVG stored locally','mint')
    terminal.line(f'[ok] {checked} local references resolve','mint')
    terminal.line()
    terminal.line('SOURCE SERVER: STILL OFF','violet',True)
    terminal.line('Every link stays in the mirror.','muted')
    terminal.line()
    terminal.line('A little web, ready to travel.','muted')
    terminal.end('OFFLINE MIRROR VERIFIED')


def case_art(record,mobile=False,findings=False):
    w,h=(600,370) if mobile else (1000,270)
    if findings: w,h=600,400
    p=surface(w,h,'IOC Inspector / '+record['week'],record['scope'])
    p += ['<style>.scan{animation:scan 4s ease-in-out infinite}.scan-line{animation:sweep 4s ease-in-out infinite}@keyframes scan{50%{opacity:.25}}@keyframes sweep{0%,100%{transform:translateY(-24px)}50%{transform:translateY(24px)}}@media(prefers-reduced-motion:reduce){.scan,.scan-line{animation:none}}</style>',txt(28,34,'IOC INSPECTOR / '+record['week'],15,'#A995FF',600)]
    if findings:
        raw=record['findings']
        ip_label='IP' if len(raw['ips'])==1 else 'IPs'
        p += [txt(28,80,f'{len(raw["urls"])} unique URLs / {len(raw["ips"])} {ip_label}',26,TEXT,600)]
        for i,url in enumerate(raw['urls']):
            p += [txt(28,121+i*32,url.replace('http','hxxp').replace('.','[.]'),18,'#43E6C5')]
        p += [txt(28,253,f'Actual tool output: {raw["verdict"]} / score {raw["score"]}',20,'#A995FF',600),txt(28,290,'0 embedded files / 0 JavaScript objects',18,MUTED),txt(28,335,'Static result on a known harmless fixture.',18,MUTED),txt(28,368,'A heuristic verdict is not a security guarantee.',16,MUTED)]
    else:
        p += [txt(28,83,'A small document. A few clues.',28,TEXT,600),txt(28,126,record['title'],21,MUTED),txt(28,170 if not mobile else 176,record['prompt'],20,'#43E6C5'),txt(28,h-30,'EXPAND “REVEAL THE FINDINGS” BELOW',14,'#A995FF',600),f'<path class="scan" d="M28 {h-76}H{w-28}" stroke="#A995FF" stroke-width="2" stroke-dasharray="8 10"/>']
        x,y=(300,262) if mobile else (867,128)
        p += [f'<g transform="translate({x} {y})" fill="#121A26" stroke="#A995FF" stroke-width="2"><path d="M-32-43H12L32-23V43H-32Z"/><path d="M12-43V-23H32M-19-8H17M-19 5H8M-19 18H13" fill="none" stroke-opacity=".5"/><path class="scan-line" d="M-39 0H39" stroke="#43E6C5" stroke-width="3"/><circle cx="26" cy="27" r="15" fill="#121A26" stroke="#43E6C5"/><path d="M37 38L49 50" stroke="#43E6C5"/></g>']
    return '\n'.join(p+['</g></svg>\n'])


def finish():
    from PIL import Image
    reels={}
    for name in ('inspector','inspector-mobile','downloader','downloader-mobile'):
        stem=name.replace('-mobile','-demo-mobile') if name.endswith('-mobile') else name+'-demo'
        gif=OUT/(stem+'.gif')
        with Image.open(gif) as img:
            duration=sum(frame.info.get('duration',0) for frame in __import__('PIL.ImageSequence',fromlist=['Iterator']).Iterator(img))
            expected_size=(600,740) if name.endswith('-mobile') else (900,700)
            if img.n_frames<2 or img.size!=expected_size or gif.stat().st_size>4_000_000 or not 1_000<duration<60_000:
                raise ValueError('Invalid or oversized demo reel')
            img.seek(max(0,img.n_frames-2))
            img.convert('RGB').save(OUT/(stem+'.webp'),'WEBP',lossless=True,method=6)
            reels[name]={'sha256':hashlib.sha256(gif.read_bytes()).hexdigest(),'width':img.width,'height':img.height,'duration_ms':duration,'bytes':gif.stat().st_size}
    record=json.loads((OUT/'case-report.json').read_text())
    save('case-file.svg',case_art(record))
    save('case-file-mobile.svg',case_art(record,True))
    save('case-findings.svg',case_art(record,findings=True))
    raw=record['findings']
    md=f'# IOC Inspector case file / {record["week"]}\n\n{record["title"]}\n\n{record["scope"]}\n\n'
    md+=f'Released source: [{record["source"]["tag"]}](https://github.com/PKHarsimran/IOC-Inspector/tree/{record["source"]["sha"]}). Fixture SHA-256: `{record["fixture_sha256"]}`.\n\n'
    ip_label='IP' if len(raw['ips'])==1 else 'IPs'
    md+=f'Actual tool verdict: **{raw["verdict"]}**, score **{raw["score"]}**. {len(raw["urls"])} unique URLs and {len(raw["ips"])} {ip_label}.\n\n'
    md+='\n'.join('- `'+u.replace('http','hxxp').replace('.','[.]')+'`' for u in raw['urls'])+'\n\n[Raw findings](./case-report.json) · [Reproducible fixture recipe](../demos/cases.json)\n'
    save('case-report.md',md)
    save('demo-provenance.json',{**plan(),'recorded_at':datetime.now(timezone.utc).isoformat(),'method':'VHS records guided terminal presentations of actual released CLI executions. Commands use the isolated venv Python; results come from verified generated files, not canned product output.','reels':reels})
    print('Demo reels, static posters, case findings, and source provenance verified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','fixture','inspector','downloader','finish'])
    parser.add_argument('--record',action='store_true',help='Animate the guided terminal presentation when attached to a TTY')
    parser.add_argument('--compact',action='store_true',help='Use the 32-column mobile layout')
    args=parser.parse_args()
    try:
        if args.command in ('inspector','downloader'):
            globals()[args.command](args.record,args.compact)
        else:
            globals()[args.command]()
    finally:
        if args.record and sys.stdout.isatty():
            print('\x1b[?25h',end='',flush=True)
