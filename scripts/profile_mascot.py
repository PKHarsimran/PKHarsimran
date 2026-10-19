"""Animated Hacker Bender fan art, shared by the README's existing illustrations.

Original SVG drawing of Bender from Futurama, in the selected charcoal hoodie
with mint/pink trim. No remote images, scripts, or raster dependencies.
"""

MINT, PINK = '#43E6C5', '#F36BAA'

STYLE = '''
.bender-idle{animation:bender-idle 7s ease-in-out infinite}
.bender-eyes{transform-box:fill-box;transform-origin:center;animation:bender-blink 8s linear infinite}
.bender-wave{transform-origin:0 0;animation:bender-wave 14s ease-in-out infinite}
.bender-signal{transform-box:fill-box;transform-origin:center;opacity:0;animation:bender-signal 7s ease-out infinite}
.bender-cursor{animation:bender-cursor 3s steps(1,end) infinite}
@keyframes bender-idle{50%{transform:translateY(-2px)}}
@keyframes bender-blink{0%,43%,47%,100%{transform:scaleY(1)}45%{transform:scaleY(.12)}}
@keyframes bender-wave{0%,62%,88%,100%{transform:rotate(0)}68%,78%{transform:rotate(-9deg)}73%,83%{transform:rotate(5deg)}}
@keyframes bender-signal{0%,67%,100%{opacity:0;transform:scale(.7)}72%{opacity:.55}89%{opacity:0;transform:scale(1.7)}}
@keyframes bender-cursor{0%,62%,100%{opacity:1}63%,99%{opacity:.2}}
@media(prefers-reduced-motion:reduce){.bender-idle,.bender-eyes,.bender-wave,.bender-signal,.bender-cursor{animation:none}.bender-signal{display:none}.bender-cursor{opacity:.7}}
'''


