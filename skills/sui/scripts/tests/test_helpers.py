"""Behavioral regression tests for Sui helpers; no network or production mutations."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

CORE=Path(__file__).resolve().parents[2]
ROOT=CORE.parent
def resolve(name):
    for p in ROOT.glob('*/SKILL.md'):
        if ('\nname: '+name+'\n') in p.read_text().split('---',2)[1]+'\n':
            return p.parent
    raise RuntimeError('Required companion skill missing: '+name)

def load(skill,filename):
    p=resolve(skill)/'scripts'/filename
    spec=importlib.util.spec_from_file_location(skill.replace('-','_')+'_'+filename.replace('.','_'),p)
    module=importlib.util.module_from_spec(spec)
    sys.path.insert(0,str(p.parent))
    try:spec.loader.exec_module(module)
    finally:sys.path.pop(0)
    return module

contract=load('sui-discovery','validate_contract.py')
matrix=load('sui-testing','validate_test_matrix.py')
gate=load('sui-delivery','run_gate.py')
slo=load('sui-reliability','slo_report.py')
evaluation=load('sui-ai-systems','eval_report.py')
evidence=load('sui-evidence','audit_evidence.py')
sources=load('sui','source_audit.py')
inventory=load('sui','inspect_repo.py')
pack=load('sui','validate_pack.py')

def asset(skill,name):return json.loads((resolve(skill)/'assets'/name).read_text())

class ContractTests(unittest.TestCase):
    def setUp(self):self.data=asset('sui-discovery','contract.example.json')
    def test_valid_plan(self):self.assertEqual(contract.validate(self.data),[])
    def test_empty(self):self.assertTrue(contract.validate({}))
    def test_duplicate_id(self):self.data['requirements']*=2;self.assertTrue(contract.validate(self.data))
    def test_unknown_ref(self):self.data['checks'][0]['requirements']=['R2'];self.assertTrue(contract.validate(self.data))
    def test_uncovered_requirement(self):self.data['checks'][0]['requirements']=[];self.assertTrue(contract.validate(self.data))
    def test_blank_acceptance(self):self.data['requirements'][0]['acceptance']=[' '];self.assertTrue(contract.validate(self.data))
    def test_pass_needs_evidence(self):self.data['checks'][0]['status']='passed';self.assertTrue(contract.validate(self.data))
    def test_non_object(self):self.assertTrue(contract.validate([]))
    def test_bad_ref_type(self):self.data['checks'][0]['requirements']=[{}];self.assertTrue(contract.validate(self.data))

class MatrixTests(unittest.TestCase):
    def setUp(self):self.data=asset('sui-testing','matrix.example.json')
    def test_valid(self):self.assertEqual(matrix.validate(self.data),[])
    def test_empty_cases(self):self.data['cases']=[];self.assertTrue(matrix.validate(self.data))
    def test_invalid_level(self):self.data['cases'][0]['level']='magical';self.assertTrue(matrix.validate(self.data))
    def test_missing_oracle(self):self.data['cases'][0]['oracle']='';self.assertTrue(matrix.validate(self.data))
    def test_string_command(self):self.data['cases'][0]['command']='echo test';self.assertTrue(matrix.validate(self.data))
    def test_skipped_reason(self):self.data['cases'][0]['status']='skipped';self.assertTrue(matrix.validate(self.data))
    def test_duplicate_case(self):self.data['cases']*=2;self.assertTrue(matrix.validate(self.data))
    def test_unknown_ref(self):self.data['cases'][0]['requirements']=['unrelated'];self.assertTrue(matrix.validate(self.data))

class GateTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def plan(self,code='pass',**kwargs):
        c={'id':'test','argv':[sys.executable,'-c',code],'timeoutSeconds':2};c.update(kwargs)
        return {'checks':[c]}
    def test_preview_does_not_execute(self):
        r=gate.run(self.plan("open('unexpected','w').write('x')"),self.root)
        self.assertEqual(r['status'],'preview');self.assertFalse((self.root/'unexpected').exists())
    def test_pass(self):self.assertEqual(gate.run(self.plan(),self.root,True)['status'],'passed')
    def test_failure(self):self.assertEqual(gate.run(self.plan('raise SystemExit(7)'),self.root,True)['checks'][0]['returnCode'],7)
    def test_missing_binary_is_blocked(self):
        p=self.plan();p['checks'][0]['argv']=['/nonexistent-sui-command'];r=gate.run(p,self.root,True)
        self.assertEqual(r['checks'][0]['status'],'blocked');self.assertEqual(r['status'],'failed')
    def test_timeout(self):self.assertEqual(gate.run(self.plan('import time; time.sleep(5)',timeoutSeconds=.04),self.root,True)['checks'][0]['status'],'timeout')
    def test_escape(self):self.assertEqual(gate.run(self.plan(cwd='..'),self.root)['status'],'invalid')
    def test_symlink_escape(self):
        (self.root/'outside').symlink_to(self.root.parent,target_is_directory=True)
        self.assertEqual(gate.run(self.plan(cwd='outside'),self.root)['status'],'invalid')
    def test_string_argv(self):p=self.plan();p['checks'][0]['argv']='echo hi';self.assertTrue(gate.validate(p,self.root))
    def test_boolean_timeout(self):self.assertTrue(gate.validate(self.plan(timeoutSeconds=True),self.root))
    def test_nan_timeout(self):self.assertTrue(gate.validate(self.plan(timeoutSeconds=float('nan')),self.root))
    def test_optional_only_not_passed(self):self.assertEqual(gate.run(self.plan(required=False),self.root,True)['status'],'incomplete')
    def test_empty_plan_not_passed(self):self.assertEqual(gate.run({'checks':[]},self.root,True)['status'],'invalid')
    def test_no_implicit_shell(self):
        p=self.plan();p['checks'][0]['argv']=[sys.executable,'-c','import sys; print(sys.argv[1])','$(touch leaked)']
        self.assertEqual(gate.run(p,self.root,True)['status'],'passed');self.assertFalse((self.root/'leaked').exists())
    def test_output_suppressed(self):
        r=gate.run(self.plan("print('FAKE_TEST_SECRET')"),self.root,True)
        self.assertNotIn('FAKE_TEST_SECRET',json.dumps(r));self.assertGreater(r['checks'][0]['outputBytes'],0)
    def test_output_limit(self):
        r=gate.run(self.plan("import sys; sys.stdout.write('x'*3000000)"),self.root,True)
        self.assertEqual(r['checks'][0]['status'],'output_limit');self.assertLessEqual(r['checks'][0]['outputBytes'],2097152)
    def test_duplicates(self):p=self.plan();p['checks']*=2;self.assertTrue(gate.validate(p,self.root))
    @unittest.skipUnless(os.name=='posix','POSIX process-group check')
    def test_redirected_descendant_is_not_success(self):
        code="import subprocess,sys; subprocess.Popen([sys.executable,'-c','import time; time.sleep(5)'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)"
        r=gate.run(self.plan(code,timeoutSeconds=.5),self.root,True)
        self.assertEqual(r['status'],'failed');self.assertEqual(r['checks'][0]['status'],'descendants_running')

class SloTests(unittest.TestCase):
    def setUp(self):self.data=asset('sui-reliability','events.example.json')
    def test_boundary(self):r=slo.report(self.data,.999);self.assertEqual(r['status'],'within_objective');self.assertAlmostEqual(r['budgetConsumedFraction'],1)
    def test_exceeded(self):self.data['good']=9980;self.assertEqual(slo.report(self.data,.999)['status'],'exceeded')
    def test_no_traffic(self):self.data.update(good=0,eligible=0);self.assertEqual(slo.report(self.data,.999)['status'],'no_data')
    def test_impossible_counts(self):self.data['good']=11000;self.assertRaises(ValueError,slo.report,self.data,.999)
    def test_boolean_counts(self):self.data['good']=True;self.assertRaises(ValueError,slo.report,self.data,.999)
    def test_target_one(self):self.assertRaises(ValueError,slo.report,self.data,1)
    def test_nan(self):self.assertRaises(ValueError,slo.report,self.data,float('nan'))
    def test_unit(self):self.data['unit']='minutes';self.assertRaises(ValueError,slo.report,self.data,.999)

class EvalTests(unittest.TestCase):
    def setUp(self):self.data=asset('sui-ai-systems','eval.example.json')
    def test_valid(self):r=evaluation.report(self.data);self.assertEqual(r['comparisons'][0]['pairedMeanPassRateDelta'],1)
    def test_boolean_required(self):self.data['trials'][0]['passed']='false';self.assertRaises(ValueError,evaluation.report,self.data)
    def test_leakage(self):r=copy.deepcopy(self.data['trials'][0]);r['split']='train';self.data['trials'].append(r);self.assertRaises(ValueError,evaluation.report,self.data)
    def test_no_holdout(self):
        for r in self.data['trials']:r['split']='dev'
        self.assertRaises(ValueError,evaluation.report,self.data)
    def test_negative_cost(self):self.data['trials'][0]['costUsd']=-1;self.assertRaises(ValueError,evaluation.report,self.data)
    def test_nan_latency(self):self.data['trials'][0]['latencyMs']=float('nan');self.assertRaises(ValueError,evaluation.report,self.data)
    def test_case_weighting(self):
        rows=[{'caseId':'easy','variant':'v','split':'test','passed':True,'latencyMs':1,'costUsd':0} for _ in range(10)]
        rows.append({'caseId':'hard','variant':'v','split':'test','passed':False,'latencyMs':1,'costUsd':0})
        self.assertEqual(evaluation.report({'trials':rows})['variants']['v']['caseWeightedPassRate'],.5)
    def test_mismatched_cases_flagged(self):self.data['trials'][1]['caseId']='other';r=evaluation.report(self.data);self.assertFalse(r['comparisons'][0]['sameCaseSet']);self.assertIsNone(r['comparisons'][0]['pairedMeanPassRateDelta'])
    def test_percentile(self):self.assertEqual(evaluation.percentile([1,2,3,4,100],.95),100)
    def test_duplicate_trial_id(self):
        r=copy.deepcopy(self.data['trials'][0]);r['trialId']='x';self.data['trials']=[r,copy.deepcopy(r)]
        self.assertRaises(ValueError,evaluation.report,self.data)

class EvidenceTests(unittest.TestCase):
    def setUp(self):self.data=asset('sui-evidence','evidence.example.json')
    def test_valid(self):self.assertEqual(evidence.audit(self.data,'2026-10-31'),[])
    def test_missing_source(self):self.data['claims'][0]['sources']=['missing'];self.assertTrue(evidence.audit(self.data,'2026-10-31'))
    def test_future_date(self):self.data['sources'][0]['checkedAt']='2027-01-01';self.assertTrue(evidence.audit(self.data,'2026-10-31'))
    def test_credentials(self):self.data['sources'][0]['url']='https://user:password@example.org';self.assertTrue(evidence.audit(self.data,'2026-10-31'))
    def test_unverified_allowed(self):self.data['claims'][0].update(status='unverified',sources=[]);self.assertEqual(evidence.audit(self.data,'2026-10-31'),[])
    def test_inference_needs_source(self):self.data['claims'][0].update(status='inference',sources=[]);self.assertTrue(evidence.audit(self.data,'2026-10-31'))
    def test_stale_versioned(self):self.data['sources'][0].update(kind='versioned',checkedAt='2025-01-01');self.assertTrue(evidence.audit(self.data,'2026-10-31'))

class SourceTests(unittest.TestCase):
    def test_registry(self):self.assertEqual(sources.audit(json.loads((CORE/'references/sources.json').read_text()),'2026-11-01'),[])
    def test_empty(self):self.assertTrue(sources.audit({'sources':[]},'2026-10-31'))
    def test_stale(self):
        d=json.loads((CORE/'references/sources.json').read_text());self.assertTrue(sources.audit(d,'2027-10-31'))

class InventoryTests(unittest.TestCase):
    def test_no_contents_or_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'package.json').write_text('{"scripts":{"test":"touch EXECUTED"},"secret":"FAKE_TEST_SECRET"}')
            (p/'test_sample.py').write_text('raise RuntimeError("must not import")')
            (p/'.env').write_text('PRIVATE_VALUE=FAKE_TEST_SECRET')
            (p/'node_modules').mkdir();(p/'node_modules/hidden').write_text('x')
            r=inventory.inspect(p)
            self.assertIn('package.json',r['manifests']);self.assertFalse(r['contentsRead']);self.assertNotIn('FAKE_TEST_SECRET',json.dumps(r));self.assertFalse((p/'EXECUTED').exists())
    def test_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(5):(Path(tmp)/str(i)).touch()
            self.assertTrue(inventory.inspect(tmp,2)['truncated'])
    def test_invalid_root(self):self.assertRaises(ValueError,inventory.inspect,'/no-sui-fixture')

class PackTests(unittest.TestCase):
    def test_pack_resolves(self):self.assertTrue(pack.validate(ROOT)['ok'])
    def test_resolution_after_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'skill-opaque';p.mkdir();(p/'SKILL.md').write_text('---\nname: sui\ndescription: test\n---\n')
            self.assertEqual(pack.resolve(tmp)['sui'],[p])
    def test_missing_companions_not_success(self):
        with tempfile.TemporaryDirectory() as tmp:self.assertFalse(pack.validate(tmp)['ok'])
    def test_missing_command_helper_not_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in pack.NAMES:shutil.copytree(resolve(name),Path(tmp)/name)
            (Path(tmp)/'sui/scripts/inspect_repo.py').unlink()
            result=pack.validate(tmp)
            self.assertFalse(result['ok']);self.assertTrue(any('inspect_repo.py' in e for e in result['errors']))

class CliTests(unittest.TestCase):
    def test_all_helpers_executable(self):
        paths=[resolve(s)/'scripts'/f for s,f in [('sui','inspect_repo.py'),('sui','source_audit.py'),('sui','validate_pack.py'),('sui-discovery','validate_contract.py'),('sui-testing','validate_test_matrix.py'),('sui-delivery','run_gate.py'),('sui-reliability','slo_report.py'),('sui-ai-systems','eval_report.py'),('sui-evidence','audit_evidence.py')]]
        for p in paths:
            r=subprocess.run([sys.executable,str(p),'--help'],capture_output=True,timeout=5)
            self.assertEqual(r.returncode,0,str(p))

if __name__=='__main__':unittest.main()
