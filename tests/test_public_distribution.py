"""Portable checks for release evidence and immutable explanatory artwork."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / '6-1-sol-orch-3set-fast'
PINNED_GLYPHS = {
    'sol': '5b95b54628748423d497ff146ffe72ba148ce6ba5a19c21f1d9b14aabb22d68b',
    'luna': '8412975fe357485946d22bf183e333731131ae2fc46d7ea4b5b18c922022d3f9',
    'astra': '786171f60d98885771541045472318ec8142a28e142729a0517ba737ee088923',
    'json': '71595549f972a18ab65501db1d13e1c35aae1ec639c215b4045bcc35e7fbe924',
}


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.records = json.loads((ROOT / 'examples' / 'verification-records.json').read_text(encoding='utf-8'))

    def test_historical_capacity_arithmetic_and_limits(self):
        capacity = self.records['capacity_experiment']
        self.assertEqual('bounded-idle-hold', capacity['method'])
        self.assertEqual(16, capacity['chief_count'] + capacity['set_root_count'] + capacity['child_count'])
        self.assertEqual(16, capacity['total_active_test_agents'])
        self.assertEqual([4, 4, 4], capacity['children_per_set'])
        self.assertEqual([17, 17, 17], capacity['new_set_roots_advertised_total_slots'])
        self.assertEqual(4, capacity['old_chief_advertised_total_slots'])
        self.assertEqual(35.131341, capacity['overlap_hold_window_seconds'])
        self.assertTrue(capacity['cleanup_verified'])
        self.assertFalse(capacity['speed_benchmark'])

    def test_shared_json_integration_retains_evidence_limits(self):
        integration = self.records['information_integration_experiment']
        for field in ('information_transfer_verified', 'receiver_receipt_verified',
                      'three_set_integration_verified', 'chief_independent_verification',
                      'source_nonces_match', 'source_byte_hashes_match', 'source_provenance_retained'):
            self.assertTrue(integration[field], field)
        self.assertEqual(11, integration['merged_fact_count'])
        self.assertEqual(0, integration['new_subagents_created_this_test'])
        self.assertFalse(integration['automatic_conversation_history_shared'])
        self.assertIsNone(integration['observed_serving_tier'])
        self.assertEqual('priority', integration['fast_configured_tier'])
        self.assertTrue(integration['fast_feature_enabled'])

    def test_public_records_omit_private_identifiers(self):
        text = json.dumps(self.records)
        self.assertNotRegex(text, r'(?i)[A-Z]:[\\/]|/Users/|/home/|thread_ids|chat_id')
        self.assertNotRegex(text, r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    def test_glyph_files_match_original_hashes_and_license(self):
        manifest = json.loads((SKILL / 'assets' / 'assets.json').read_text(encoding='utf-8'))
        for name, expected in PINNED_GLYPHS.items():
            with self.subTest(glyph=name):
                self.assertEqual(expected, manifest[name]['sha256'])
                asset = SKILL / 'assets' / manifest[name]['path']
                self.assertEqual(expected, hashlib.sha256(asset.read_bytes()).hexdigest())
        license_text = (SKILL / 'assets' / 'LICENSE.icons').read_text(encoding='utf-8')
        self.assertIn('Apache License', license_text)
        self.assertIn('CC0', manifest['json']['license'])

    def test_skill_relative_links_exist(self):
        for document in SKILL.rglob('*.md'):
            for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                with self.subTest(document=document.name, target=target):
                    self.assertTrue((document.parent / target).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