def hacker_bender(x=0, y=0, scale=1, pose='wave', key='mascot'):
    """Anchor at the jacket collar; bounds are approximately -82,-103 to 82,67."""
    if pose not in ('wave', 'laptop'): raise ValueError('Unknown Bender pose')
    metal, hood = f'bender-{key}-metal', f'bender-{key}-hood'
    p = [f'<g transform="translate({x} {y}) scale({scale})" data-mascot="hacker-bender" aria-hidden="true">',
         f'<style>{STYLE}</style>',
         f'<defs><linearGradient id="{metal}" x2="1" y2=".3"><stop stop-color="#E5EDF4"/><stop offset=".38" stop-color="#AABAC9"/><stop offset="1" stop-color="#75889E"/></linearGradient>',
         f'<linearGradient id="{hood}" x2="1" y2="1"><stop stop-color="#303D50"/><stop offset=".55" stop-color="#1C2738"/><stop offset="1" stop-color="#111B2A"/></linearGradient></defs>',
         '<ellipse cx="1" cy="68" rx="41" ry="5" fill="#050A12" fill-opacity=".45"/>',
         '<g class="bender-idle" stroke="#080F19" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">',
         # Short, ribbed silver legs and broad soft-edged metal feet.
         f'<path d="M-23 29H-6L-7 56H-25ZM7 29H24L26 56H8Z" fill="url(#{metal})"/>',
         '<path d="M-24 39L-7 40M-24 47L-7 48M8 40L25 39M8 48L25 47" fill="none" stroke="#53667E" stroke-width="1.7"/>',
         f'<path d="M-26 53Q-34 54-35 62Q-34 67-9 65Q-5 64-6 57L-9 54ZM10 54L25 53Q35 56 36 63Q34 67 10 65Q6 64 8 57Z" fill="url(#{metal})"/>',
         '<path d="M-29 61H-12M13 61H30" stroke="#EDF6FF" stroke-opacity=".55" stroke-width="1.2"/>',
         # Jacket and a small glimpse of Bender's chest door.
         f'<path d="M-27-12Q-44-8-42 12L-31 33Q0 41 32 33L40 10Q44-8 26-12L7-5H-8Z" fill="url(#{hood})"/>',
         f'<path d="M-15-8H15L17 33Q0 37-16 33Z" fill="url(#{metal})"/>',
         '<rect x="-9" y="7" width="17" height="20" rx="3" fill="#9BAEC0" stroke="#465B72" stroke-width="1.4"/>',
         '<circle cx="4" cy="17" r="1.5" fill="#DCE8F2" stroke="#465B72" stroke-width="1"/>',
         '<path d="M-26-10L-9 1L-19 12L-22 32M25-10L9 1L20 13L21 32" fill="none" stroke="#536176" stroke-width="1.6"/>',
         f'<path d="M-34 0L-29 27M31-1L29 28" fill="none" stroke="{MINT}" stroke-width="1.7"/>',
         f'<path d="M35 7L32 29" fill="none" stroke="{PINK}" stroke-width="1.6"/>',
         '<path d="M-17-2L-20 13M18-2L21 14" stroke="#BAC7D7" stroke-width="1.1"/>',
         '<path d="M-21 12V16M22 13V17" stroke="#D6E0ED" stroke-width="2"/>']
    if pose == 'wave':
        p += [f'<path d="M-35-1Q-47 9-43 23L-35 27L-28 18" fill="url(#{hood})"/>',
              f'<path d="M-43 21Q-50 24-45 32Q-39 38-34 31L-34 27Z" fill="url(#{metal})"/>',
              '<g transform="translate(30 3)"><g class="bender-wave">',
              f'<path d="M-2-11Q12-13 17 3L22-11L32-7Q28 18 13 17L-3 8Z" fill="url(#{hood})"/>',
              f'<path d="M17 7Q24 5 27-6" fill="none" stroke="{PINK}" stroke-width="1.8"/>',
              f'<path d="M20-16L32-12L29-5L18-9Z" fill="url(#{metal})"/>',
              f'<path d="M22-20L18-30Q17-35 21-36Q25-37 27-27L27-39Q27-44 31-44Q35-44 35-39L35-28L39-34Q42-38 45-35Q48-33 45-28L38-15Q32-10 26-16Z" fill="url(#{metal})"/>',
              '<path d="M25-19L32-16M30-28L34-25" fill="none" stroke="#6B7F95" stroke-width="1.3"/>',
              '</g></g>']
    else:
        p += [f'<path d="M-33-4Q-46-1-50 13L-40 23L-25 9" fill="url(#{hood})"/>',
              f'<path d="M-49 13Q-59 11-59 20Q-54 29-44 23L-40 19Z" fill="url(#{metal})"/>',
              f'<path d="M31-5Q44 0 40 17L29 26L20 20L27 10" fill="url(#{hood})"/>',
              f'<path d="M31 14Q23 9 20 17L25 24L31 21" fill="url(#{metal})"/>',
              '<path d="M24 27L34 22" fill="none" stroke="#708096" stroke-width="1.2"/>']
    # Hood behind the face, with narrow coloured piping rather than neon fill.
    p += [f'<path d="M-37-53Q-38-77-10-82Q20-91 39-64Q49-45 39-20L30-5Q1 6-32-9Q-49-22-37-53Z" fill="url(#{hood})"/>',
          '<path d="M-28-65Q-9-82 12-77" fill="none" stroke="#617087" stroke-opacity=".65" stroke-width="1.4"/>',
          f'<path d="M-31-11Q-47-34-34-61Q-27-81-7-81" fill="none" stroke="{MINT}" stroke-width="1.8"/>',
          f'<path d="M17-80Q46-68 43-40L38-19" fill="none" stroke="{PINK}" stroke-width="1.8"/>',
          # Antenna remains visible above the hood.
          f'<path d="M0-76L3-94L9-93L7-75Z" fill="url(#{metal})" stroke-width="1.8"/>',
          f'<circle cx="7" cy="-97" r="5.5" fill="url(#{metal})" stroke-width="1.8"/>',
          '<path d="M4-99L7-101" stroke="#F4FBFF" stroke-width="1.4"/>',
          f'<circle class="bender-signal" cx="7" cy="-97" r="8" fill="none" stroke="{MINT}" stroke-width="1"/>',
          # The silver cylindrical head and protruding visor carry the identity.
          f'<path d="M-29-44V-53Q-29-72 1-72Q31-72 31-51V-14Q31-5 0-5Q-29-5-29-17Z" fill="url(#{metal})"/>',
          '<path d="M-22-54Q-20-66-5-66" fill="none" stroke="#F1F7FD" stroke-opacity=".75" stroke-width="2.4"/>',
          '<path d="M21-65Q30-57 28-48" fill="none" stroke="#64778F" stroke-width="2"/>',
          f'<path d="M-28-49H28Q38-49 38-38Q38-25 27-25H-27Q-38-25-38-38Q-38-49-28-49Z" fill="url(#{metal})"/>',
          '<rect x="-32" y="-45" width="64" height="17" rx="8" fill="#0A111B" stroke-width="1.5"/>',
          '<g class="bender-eyes" stroke="none">',
          '<path d="M-29-40H-4Q-5-28-16-28Q-28-28-29-40ZM3-40H29Q29-28 17-28Q5-28 3-40Z" fill="#F5E6A6"/>',
          '<path d="M-18-40H-13V-34H-18ZM14-40H19V-34H14Z" fill="#131D2A"/>',
          '</g>',
          '<path d="M-27-43H-5M5-43H27" stroke="#3C4A5F" stroke-width="2.5"/>',
          '<rect x="-25" y="-23" width="51" height="16" rx="6" fill="#F3E8BA" stroke-width="2"/>',
          '<path d="M-16-22V-8M-5-23V-7M6-23V-7M17-22V-8M-24-15H25" fill="none" stroke="#47515E" stroke-width="1.1"/>',
          '<path d="M-22-2Q0 7 25-3" fill="none" stroke="#63748B" stroke-width="1.4"/>']
    if pose == 'laptop':
        p += ['<g stroke-width="2">',
              '<path d="M-76-5L-30-2L-21 24L-66 22Z" fill="#111D2C"/>',
              f'<path d="M-73-2L-33 1" fill="none" stroke="{MINT}" stroke-opacity=".35" stroke-width="1"/>',
              '<path d="M-66 22L-21 24L-10 20L-21 30L-65 28L-79 23Z" fill="#42536C"/>',
              '<path d="M-66 24L-25 27" stroke="#8294AB" stroke-width="1"/>',
              f'<path d="M-61 6L-54 11L-59 15" fill="none" stroke="{MINT}" stroke-width="2.5"/>',
              f'<path class="bender-cursor" d="M-51 16H-43" stroke="{MINT}" stroke-width="2.5"/>',
              f'<path d="M-28 25H-24" stroke="{PINK}" stroke-width="1.3"/>', '</g>']
    return ''.join(p+['</g></g>'])


