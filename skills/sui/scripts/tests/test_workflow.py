import copy
from datetime import datetime,timedelta,timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from test_helpers import CORE,ROOT,load,resolve,contract,matrix,evidence,sources,pack

state=load('sui','work_state.py')
scope=load('sui','file_scope.py')
proof=load('sui-delivery','verify_evidence.py')
gate=load('sui-delivery','run_gate.py')
routes=load('sui','evaluate_routes.py')

def example():
    return {'schemaVersion':1,'goal':'Add a bounded behavior','requirements':['R1'],'inputs':['code.py'],'tasks':[{'id':'T1','title':'Implement behavior','requirements':['R1'],'dependsOn':[],'checks':['C1'],'status':'planned'}],'checks':[{'id':'C1','status':'planned'}]}

class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'code.py').write_text('value = 1\n');self.data=example()
    def tearDown(self):self.temp.cleanup()
    def save(self):
        state.checkpoint(self.data,self.root,'.sui/state.json','new')
        return json.loads((self.root/'.sui/state.json').read_text())
    def test_ready_task(self):self.assertEqual(state.analyze(self.data)['ready'],['T1'])
    def test_boolean_schema_rejected(self):self.data['schemaVersion']=True;self.assertFalse(state.analyze(self.data)['ok'])
    def test_array_status_rejected(self):self.data['tasks'][0]['status']=[];self.assertFalse(state.analyze(self.data)['ok'])
    def test_object_check_status_rejected(self):self.data['checks'][0]['status']={};self.assertFalse(state.analyze(self.data)['ok'])
    def test_unknown_requirement(self):self.data['tasks'][0]['requirements']=['other'];self.assertFalse(state.analyze(self.data)['ok'])
    def test_duplicate_ids(self):self.data['tasks']*=2;self.assertFalse(state.analyze(self.data)['ok'])
    def test_self_cycle(self):self.data['tasks'][0]['dependsOn']=['T1'];self.assertFalse(state.analyze(self.data)['ok'])
    def test_two_task_cycle(self):
        self.data['tasks'].append({**copy.deepcopy(self.data['tasks'][0]),'id':'T2','dependsOn':['T1']});self.data['tasks'][0]['dependsOn']=['T2'];self.assertFalse(state.analyze(self.data)['ok'])
    def test_unknown_dependency(self):self.data['tasks'][0]['dependsOn']=['missing'];self.assertFalse(state.analyze(self.data)['ok'])
    def test_done_needs_checks(self):self.data['tasks'][0].update(status='done',checks=[]);self.assertFalse(state.analyze(self.data)['ok'])
    def test_done_needs_pass(self):self.data['tasks'][0]['status']='done';self.assertFalse(state.analyze(self.data)['ok'])
    def test_done_is_only_declaration(self):
        self.data['tasks'][0]['status']='done';self.data['checks'][0].update(status='passed',evidenceRef='proof.json')
        r=state.analyze(self.data);self.assertTrue(r['declaredComplete']);self.assertFalse(r['evidenceVerified'])
    def test_pass_needs_evidence_ref(self):self.data['checks'][0]['status']='passed';self.assertFalse(state.analyze(self.data)['ok'])
    def test_blocked_needs_reason(self):self.data['tasks'][0]['status']='blocked';self.assertFalse(state.analyze(self.data)['ok'])
    def test_checkpoint_and_resume(self):saved=self.save();self.assertTrue(state.resume(saved,self.root)['ok'])
    def test_resume_source_drift(self):saved=self.save();(self.root/'code.py').write_text('value = 2\n');self.assertFalse(state.resume(saved,self.root)['ok'])
    def test_resume_scope_drift(self):saved=self.save();saved['inputs']=['other.py'];self.assertFalse(state.resume(saved,self.root)['ok'])
    def test_root_mismatch(self):saved=self.save();self.assertFalse(state.resume(saved,self.root/'other')['ok'])
    def test_overwrite_needs_expected_version(self):self.save();self.assertRaises(ValueError,state.checkpoint,self.data,self.root,'.sui/state.json','new')
    def test_cas_update(self):
        self.save();p=self.root/'.sui/state.json';digest=hashlib.sha256(p.read_bytes()).hexdigest();self.data['nextAction']='Inspect a boundary'
        state.checkpoint(self.data,self.root,p,digest);self.assertEqual(json.loads(p.read_text())['nextAction'],'Inspect a boundary')
    def test_stale_cas_preserves_content(self):
        self.save();p=self.root/'.sui/state.json';before=p.read_bytes();self.assertRaises(ValueError,state.checkpoint,self.data,self.root,p,'0'*64);self.assertEqual(p.read_bytes(),before)
    def test_existing_lock_preserved(self):
        (self.root/'state.json.lock').write_text('owner')
        self.assertRaises(FileExistsError,state.checkpoint,self.data,self.root,'state.json','new');self.assertEqual((self.root/'state.json.lock').read_text(),'owner')
    def test_outside_write_rejected(self):self.assertRaises(ValueError,state.checkpoint,self.data,self.root,self.root.parent/'escape.json','new')
    def test_symlink_parent_write_rejected(self):
        (self.root/'real').mkdir();(self.root/'alias').symlink_to(self.root/'real',target_is_directory=True)
        self.assertRaises(ValueError,state.checkpoint,self.data,self.root,'alias/state.json','new')
    def test_state_cannot_be_input(self):self.data['inputs'].append('state.json');self.assertRaises(ValueError,state.checkpoint,self.data,self.root,'state.json','new')
    def test_null_input_scope(self):self.data['inputs']=None;self.assertRaises(ValueError,state.checkpoint,self.data,self.root,'state.json','new')

class ScopeTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'file.txt').write_text('abc')
    def tearDown(self):self.temp.cleanup()
    def test_stable_digest(self):self.assertEqual(scope.capture(self.root,['file.txt']),scope.capture(self.root,['file.txt']))
    def test_content_change(self):before=scope.capture(self.root,['file.txt']);(self.root/'file.txt').write_text('abd');self.assertNotEqual(before,scope.capture(self.root,['file.txt']))
    def test_explicit_deletion(self):r=scope.capture(self.root,['file.txt','deleted.py']);self.assertIsNone(r['files'][0]['sha256'])
    def test_duplicate_path(self):self.assertRaises(ValueError,scope.capture,self.root,['file.txt','file.txt'])
    def test_empty(self):self.assertRaises(ValueError,scope.capture,self.root,[])
    def test_missing_only(self):self.assertRaises(ValueError,scope.capture,self.root,['absent'])
    def test_directory(self):self.assertRaises(ValueError,scope.capture,self.root,['.'])
    def test_escape(self):self.assertRaises(ValueError,scope.capture,self.root,['../file.txt'])
    def test_backslash(self):self.assertRaises(ValueError,scope.capture,self.root,['a'+chr(92)+'file'])
    def test_null(self):self.assertRaises(ValueError,scope.capture,self.root,['x'+chr(0)])
    def test_credentials(self):self.assertRaises(ValueError,scope.capture,self.root,['.env'])
    def test_symlink(self):(self.root/'alias').symlink_to(self.root/'file.txt');self.assertRaises(ValueError,scope.capture,self.root,['alias'])
    def test_oversized(self):
        with (self.root/'big').open('wb') as f:f.truncate(8388609)
        self.assertRaises(ValueError,scope.capture,self.root,['big'])
    def test_vendored_helpers_match(self):self.assertEqual((CORE/'scripts/file_scope.py').read_bytes(),(resolve('sui-delivery')/'scripts/file_scope.py').read_bytes())

class ProofTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'code.py').write_text('value=1\n')
        import sys
        self.plan={'inputs':['code.py'],'checks':[{'id':'C1','argv':[sys.executable,'-c','pass'],'required':True}]}
        self.report=gate.run(self.plan,self.root,True)
    def tearDown(self):self.temp.cleanup()
    def test_current_evidence(self):self.assertTrue(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_source_drift(self):(self.root/'code.py').write_text('value=2\n');self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_plan_drift(self):self.plan['checks'][0]['timeoutSeconds']=20;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_root_drift(self):self.assertFalse(proof.verify(self.report,self.plan,self.root/'other')['ok'])
    def test_old_evidence(self):self.assertFalse(proof.verify(self.report,self.plan,self.root,now=datetime.now(timezone.utc)+timedelta(days=2))['ok'])
    def test_future_timestamp(self):self.report['finishedAt']=(datetime.now(timezone.utc)+timedelta(days=2)).isoformat();self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_missing_timezone(self):self.report['finishedAt']='2026-10-31T12:00:00';self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_unbound_evidence(self):self.report['inputSnapshot']=None;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_preview_is_not_execution(self):self.report['executed']=False;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_failed_check(self):self.report['checks'][0]['returnCode']=1;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_missing_check(self):self.report['checks']=[];self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_duplicate_check(self):self.report['checks']*=2;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_bad_plan_id_type(self):self.plan['checks'][0]['id']=[];self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_changed_during_execution(self):
        self.plan['checks'][0]['argv'][2]="open('code.py','w').write('value=3')"
        self.assertEqual(gate.run(self.plan,self.root,True)['status'],'inputs_changed')
    def test_invalid_age(self):self.assertRaises(ValueError,proof.verify,self.report,self.plan,self.root,float('nan'))
    def test_huge_timeout(self):self.plan['checks'][0]['timeoutSeconds']=10**400;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_required_flag_mismatch(self):self.report['checks'][0]['required']=False;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_output_limit_not_boolean(self):self.report['checks'][0]['outputLimited']=1;self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])
    def test_declared_binding_mismatch(self):self.report['evidenceScope']='unbound';self.assertFalse(proof.verify(self.report,self.plan,self.root)['ok'])

