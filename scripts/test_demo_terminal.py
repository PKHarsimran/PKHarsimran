import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from demo_terminal import Terminal, resource_lines


class TTY(io.StringIO):
    def isatty(self):
        return True


class TerminalTests(unittest.TestCase):
    def test_ci_logs_stay_plain_and_do_not_wait(self):
        stream=io.StringIO()
        terminal=Terminal(record=True,stream=stream)
        with patch('demo_terminal.time.sleep') as sleep:
            terminal.page('Inspector','v1.0.0','01 / RUN')
            terminal.command(['$ python main.py'])
            self.assertEqual(terminal.perform(lambda:42,'Running'),42)
            terminal.end('VERIFIED')
        sleep.assert_not_called()
        self.assertNotIn('\x1b',stream.getvalue())

    def test_failed_process_cannot_reach_a_verified_screen(self):
        stream=TTY()
        terminal=Terminal(record=True,stream=stream)
        def failed():
            raise RuntimeError('real process failed')
        with patch('demo_terminal.time.sleep'), self.assertRaises(RuntimeError):
            terminal.perform(failed,'Running')
            terminal.end('VERIFIED')
        self.assertNotIn('VERIFIED',stream.getvalue())
        self.assertIn('RUN FAILED',stream.getvalue())

    def test_compact_findings_wrap_without_losing_the_url(self):
        stream=io.StringIO()
        terminal=Terminal(compact=True,stream=stream)
        url='hxxps://portal[.]example[.]com/invoice'
        terminal.line(url)
        lines=stream.getvalue().splitlines()
        self.assertTrue(all(len(line)<=32 for line in lines))
        self.assertEqual(''.join(lines),url)

    def test_labels_cannot_inject_terminal_controls(self):
        stream=io.StringIO()
        terminal=Terminal(stream=stream)
        terminal.line('release\x1b[2J\r\n\x9bhidden')
        self.assertNotIn('\x1b',stream.getvalue())
        self.assertNotIn('\x9b',stream.getvalue())
        self.assertEqual(len(stream.getvalue().splitlines()),1)

    def test_mobile_links_keep_the_hostname_and_path_readable(self):
        url='hxxp://198[.]51[.]100[.]23/tracking'
        self.assertEqual(resource_lines(url,32),['hxxp://198[.]51[.]100[.]23','/tracking'])

    def test_resource_wrapping_preserves_long_hosts_and_queries(self):
        urls=['hxxps://portal[.]example[.]com/invoice',
              'hxxps://'+('a'*90)+'[.]example/path/to/file?item=12&lang=en#end',
              'mirror/pages/one/two/three/index.html']
        for width in (32,52):
            for url in urls:
                lines=resource_lines(url,width)
                self.assertEqual(''.join(lines),url)
                self.assertTrue(all(0<len(line)<=width for line in lines))

    def test_transcript_keeps_the_original_url_across_mobile_wraps(self):
        terminal=Terminal(compact=True,stream=io.StringIO())
        terminal.page('Inspector','v1.0.0','02 / READ')
        url='hxxps://portal[.]example[.]com/invoice'
        terminal.resource(url)
        self.assertIn(url,terminal.transcript())
        self.assertNotIn('portal[.]example[.]com\n',terminal.transcript())

    def test_transcript_is_saved_with_all_chapters_and_no_terminal_codes(self):
        stream=TTY()
        terminal=Terminal(record=True,stream=stream)
        with tempfile.TemporaryDirectory() as folder, patch('demo_terminal.time.sleep'):
            path=Path(folder)/'replay.md'
            for step,label in enumerate(('RUN','READ','PROVE'),1):
                terminal.page('Inspector','v1.0.0',f'{step:02} / {label}')
                terminal.line('Actual finding')
            terminal.command(['$ python main.py --report'])
            terminal.end('CASE VERIFIED',path)
            text=path.read_text(encoding='utf-8')
            self.assertEqual(text.count('## 0'),3)
            self.assertIn('$ python main.py --report',text)
            self.assertEqual(text.count('CASE VERIFIED'),1)
            self.assertNotIn('\x1b',text)

    def test_failed_transcript_export_cannot_show_verified(self):
        stream=io.StringIO()
        terminal=Terminal(stream=stream)
        terminal.page('Inspector','v1.0.0','03 / PROVE')
        with patch('demo_terminal.Path.write_text',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                terminal.end('CASE VERIFIED','unused.md')
        self.assertNotIn('CASE VERIFIED',stream.getvalue())

    def test_backticks_in_findings_cannot_end_the_transcript_code_block(self):
        terminal=Terminal(stream=io.StringIO())
        terminal.page('Inspector','v1.0.0','02 / READ')
        terminal.line('```# not a heading')
        text=terminal.transcript()
        self.assertIn('````text\n```# not a heading\n````',text)


if __name__=='__main__':
    unittest.main()
