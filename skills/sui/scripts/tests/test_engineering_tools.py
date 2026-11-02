"""Behavioral tests for planning, metrics, RTM, report adapters and local parser exploration."""
import copy
import itertools
import json
import tempfile
import unittest
from pathlib import Path
from test_helpers import load, resolve, asset

planning=load('sui-discovery','project_plan.py')
rtm=load('sui-discovery','traceability.py')
metrics=load('sui-evidence','quality_metrics.py')
design=load('sui-testing','test_design.py')
fuzz=load('sui-testing','fuzz_lab.py')
formats=load('sui-implementation','report_formats.py')
checks=load('sui-implementation','tool_checks.py')
sbom=load('sui-security','sbom_inventory.py')
probe=load('sui-reliability','load_probe.py')

class PlanningTests(unittest.TestCase):
    def test_cocomo_known_case(self):
        r=planning.run('cocomo',{'mode':'organic','kloc':10})
        self.assertAlmostEqual(r['effortPersonMonths'],2.4*10**1.05)
        self.assertAlmostEqual(r['averageStaff'],r['effortPersonMonths']/r['durationMonths'])
    def test_cocomo_invalid(self):
        for data in [{'mode':[],'kloc':10},{'mode':'organic','kloc':True},{'mode':'organic','kloc':10**400}]:
            with self.subTest(data=data),self.assertRaises(ValueError):planning.run('cocomo',data)
    def test_critical_path_and_slack(self):
        r=planning.schedule(asset('sui-discovery','project-plan.example.json'))
        self.assertEqual(r['duration'],7);self.assertEqual(r['criticalTasks'],['A','B','D']);self.assertEqual(r['tasks']['C']['slack'],2)
    def test_multiple_critical_paths(self):
        r=planning.schedule({'unit':'days','tasks':[{'id':'a','duration':1},{'id':'b','duration':1}]})
        self.assertEqual(r['criticalTasks'],['a','b'])
    def test_cycle_and_unknown_dependency(self):
        for dep in ['a','unknown']:
            with self.assertRaises(ValueError):planning.schedule({'unit':'days','tasks':[{'id':'a','duration':1,'dependsOn':[dep]}]})
    def test_bad_duration_and_roles(self):
        with self.assertRaises(ValueError):planning.schedule({'unit':'days','tasks':[{'id':'a','duration':float('nan')}]})
        with self.assertRaises(ValueError):planning.raci({'assignments':[{'task':'a','people':{'p':[[]]}}]})
    def test_raci_accountability(self):
        d=asset('sui-discovery','raci.example.json');self.assertTrue(planning.raci(d)['ok'])
        d['assignments'][0]['people']['engineer']=['A','R'];self.assertFalse(planning.raci(d)['ok'])
    def test_traceability_forward_and_reverse(self):
        d=asset('sui-discovery','traceability.example.json');self.assertEqual(rtm.validate(d),[])
        d['links'].pop();self.assertTrue(any('acceptance' in x for x in rtm.validate(d)))
        self.assertTrue(any('orphan' in x for x in rtm.validate(d)))
    def test_traceability_reasoned_waiver(self):
        d=asset('sui-discovery','traceability.example.json');d['requiredKinds'].append('security');d['artifacts'][0]['waivers']={'security':'Local synthetic educational case; no added security control'}
        self.assertEqual(rtm.validate(d),[])
    def test_dangling_change_and_verified_evidence(self):
        d=asset('sui-discovery','traceability.example.json');d['changes'][0]['affected']=['missing'];self.assertTrue(rtm.validate(d))
        d=asset('sui-discovery','traceability.example.json');d['changes'][0]['status']='verified';self.assertTrue(rtm.validate(d))

