#!/usr/bin/env python3
"""Search named tools and explicit support tiers. Does not install or execute tools."""
import argparse
import json
from pathlib import Path

def search(query,limit=20):
    if not isinstance(query,str) or not query.strip():raise ValueError('query must be nonempty')
    if type(limit) is not int or not 1<=limit<=200:raise ValueError('limit must be1..200')
    data=json.loads((Path(__file__).resolve().parents[1]/'assets/tool-catalog.json').read_text())
    tokens=query.casefold().split();matches=[]
    for row in data['tools']:
        haystack=json.dumps(row,ensure_ascii=False).casefold()
        if all(token in haystack for token in tokens):matches.append(row)
    return {'matches':matches[:limit],'totalMatches':len(matches),'truncated':len(matches)>limit,
            'limitations':'Support tiers distinguish a procedure, fixture-tested report parser, native trial and external target validation. Catalog presence alone is not integration or an executed scan.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('query');p.add_argument('--limit',type=int,default=20);a=p.parse_args()
    try:print(json.dumps(search(a.query,a.limit),indent=2))
    except (OSError,ValueError) as error:print(json.dumps({'ok':False,'error':str(error)}));raise SystemExit(2)
