"""Small, dependency-free presentation layer for real, recorded CLI runs."""
from concurrent.futures import ThreadPoolExecutor
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


class Terminal:
    def __init__(self, record=False, compact=False, stream=None):
        self.stream = sys.stdout if stream is None else stream
        self.animated = record and self.stream.isatty()
        self.width = 32 if compact else 52

    def write(self, text):
        self.stream.write(text)
        self.stream.flush()

    def styled(self, text, color='text', bold=False):
        if not self.animated:
            return text
        return f'\x1b[{"1;" if bold else ""}38;2;{COLORS[color]}m{text}\x1b[0m'

    def line(self, text='', color='text', bold=False):
        for line in textwrap.wrap(safe_text(text), self.width,
                                  break_on_hyphens=False) or ['']:
            self.write(self.styled(line, color, bold) + '\n')

    def pause(self, seconds):
        if self.animated:
            time.sleep(seconds)

    def page(self, title, version, chapter):
        if self.animated:
            self.write('\x1b[?25l\x1b[2J\x1b[H')
        step=chapter.split(' / ',1)[0]
        self.line('PK / FIELD NOTES' + f'{step} / 03'.rjust(self.width-16), 'muted')
        self.line(title, 'mint', True)
        self.line(version + ' / GUIDED CLI RUN', 'muted')
        self.line('-' * self.width, 'rule')
        self.line()
        self.line(chapter, 'violet', True)
        self.line()

    def command(self, lines):
        for line in lines:
            # These are the command's actual arguments, with the venv's Python
            # shortened to "python". No invented product flags or canned output.
            for part in textwrap.wrap(safe_text(line), self.width,
                                      break_on_hyphens=False):
                for char in part:
                    self.write(self.styled(char, 'text'))
                    self.pause(.022)
                self.write('\n')
        self.line()

    def perform(self, action, label):
        """Animate only while the actual work is pending; propagate failures."""
        if not self.animated:
            self.line(label)
            return action()
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

    def end(self, marker):
        self.line()
        self.line('-' * self.width, 'rule')
        self.line(marker, 'mint', True)
        # VHS holds this completed frame; interactive runs restore the cursor.
        try:
            self.pause(7)
        finally:
            if self.animated:
                self.write('\x1b[?25h')