class MetricTests(unittest.TestCase):
    def test_halstead_convention(self):self.assertEqual(metrics.run('halstead',{'distinctOperators':2,'distinctOperands':2,'totalTokens':8})['volume'],16)
    def test_bad_vocabulary(self):
        with self.assertRaises(ValueError):metrics.run('halstead',{'distinctOperators':5,'distinctOperands':5,'totalTokens':2})
    def test_cfg_arithmetic(self):
        r=metrics.run('cyclomatic',{'nodes':['entry','left','right','exit'],'edges':[['entry','left'],['entry','right'],['left','exit'],['right','exit']]})
        self.assertEqual(r['complexity'],2)
    def test_cfg_dangling_rejected(self):
        with self.assertRaises(ValueError):metrics.run('cyclomatic',{'nodes':['a'],'edges':[['a','b']]})
    def test_function_points_no_default(self):
        with self.assertRaises(ValueError):metrics.run('function-points',{'counts':{}})
        cats=['EI','EO','EQ','ILF','EIF'];data={'counts':{c:{'simple':1,'average':0,'complex':0} for c in cats},'weights':{c:{'simple':2,'average':3,'complex':4} for c in cats}}
        self.assertEqual(metrics.run('function-points',data)['unadjustedFunctionPoints'],10)
    def test_defect_denominators(self):
        r=metrics.run('defects',{'foundBeforeRelease':8,'escapedAfterRelease':2,'size':5,'sizeUnit':'KLOC','window':'release30days'})
        self.assertEqual(r['faultDensity'],2);self.assertEqual(r['escapeFraction'],.2)
    def test_no_failure_not_infinite(self):self.assertIsNone(metrics.run('reliability',{'operatingExposure':100,'failures':0,'timeUnit':'hours'})['meanOperatingTimeBetweenObservedFailures'])
    def test_no_exposure_rejected_with_failures(self):
        with self.assertRaises(ValueError):metrics.run('reliability',{'operatingExposure':0,'failures':1,'timeUnit':'hours'})
    def test_latency_mixture(self):
        r=metrics.run('latency',{'samples':[10]*9+[5210],'unit':'ms'})
        self.assertEqual(r['mean'],530);self.assertEqual(r['p95'],5210)
    def test_bad_metric_types(self):
        for x in [True,float('nan'),10**400]:
            with self.subTest(x=x),self.assertRaises(ValueError):metrics.run('latency',{'samples':[x]})

class DesignTests(unittest.TestCase):
    def test_pairwise_all_pairs_independently(self):
        factors={'os':['a','b'],'browser':['x','y','z'],'role':['user','admin']};r=design.pairwise(factors)
        for first,second in itertools.combinations(factors,2):
            observed={(row[first],row[second]) for row in r['cases']}
            self.assertEqual(observed,set(itertools.product(factors[first],factors[second])))
    def test_pairwise_bounded_and_bad_levels(self):
        for factors in [{'x':[[]],'y':[1]},{str(i):list(range(8)) for i in range(8)}]:
            with self.assertRaises(ValueError):design.pairwise(factors)
    def test_null_short_circuit_not_false(self):
        r=design.avg_abs_trace(None);self.assertIsNone(r['conditions'][1]['value']);self.assertEqual(r['error'],'IllegalArgumentException')
    def test_empty_evaluates_second_condition(self):self.assertTrue(design.avg_abs_trace([])['conditions'][1]['value'])
    def test_mixed_paths_and_mean(self):
        r=design.avg_abs_trace([-2,2]);self.assertEqual(r['value'],2);self.assertIn('subtract-negative',r['statements']);self.assertIn('add-nonnegative',r['statements'])
    def test_seeded_fuzz_repeatability(self):self.assertEqual(fuzz.run(12,1000),fuzz.run(12,1000))
    def test_valid_frames_are_exercised(self):self.assertGreaterEqual(fuzz.run(1,1000)['accepted'],500)
    def test_minimizer_preserves_failure_predicate(self):self.assertEqual(fuzz.minimize(b'abcXdef',lambda raw:b'X' in raw),b'X')
    def test_fuzz_captures_a_replayable_unexpected_fault(self):
        from unittest.mock import patch
        with patch.object(fuzz.framed,'decode',return_value=b''):
            r=fuzz.run(1,10);self.assertEqual(r['unexpectedFailures'],1)
            with self.assertRaises(AssertionError):fuzz.exercise(bytes.fromhex(r['inputHex']),r['expectValid'])

