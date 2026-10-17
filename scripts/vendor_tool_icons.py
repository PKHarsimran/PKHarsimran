"""Optional preparation: vendor the toolkit's pinned Simple Icons SVGs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'profile/icons'
REV='4d29a35c954699b389a834aacc97dd6e7e74143c'
ICONS={'Python':'python','Bash':'gnubash','C++':'cplusplus','Splunk':'splunk','Cortex XDR':'paloaltonetworks','Kibana':'kibana','F5 BIG-IP':'f5','Docker':'docker','Ansible':'ansible','Raspberry Pi':'raspberrypi','Grafana':'grafana','InfluxDB':'influxdb','MQTT':'mqtt'}


def fetch(item):
    label,slug=item
    url=f'https://raw.githubusercontent.com/simple-icons/simple-icons/{REV}/icons/{slug}.svg'
    raw=urlopen(url,timeout=30).read()
    root=ET.fromstring(raw)
    if root.tag!='{http://www.w3.org/2000/svg}svg' or root.get('viewBox')!='0 0 24 24':
        raise ValueError('Unexpected source icon: '+slug)
    (OUT/(slug+'.svg')).write_bytes(raw)
    return label,{'file':slug+'.svg','source':url,'sha256':hashlib.sha256(raw).hexdigest()}


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool: sources=dict(pool.map(fetch,ICONS.items()))
    license_url=f'https://raw.githubusercontent.com/simple-icons/simple-icons/{REV}/LICENSE.md'
    (OUT/'LICENSE.md').write_bytes(urlopen(license_url,timeout=30).read())
    (OUT/'sources.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8')
    (OUT/'README.md').write_text('# Toolkit icons\n\nLocal SVGs from [Simple Icons](https://github.com/simple-icons/simple-icons), pinned to `'+REV+'`. Source URLs and SHA-256 hashes are in sources.json. The CC0 license is included. Cortex XDR uses its parent Palo Alto Networks brand mark.\n\nThe toolkit generator embeds the paths in each panel and colours them to match the profile. No runtime CDN requests are needed. Refresh deliberately with `python scripts/vendor_tool_icons.py`.\n',encoding='utf-8')
    with (OUT/'README.md').open('a',encoding='utf-8') as f:
        f.write('\nThe small Splunk chip uses an original terminal chevron for legibility in place of its full wordmark.\n')
    print('Vendored',len(sources),'toolkit icons with pinned sources.')
