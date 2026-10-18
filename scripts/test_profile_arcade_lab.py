from copy import deepcopy
from datetime import date, timedelta
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from profile_arcade_lab import PROJECTS, START, END, build_lab, render_heist, render_relic, readme_slot, update_readme, retained_editions, prune_editions


class ArcadeLabTests(unittest.TestCase):
    def fixtures(self):
        snapshot={'generated_at':'2026-10-18T12:00:00Z','projects':[
            {'repo':repo,'release':'v2.16.9','ci':'PASSING','stars':i+10,'latest_commit_at':'2026-10-17T12:00:00Z'} for i,repo in enumerate(PROJECTS)]}
        calendar={'generated_at':snapshot['generated_at'],'days':[
            {'date':(date(2026,9,1)+timedelta(days=i)).isoformat(),'level':1,'count':i+1} for i in range(40)]}
        return snapshot,calendar

    def test_snapshot_build_is_reproducible_and_ignores_unrelated_fields(self):
        snapshot,calendar=self.fixtures()
        first=build_lab(snapshot,calendar)
        snapshot['unused_secret']='never publish this'
        snapshot['projects'][0]['extra']='also never publish this'
        self.assertEqual(first,build_lab(snapshot,calendar))
        self.assertEqual(render_relic(first),render_relic(build_lab(snapshot,calendar)))

    def test_every_daily_puzzle_has_one_unique_solution_including_leading_zeroes(self):
        snapshot,calendar=self.fixtures()
        for day in range(1,32):
            snapshot['generated_at']=f'2026-10-{day:02}T12:00:00Z'
            lab=build_lab(snapshot,calendar)
            expected=''.join(str(next(g['value'] for g in lab['gates'] if g['id']==key)%10) for key in lab['route'])
            self.assertEqual(lab['solution'],expected)
            self.assertEqual(len(set(lab['choices'])),3)
            self.assertEqual(lab['choices'].count(expected),1)
            self.assertTrue(all(len(c)==3 and c.isdigit() for c in lab['choices']))
        for project in snapshot['projects']:
            project.update(release='v0.0.0',stars=0,ci='UNAVAILABLE')
        for day in calendar['days']:
            day.update(level=0,count=0)
        lab=build_lab(snapshot,calendar)
        self.assertEqual(lab['solution'],'000')
        self.assertIn('000',lab['choices'])

    def test_release_digit_matches_the_printed_minor_or_patch_rule(self):
        snapshot,calendar=self.fixtures()
        lab=build_lab(snapshot,calendar)
        gate=lab['gates'][0]
        self.assertEqual(gate['value'],16 if gate['hint'].startswith('Minor') else 9)
        self.assertEqual(gate['digit'],6 if gate['hint'].startswith('Minor') else 9)

    def test_changed_snapshot_gets_new_asset_urls_and_matching_readme_references(self):
        snapshot,calendar=self.fixtures()
        old=build_lab(snapshot,calendar)
        snapshot['projects'][0]['stars']+=1
        new=build_lab(snapshot,calendar)
        self.assertNotEqual(old['assets'],new['assets'])
        rendered=readme_slot(new)
        self.assertTrue(all(path in rendered for path in new['assets'].values()))
        self.assertTrue(all(path not in rendered for path in old['assets'].values()))

    def test_retention_bounds_history_and_only_prunes_owned_svg_names(self):
        ids=[f'{i:016x}' for i in range(21)]
        kept=retained_editions({'retained':ids[:20]},ids[20])
        self.assertEqual(kept,ids[-14:])
        with TemporaryDirectory() as temporary:
            directory=Path(temporary)
            for name in (f'heist-{ids[0]}.svg',f'relic-{ids[20]}.svg','manual.svg','heist-untrusted.svg'):
                (directory/name).write_text('<svg/>')
            prune_editions(directory,kept)
            self.assertFalse((directory/f'heist-{ids[0]}.svg').exists())
            self.assertTrue((directory/f'relic-{ids[20]}.svg').exists())
            self.assertTrue((directory/'manual.svg').exists())
            self.assertTrue((directory/'heist-untrusted.svg').exists())
        with self.assertRaises(ValueError):
            retained_editions({'retained':['../outside']},ids[0])

    def test_missing_release_and_counts_use_available_facts(self):
        snapshot,calendar=self.fixtures()
        for project in snapshot['projects']:
            project['release']=None
        for day in calendar['days']:
            del day['count']
        lab=build_lab(snapshot,calendar)
        self.assertEqual(lab['gates'][0]['label'],'PROJECT STARS')
        self.assertEqual(lab['gates'][1]['value'],40)
        self.assertEqual(lab['gates'][1]['source'],'Days with activity')

    def test_rewind_reports_only_actual_observed_changes(self):
        snapshot,calendar=self.fixtures()
        previous=deepcopy(snapshot)
        previous['generated_at']='2026-10-17T12:00:00Z'
        self.assertEqual(build_lab(snapshot,calendar,previous)['rewind']['changes'],[])
        snapshot['projects'][0]['ci']='UNAVAILABLE'
        snapshot['projects'][1]['stars']+=1
        changes=build_lab(snapshot,calendar,previous)['rewind']['changes']
        self.assertEqual([(c['field'],c['before'],c['after']) for c in changes],[('ci','PASSING','UNAVAILABLE'),('stars',11,12)])

    def test_non_allowlisted_project_sets_are_rejected(self):
        snapshot,calendar=self.fixtures()
        snapshot['projects'][0]['repo']='private-repository'
        with self.assertRaises(ValueError):
            build_lab(snapshot,calendar)

    def test_readme_edits_are_bounded_idempotent_and_have_one_winning_hatch(self):
        snapshot,calendar=self.fixtures()
        lab=build_lab(snapshot,calendar)
        source='keep this before\n'+START+'\nold\n'+END+'\nkeep this after'
        result=update_readme(source,lab)
        self.assertTrue(result.startswith('keep this before\n'))
        self.assertTrue(result.endswith('\nkeep this after'))
        self.assertEqual(result.count('Signal recovered.'),1)
        self.assertEqual(result.count('Decoy hatch.'),2)
        self.assertEqual(result,update_readme(result,lab))
        with self.assertRaises(ValueError):
            update_readme(source+START,lab)

    def test_rewind_cannot_inject_readme_html_and_artwork_is_valid(self):
        snapshot,calendar=self.fixtures()
        previous=deepcopy(snapshot)
        previous['projects'][0]['release']='<script>alert(1)</script>|bad'
        lab=build_lab(snapshot,calendar,previous)
        rendered=readme_slot(lab)
        self.assertNotIn('<script>',rendered)
        self.assertIn('&lt;script&gt;',rendered)
        for source in (render_heist(lab),render_heist(lab,True),render_relic(lab)):
            ET.fromstring(source)


if __name__=='__main__':
    unittest.main()