class ReportTests(unittest.TestCase):
    def test_empty_analysis_scope_is_not_clean(self):
        for format_,raw in [('spotbugs','<BugCollection/>'),('checkstyle','<checkstyle/>'),('nmap','<nmaprun><runstats><finished exit="success"/></runstats></nmaprun>')]:
            with self.subTest(format_=format_),self.assertRaises(ValueError):formats.parse(format_,raw)
    def test_spotbugs_failure_flags_and_summary(self):
        valid='<BugCollection><FindBugsSummary total_classes="1"/></BugCollection>'
        self.assertEqual(formats.parse('spotbugs',valid)['findingCount'],0)
        with self.assertRaises(ValueError):formats.parse('spotbugs',valid,2)
        faulty='<BugCollection><BugInstance type="NP"><LongMessage>null</LongMessage></BugInstance></BugCollection>'
        self.assertEqual(formats.parse('spotbugs',faulty,1)['findingCount'],1)
        with self.assertRaises(ValueError):formats.parse('spotbugs',faulty,4)
    def test_invocation_status_must_be_boolean(self):
        d={'version':'2.1.0','runs':[{'tool':{'driver':{'name':'fixture'}},'results':[],'invocations':[{'executionSuccessful':[]}]}]}
        with self.assertRaises(ValueError):formats.parse('sarif',json.dumps(d))
    def test_failed_import_return_codes_cannot_be_normalized(self):
        cases=[('snyk','{"ok":false,"vulnerabilities":[]}',2),('sarif','{"version":"2.1.0","runs":[{"tool":{"driver":{"name":"lab"}},"results":[]}]}',-9),('junit','<testsuite><testcase name="one"/></testsuite>',2)]
        for format_,raw,code in cases:
            with self.subTest(format_=format_),self.assertRaises(ValueError):formats.parse(format_,raw,code)
    def test_mypy_diagnostic_and_no_tests_confusion(self):
        r=formats.parse('mypy','app.py:1:2: error: bad assignment  [assignment]\n',1)
        self.assertEqual(r['findingCount'],1);self.assertEqual(r['findings'][0]['rule'],'assignment')
        with self.assertRaises(ValueError):formats.parse('mypy','missing dependency',2)
    def test_tsc_diagnostic(self):self.assertEqual(formats.parse('tsc','a.ts(1,2): error TS2322: wrong type',2)['findings'][0]['rule'],'TS2322')
    def test_sarif_empty_run_and_failed_invocation(self):
        d={'version':'2.1.0','runs':[{'tool':{'driver':{'name':'fixture'}},'results':[]}]}
        self.assertEqual(formats.parse('sarif',json.dumps(d))['findingCount'],0)
        d['runs'][0]['invocations']=[{'executionSuccessful':False}]
        with self.assertRaises(ValueError):formats.parse('sarif',json.dumps(d))
    def test_sarif_suppressions_preserved(self):
        d={'version':'2.1.0','runs':[{'tool':{'driver':{'name':'fixture'}},'results':[{'ruleId':'R','message':{'text':'diagnostic'},'suppressions':[{'kind':'inSource'}]}]}]}
        self.assertTrue(formats.parse('sarif',json.dumps(d))['findings'][0]['suppressed'])
    def test_sarif_malformed_nested(self):
        for d in [{'version':'2.1.0','runs':[]},{'version':'2.1.0','runs':[{'tool':[]}]},[]]:
            with self.subTest(d=d),self.assertRaises(ValueError):formats.parse('sarif',json.dumps(d))
    def test_spotbugs_missing_class_not_clean(self):
        with self.assertRaises(ValueError):formats.parse('spotbugs','<BugCollection><Errors><MissingClass>x</MissingClass></Errors></BugCollection>')
    def test_spotbugs_bug(self):self.assertEqual(formats.parse('spotbugs','<BugCollection><BugInstance type="NP"><LongMessage>null</LongMessage></BugInstance></BugCollection>')['findingCount'],1)
    def test_checkstyle(self):self.assertEqual(formats.parse('checkstyle','<checkstyle><file name="a"><error line="2" message="bad" source="rule"/></file></checkstyle>')['findingCount'],1)
    def test_sonar_pagination_not_clean(self):
        with self.assertRaises(ValueError):formats.parse('sonar',json.dumps({'issues':[],'paging':{'total':2}}))
    def test_snyk_error_not_clean(self):
        with self.assertRaises(ValueError):formats.parse('snyk',json.dumps({'ok':False,'error':'unauthorized'}))
    def test_infer(self):self.assertEqual(formats.parse('infer',json.dumps([{'bug_type':'NULL','qualifier':'deref','file':'a','line':2}]))['findingCount'],1)
    def test_junit_cases_not_only_aggregate(self):
        with self.assertRaises(ValueError):formats.parse('junit','<testsuite tests="10"/>')
        with self.assertRaises(ValueError):formats.parse('junit','<testsuite><testcase name="one"><skipped/></testcase></testsuite>')
        r=formats.parse('junit','<testsuite tests="1"><testcase name="one"><failure/></testcase></testsuite>');self.assertEqual(r['failed'],1)
        with self.assertRaises(ValueError):formats.parse('junit','<testsuite tests="1" failures="1"><testcase name="one"/></testsuite>')
    def test_external_doctype_header_is_ignored_without_fetching(self):
        nmap='<!DOCTYPE nmaprun><nmaprun><host><status state="down"/></host><runstats><finished exit="success"/></runstats></nmaprun>'
        self.assertTrue(formats.parse('nmap',nmap)['observationsOnly'])
        jacoco='<!DOCTYPE report PUBLIC "-//JACOCO//DTD Report 1.1//EN" "report.dtd"><report><counter type="BRANCH" missed="1" covered="1"/></report>'
        self.assertEqual(formats.parse('jacoco',jacoco)['counters']['BRANCH']['total'],2)
    def test_coverage_empty_rejected(self):
        with self.assertRaises(ValueError):formats.parse('coverage-py',json.dumps({'files':{},'totals':{'covered_lines':0,'num_statements':0}}))
    def test_jacoco(self):self.assertEqual(formats.parse('jacoco','<report><counter type="BRANCH" missed="2" covered="3"/></report>')['counters']['BRANCH']['total'],5)
    def test_nmap_completion_required(self):
        with self.assertRaises(ValueError):formats.parse('nmap','<nmaprun/>')
        r=formats.parse('nmap','<nmaprun><host><status state="down"/></host><runstats><finished exit="success"/></runstats></nmaprun>');self.assertTrue(r['observationsOnly'])
    def test_zap_scope_required(self):
        with self.assertRaises(ValueError):formats.parse('zap','{"site":[]}')
    def test_external_entities_rejected(self):
        with self.assertRaises(ValueError):formats.parse('junit','<!DOCTYPE x [<!ENTITY e SYSTEM "file:///etc/passwd">]><testsuite/>')
    def test_source_filename_cannot_be_an_option(self):self.assertEqual(checks.command('gcc',['--help.c'])[-1],'./--help.c')
    def test_missing_tool_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'a.py').write_text('x=1')
            self.assertEqual(checks.run('mypy',tmp,['a.py'],True,'/nonexistent-sui-tool')['status'],'blocked')
    def test_symlinks_not_fingerprinted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'a').write_text('x');(p/'b').symlink_to(p/'a')
            with self.assertRaises(ValueError):checks.snapshot(p,['b'])

