#!/usr/bin/env python3
"""Bounded independent-factor pairwise cases and an avgAbs coverage trace."""
import argparse
import itertools
import json
import math
from pathlib import Path

def pairwise(factors):
    if not isinstance(factors,dict) or not 2<=len(factors)<=8:
        raise ValueError('provide 2..8 independent factors')
    names=list(factors);levels=[];total=1
    for key,values in factors.items():
        if not isinstance(key,str) or not key.strip() or not isinstance(values,list) or not 1<=len(values)<=8:
            raise ValueError('factors need names and 1..8 levels')
        for value in values:
            if type(value) not in (str,int,float,bool) or (type(value) in (int,float) and (abs(value)>1e100 or not math.isfinite(value))):
                raise ValueError('levels must be bounded finite scalars')
        if len({json.dumps(v,sort_keys=True) for v in values})!=len(values):raise ValueError('duplicate factor level')
        levels.append(range(len(values)));total*=len(values)
    if total>10000:raise ValueError('candidate space exceeds 10000; partition factors first')
    candidates=list(itertools.product(*levels))
    def pairs(row):return {(i,row[i],j,row[j]) for i in range(len(names)) for j in range(i+1,len(names))}
    required={(i,a,j,b) for i in range(len(names)) for j in range(i+1,len(names)) for a in levels[i] for b in levels[j]}
    remaining=set(required);selected=[]
    covers={row:pairs(row) for row in candidates}
    while remaining:
        best=max(candidates,key=lambda row:len(covers[row]&remaining))
        gained=covers[best]&remaining
        if not gained:raise ValueError('pairwise construction failed')
        selected.append(dict(zip(names,[factors[name][best[i]] for i,name in enumerate(names)])))
        remaining-=gained;candidates.remove(best)
    return {'cases':selected,'requiredPairs':len(required),'coveredPairs':len(required),'candidateCount':total,
            'limitations':'All factors are independent; forbidden combinations/constraints are unsupported. Pairwise coverage does not cover higher-order interactions or prove correctness; add risk-specific cases and real oracles.'}

def avg_abs_trace(numbers):
    if numbers is not None and (not isinstance(numbers,list) or len(numbers)>10000 or any(type(x) not in (int,float) or abs(x)>1e100 or not math.isfinite(x) for x in numbers)):
        raise ValueError('example domain is null or a bounded list of finite numbers')
    null=numbers is None;empty=None if null else len(numbers)==0
    conditions=[{'id':'numbers-is-null','value':null},{'id':'length-is-zero','value':empty}]
    guard=null or bool(empty)
    decisions=[{'id':'invalid-input','value':guard}]
    statements=['entry','guard']
    if guard:
        statements.append('throw')
        return {'error':'IllegalArgumentException','conditions':conditions,'decisions':decisions,'statements':statements,
                'note':'A null value short-circuits the length condition; null means not evaluated in the trace, not false.'}
    total=0;statements.extend(['sum-initialization','loop-initialization'])
    for value in numbers:
        decisions.append({'id':'loop-has-next','value':True})
        negative=value<0;conditions.append({'id':'d-is-negative','value':negative});decisions.append({'id':'negative-branch','value':negative})
        statements.extend(['read-element','sign-check','subtract-negative' if negative else 'add-nonnegative','increment'])
        total=total-value if negative else total+value
    decisions.append({'id':'loop-has-next','value':False});statements.append('return')
    return {'value':total/len(numbers),'conditions':conditions,'decisions':decisions,'statements':list(dict.fromkeys(statements)),
            'note':'Educational trace of U4 p211 logic over finite numbers; no MC/DC or universal path-minimality claim.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('kind',choices=['pairwise','avg-abs']);p.add_argument('input');a=p.parse_args()
    try:
        data=json.loads(Path(a.input).read_text());r=pairwise(data) if a.kind=='pairwise' else avg_abs_trace(data)
        print(json.dumps(r,indent=2,allow_nan=False))
    except (OSError,ValueError,OverflowError) as error:
        print(json.dumps({'ok':False,'error':str(error)}));raise SystemExit(2)
