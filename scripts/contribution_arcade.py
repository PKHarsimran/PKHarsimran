"""One responsive contribution panel, built only from the public calendar snapshot."""
from datetime import date, timedelta
from html import escape

from profile_theme import apply_theme

TEXT, MUTED, BORDER = '#EFF4FC', '#B8C6DB', '#29364B'
MINT, VIOLET, PINK = '#43E6C5', '#A995FF', '#F36BAA'
LEVELS = ('#182331', '#174B45', '#217466', '#2DAA92', MINT)


def text(x, y, value, size=18, color=TEXT, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def calendar_summary(calendar):
    days = calendar['days']
    if not days:
        raise ValueError('A contribution panel needs calendar days')
    previous = None
    for item in days:
        current = date.fromisoformat(item['date'])
        if previous and current - previous != timedelta(days=1):
            raise ValueError('Calendar dates must be consecutive and unique')
        if type(item['level']) is not int or item['level'] not in range(5):
            raise ValueError('Invalid calendar activity level')
        if 'count' in item:
            count = item['count']
            if type(count) is not int or count < 0 or (count == 0) != (item['level'] == 0):
                raise ValueError('Calendar contribution count conflicts with its activity level')
        previous = current
    recent = [d for d in days if date.fromisoformat(d['date']) >= previous - timedelta(days=29)]
    def total(items):
        return sum(d['count'] for d in items) if all('count' in d for d in items) else None
    return {'total': total(days), 'active': sum(d['level'] > 0 for d in days), 'recent': total(recent)}


def mascot(x, y, scale=1):
    return f'''<g transform="translate({x} {y}) scale({scale})" aria-hidden="true">
      <circle r="40" fill="{VIOLET}" fill-opacity=".035" stroke="{VIOLET}" stroke-opacity=".2"/>
      <path d="M-58 12Q0-38 58-12M-58 12Q0 52 58-12" fill="none" stroke="{MINT}" stroke-opacity=".2"/>
      <g class="arcade-bot" shape-rendering="crispEdges">
        <path d="M-4-32H0V-20H20V-10H26V10H18V26H8V16H-8V26H-18V10H-26V-10H-20V-20H-4Z" fill="{VIOLET}"/>
        <path d="M-15-11H15V7H-15Z" fill="#0D1117"/>
        <path class="arcade-eyes" d="M-10-5H-4V1H-10ZM4-5H10V1H4Z" fill="{MINT}"/>
        <path d="M-24-5H-31V-16H-37V2H-24Z" fill="{PINK}"/>
      </g><circle cx="-3" cy="-37" r="3" fill="{PINK}"/>
    </g>'''


def calendar_grid(days, start, first_week, last_week, y, mobile=False):
    """Columns remain weeks; phone panels split the complete calendar in half."""
    step = 18 if mobile else 17
    left, cell = (60, 14) if mobile else (58, 13)
    p = []
    for row, label in ((1, 'M'), (3, 'W'), (5, 'F')):
        p.append(text(left-22, y+row*step+10, label, 11, MUTED))
    groups = [[] for _ in LEVELS]
    points, last_month_x, first_in_grid = [], -100, True
    for item in days:
        day = date.fromisoformat(item['date'])
        week = (day-start).days // 7
        if not first_week <= week <= last_week:
            continue
        x = left+(week-first_week)*step
        cy = y+((day.weekday()+1) % 7)*step
        if (day.day == 1 or first_in_grid) and x-last_month_x >= 28:
            p.append(text(x, y-13, day.strftime('%b'), 12 if mobile else 11, MUTED))
            last_month_x = x
        first_in_grid = False
        count = f"{item['count']:,} contributions; " if 'count' in item else ''
        title = f"{item['date']}: {count}activity level {item['level']} of 4"
        groups[item['level']].append(f'<rect data-date="{item["date"]}" x="{x}" y="{cy}" width="{cell}" height="{cell}" rx="3"><title>{title}</title></rect>')
        if item['level']:
            points.append((x+cell/2, cy+cell/2))
    p.append('<g class="calendar">')
    p += [f'<g fill="{color}">'+''.join(group)+'</g>' for color, group in zip(LEVELS, groups) if group]
    p.append('</g>')
    if points:
        # A few actual active dates guide a decorative courier; the grid never changes.
        n = min(12, len(points))
        selected = [points[round(i*(len(points)-1)/max(1,n-1))] for i in range(n)]
        route = 'M'+'L'.join(f'{x:g} {cy:g}' for x,cy in selected+[selected[0]])
        motion = f'<animateMotion dur="38s" repeatCount="indefinite" path="{route}"/>' if len(selected)>1 else ''
        position = '' if motion else f'transform="translate({selected[0][0]} {selected[0][1]})"'
        p += [f'<g class="arcade-courier" {position} aria-hidden="true"><circle r="10" fill="#121A26" fill-opacity=".65" stroke="{VIOLET}" stroke-opacity=".6"/><path d="M-2-5H2V-2H5V3H2V6H-2V3H-5V-2H-2Z" fill="{PINK}"/><rect x="-1" y="-2" width="2" height="4" fill="{MINT}"/>{motion}</g>']
    return '\n'.join(p)


def render_contributions(calendar, mobile=False):
    summary = calendar_summary(calendar)
    days = calendar['days']
    first, last = (date.fromisoformat(days[i]['date']) for i in (0, -1))
    start = first-timedelta(days=(first.weekday()+1) % 7)
    weeks = (last-start).days//7+1
    if weeks > 54:
        raise ValueError('Calendar exceeds the panel window')
    w,h = (600,790) if mobile else (1000,500)
    period = f'{first:%d %b %Y} — {last:%d %b %Y}'
    total = f"{summary['total']:,}" if summary['total'] is not None else 'unavailable'
    desc = f"{period}. {total} calendar contributions; {summary['active']} days with activity. A decorative courier follows selected active dates. Activity includes automation and any private contribution totals the owner shares publicly. Every calendar date is preserved; reduced motion hides the courier."
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="arcade-title arcade-desc"><title id="arcade-title">Contribution arcade</title><desc id="arcade-desc">{escape(desc)}</desc>',
         '<defs><linearGradient id="arcade-surface" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs>',
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#arcade-surface)" stroke="{BORDER}"/>',
         f'<path d="M25 1H{190 if mobile else 310}" stroke="{MINT}" stroke-opacity=".65"/>',
         '<style>.arcade-bot{animation:arcade-float 7s ease-in-out infinite}.arcade-eyes{transform-box:fill-box;transform-origin:center;animation:arcade-blink 8s linear infinite}@keyframes arcade-float{50%{transform:translateY(-4px)}}@keyframes arcade-blink{0%,62%,66%,100%{transform:scaleY(1)}64%{transform:scaleY(.12)}}@media(prefers-reduced-motion:reduce){.arcade-courier{display:none}.arcade-bot,.arcade-eyes{animation:none}}</style>',
         '<g font-family="Segoe UI,Arial,sans-serif">',
         text(28,34,'CONTRIBUTION ARCADE / DAILY SNAPSHOT',13 if mobile else 12,MINT,600),
         text(28,80,'Side quests leave a trail.',34 if mobile else 38,TEXT,700),
         text(28,111,period,18,MUTED),mascot(548 if mobile else 910,77,.6 if mobile else .9)]
    metrics = [('total', 'CONTRIBUTIONS', 'in this calendar', MINT), ('active', 'ACTIVE DAYS', f'of {len(days)} displayed', VIOLET), ('recent', 'LAST 30 DAYS', 'contributions', PINK)]
    metric_width = 172 if mobile else 298
    gap = 14 if mobile else 24
    for i,(key,label,context,color) in enumerate(metrics):
        x = 28+i*(metric_width+gap)
        value = summary[key]
        p += [f'<rect x="{x}" y="135" width="{metric_width}" height="112" rx="14" fill="#101925" stroke="{BORDER}"/>',
              text(x+17,178,f'{value:,}' if value is not None else '—',36 if mobile else 38,color,700,f'data-metric="{key}"'),
              text(x+17,208,label,16 if mobile else 12,TEXT,600),
              text(x+17,230,context if value is not None else 'count unavailable',16 if mobile else 13,MUTED)]
    if mobile:
        split = (weeks+1)//2
        for i,(a,b,y) in enumerate(((0,split-1,311),(split,weeks-1,526))):
            section_start = max(first,start+timedelta(weeks=a))
            section_end = min(last,start+timedelta(weeks=b+1,days=-1))
            p += [text(28,y-31,f'{section_start:%b %Y} — {section_end:%b %Y}',18,MUTED),
                  calendar_grid(days,start,a,b,y,mobile=True)]
        legend_y, footer_y = 698, 741
    else:
        p += [text(28,279,'THE CALENDAR / ONE COLUMN PER WEEK',12,MUTED),calendar_grid(days,start,0,weeks-1,310)]
        legend_y, footer_y = 452, 481
    p += [text(28,legend_y,'Less',16 if mobile else 12,MUTED)]
    for i,color in enumerate(LEVELS):
        p.append(f'<rect x="{78+i*19}" y="{legend_y-12}" width="13" height="13" rx="3" fill="{color}"/>')
    p += [text(181,legend_y,'More',16 if mobile else 12,MUTED),
          text(w-28,legend_y,'GitHub activity levels',16 if mobile else 12,MUTED,extra='text-anchor="end"'),
          text(28,footer_y,'Calendar activity includes automation.',16 if mobile else 12,MUTED)]
    stamp = calendar['generated_at'][:10]
    p += [text(28 if mobile else w-28,footer_y+27 if mobile else footer_y,'SNAPSHOT / '+stamp,14 if mobile else 12,MUTED,extra='' if mobile else 'text-anchor="end"'),'</g></svg>\n']
    return apply_theme('\n'.join(p))
