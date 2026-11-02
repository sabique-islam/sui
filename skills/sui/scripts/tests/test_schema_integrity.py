"""Pinned-cache validation, reference bases and strict JSON regressions."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from test_helpers import load, resolve

schema=load('sui-security','schema_check.py')
coverage=load('sui','check_coverage.py')
HAS_JSON=bool(importlib.util.find_spec('jsonschema')) and bool(importlib.util.find_spec('referencing'))
HAS_XML=bool(importlib.util.find_spec('lxml'))

class SchemaTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def fixture(self,files,document,kind='json'):
        rows=[]
        for name,content in files.items():
            raw=(json.dumps(content) if isinstance(content,(dict,bool)) else content).encode()
            (self.root/name).write_bytes(raw)
            rows.append({'path':name,'uri':'https://example.test/'+name,'sha256':hashlib.sha256(raw).hexdigest()})
        manifest=self.root/'manifest.json';manifest.write_text(json.dumps({'type':kind,'root':next(iter(files)),'files':rows}))
        input_=self.root/'input';input_.write_text(document)
        return input_,manifest
    def test_hash_drift_is_rejected(self):
        inp,manifest=self.fixture({'root.json':{'type':'integer'}},'1')
        (self.root/'root.json').write_text('{}')
        with self.assertRaises(ValueError):schema.cached(manifest)
    def test_traversal_is_rejected(self):
        inp,manifest=self.fixture({'root.json':{}},'1')
        data=json.loads(manifest.read_text());data['files'][0]['path']='../outside';manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):schema.cached(manifest)
    @unittest.skipUnless(HAS_JSON,'extended JSON-schema dependency not installed')
    def test_relative_ref_uses_manifest_base(self):
        inp,manifest=self.fixture({'root.json':{'$ref':'child.json'},'child.json':{'type':'integer'}},'1')
        self.assertTrue(schema.validate(inp,manifest)['ok'])
        inp.write_text('"wrong"');self.assertFalse(schema.validate(inp,manifest)['ok'])
    @unittest.skipUnless(HAS_JSON,'extended JSON-schema dependency not installed')
    def test_non_json_numbers_and_duplicate_keys_rejected(self):
        inp,manifest=self.fixture({'root.json':{'type':'number'}},'NaN')
        with self.assertRaises(ValueError):schema.validate(inp,manifest)
        for raw in ['Infinity','-Infinity','{"a":1,"a":2}']:
            with self.assertRaises(ValueError):schema.strict_json(raw)
    @unittest.skipUnless(HAS_JSON,'extended JSON-schema dependency not installed')
    def test_referenced_schema_is_schema_checked(self):
        from jsonschema.exceptions import SchemaError
        inp,manifest=self.fixture({'root.json':{'$ref':'child.json'},'child.json':{'type':'object','required':'name'}},'{}')
        with self.assertRaises(SchemaError):schema.validate(inp,manifest)
    @unittest.skipUnless(HAS_JSON,'extended JSON-schema dependency not installed')
    def test_child_inherits_root_dialect_policy(self):
        inp,manifest=self.fixture({'root.json':{'$schema':'https://json-schema.org/draft/2020-12/schema','$ref':'child.json'},'child.json':{'type':'array','prefixItems':[{'type':'integer'}]}},'["bad"]')
        self.assertFalse(schema.validate(inp,manifest)['ok'])
    @unittest.skipUnless(HAS_JSON,'extended JSON-schema dependency not installed')
    def test_unknown_dialect_rejected(self):
        inp,manifest=self.fixture({'root.json':{'$schema':'https://example.test/unknown'}},'1')
        with self.assertRaises(ValueError):schema.validate(inp,manifest)
    @unittest.skipUnless(HAS_XML,'extended XSD dependency not installed')
    def test_cached_xsd_include(self):
        inp,manifest=self.fixture({'root.xsd':'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:include schemaLocation="child.xsd"/></xs:schema>','child.xsd':'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="x" type="xs:integer"/></xs:schema>'},'<x>1</x>','xsd')
        self.assertTrue(schema.validate(inp,manifest)['ok']);inp.write_text('<x>bad</x>');self.assertFalse(schema.validate(inp,manifest)['ok'])

class CoverageIntegrityTests(unittest.TestCase):
    def setUp(self):self.root=resolve('sui').parent;self.data=json.loads((resolve('sui')/'assets/capability-coverage.json').read_text())
    def test_all_audit_entries_resolve(self):self.assertTrue(coverage.check(self.root,self.data)['ok'])
    def test_lost_entry_detected(self):self.data['items'].pop();self.assertFalse(coverage.check(self.root,self.data)['ok'])
    def test_missing_reference_detected(self):self.data['items'][0]['resources'][0]['path']='references/does-not-exist.md';self.assertFalse(coverage.check(self.root,self.data)['ok'])
    def test_invalid_tier_container(self):self.data['items'][0]['resolutionTier']=[];self.assertFalse(coverage.check(self.root,self.data)['ok'])

if __name__=='__main__':unittest.main()
