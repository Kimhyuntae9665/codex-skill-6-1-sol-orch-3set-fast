import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/6-1-sol-orch-3set-fast/scripts/check_plan.py'
spec = importlib.util.spec_from_file_location('plan_checker', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    return {'version': 2, 'run_id': 'test', 'objective': 'Build a feature',
            'execution_mode': 'parallel-only', 'deployment': 'single-tree',
            'capacity_total': 13, 'concurrent_reviewers': 0,
            'chief_write_scope': ['work/shared'],
            'sets': [{'id': f'SET{i}', 'objective': f'Unit {i}',
                      'work_keys': [f'implement:unit-{i}'],
                      'read_inputs': ['src/shared/schema.json'],
                      'write_scope': [f'src/unit-{i}', f'work/set-{i}'],
                      'outputs': [f'src/unit-{i}/result.txt'],
                      'checks': ['Inspect result'], 'depends_on': [],
                      'state': 'ready'} for i in range(1, 4)]}


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.plan = fixture()

    def errors(self):
        return module.validate(self.plan, self.root)

    def test_separate_outputs_and_shared_reads(self):
        self.assertEqual([], self.errors())

    def test_case_and_dot_alias_conflict(self):
        self.plan['sets'][1]['write_scope'].append('SRC/unit-1/../unit-1')
        self.assertTrue(any('write overlap' in x for x in self.errors()))

    def test_parent_directory_conflict(self):
        self.plan['sets'][2]['write_scope'].append('src')
        self.assertTrue(any('write overlap' in x for x in self.errors()))

    def test_chief_and_worker_same_file(self):
        self.plan['chief_write_scope'].append('src/unit-1/result.txt')
        self.assertTrue(any('write overlap' in x for x in self.errors()))

    def test_unowned_artifact(self):
        self.plan['sets'][1]['outputs'] = ['docs/not-owned.md']
        self.assertTrue(any('outside owned scope' in x for x in self.errors()))

    def test_duplicate_search_work(self):
        self.plan['sets'][0]['work_keys'].append('Research: official auth')
        self.plan['sets'][2]['work_keys'].append('research:   OFFICIAL auth')
        self.assertTrue(any('duplicate work key' in x for x in self.errors()))

    def test_dependency_cycle(self):
        for index in range(3):
            self.plan['sets'][index]['depends_on'] = [f'SET{(index+1)%3+1}']
        self.assertTrue(any('dependency cycle' in x for x in self.errors()))

    def test_linear_dependencies(self):
        self.plan['sets'][1]['depends_on'] = ['SET1']
        self.plan['sets'][2]['depends_on'] = ['SET2']
        self.assertTrue(any('serialize teams' in x for x in self.errors()))

    def test_legacy_plan_rejected(self):
        self.plan['version'] = 1
        self.assertTrue(any('version must be 2' in x for x in self.errors()))

    def test_sequential_or_missing_mode_rejected(self):
        for mode in ('sequential', 'staggered', None):
            with self.subTest(mode=mode):
                self.plan['execution_mode'] = mode
                self.assertTrue(any('parallel-only' in x for x in self.errors()))

    def test_insufficient_capacity_rejected(self):
        for capacity in (4, 12, True, '13', None):
            with self.subTest(capacity=capacity):
                self.plan['capacity_total'] = capacity
                self.assertTrue(any('at least 13' in x for x in self.errors()))

    def test_reviewers_require_additional_slots(self):
        for count in range(1, 4):
            with self.subTest(reviewers=count):
                self.plan['concurrent_reviewers'] = count
                self.plan['capacity_total'] = 12 + count
                self.assertTrue(any(f'at least {13 + count}' in x for x in self.errors()))
                self.plan['capacity_total'] = 13 + count
                self.assertEqual([], self.errors())

    def test_invalid_reviewer_counts_rejected(self):
        for count in (-1, 4, True, '1', None):
            with self.subTest(reviewers=count):
                self.plan['concurrent_reviewers'] = count
                self.assertTrue(any('concurrent_reviewers' in x for x in self.errors()))

    def test_queued_set_rejected(self):
        self.plan['sets'][0]['state'] = 'queued'
        self.assertTrue(any('invalid state' in x for x in self.errors()))

    def test_implicit_chief_plan_reservation(self):
        self.plan['sets'][0]['write_scope'].append('work/three-set/test/plan.json')
        self.assertTrue(any('write overlap' in x for x in self.errors()))

    def test_backslash_paths_are_portable(self):
        self.plan['sets'][0]['write_scope'][0] = 'src\\unit-1'
        self.plan['sets'][0]['outputs'][0] = 'src\\unit-1\\result.txt'
        self.assertEqual([], self.errors())

    def test_symlink_alias_conflict_when_supported(self):
        source = self.root / 'src' / 'unit-1'
        source.mkdir(parents=True)
        try:
            (self.root / 'alias').symlink_to(source, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Host does not permit directory symlinks')
        self.plan['sets'][1]['write_scope'].append('alias')
        self.assertTrue(any('write overlap' in x for x in self.errors()))

    def test_cli_valid_and_invalid_exit_codes(self):
        plan_path = self.root / 'plan.json'
        for valid in (True, False):
            with self.subTest(valid=valid):
                self.plan['execution_mode'] = 'parallel-only' if valid else 'sequential'
                plan_path.write_text(json.dumps(self.plan), encoding='utf-8-sig')
                result = subprocess.run([sys.executable, '-B', str(SCRIPT),
                                         str(plan_path), '--workspace', str(self.root)],
                                        capture_output=True, text=True, check=False)
                self.assertEqual(0 if valid else 2, result.returncode)
                self.assertEqual(valid, json.loads(result.stdout)['valid'])

    def test_cli_malformed_json(self):
        plan_path = self.root / 'broken.json'
        plan_path.write_text('{invalid', encoding='utf-8')
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(plan_path),
                                 '--workspace', str(self.root)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(2, result.returncode)
        self.assertFalse(json.loads(result.stdout)['valid'])

    def test_external_path(self):
        self.plan['sets'][0]['write_scope'].append('../other-project')
        self.assertTrue(any('escapes workspace' in x for x in self.errors()))

    def test_absolute_path(self):
        self.plan['sets'][0]['write_scope'].append('C:\\outside-project')
        self.assertTrue(any('workspace-relative' in x for x in self.errors()))

    def test_cancelled_writer_still_reserves_scope(self):
        self.plan['sets'][0]['state'] = 'cancelled'
        self.plan['sets'][1]['write_scope'].append('src/unit-1')
        self.assertTrue(any('write overlap' in x for x in self.errors()))

    def test_windows_trailing_dot_alias(self):
        self.plan['sets'][1]['write_scope'].append('src/unit-1./result.txt')
        self.assertTrue(any('ambiguous Windows' in x for x in self.errors()))

    def test_windows_trailing_space_alias(self):
        self.plan['sets'][1]['write_scope'].append('src/unit-1 /result.txt')
        self.assertTrue(any('ambiguous Windows' in x for x in self.errors()))

    def test_alternate_stream_path(self):
        self.plan['sets'][1]['write_scope'].append('src/unit-1/result.txt:notes')
        self.assertTrue(any('invalid portable path' in x for x in self.errors()))

    def test_duplicate_set_id(self):
        self.plan['sets'][1]['id'] = 'SET1'
        self.assertTrue(any('duplicate set ID' in x for x in self.errors()))

    def test_bad_dependency_type(self):
        self.plan['sets'][0]['depends_on'] = [{}]
        self.assertTrue(self.errors())

    def test_missing_set(self):
        self.plan['sets'].pop()
        self.assertTrue(self.errors())


if __name__ == '__main__':
    unittest.main(verbosity=2)
