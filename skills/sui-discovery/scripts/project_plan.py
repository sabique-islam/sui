#!/usr/bin/env python3
"""Calculate assumption-labelled COCOMO/CPM and audit a RACI matrix. No calendar/resource leveling."""
import argparse
import json
import math
from pathlib import Path

COCOMO = {'organic': (2.4, 1.05, 2.5, .38),
          'semi-detached': (3.0, 1.12, 2.5, .35),
          'embedded': (3.6, 1.20, 2.5, .32)}

def number(value, name, minimum=0):
    if type(value) not in (int, float):
        raise ValueError(f'{name} must be a finite number')
    try:
        good = math.isfinite(value) and value >= minimum
    except OverflowError:
        good = False
    if not good:
        raise ValueError(f'{name} must be finite and >= {minimum}')
    return float(value)

def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name} must be nonempty text')
    return value

def cocomo(data):
    mode = data.get('mode')
    if not isinstance(mode, str) or mode not in COCOMO:
        raise ValueError('mode must be organic, semi-detached or embedded')
    size = number(data.get('kloc'), 'kloc', .001)
    if size > 1000000:
        raise ValueError('kloc exceeds this educational model limit')
    a, b, c, d = COCOMO[mode]
    effort = a * size**b
    duration = c * effort**d
    return {'model': 'Basic COCOMO (historical)', 'mode': mode,
            'coefficients': {'a': a, 'b': b, 'c': c, 'd': d},
            'effortPersonMonths': effort, 'durationMonths': duration,
            'averageStaff': effort/duration,
            'limitations': 'Uncalibrated historical estimate, not a commitment. KLOC is not known reliably before design. Duration assumes this model, not actual staffing availability.'}

def schedule(data):
    tasks = data.get('tasks')
    if not isinstance(tasks, list) or not 1 <= len(tasks) <= 1000:
        raise ValueError('tasks must contain 1..1000 records')
    unit = text(data.get('unit'), 'unit')
    nodes = {}
    for row in tasks:
        if not isinstance(row, dict):
            raise ValueError('task must be an object')
        key = text(row.get('id'), 'task id')
        if key in nodes:
            raise ValueError('duplicate task id')
        duration = number(row.get('duration'), 'duration')
        deps = row.get('dependsOn', [])
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps) or len(set(deps)) != len(deps):
            raise ValueError('dependsOn must contain unique string ids')
        nodes[key] = {'duration': duration, 'dependsOn': deps}
    if any(dep not in nodes for row in nodes.values() for dep in row['dependsOn']):
        raise ValueError('unknown dependency')
    children = {key: [] for key in nodes}
    indegree = {key: len(row['dependsOn']) for key, row in nodes.items()}
    for key, row in nodes.items():
        for dep in row['dependsOn']:
            children[dep].append(key)
    queue = sorted(key for key, degree in indegree.items() if degree == 0)
    order = []
    while queue:
        key = queue.pop(0)
        order.append(key)
        for child in children[key]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
        queue.sort()
    if len(order) != len(nodes):
        raise ValueError('dependency cycle')
    for key in order:
        row = nodes[key]
        row['earlyStart'] = max((nodes[d]['earlyFinish'] for d in row['dependsOn']), default=0)
        row['earlyFinish'] = row['earlyStart'] + row['duration']
        if not math.isfinite(row['earlyFinish']):
            raise ValueError('schedule duration overflow')
    finish = max(row['earlyFinish'] for row in nodes.values())
    for key in reversed(order):
        row = nodes[key]
        row['lateFinish'] = min((nodes[c]['lateStart'] for c in children[key]), default=finish)
        row['lateStart'] = row['lateFinish'] - row['duration']
        row['slack'] = max(0, row['lateStart'] - row['earlyStart'])
        row['critical'] = math.isclose(row['slack'], 0, abs_tol=1e-9)
    return {'unit': unit, 'duration': finish, 'topologicalOrder': order, 'tasks': nodes,
            'criticalTasks': [key for key in order if nodes[key]['critical']],
            'limitations': 'CPM with unlimited resources and deterministic durations. No calendar, holidays, staffing allocation or resource leveling is inferred; critical tasks may form several paths.'}

def raci(data):
    rows = data.get('assignments')
    if not isinstance(rows, list) or not rows:
        raise ValueError('assignments must be nonempty')
    ids = set()
    errors = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('assignment must be an object')
        key = text(row.get('task'), 'task')
        if key in ids:
            errors.append(f'{key}: duplicate task')
        ids.add(key)
        people = row.get('people')
        if not isinstance(people, dict) or not people:
            raise ValueError('people must map names to role arrays')
        accountable = responsible = 0
        for person, roles in people.items():
            text(person, 'person')
            if not isinstance(roles, list) or not roles or any(not isinstance(r, str) or r not in ('R','A','C','I') for r in roles) or len(set(roles)) != len(roles):
                raise ValueError('roles must contain unique R/A/C/I values')
            accountable += 'A' in roles
            responsible += 'R' in roles
        if accountable != 1:
            errors.append(f'{key}: require exactly one accountable owner')
        if responsible < 1:
            errors.append(f'{key}: require at least one responsible owner')
    return {'ok': not errors, 'errors': errors, 'policy': 'One A and at least one R per activity; the same person may be both.'}

def run(kind, data):
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    return {'cocomo': cocomo, 'schedule': schedule, 'raci': raci}[kind](data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['cocomo','schedule','raci'])
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        result = run(args.kind, json.loads(Path(args.input).read_text()))
        print(json.dumps(result, indent=2, allow_nan=False))
        raise SystemExit(1 if result.get('ok') is False else 0)
    except (OSError, ValueError, OverflowError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}))
        raise SystemExit(2)