class LoadProbeTests(unittest.TestCase):
    def test_remote_target_is_not_implicitly_authorized(self):
        with self.assertRaises(ValueError):probe.validate('http://example.com/')
    def test_preview_has_no_execution(self):self.assertFalse(probe.demo(execute=False)['executed'])
    def test_local_demo_collects_actual_requests(self):
        r=probe.demo(requests=4,concurrency=2,execute=True,max_p95_ms=5000)
        self.assertEqual(r['status'],'passed');self.assertEqual(r['sampleCount'],4)
    def test_total_deadline_cannot_be_extended_by_trickle(self):
        import threading,time
        from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200);self.send_header('Content-Length','10000');self.end_headers()
                try:
                    for _ in range(15):self.wfile.write(b'x');self.wfile.flush();time.sleep(.1)
                except (BrokenPipeError,ConnectionResetError):pass
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            started=time.monotonic();r=probe.probe(f'http://127.0.0.1:{server.server_port}/',requests=1,timeout=.3,execute=True,max_seconds=.4)
            self.assertTrue(r['deadlineReached']);self.assertLess(time.monotonic()-started,3);self.assertNotEqual(r['status'],'passed')
        finally:server.shutdown();server.server_close();thread.join(2)

def bom(licenses=None):
    return {'bomFormat':'CycloneDX','specVersion':'1.6','components':[{'bom-ref':'lib','name':'example','version':'1','licenses':licenses or [{'license':{'id':'MIT'}}]}]}

