from datetime import date, timedelta
from pathlib import Path
import unittest
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

import generate_profile_lab as lab
from contribution_arcade import calendar_summary


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

    def test_calendar_counts_match_cells_by_id_and_allow_comma_totals(self):
        html='''<td id="day-a" class="ContributionCalendar-day" data-date="2026-10-16" data-level="0"></td>
        <td id="day-b" class="ContributionCalendar-day" data-date="2026-10-17" data-level="4"></td>
        <tool-tip for="unrelated">999 contributions on October 17th.</tool-tip>
        <tool-tip for="day-b">1,234 contributions on October 17th.</tool-tip>
        <tool-tip for="day-a">No contributions on October 16th.</tool-tip>'''
        days=lab.parse_calendar(html,date(2026,10,17),minimum=2)
        self.assertEqual([d['count'] for d in days],[0,1234])

    def test_conflicting_calendar_count_is_rejected(self):
        html='''<td id="day" class="ContributionCalendar-day" data-date="2026-10-17" data-level="2"></td>
        <tool-tip for="day">No contributions on October 17th.</tool-tip>'''
        with self.assertRaises(ValueError):
            lab.parse_calendar(html,date(2026,10,17),minimum=1)

    def test_unknown_tooltip_format_keeps_count_unavailable(self):
        html='''<td id="day" class="ContributionCalendar-day" data-date="2026-10-17" data-level="2"></td>
        <tool-tip for="day">Unexpected calendar format</tool-tip>'''
        days=lab.parse_calendar(html,date(2026,10,17),minimum=1)
        summary=calendar_summary({'days':days})
        self.assertIsNone(summary['total'])
        self.assertIsNone(summary['recent'])
        self.assertEqual(summary['active'],1)

    def test_recent_total_is_exactly_the_last_thirty_displayed_days(self):
        days=[{'date':(date(2026,9,1)+timedelta(days=i)).isoformat(),'level':1,'count':i+1} for i in range(40)]
        summary=calendar_summary({'days':days})
        self.assertEqual(summary,{'total':820,'active':40,'recent':765})
        del days[0]['count']
        summary=calendar_summary({'days':days})
        self.assertIsNone(summary['total'])
        self.assertEqual(summary['recent'],765)

    def test_both_layouts_preserve_every_date_once_without_inventing_counts(self):
        days=[{'date':(date(2025,10,12)+timedelta(days=i)).isoformat(),'level':i%5,'count':(i%5)*2} for i in range(371)]
        calendar={'generated_at':'2026-10-17T12:00:00Z','days':days}
        ns={'s':'http://www.w3.org/2000/svg'}
        for mobile in (False,True):
            root=ET.fromstring(lab.render_contributions(calendar,mobile))
            cells=root.findall('.//s:rect[@data-date]',ns)
            self.assertEqual(len(cells),len(days))
            self.assertEqual({c.get('data-date') for c in cells},{d['date'] for d in days})
            self.assertEqual(root.find('.//s:text[@data-metric="total"]',ns).text,f"{sum(d['count'] for d in days):,}")

    def test_empty_activity_keeps_a_valid_static_calendar(self):
        svg=lab.render_contributions({"generated_at":"2026-10-17T12:00:00Z","days":[{"date":"2026-10-17","level":0}]})
        ET.fromstring(svg)
        self.assertIn('0 days with activity',svg)
        self.assertIn('prefers-reduced-motion',svg)

    def test_compact_calendar_preserves_every_day_and_level(self):
        days = [{"date":f"2026-10-{n+12}","level":n} for n in range(5)]
        tree = ET.fromstring(lab.render_contributions({"generated_at":"2026-10-17T12:00:00Z","days":days}))
        ns = {"s":"http://www.w3.org/2000/svg"}
        groups = tree.findall('.//s:g[@class="calendar"]/s:g', ns)
        self.assertEqual(len(groups), 5)
        for day, group in zip(days, groups):
            rect = group.find('s:rect', ns)
            self.assertEqual(rect.find('s:title', ns).text, f'{day["date"]}: activity level {day["level"]} of 4')
            self.assertIn('x', rect.attrib)
            self.assertIn('y', rect.attrib)
            self.assertIn('fill', group.attrib)


if __name__=="__main__":
    unittest.main()