def pixel_bender():
    """A tiny, high-contrast hoodie sprite; the courier's foot hooks stay stable."""
    return f'''<g shape-rendering="crispEdges" data-mascot="hacker-bender-pixel">
      <path d="M-7-21H6V-18H10V-3H7V7H-8V-3H-12V-17H-9V-20Z" fill="#314157"/>
      <path d="M-10-17H-8V-5H-10ZM-8-20H-5V-18H-8Z" fill="{MINT}"/>
      <path d="M8-17H10V-5H8ZM5-20H8V-18H5Z" fill="{PINK}"/>
      <path d="M-7-17H6V-14H9V-3H-8V-14H-7Z" fill="#B6C6D5"/>
      <path d="M-9-14H9V-7H-9Z" fill="#0A111B"/>
      <path d="M-7-12H-1V-8H-6ZM2-12H8L7-8H3Z" fill="#F5E6A6"/>
      <path d="M-4-12H-2V-10H-4ZM4-12H6V-10H4Z" fill="#182331"/>
      <path d="M-6-6H7V-2H-6Z" fill="#F3E8BA"/>
      <path d="M-3-6V-2M1-6V-2M5-6V-2M-6-4H7" stroke="#53637B" stroke-width="1"/>
      <path d="M-1-26H1V-21H-1Z" fill="#C1D1DD"/><path d="M-2-28H2V-25H-2Z" fill="#DEEAF4"/>
      <path d="M-8 0H-3V6H-8ZM3 0H8V6H3Z" fill="#182638"/>
      <path d="M-8 0H-6V6H-8ZM6 0H8V6H6Z" fill="{MINT}"/>
      <path d="M-2 0H2V6H-2Z" fill="#A2B4C6"/>
      <g class="quest-foot-a"><path d="M-7 7H-2V13H-10V10H-7Z" fill="#B6C6D5"/></g>
      <g class="quest-foot-b"><path d="M3 7H8V10H10V13H3Z" fill="#B6C6D5"/></g>
      <path d="M9-3H22V9H9Z" fill="{PINK}"/><path d="M14-3H17V1H14Z" fill="#EFF4FC"/>
      <path d="M-13-2H-9V4H-13Z" fill="#B6C6D5"/>
    </g>'''


def portrait(pose='laptop'):
    """Reusable transparent avatar, kept out of the README's reading flow."""
    detail = 'a tiny terminal laptop' if pose == 'laptop' else 'a friendly three-finger wave'
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="320" height="340" viewBox="-96 -117 192 196" role="img" aria-labelledby="title desc">'
            '<title id="title">Hacker Bender</title><desc id="desc">Cute Bender fan art: silver face, sleepy yellow eyes, toothy grin, charcoal hoodie, mint and pink piping, and '+detail+'. Eyes blink and the antenna softly pings. Reduced motion keeps the character still.</desc>'
            +hacker_bender(pose=pose, key='portrait')+'</svg>\n')
