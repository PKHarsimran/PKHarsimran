from datetime import date
from pathlib import Path
import unittest
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

import generate_profile_lab as lab


class ProfileLabTests(unittest.TestCase):
    def fake_fetch(self, repo, suffix="", **kwargs):
        if not suffix:
            return {"private":False,"default_branch":"main","stargazers_count":12}
        if suffix.startswith("/commits"):
            return [{"commit":{"committer":{"date":"2026-10-17T12:00:00Z"}}}]
        if suffix=="/releases/latest":
            return None
        return {"workflow_runs":[{"id":123,"status":"completed","conclusion":"success"}]}

    def test_ci_does_not_turn_incomplete_or_unknown_runs_green(self):
        self.assertEqual(lab.ci_state({"status":"in_progress","conclusion":None}),"RUNNING")
        self.assertEqual(lab.ci_state({"status":"completed","conclusion":None}),"UNKNOWN")
        self.assertEqual(lab.ci_state(None),"NO RUNS")

    def test_unreleased_is_distinct_from_ci_network_failure(self):
        def fetch(repo,suffix="",**kwargs):
            if suffix.startswith("/actions/"):
                raise HTTPError("https://api.github.com",503,"unavailable",{},None)
            return self.fake_fetch(repo,suffix,**kwargs)
        item=lab.collect_project(lab.PROJECTS[0],fetch)
        self.assertEqual(item["release_state"],"unreleased")
        self.assertEqual(item["ci"],"UNAVAILABLE")

    def test_private_metadata_is_rejected_before_secondary_requests(self):
        calls=[]
        def fetch(repo,suffix="",**kwargs):
            calls.append(suffix)
            return {"private":True}
        with self.assertRaises(ValueError):
            lab.collect_project(lab.PROJECTS[0],fetch)
        self.assertEqual(calls,[""])

    def test_no_new_repository_can_be_fetched(self):
        with self.assertRaises(ValueError):
            lab.github_json("not-in-the-public-list")

    def test_release_text_cannot_inject_svg_markup(self):
        item=lab.collect_project(lab.PROJECTS[0],self.fake_fetch)
        item["release"]='<script>alert(1)</script>'
        svg=lab.render_radar({"generated_at":"2026-10-17T12:00:00Z","projects":[item]})
        ET.fromstring(svg)
        self.assertNotIn('<script>',svg)

    def test_calendar_ignores_unrelated_html_and_future_cells(self):
        html='''<div data-date="2026-10-16" data-level="4"></div><td class="ContributionCalendar-day" data-date="2026-10-16" data-level="2"></td><td class="ContributionCalendar-day" data-date="2026-10-17" data-level="3"></td><td class="ContributionCalendar-day" data-date="2026-10-18" data-level="4"></td>'''
        days=lab.parse_calendar(html,date(2026,10,17),minimum=2)
        self.assertEqual([d["level"] for d in days],[2,3])

    def test_missing_calendar_does_not_publish_an_empty_game(self):
        with self.assertRaises(ValueError):
            lab.parse_calendar('<html>rate limit</html>',date(2026,10,17))

    def test_calendar_gaps_are_rejected(self):
        html=''.join(f'<td class="ContributionCalendar-day" data-date="2026-10-{d}" data-level="1"></td>' for d in ['15','17'])
        with self.assertRaises(ValueError):
            lab.parse_calendar(html,date(2026,10,17),minimum=2)

    def test_empty_activity_keeps_a_valid_static_calendar(self):
        svg=lab.render_patrol({"generated_at":"2026-10-17T12:00:00Z","days":[{"date":"2026-10-17","level":0}]})
        ET.fromstring(svg)
        self.assertIn('0 active days',svg)
        self.assertIn('prefers-reduced-motion',svg)


if __name__=="__main__":
    unittest.main()
