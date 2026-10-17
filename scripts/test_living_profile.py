from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import living_profile as living
import profile_demos as demos


class LivingProfileTests(unittest.TestCase):
    def diagnostic(self):
        return {'ts':'2026-10-17T12:00:00Z','collections':{'observables':12,'vulnerabilities':3},'total':15,'duplicates_removed':6,'delta_counts':{'added':2,'updated':1,'removed':1}}

    def test_inconsistent_or_negative_counts_fail_instead_of_becoming_art(self):
        run=self.diagnostic(); run['total']=16
        with self.assertRaises(ValueError):
            living.intel_snapshot(run,{},datetime(2026,10,17,13,tzinfo=timezone.utc))
        run=self.diagnostic(); run['duplicates_removed']=-1
        with self.assertRaises(ValueError):
            living.intel_snapshot(run,{},datetime(2026,10,17,13,tzinfo=timezone.utc))

    def test_unknown_attempt_status_is_never_accepted(self):
        record=living.intel_snapshot(self.diagnostic(),{'status':'surprise'},datetime(2026,10,17,13,tzinfo=timezone.utc))
        self.assertEqual(record['latest_attempt'],'unknown')

    def test_future_collection_timestamp_fails(self):
        with self.assertRaises(ValueError):
            living.intel_snapshot(self.diagnostic(),{},datetime(2026,10,16,13,tzinfo=timezone.utc))

    def test_service_manifest_rejects_configuration_and_addresses(self):
        data=json.loads((living.OUT/'lab-services.json').read_text())
        data['media_flow'][0]['services']=['http://192.168.1.2:8096']
        with self.assertRaises(ValueError): living.validate_lab(data)
        data=json.loads((living.OUT/'lab-services.json').read_text())
        data['private_config']='anything'
        with self.assertRaises(ValueError): living.validate_lab(data)

    def test_released_demo_tags_cannot_be_shell_options(self):
        with self.assertRaises(ValueError): living.resolve_tag('IOC-Inspector','--upload-pack=anything')

    def test_demo_cache_is_stable_within_a_week_and_rotates_next_week(self):
        releases=[{'repo':repo,'tag':'v1.0.0'} for repo in living.DEMO_REPOS.values()]
        with patch.object(living,'resolve_tag',return_value='a'*40):
            first=living.demo_plan(releases,datetime(2026,10,17,tzinfo=timezone.utc))
            same=living.demo_plan(releases,datetime(2026,10,18,tzinfo=timezone.utc))
            next_week=living.demo_plan(releases,datetime(2026,10,19,tzinfo=timezone.utc))
        self.assertEqual(first['fingerprint'],same['fingerprint'])
        self.assertNotEqual(first['fingerprint'],next_week['fingerprint'])

    def test_mirror_rejects_external_and_missing_links(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            (root/'style.css').write_text('')
            (root/'mark.svg').write_text('<svg/>')
            for file in ('index.html','guide.html','about.html'):
                (root/file).write_text('<a href="https://example.com/">Remote</a>')
            with self.assertRaises(ValueError): demos.verify_mirror(root)
            (root/'index.html').write_text('<a href="missing.html">Missing</a>')
            with self.assertRaises(ValueError): demos.verify_mirror(root)

    def test_complete_mirror_has_only_resolving_relative_references(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            (root/'style.css').write_text('')
            (root/'mark.svg').write_text('<svg/>')
            for file in ('index.html','guide.html','about.html'):
                (root/file).write_text('<a href="index.html">Home</a><img src="mark.svg"><link href="style.css">')
            self.assertEqual(demos.verify_mirror(root),9)

    def test_svg_variants_escape_untrusted_release_labels_and_reduce_motion(self):
        record=living.intel_snapshot(self.diagnostic(),{},datetime(2026,10,17,13,tzinfo=timezone.utc))
        lab=living.validate_lab(json.loads((living.OUT/'lab-services.json').read_text()))
        release=[{'name':'<script>','tag':'<script>','published_at':'2026-10-17T12:00:00Z','color':'#43E6C5'}]
        for mobile in (False,True):
            for art in (living.conveyor(record,mobile),living.lab_flow(lab,mobile),living.patches(release,mobile)):
                ET.fromstring(art)
                self.assertNotIn('<script>',art)
            self.assertIn('prefers-reduced-motion',living.conveyor(record,mobile))


if __name__=='__main__': unittest.main()
