"""One responsive contribution panel, built only from the public calendar snapshot."""
from datetime import date, timedelta
from html import escape

from profile_theme import apply_theme
from profile_arcade_scene import side_quest, SCENE_CSS
from profile_mascot import hacker_bender

TEXT, MUTED, BORDER = '#EFF4FC', '#B8C6DB', '#29364B'
MINT, VIOLET, PINK = '#43E6C5', '#A995FF', '#F36BAA'
LEVELS = ('#182331', '#174B45', '#217466', '#2DAA92', MINT)
DAILY_DROPS = (
    'The backlog has a snake now.',
    'Small patches. New possibilities.',
    'Evidence first. Confetti later.',
    'One more side quest? Obviously.',
    'Plot twist: it was DNS.',
    'Read the logs. Befriend the bot.',
    'Containers all the way down.',
)
MOTION = '''
.arcade-bot{animation:arcade-float 7s ease-in-out infinite}
.arcade-eyes{transform-box:fill-box;transform-origin:center;animation:arcade-blink 8s linear infinite}
.arcade-wave{transform-box:fill-box;transform-origin:100% 100%;animation:arcade-wave 12s ease-in-out infinite}
.arcade-jet{animation:arcade-jet 3s ease-in-out infinite;opacity:.6}
.arcade-spark{transform-box:fill-box;transform-origin:center;animation:arcade-spark 8s ease-in-out infinite;opacity:.25}
.arcade-greeting{animation:arcade-greeting 12s ease-in-out infinite;opacity:0}
@keyframes arcade-float{50%{transform:translateY(-4px)}}
@keyframes arcade-blink{0%,62%,66%,100%{transform:scaleY(1)}64%{transform:scaleY(.12)}}
@keyframes arcade-wave{0%,70%,100%{transform:rotate(0)}78%,90%{transform:rotate(-20deg)}84%,96%{transform:rotate(6deg)}}
@keyframes arcade-jet{50%{transform:translateY(3px);opacity:.25}}
@keyframes arcade-spark{0%,65%,100%{opacity:.25;transform:scale(.8)}80%{opacity:.65;transform:scale(1.1)}}
@keyframes arcade-greeting{0%,67%,100%{opacity:0}73%,94%{opacity:1}}
@media(prefers-reduced-motion:reduce){.arcade-orbit,.arcade-jet,.arcade-greeting{display:none}.arcade-bot,.arcade-eyes,.arcade-wave,.arcade-spark{animation:none}}
'''


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
      {hacker_bender(0,8,.52,key='calendar')}
      <g class="arcade-orbit"><circle r="3" fill="{PINK}"/><path d="M-10 0H-5" stroke="{PINK}" stroke-opacity=".4"/><animateMotion dur="24s" repeatCount="indefinite" rotate="auto" path="M-53 12A55 21-20 1 1 53-12A55 21-20 1 1-53 12"/></g>
    </g>'''


def sparkle(x, y, color, delay=0):
    return f'<g transform="translate({x} {y})" aria-hidden="true"><path class="arcade-spark" style="animation-delay:{delay}s" d="M0-5L1.5-1.5L5 0L1.5 1.5L0 5L-1.5 1.5L-5 0L-1.5-1.5Z" fill="{color}"/></g>'


def metric_icon(x, y, kind, color):
    shapes = {
        'total': '<path d="M0-10V10M-8-5V1Q-8 5 0 5M0-2Q8-2 8-7"/><circle cy="-10" r="2.5"/><circle cx="-8" cy="-7" r="2.5"/><circle cx="8" cy="-9" r="2.5"/><circle cy="10" r="2.5"/>',
        'active': '<rect x="-10" y="-8" width="20" height="18" rx="3"/><path d="M-10-2H10M-5-11V-5M5-11V-5M-5 3H-2M3 3H6M-5 7H-2"/>',
        'recent': '<circle r="10"/><path d="M0-6V0L4 3M-3-14H3M0-14V-10"/>',
    }
    return f'<g transform="translate({x} {y})" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" opacity=".7" aria-hidden="true">{shapes[kind]}</g>'


def calendar_grid(days, start, first_week, last_week, y, mobile=False):
    """Columns remain weeks; phone panels split the complete calendar in half."""
    step = 18 if mobile else 17
    left, cell = (60, 14) if mobile else (58, 13)
    p = []
    for row, label in ((1, 'M'), (3, 'W'), (5, 'F')):
        p.append(text(left-22, y+row*step+10, label, 11, MUTED))
    groups = [[] for _ in LEVELS]
    month_spans = {}
    for item in days:
        day = date.fromisoformat(item['date'])
        week = (day-start).days // 7
        if not first_week <= week <= last_week:
            continue
        x = left+(week-first_week)*step
        cy = y+((day.weekday()+1) % 7)*step
        month = (day.year, day.month)
        if month not in month_spans:
            month_spans[month] = [day, day]
        month_spans[month][1] = day
        count = f"{item['count']:,} contributions; " if 'count' in item else ''
        title = f"{item['date']}: {count}activity level {item['level']} of 4"
        groups[item['level']].append(f'<rect data-date="{item["date"]}" x="{x}" y="{cy}" width="{cell}" height="{cell}" rx="3"><title>{title}</title></rect>')
    # Label the first full week of a month. If a very short edge month crowds
    # its neighbour, the longer visible month keeps its label.
    labels = []
    for first, last in month_spans.values():
        sunday = first+timedelta(days=(6-first.weekday()) % 7)
        anchor = sunday if sunday <= last else first
        week = (anchor-start).days//7
        x = left+(week-first_week)*step
        span = (last-first).days
        if labels and x-labels[-1][0] < (32 if mobile else 28):
            if span <= labels[-1][2]:
                continue
            labels.pop()
        labels.append((x,first.strftime('%b'),span))
    p += [text(x,y-13,month,16 if mobile else 11,MUTED) for x,month,_ in labels]
    p.append('<g class="calendar">')
    p += [f'<g fill="{color}">'+''.join(group)+'</g>' for color, group in zip(LEVELS, groups) if group]
    p.append('</g>')
    return '\n'.join(p)


def render_contributions(calendar, mobile=False):
    summary = calendar_summary(calendar)
    days = calendar['days']
    first, last = (date.fromisoformat(days[i]['date']) for i in (0, -1))
    start = first-timedelta(days=(first.weekday()+1) % 7)
    weeks = (last-start).days//7+1
    if weeks > 54:
        raise ValueError('Calendar exceeds the panel window')
    w,h = (600,985) if mobile else (1000,700)
    period = f'{first:%d %b %Y} — {last:%d %b %Y}'
    total = f"{summary['total']:,}" if summary['total'] is not None else 'unavailable'
    desc = f"{period}. {total} calendar contributions; {summary['active']} days with activity. Beneath the complete calendar, a decorative pixel bot collects clues, passes an inspection station and delivers a parcel through a portal. The bonus loop illustrates a side quest; it does not depict live activity. A bot message rotates daily. Activity includes automation and any private contribution totals the owner shares publicly. Reduced motion preserves a still scene."
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="arcade-title arcade-desc"><title id="arcade-title">Contribution arcade</title><desc id="arcade-desc">{escape(desc)}</desc>',
         '<defs><linearGradient id="arcade-surface" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs>',
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#arcade-surface)" stroke="{BORDER}"/>',
         f'<path d="M25 1H{190 if mobile else 310}" stroke="{MINT}" stroke-opacity=".65"/>',
         '<style>'+MOTION+SCENE_CSS+'</style>',
         '<g font-family="Segoe UI,Arial,sans-serif">',
         text(28,34,'CONTRIBUTION ARCADE / SIDE QUESTS',13 if mobile else 12,MINT,600),
         text(28,80,'Side quests leave a trail.',34 if mobile else 38,TEXT,700),
         text(28,111,period,18,MUTED),mascot(548 if mobile else 910,77,.67 if mobile else .95)]
    if not mobile:
        p += [f'<g class="arcade-greeting" aria-hidden="true"><path d="M746 17H845V43H835L849 55L825 43H746Z" fill="#182331" stroke="{BORDER}"/>',text(795,34,'HEY, HUMAN.',11,MINT,extra='text-anchor="middle"'),'</g>']
    p += [sparkle(w-30,124,MINT,-4),sparkle(w-156,88,VIOLET,-2)]
    metrics = [('total', 'CONTRIBUTIONS', 'in this calendar', MINT), ('active', 'ACTIVE DAYS', f'of {len(days)} displayed', VIOLET), ('recent', 'LAST 30 DAYS', 'contributions', PINK)]
    metric_width = 172 if mobile else 298
    gap = 14 if mobile else 24
    for i,(key,label,context,color) in enumerate(metrics):
        x = 28+i*(metric_width+gap)
        value = summary[key]
        p += [f'<rect x="{x}" y="135" width="{metric_width}" height="112" rx="14" fill="#101925" stroke="{BORDER}"/>',
              text(x+17,178,f'{value:,}' if value is not None else '—',36 if mobile else 38,color,700,f'data-metric="{key}"'),
              text(x+17,208,label,16 if mobile else 12,TEXT,600),
              text(x+17,230,context if value is not None else 'count unavailable',16 if mobile else 13,MUTED),metric_icon(x+metric_width-27,164,key,color)]
    # A recessed map and pixel corners give the calendar an arcade-cabinet frame.
    p += [f'<rect x="28" y="260" width="{w-56}" height="{411 if mobile else 176}" rx="16" fill="#0B121C" stroke="{BORDER}" stroke-opacity=".6"/>']
    for x, y, sx, sy in ((36,268,1,1),(w-36,268,-1,1),(36,663 if mobile else 428,1,-1),(w-36,663 if mobile else 428,-1,-1)):
        p += [f'<path d="M{x+sx*10} {y}H{x}V{y+sy*10}" fill="none" stroke="{VIOLET}" stroke-opacity=".45" stroke-width="2"/>']
    if mobile:
        split = (weeks+1)//2
        for i,(a,b,y) in enumerate(((0,split-1,311),(split,weeks-1,526))):
            section_start = max(first,start+timedelta(weeks=a))
            section_end = min(last,start+timedelta(weeks=b+1,days=-1))
            p += [text(54,y-31,f'{section_start:%b %Y} — {section_end:%b %Y}',18,MUTED),
                  calendar_grid(days,start,a,b,y,mobile=True)]
        legend_y, footer_y = 698, 936
    else:
        p += [text(54,279,'YEAR MAP / ONE COLUMN PER WEEK',12,MUTED),calendar_grid(days,start,0,weeks-1,310)]
        legend_y, footer_y = 460, 681
    p += [text(28,legend_y,'Less',16 if mobile else 12,MUTED)]
    for i,color in enumerate(LEVELS):
        p.append(f'<rect x="{78+i*19}" y="{legend_y-12}" width="13" height="13" rx="3" fill="{color}"/>')
    p += [text(181,legend_y,'More',16 if mobile else 12,MUTED),
          text(w-28,legend_y,'GitHub activity levels',16 if mobile else 12,MUTED,extra='text-anchor="end"'),
          text(28,footer_y,'Calendar activity includes automation.',16 if mobile else 12,MUTED)]
    stamp = date.fromisoformat(calendar['generated_at'][:10])
    p += [side_quest(DAILY_DROPS[stamp.weekday()],721 if mobile else 486,mobile)]
    stamp = calendar['generated_at'][:10]
    p += [text(28 if mobile else w-28,footer_y+27 if mobile else footer_y,'SNAPSHOT / '+stamp,14 if mobile else 12,MUTED,extra='' if mobile else 'text-anchor="end"'),'</g></svg>\n']
    return apply_theme('\n'.join(p))
