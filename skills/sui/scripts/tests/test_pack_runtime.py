"""Regression cases from the capability audit and malformed external inputs."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from test_helpers import load, resolve, asset

evaluation = load('sui-ai-systems', 'eval_report.py')
gate = load('sui-delivery', 'run_gate.py')
proof = load('sui-delivery', 'verify_evidence.py')
pack = load('sui', 'validate_pack.py')

class AuditRegressionTests(unittest.TestCase):
    def test_unhashable_split_is_a_validation_error(self):
        for invalid in [[], {}, None, 1, True]:
            data = asset('sui-ai-systems', 'eval.example.json')
            data['trials'][0]['split'] = invalid
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                evaluation.report(data)

    def test_huge_metrics_are_validation_errors(self):
        for field in ['costUsd', 'latencyMs']:
            data = asset('sui-ai-systems', 'eval.example.json')
            data['trials'][0][field] = 10**400
            with self.subTest(field=field), self.assertRaises(ValueError):
                evaluation.report(data)
    def test_total_cost_overflow_is_a_validation_error(self):
        data=asset('sui-ai-systems','eval.example.json')
        for row in data['trials']:row['costUsd']=1e308
        row=copy.deepcopy(data['trials'][0]);row['trialId']='overflow-extra';data['trials'].append(row)
        with self.assertRaises(ValueError):evaluation.report(data)

    def test_aba_has_only_the_declared_endpoint_guarantee(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'input.txt').write_text('original')
            program = "from pathlib import Path; p=Path('input.txt'); old=p.read_bytes(); p.write_bytes(b'temporary'); p.write_bytes(old)"
            plan = {'inputs':['input.txt'], 'checks':[{'id':'aba','argv':[sys.executable,'-c',program]}]}
            report = gate.run(plan, root, True)
            self.assertEqual(report['status'], 'passed')
            self.assertEqual(report['inputBinding'], 'endpoint-content-equality')
            self.assertIn('ABA', report['limitations'])
            self.assertTrue(proof.verify(report, plan, root)['ok'])
            del report['inputBinding']
            self.assertFalse(proof.verify(report, plan, root)['ok'])

    def test_inventory_cannot_be_omitted(self):
        # Use the installed pack for reads; patch the manifest read in memory.
        from unittest.mock import patch
        manifest = resolve('sui')/'assets/pack.json'
        original = Path.read_text
        changed = json.loads(original(manifest)); changed.pop('requiredFiles')
        def read(path, *args, **kwargs):
            return json.dumps(changed) if path == manifest else original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', read):
            result = pack.validate(resolve('sui').parent)
        self.assertFalse(result['ok'])
        self.assertTrue(any('mandatory' in x for x in result['errors']))

if __name__ == '__main__':
    unittest.main()