class SbomTests(unittest.TestCase):
    def test_spdx_package_graph(self):
        d={'spdxVersion':'SPDX-2.3','SPDXID':'SPDXRef-DOCUMENT','documentNamespace':'https://example.test/lab','packages':[{'SPDXID':'SPDXRef-a','name':'a','licenseDeclared':'MIT'},{'SPDXID':'SPDXRef-b','name':'b','licenseDeclared':'NOASSERTION'}],'relationships':[{'spdxElementId':'SPDXRef-a','relationshipType':'DEPENDS_ON','relatedSpdxElement':'SPDXRef-b'}]}
        r=sbom.normalize(d);self.assertEqual(len(r['components']),2);self.assertEqual(r['dependencies'],[['SPDXRef-a','SPDXRef-b']])
    def test_swid_supported_namespace(self):
        r=sbom.normalize('<SoftwareIdentity xmlns="http://standards.iso.org/iso/19770/-2/2015/schema.xsd" tagId="lab" name="example" version="1"/>')
        self.assertEqual(r['components'][0]['id'],'lab');self.assertEqual(r['components'][0]['licenses'],['NOASSERTION'])
    def test_supported_inventory(self):self.assertEqual(sbom.normalize(bom())['components'][0]['licenses'],['MIT'])
    def test_transitive_dependencies_and_dangling(self):
        d=bom();d['dependencies']=[{'ref':'lib','dependsOn':['unknown']}]
        with self.assertRaises(ValueError):sbom.normalize(d)
    def test_duplicate_identity(self):
        d=bom();d['components']*=2
        with self.assertRaises(ValueError):sbom.normalize(d)
    def test_unknown_and_dual_expression_need_review(self):
        for licenses in [[],[{'expression':'MIT OR GPL-3.0-only'}]]:
            d=bom();d['components'][0]['licenses']=licenses
            self.assertEqual(sbom.policy(sbom.normalize(d),{'allow':['MIT']})['needsReview'],1)
    def test_license_allow_and_deny(self):
        self.assertEqual(sbom.policy(sbom.normalize(bom()),{'deny':['MIT']})['denied'],1)
        self.assertEqual(sbom.policy(sbom.normalize(bom()),{'allow':['MIT']})['needsReview'],0)
    def test_policy_contradiction_rejected(self):
        with self.assertRaises(ValueError):sbom.policy(sbom.normalize(bom()),{'allow':['MIT'],'deny':['MIT']})
    def test_swid_dtd_rejected(self):
        with self.assertRaises(ValueError):sbom.normalize('<!DOCTYPE bad><SoftwareIdentity/>')
    def test_empty_inventory_not_a_clean_result(self):
        d=bom();d['components']=[]
        with self.assertRaises(ValueError):sbom.normalize(d)

if __name__=='__main__':unittest.main()
