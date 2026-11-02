#!/usr/bin/env python3
"""Explicit-denominator quality arithmetic. Educational models, not productivity scores."""
import argparse
import json
import math
from pathlib import Path

def n(value, name, positive=False, integer=False):
    if type(value) not in (int, float) or (integer and type(value) is not int):
        raise ValueError(f'{name}: wrong numeric type')
    try:
        valid = math.isfinite(value) and value >= 0 and (not positive or value > 0)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(f'{name}: require finite nonnegative value' + (' >0' if positive else ''))
    return value

def run(kind, data):
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    if kind == 'halstead':
        operators = n(data.get('distinctOperators'), 'distinctOperators', integer=True)
        operands = n(data.get('distinctOperands'), 'distinctOperands', integer=True)
        count = n(data.get('totalTokens'), 'totalTokens', integer=True)
        vocabulary = operators + operands
        if vocabulary > count:
            raise ValueError('distinct vocabulary exceeds total tokens')
        if vocabulary == 0 and count != 0:
            raise ValueError('tokens require a vocabulary')
        return {'vocabulary': vocabulary, 'length': count,
                'volume': count * math.log2(vocabulary) if vocabulary else 0,
                'limitations': 'Caller supplies a consistent tokenization convention; no language parser or defect estimate is implied.'}
    if kind == 'cyclomatic':
        nodes, edges = data.get('nodes'), data.get('edges')
        if not isinstance(nodes,list) or not nodes or any(not isinstance(x,str) or not x for x in nodes) or len(set(nodes))!=len(nodes):
            raise ValueError('nodes must be unique nonempty strings')
        if not isinstance(edges,list) or any(not isinstance(e,list) or len(e)!=2 or any(not isinstance(x,str) or x not in nodes for x in e) for e in edges):
            raise ValueError('edges must be node-id pairs')
        if len({tuple(e) for e in edges})!=len(edges):
            raise ValueError('duplicate edge')
        adjacent = {x:set() for x in nodes}
        for a,b in edges:
            adjacent[a].add(b); adjacent[b].add(a)
        remaining = set(nodes); components = 0
        while remaining:
            components += 1; todo = [remaining.pop()]
            while todo:
                node = todo.pop()
                new = adjacent[node] & remaining
                remaining -= new; todo.extend(new)
        value = len(edges)-len(nodes)+2*components
        return {'nodes':len(nodes),'edges':len(edges),'components':components,'complexity':value,
                'assumptions':'Each weakly connected component represents a well-formed CFG with one entry/exit. Graph shape and path feasibility require manual review; this is not automatic source analysis or a minimum branch-test count.'}
    if kind == 'function-points':
        counts, weights = data.get('counts'), data.get('weights')
        categories = {'EI','EO','EQ','ILF','EIF'}
        if not isinstance(counts,dict) or not isinstance(weights,dict) or set(counts)!=categories or set(weights)!=categories:
            raise ValueError('counts and weights must explicitly cover EI/EO/EQ/ILF/EIF')
        levels = {'simple','average','complex'}
        subtotal = {}
        for cat in sorted(categories):
            if not isinstance(counts[cat],dict) or not isinstance(weights[cat],dict) or set(counts[cat])!=levels or set(weights[cat])!=levels:
                raise ValueError('each category needs simple/average/complex counts and weights')
            subtotal[cat] = sum(n(counts[cat][lev], 'count', integer=True)*n(weights[cat][lev], 'weight', positive=True) for lev in levels)
        total = sum(subtotal.values())
        if not math.isfinite(total):
            raise ValueError('function-point overflow')
        result = {'unadjustedFunctionPoints':total,'categoryTotals':subtotal,
                  'limitations':'Explicit caller-supplied weighting table. No default weighting, adjustment factor or productivity calibration is inferred.'}
        if 'personHoursPerFP' in data:
            result['estimatedPersonHours'] = total*n(data['personHoursPerFP'],'personHoursPerFP',positive=True)
        return result
    if kind == 'defects':
        found = n(data.get('foundBeforeRelease'),'foundBeforeRelease',integer=True)
        escaped = n(data.get('escapedAfterRelease'),'escapedAfterRelease',integer=True)
        size = n(data.get('size'),'size',positive=True)
        if not isinstance(data.get('sizeUnit'),str) or not data['sizeUnit'].strip() or not isinstance(data.get('window'),str) or not data['window'].strip():
            raise ValueError('explicit sizeUnit and window are required')
        total = found+escaped
        return {'totalObservedDefects':total,'faultDensity':total/size,'densityUnit':f'defects/{data["sizeUnit"]}',
                'escapeFraction':escaped/total if total else None,'window':data['window'],
                'definitions':'Escape fraction = post-release / (pre-release + post-release) for this observed cohort/window. Defect share by module uses all observed defects as denominator, not module size. Unseen defects are unknown.'}
    if kind == 'reliability':
        exposure = n(data.get('operatingExposure'),'operatingExposure')
        failures = n(data.get('failures'),'failures',integer=True)
        if failures and exposure == 0:
            raise ValueError('failures require operating exposure')
        if not isinstance(data.get('timeUnit'),str) or not data['timeUnit'].strip():
            raise ValueError('timeUnit is required')
        return {'observedFailureRate':failures/exposure if exposure else None,
                'meanOperatingTimeBetweenObservedFailures':exposure/failures if failures else None,
                'timeUnit':data['timeUnit'],'status':'no_failures_observed' if failures==0 else 'observed',
                'limitations':'No-failure exposure does not imply infinite reliability. This ratio needs a defined failure/repair policy; no exponential survival model, future MTBF or confidence bound is inferred.'}
    if kind == 'latency':
        values = data.get('samples')
        if not isinstance(values,list) or not values or len(values)>100000:
            raise ValueError('samples must contain 1..100000 observations')
        vals = sorted(n(x,'sample') for x in values)
        try:mean=math.fsum(vals)/len(vals)
        except OverflowError:raise ValueError('sample aggregate overflow')
        return {'count':len(vals),'mean':mean,**{f'p{q}':vals[math.ceil(q/100*len(vals))-1] for q in [50,95,99]},
                'method':'nearest-rank','unit':data.get('unit','unspecified'),
                'limitations':'A sample percentile is not a stable population estimate; small n and correlated samples need interpretation. Do not average percentiles.'}
    raise ValueError('unknown metric kind')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=['halstead','cyclomatic','function-points','defects','reliability','latency'])
    parser.add_argument('input');args=parser.parse_args()
    try:
        result=run(args.kind,json.loads(Path(args.input).read_text()))
        print(json.dumps(result,indent=2,allow_nan=False))
    except (OSError,ValueError,OverflowError) as error:
        print(json.dumps({'ok':False,'error':str(error)}));raise SystemExit(2)
