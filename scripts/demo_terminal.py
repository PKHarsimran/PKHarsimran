"""Small, dependency-free presentation layer for real, recorded CLI runs."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import sys
import textwrap
import time


COLORS = {'text': '230;237;243', 'muted': '147;164;184',
          'mint': '67;230;197', 'violet': '169;149;255',
          'rule': '41;54;75', 'red': '255;123;146'}
SPINNER = '|/-\\'


def safe_text(value):
    # Findings and release labels must never become terminal control sequences.
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(value))


def resource_lines(value, width):
    """Prefer URL/path boundaries while preserving every displayed character."""
    value=safe_text(value)
    authority=value.find('://')
    start=authority+3 if authority>=0 else 0
    boundaries=[m.start() for m in re.finditer(r'[/\?#&]',value) if m.start()>=start]
    lines=[]
    offset=0
    while len(value)-offset>width:
        candidates=[point for point in boundaries if offset<point<=offset+width]
        end=max(candidates) if candidates else offset+width
        lines.append(value[offset:end])
        offset=end
    return lines+[value[offset:]]


class Terminal:
    def __init__(self, record=False, compact=False, stream=None):
        self.stream = sys.stdout if stream is None else stream
        self.animated = record and self.stream.isatty()
        self.width = 32 if compact else 52
        self.pages=[]
        self.collect=True
        self.title='CLI replay'
        self.version=''

    def write(self, text):
        self.stream.write(text)
        self.stream.flush()

    def styled(self, text, color='text', bold=False):
        if not self.animated:
            return text
        return f'\x1b[{"1;" if bold else ""}38;2;{COLORS[color]}m{text}\x1b[0m'

    def line(self, text='', color='text', bold=False):
        text=safe_text(text)
        if self.collect and self.pages:
            self.pages[-1]['lines'].append(text)
        for line in textwrap.wrap(text, self.width,
                                  break_on_hyphens=False) or ['']:
            self.write(self.styled(line, color, bold) + '\n')

    def pause(self, seconds):
        if self.animated:
            time.sleep(seconds)

    def page(self, title, version, chapter):
        self.title=safe_text(title)
        self.version=safe_text(version)
        self.pages.append({'chapter':safe_text(chapter),'lines':[]})
        self.collect=False
        if self.animated:
            self.write('\x1b[?25l\x1b[2J\x1b[H')
        step=chapter.split(' / ',1)[0]
        self.line('PK / FIELD NOTES' + f'{step} / 03'.rjust(self.width-16), 'muted')
        self.line(title, 'mint', True)
        self.line(version + ' / GUIDED CLI RUN', 'muted')
        active=int(step)-1
        for index,label in enumerate(('RUN','READ','PROVE')):
            if index:
                self.write(self.styled('  >  ','rule'))
            color='violet' if index==active else ('mint' if index<active else 'muted')
            self.write(self.styled(label,color,index==active))
        self.write('\n')
        self.line()
        self.line(chapter, 'violet', True)
        self.line()
        self.collect=True

    def command(self, lines):
        for line in lines:
            if self.pages:
                self.pages[-1]['lines'].append(safe_text(line))
            # These are the command's actual arguments, with the venv's Python
            # shortened to "python". No invented product flags or canned output.
            for part in textwrap.wrap(safe_text(line), self.width,
                                      break_on_hyphens=False):
                for char in part:
                    self.write(self.styled(char, 'text'))
                    self.pause(.022)
                self.write('\n')
        self.line()
        # Hold the complete command before launching, without inventing progress.
        self.pause(.8)

    def resource(self, value):
        value=safe_text(value)
        if self.pages:
            self.pages[-1]['lines'].append(value)
        self.collect=False
        try:
            for index,line in enumerate(resource_lines(value,self.width)):
                self.line(line,'text' if index==0 else 'muted')
        finally:
            self.collect=True

    def perform(self, action, label):
        """Animate only while the actual work is pending; propagate failures."""
        if not self.animated:
            self.line(label)
            result=action()
            self.line('[ok] process exited successfully','mint')
            return result
        started = time.monotonic()
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(action)
            frame = 0
            while not future.done():
                elapsed = time.monotonic() - started
                status = f'{SPINNER[frame % 4]} {label} / {elapsed:.1f}s'
                self.write('\r\x1b[2K' + self.styled(status[:self.width], 'violet'))
                time.sleep(.1)
                frame += 1
            self.write('\r\x1b[2K')
            try:
                result = future.result()
            except Exception:
                self.line('RUN FAILED / recording rejected', 'red', True)
                raise
        self.line('[ok] process exited successfully', 'mint')
        return result

    def transcript(self):
        text=f'# {self.title} / CLI replay\n\nReleased version: `{self.version}`. Guided presentation of a real run on an owned fixture.\n\n'
        for page in self.pages:
            content='\n'.join(page['lines']).strip()
            # Findings remain literal even if a future fixture contains backticks.
            fence='`'*max(3,1+max((len(m.group()) for m in re.finditer(r'`+',content)),default=0))
            text+=f'## {page["chapter"]}\n\n{fence}text\n{content}\n{fence}\n\n'
        return text+'[Reproduce the run](../demos/README.md) · [Source provenance](./demo-provenance.json)\n'

    def end(self, marker, transcript=None):
        self.line()
        self.collect=False
        self.line('-' * self.width, 'rule')
        if transcript is not None:
            self.pages[-1]['lines'].append(safe_text(marker))
            Path(transcript).write_text(self.transcript(),encoding='utf-8')
        else:
            self.collect=True
        self.line(marker, 'mint', True)
        self.collect=True
        # VHS holds this completed frame; interactive runs restore the cursor.
        try:
            self.pause(7)
        finally:
            if self.animated:
                self.write('\x1b[?25h')
