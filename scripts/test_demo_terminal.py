import io
import unittest
from unittest.mock import patch

from demo_terminal import Terminal


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


if __name__=='__main__':
    unittest.main()
