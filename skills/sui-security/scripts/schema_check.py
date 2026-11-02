#!/usr/bin/env python3
"""Validate against explicitly cached, hash-pinned JSON/XSD schemas; never retrieve references."""
import argparse
import hashlib
import itertools
import json
import re
from urllib.parse import urljoin
from pathlib import Path

def strict_json(raw):
    def constant(_):raise ValueError('non-JSON numeric constant')
    def pairs(entries):
        result={}
        for key,value in entries:
            if key in result:raise ValueError('duplicate JSON property')
            result[key]=value
        return result
    return json.loads(raw,parse_constant=constant,object_pairs_hook=pairs)

def cached(manifest_path):
    path=Path(manifest_path).resolve();base=path.parent
    if path.stat().st_size>1048576:raise ValueError('schema manifest too large')
    manifest=strict_json(path.read_text())
    if not isinstance(manifest,dict) or manifest.get('type') not in ('json','xsd') or not isinstance(manifest.get('files'),list) or not 1<=len(manifest['files'])<=100:raise ValueError('invalid schema-cache manifest')
    files={};by_uri={}
    for row in manifest['files']:
        if not isinstance(row,dict):raise ValueError('invalid schema entry')
        name=row.get('path');digest=row.get('sha256');uri=row.get('uri')
        if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts or not isinstance(digest,str) or not re.fullmatch('[a-f0-9]{64}',digest) or not isinstance(uri,str) or not uri:raise ValueError('schema entry needs safe path, SHA256 and URI')
        source=base/name
        current=base
        for part in Path(name).parts:
            current=current/part
            if current.is_symlink():raise ValueError('schema symlinks unsupported')
        if not source.is_file() or not source.resolve().is_relative_to(base) or source.stat().st_size>4194304:raise ValueError('missing/oversized/outside schema')
        blob=source.read_bytes()
        if hashlib.sha256(blob).hexdigest()!=digest:raise ValueError('schema hash mismatch')
        if name in files or uri in by_uri:raise ValueError('duplicate schema identity')
        files[name]=(uri,blob);by_uri[uri]=blob
    if not isinstance(manifest.get('root'),str) or manifest['root'] not in files:raise ValueError('missing root schema')
    return manifest,files,by_uri

def validate(input_path,manifest_path):
    manifest,files,by_uri=cached(manifest_path);target=Path(input_path)
    if target.stat().st_size>8388608:raise ValueError('input exceeds8MiB')
    blob=target.read_bytes();uri,root=files[manifest['root']]
    if manifest['type']=='json':
        from jsonschema.validators import validator_for
        from referencing import Registry,Resource
        from referencing.jsonschema import DRAFT7
        def reject(reference):raise ValueError('schema reference was not explicitly cached')
        registry=Registry(retrieve=reject);schemas={}
        root_document=strict_json(root)
        default_draft=root_document.get('$schema','http://json-schema.org/draft-07/schema#') if isinstance(root_document,dict) else 'http://json-schema.org/draft-07/schema#'
        for location,body in by_uri.items():
            schema=strict_json(body)
            if isinstance(schema,dict):
                draft=schema.get('$schema',default_draft)
                if draft not in ('http://json-schema.org/draft-07/schema#','https://json-schema.org/draft-07/schema#','https://json-schema.org/draft/2020-12/schema'):raise ValueError('unsupported JSON Schema dialect')
                schema['$schema']='http://json-schema.org/draft-07/schema#' if 'draft-07' in draft else draft
                schema['$id']=urljoin(location,schema.get('$id',location))
            klass=validator_for(schema);klass.check_schema(schema)
            schemas[location]=schema
            registry=registry.with_resource(location,Resource.from_contents(schema,default_specification=DRAFT7))
        registry=registry.crawl();schema=schemas[uri];klass=validator_for(schema)
        # Resolve the root *as a retrieved resource*. Draft7 ignores $id siblings
        # on a bare $ref schema, so injecting an id alone cannot establish its base.
        dialect=schema.get('$schema','http://json-schema.org/draft-07/schema#') if isinstance(schema,dict) else 'http://json-schema.org/draft-07/schema#'
        validator=klass({'$schema':dialect,'$ref':uri},registry=registry)
        errors=list(itertools.islice(validator.iter_errors(strict_json(blob)),1001))
        # Paths/keyword only: error messages may include secrets from the document.
        return {'ok':not errors,'schemaUri':uri,'errors':[{'path':list(e.absolute_path),'keyword':e.validator} for e in errors[:1000]],'errorsTruncated':len(errors)>1000,'networkRetrieval':False}
    from lxml import etree
    if b'<!DOCTYPE' in blob.upper() or b'<!ENTITY' in blob.upper():raise ValueError('input DTD/entities unsupported')
    class CachedResolver(etree.Resolver):
        def resolve(self,url,pubid,context):
            if url not in by_uri:raise ValueError('XSD reference was not explicitly cached')
            return self.resolve_string(by_uri[url],context,base_url=url)
    parser=etree.XMLParser(resolve_entities=False,no_network=True,load_dtd=False)
    parser.resolvers.add(CachedResolver())
    schema=etree.XMLSchema(etree.fromstring(root,parser,base_url=uri))
    document=etree.fromstring(blob,parser)
    good=schema.validate(document)
    return {'ok':good,'schemaUri':uri,'errors':[{'line':e.line,'type':e.type_name} for e in schema.error_log][:1000],'networkRetrieval':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--manifest',required=True);a=p.parse_args()
    try:
        r=validate(a.input,a.manifest);print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 1)
    except ImportError:
        print(json.dumps({'ok':False,'status':'blocked','reason':'Install version-pinned jsonschema/referencing for JSON or lxml for XSD in the project environment.'}));raise SystemExit(2)
    except Exception as error:
        print(json.dumps({'ok':False,'status':'invalid','errorType':type(error).__name__,'reason':'Input/schema invalid, dependency unsupported or a reference missing from the explicit cache; no network retrieval attempted.'}));raise SystemExit(2)
