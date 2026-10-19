"""Optional font preparation; daily generators use only the committed WOFF2 files.

Requires fonttools and brotli. Downloads OFL sources from a pinned Google Fonts commit.
"""
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
import hashlib
import json

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'fonts'
REV='47d54ca1ebb14fd864695f1d39dc734f39017c33'
BASE=f'https://raw.githubusercontent.com/google/fonts/{REV}/ofl/'


def prepare(url,name,characters,weight=None):
    raw=urlopen(url,timeout=30).read()
    font=TTFont(BytesIO(raw))
    if weight is not None: font=instantiateVariableFont(font,{'wght':weight},inplace=True)
    options=subset.Options()
    options.flavor='woff2'
    options.recalc_timestamp=False
    worker=subset.Subsetter(options=options)
    worker.populate(text=characters)
    worker.subset(font)
    # Subsetting modifies the fonts; use our own family names, including for the
    # source with a Reserved Font Name. Keep copyright and license records intact.
    family='ProfileMono' if name.startswith('ibm-') else ('ProfileButton' if 'buttons' in name else 'ProfileDisplay')
    for name_id,value in {1:family,2:'Regular',3:family+'-Subset',4:family,6:family,16:family,17:'Regular'}.items():
        font['name'].setName(value,name_id,3,1,0x409)
        font['name'].setName(value,name_id,1,0,0)
    font.recalcTimestamp=False
    font.flavor='woff2'
    font.save(OUT/name)
    return {'family':family,'source':url,'source_sha256':hashlib.sha256(raw).hexdigest(),'subset_sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()}


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    chars=''.join(chr(c) for c in range(32,127))+'·—–“”‘’→↗↑…'
    sources={}
    sources['space-grotesk-700.woff2']=prepare(BASE+'spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf','space-grotesk-700.woff2',chars,700)
    sources['space-grotesk-buttons-600.woff2']=prepare(BASE+'spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf','space-grotesk-buttons-600.woff2',chars,600)
    sources['ibm-plex-mono-500.woff2']=prepare(BASE+'ibmplexmono/IBMPlexMono-Medium.ttf','ibm-plex-mono-500.woff2',chars)
    for folder,name in [('spacegrotesk','SpaceGrotesk-OFL.txt'),('ibmplexmono','IBMPlexMono-OFL.txt')]:
        (OUT/name).write_bytes(urlopen(BASE+folder+'/OFL.txt',timeout=30).read())
    (OUT/'sources.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8')
    print({p.name:p.stat().st_size for p in OUT.glob('*.woff2')})