class RoutingTests(unittest.TestCase):
    def setUp(self):self.gold={'cases':[{'id':'a','acceptablePrimary':['sui-review'],'mode':'standard'},{'id':'b','acceptablePrimary':[None],'mode':None}]};self.pred={'variant':'x','predictions':[{'id':'a','primary':'sui-review','mode':'standard'},{'id':'b','primary':None,'mode':None}]}
    def test_correct(self):self.assertEqual(routes.score(self.gold,self.pred)['jointAccuracy'],1)
    def test_missing_not_dropped(self):self.pred['predictions'].pop();r=routes.score(self.gold,self.pred);self.assertEqual(r['jointAccuracy'],.5);self.assertEqual(r['missingIds'],['b'])
    def test_duplicate_rejected(self):self.pred['predictions']*=2;self.assertRaises(ValueError,routes.score,self.gold,self.pred)
    def test_unknown_rejected(self):self.pred['predictions'][0]['id']='unknown';self.assertRaises(ValueError,routes.score,self.gold,self.pred)
    def test_negative_case(self):self.pred['predictions'][1]['primary']='sui';self.assertEqual(routes.score(self.gold,self.pred)['outOfScopeFalsePositives'],1)
    def test_mode_independent(self):self.pred['predictions'][0]['mode']='critical';r=routes.score(self.gold,self.pred);self.assertEqual(r['primaryAccuracy'],1);self.assertEqual(r['jointAccuracy'],.5)
    def test_empty_gold(self):self.assertRaises(ValueError,routes.score,{'cases':[]},self.pred)
    def test_bad_mode_rejected(self):self.pred['predictions'][0]['mode']=[];self.assertRaises(ValueError,routes.score,self.gold,self.pred)
    def test_full_gold_has_negative_cases(self):g=json.loads((CORE/'assets/routing-evals.json').read_text());self.assertEqual(len(g['cases']),28);self.assertGreaterEqual(sum(c['acceptablePrimary']==[None] for c in g['cases']),6)

class MalformedEnumTests(unittest.TestCase):
    def test_contract_status(self):
        d=json.loads((resolve('sui-discovery')/'assets/contract.example.json').read_text());d['checks'][0]['status']=[];self.assertTrue(contract.validate(d))
    def test_matrix_level(self):
        d=json.loads((resolve('sui-testing')/'assets/matrix.example.json').read_text());d['cases'][0]['level']={};self.assertTrue(matrix.validate(d))
    def test_evidence_status(self):
        d=json.loads((resolve('sui-evidence')/'assets/evidence.example.json').read_text());d['claims'][0]['status']=[];self.assertTrue(evidence.audit(d,'2026-10-31'))
    def test_registry_status(self):
        d=json.loads((CORE/'references/sources.json').read_text());d['sources'][0]['status']={};self.assertTrue(sources.audit(d,'2026-10-31'))

class InventoryRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        for name in pack.NAMES:shutil.copytree(resolve(name),self.root/name,ignore=shutil.ignore_patterns('__pycache__'))
    def tearDown(self):self.temp.cleanup()
    def test_missing_import_helper(self):
        (self.root/'sui-delivery/scripts/file_scope.py').unlink();self.assertFalse(pack.validate(self.root)['ok'])
    def test_manifest_source_count(self):
        p=self.root/'sui/assets/pack.json';d=json.loads(p.read_text());d['sourceCount']=0;p.write_text(json.dumps(d));self.assertFalse(pack.validate(self.root)['ok'])
    def test_manifest_unsafe_path(self):
        p=self.root/'sui/assets/pack.json';d=json.loads(p.read_text());d['requiredFiles']['sui']=['../outside.py'];p.write_text(json.dumps(d));self.assertFalse(pack.validate(self.root)['ok'])

if __name__=='__main__':unittest.main()
