"""Build the profile's local typing strip and responsive toolkit panels."""
from html import escape
from pathlib import Path

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
    width, height = (600, 606) if mobile else (1000, 348)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
         '<title id="title">Operator toolkit</title><desc id="desc">Code: Python, Bash, C++. Security: Splunk, Cortex XDR, Kibana, F5 BIG-IP. Infrastructure: Docker, Ansible, Raspberry Pi. Observability: Grafana, InfluxDB, MQTT.</desc>',
         '<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs>',
         f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="22" fill="url(#surface)" stroke="{BORDER}"/>',
         text(28, 34, "OPERATOR TOOLKIT / EQUIPPED TO BUILD", 13, "#43E6C5", 'font-weight="600" letter-spacing="1.3"')]
    for i, (number, label, color, tools) in enumerate(TOOLS):
        y = 70 + i * (130 if mobile else 67)
        p += [text(28, y+17, number, 13, color, 'font-family="monospace"'),
              text(64, y+17, label, 21 if mobile else 18, TEXT, 'font-weight="600"')]
        x, chip_y = (28, y+36) if mobile else (370, y-6)
        for tool in tools:
            chip_width = round(len(tool) * (10.8 if mobile else 10) + 34)
            p += [f'<rect x="{x}" y="{chip_y}" width="{chip_width}" height="37" rx="9" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".3"/>',
                  text(x+17, chip_y+25, tool, 20 if mobile else 18, color, 'font-weight="500"')]
            x += chip_width + 10
        if i < 3:
            p += [f'<path d="M28 {y+(104 if mobile else 47)}H{width-28}" stroke="{BORDER}" stroke-opacity=".6"/>']
    p += [text(28, height-24, "FAVOURITE SHORTCUT: AUTOMATE THE BORING BITS.", 12, MUTED, 'letter-spacing="1"'), '</g></svg>\n']
    return '\n'.join(p)


def typing():
    phrases = ("Follow the evidence.", "Automate the boring bits.", "Always one more thing to build.")
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="780" height="44" viewBox="0 0 780 44" role="img" aria-labelledby="title desc">',
         '<title id="title">Follow the evidence. Automate the boring bits. Always one more thing to build.</title>',
         '<desc id="desc">Three rotating terminal lines. Reduced motion shows the first line.</desc>',
         '<defs><clipPath id="reveal"><rect class="reveal" x="130" y="0" width="520" height="44"/></clipPath></defs>',
         '<style>.line{opacity:0;animation:line 15s linear infinite}.second{animation-delay:5s}.third{animation-delay:10s}.reveal{animation:type 5s steps(31,end) infinite}.cursor{animation:blink 1s steps(2,end) infinite}@keyframes line{0%,32%{opacity:1}33.333%,100%{opacity:0}}@keyframes type{0%{width:0}55%,88%{width:520px}100%{width:0}}@keyframes blink{50%{opacity:0}}@media(prefers-reduced-motion:reduce){.line,.reveal,.cursor{animation:none}.first{opacity:1}.reveal{width:520px}.cursor{display:none}}</style>',
         '<g fill="#43E6C5" font-family="Consolas,monospace" font-size="22">',
         text(106, 29, ">", 22, "#A995FF"), '<g clip-path="url(#reveal)">']
    for cls, phrase in zip(("first", "second", "third"), phrases):
        p += [text(132, 29, phrase, 22, "#43E6C5", f'class="line {cls}"')]
    p += ['</g><path class="cursor" d="M660 12V32" stroke="#A995FF" stroke-width="2"/></g></svg>\n']
    return '\n'.join(p)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, content in {"mission-typing.svg": typing(), "mission-toolkit.svg": toolkit(), "mission-toolkit-mobile.svg": toolkit(True)}.items():
        (OUT / name).write_text(content, encoding="utf-8")
