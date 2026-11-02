#!/usr/bin/env python3
"""Run bounded seeded mutation/generation against the bundled local frame decoder."""
import argparse
import importlib.util
import json
import random
from pathlib import Path

spec=importlib.util.spec_from_file_location('sui_framed',Path(__file__).resolve().parents[1]/'assets/python-lab/framed.py')
framed=importlib.util.module_from_spec(spec);spec.loader.exec_module(framed)

def exercise(packet,expect_valid=False):
    try:decoded=framed.decode(packet)
    except ValueError:
        if expect_valid:raise AssertionError('valid generated frame rejected')
        return False
    if framed.encode(decoded)!=packet:raise AssertionError('accepted frame did not roundtrip')
    return True

def minimize(packet,predicate):
    """Deletion-based reduction preserving a specific unexpected-failure predicate."""
    candidate=packet;chunk=max(1,len(packet)//2);attempts=0
    while chunk>=1 and attempts<1000:
        changed=False
        for start in range(0,len(candidate),chunk):
            smaller=candidate[:start]+candidate[start+chunk:];attempts+=1
            if predicate(smaller):candidate=smaller;changed=True;break
        if not changed:chunk//=2
    return candidate

def run(seed=1,iterations=1000):
    if type(seed) is not int or type(iterations) is not int or not 1<=iterations<=100000:raise ValueError('seed must be integer and iterations 1..100000')
    rng=random.Random(seed);accepted=rejected=0;corpus=[b'\0',b'\x02ab']
    for index in range(iterations):
        payload=rng.randbytes(rng.randrange(65))
        expected=index%2==0
        if expected:
            packet=framed.encode(payload);corpus=(corpus+[packet])[-64:]
        else:
            mutated=bytearray(rng.choice(corpus));position=rng.randrange(len(mutated))
            if index%3==0:mutated[position]=rng.randrange(256)
            elif index%3==1:del mutated[position]
            else:mutated.insert(position,rng.randrange(256))
            packet=bytes(mutated)
        try:
            good=exercise(packet,expected)
            accepted+=good;rejected+=not good
        except Exception as error:
            def same_failure(candidate):
                if expected and (not candidate or candidate[0]>64 or len(candidate)!=candidate[0]+1):return False
                try:exercise(candidate,expected)
                except Exception as failure:return type(failure) is type(error)
                return False
            reduced=minimize(packet,same_failure)
            return {'seed':seed,'iteration':index,'unexpectedFailures':1,'failureType':type(error).__name__,'expectValid':expected,'inputHex':packet.hex(),'minimizedHex':reduced.hex(),
                    'replay':'Use --replay-hex with the recorded/minimized lab input against the same code/version; add --expect-valid if expectValid is true.'}
    return {'seed':seed,'iterations':iterations,'accepted':accepted,'expectedRejections':rejected,'unexpectedFailures':0,
            'limitations':'Bounded seeded generation/mutation of a local byte parser. No coverage guidance, native sanitizer or complete input-space assurance is claimed.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seed',type=int,default=1);p.add_argument('--iterations',type=int,default=1000);p.add_argument('--replay-hex');p.add_argument('--expect-valid',action='store_true');a=p.parse_args()
    try:
        if a.replay_hex is not None:
            raw=bytes.fromhex(a.replay_hex)
            if len(raw)>1024:raise ValueError('replay input exceeds lab bound')
            accepted=exercise(raw,a.expect_valid);result={'accepted':accepted,'expectedRejection':not accepted}
        else:result=run(a.seed,a.iterations)
        print(json.dumps(result,indent=2));raise SystemExit(1 if result.get('unexpectedFailures',0) else 0)
    except (ValueError,AssertionError) as error:
        print(json.dumps({'ok':False,'error':str(error)}));raise SystemExit(1)
