"""Strict bounded report subsets; unsupported/incomplete output is never a clean scan."""
import json
import re
import xml.etree.ElementTree as ET

FORMATS=('mypy','tsc','compiler','sarif','spotbugs','checkstyle','infer','sonar','snyk','junit','coverage-py','gcov','jacoco','nmap','zap')

def object_(value, label):
    if not isinstance(value,dict):raise ValueError(f'{label} must be an object')
    return value

def array(value, label):
    if not isinstance(value,list):raise ValueError(f'{label} must be a list')
    return value

def count(value, label):
    if type(value) is not int or value<0:raise ValueError(f'{label} must be a nonnegative integer')
    return value

def xml(raw):
    if '<!ENTITY' in raw.upper():raise ValueError('entity declarations are not supported')
    if '<!DOCTYPE' in raw.upper():
        # Ignore a single ordinary external/no-subset declaration without fetching it.
        # JaCoCo and Nmap emit these headers; internal subsets remain unsupported.
        pattern=r'''<!DOCTYPE\s+[A-Za-z_:][\w:.-]*(?:\s+(?:SYSTEM\s+(?:"[^"]*"|'[^']*')|PUBLIC\s+(?:"[^"]*"|'[^']*')\s+(?:"[^"]*"|'[^']*')))?\s*>'''
        raw,removed=re.subn(pattern,'',raw,flags=re.I)
        if removed!=1 or '<!DOCTYPE' in raw.upper():raise ValueError('internal/malformed DTD declarations are not supported')
    try:return ET.fromstring(raw)
    except ET.ParseError as error:raise ValueError('malformed XML') from error

def result(rows, **extra):
    return {'findings':rows,'findingCount':len(rows),**extra}

def finding(rule, message, path=None, line=None, level='warning', suppressed=False):
    if not isinstance(rule,str) or not rule or not isinstance(message,str) or not message:raise ValueError('finding needs rule and message')
    if path is not None and not isinstance(path,str):raise ValueError('path must be text')
    if line is not None and (type(line) is not int or line<1):raise ValueError('line must be positive')
    return {'rule':rule,'message':message,'path':path,'line':line,'level':level,'suppressed':suppressed}

def _parse(format_, raw, return_code=0):
    if format_ not in FORMATS:raise ValueError('unsupported report format')
    if not isinstance(raw,str) or len(raw.encode())>8388608:raise ValueError('report must be text <=8 MiB')
    if type(return_code) is not int:raise ValueError('return code must be an integer')
    if format_ in ('mypy','tsc','compiler'):
        patterns={
            'mypy':r'^(.*?):(\d+)(?::(\d+))?: (error|warning|note): (.*?)(?:\s+\[([^\]]+)\])?$',
            'tsc':r'^(.*?)\((\d+),(\d+)\): (error|warning) (TS\d+): (.*)$',
            'compiler':r'^(.*?):(\d+)(?::(\d+))?: (fatal error|error|warning|note): (.*)$'}
        rows=[];unparsed=[]
        for line in raw.splitlines():
            if not line.strip():continue
            match=re.match(patterns[format_],line)
            if match:
                p,ln,col,level=match.groups()[:4]
                if format_=='tsc':rule,message=match.group(5,6)
                elif format_=='mypy':message,rule=match.group(5,6);rule=rule or 'mypy'
                else:message=match.group(5);rule='compiler'
                rows.append(finding(rule,message,p,int(ln),'error' if 'error' in level else level))
            elif format_=='tsc' and re.match(r'^error TS\d+: ',line):
                rule,message=line.split(': ',1);rows.append(finding(rule,message,level='error'))
            else:unparsed.append(line)
        if return_code not in (0,1,2):raise ValueError('tool execution failed')
        if return_code and not rows:raise ValueError('nonzero execution without recognized diagnostics')
        # Continuation/source/caret lines are expected for compiler output, not a clean blank run.
        if unparsed and not rows:raise ValueError('unrecognized tool output')
        return result(rows,unparsedLineCount=len(unparsed),partialOutput=bool(unparsed))
    if format_ in ('spotbugs','checkstyle','junit','jacoco','nmap'):
        root=xml(raw)
        if format_=='spotbugs':
            if root.tag!='BugCollection':raise ValueError('expected BugCollection')
            if root.findall('.//MissingClass') or root.findall('.//Error'):raise ValueError('incomplete SpotBugs analysis')
            for node in root.findall('Errors'):
                for key in ('errors','missingClasses'):
                    value=node.get(key,'0')
                    if not value.isdigit() or int(value)!=0:raise ValueError('incomplete SpotBugs analysis')
            if not root.findall('BugInstance'):
                summary=root.find('FindBugsSummary')
                if summary is None or not summary.get('total_classes','').isdigit() or int(summary.get('total_classes'))<1:raise ValueError('SpotBugs report has no analyzed classes')
            return result([finding(x.get('type','unknown'),x.findtext('LongMessage') or x.get('type','SpotBugs finding'),(x.find('SourceLine').get('sourcepath') if x.find('SourceLine') is not None else None),int(x.find('SourceLine').get('start')) if x.find('SourceLine') is not None and x.find('SourceLine').get('start','').isdigit() and int(x.find('SourceLine').get('start'))>0 else None) for x in root.findall('BugInstance')])
        if format_=='checkstyle':
            if root.tag!='checkstyle':raise ValueError('expected checkstyle')
            if not root.findall('file') or any(not f.get('name') for f in root.findall('file')):raise ValueError('Checkstyle report has no source scope')
            return result([finding(e.get('source','checkstyle'),e.get('message','finding'),f.get('name'),int(e.get('line')) if e.get('line','').isdigit() and int(e.get('line'))>0 else None,e.get('severity','warning')) for f in root.findall('file') for e in f.findall('error')])
        if format_=='junit':
            if root.tag not in ('testsuite','testsuites'):raise ValueError('expected JUnit suite')
            cases=root.findall('.//testcase');identities=set();failed=skipped=0
            for c in cases:
                key=(c.get('classname',''),c.get('name'))
                if not key[1] or key in identities:raise ValueError('missing/duplicate test identity')
                identities.add(key)
                failed+=bool(c.findall('failure') or c.findall('error'))
                skipped+=c.find('skipped') is not None or c.get('status')=='notrun'
            if not cases or len(cases)==skipped:raise ValueError('no executed test cases')
            for suite in [root]+list(root.findall('.//testsuite')):
                local=suite.findall('.//testcase')
                actual={'tests':len(local),'failures':sum(c.find('failure') is not None for c in local),'errors':sum(c.find('error') is not None for c in local),'skipped':sum(c.find('skipped') is not None for c in local)}
                for field,value in actual.items():
                    if suite.get(field) is not None and int(suite.get(field))!=value:raise ValueError('test summary disagrees with testcase records')
            return result([],testCount=len(cases),executed=len(cases)-skipped,failed=failed,skipped=skipped)
        if format_=='jacoco':
            if root.tag!='report':raise ValueError('expected JaCoCo report')
            counters={}
            for c in root.findall('counter'):
                kind=c.get('type');missed=int(c.get('missed','-1'));covered=int(c.get('covered','-1'))
                if missed<0 or covered<0 or not kind or kind in counters:raise ValueError('invalid coverage counter')
                counters[kind]={'covered':covered,'total':missed+covered}
            if not counters or sum(x['total'] for x in counters.values())==0:raise ValueError('empty coverage')
            return result([],counters=counters)
        if root.tag!='nmaprun':raise ValueError('expected nmaprun')
        finished=root.find('runstats/finished')
        if finished is None or finished.get('exit')!='success':raise ValueError('incomplete Nmap run')
        if not root.findall('host'):raise ValueError('Nmap report has no observed hosts')
        rows=[]
        for host in root.findall('host'):
            address=host.find('address');addr=address.get('addr') if address is not None else None
            for port in host.findall('ports/port'):
                state=port.find('state')
                if state is not None and state.get('state')=='open':rows.append(finding('open-port',f'{port.get("protocol")}/{port.get("portid")} open',addr,level='note'))
        return result(rows,observationsOnly=True,hostCount=len(root.findall('host')))
    try:data=json.loads(raw)
    except (ValueError,RecursionError) as error:raise ValueError('malformed JSON') from error
    rows=[]
    if format_=='sarif':
        object_(data,'SARIF')
        if data.get('version')!='2.1.0':raise ValueError('only SARIF 2.1.0 is supported')
        runs=array(data.get('runs'),'runs')
        if not runs:raise ValueError('SARIF has no analysis runs')
        for run in runs:
            object_(run,'run');driver=object_(object_(run.get('tool'),'tool').get('driver'),'driver')
            if not isinstance(driver.get('name'),str) or not driver['name']:raise ValueError('missing tool identity')
            for invocation in array(run.get('invocations',[]),'invocations'):
                value=object_(invocation,'invocation').get('executionSuccessful')
                if type(value) is not bool:raise ValueError('invalid analysis invocation status')
                if value is False:raise ValueError('analysis invocation failed')
            for row in array(run.get('results'),'results'):
                object_(row,'result');message=object_(row.get('message'),'message').get('text')
                locations=array(row.get('locations',[]),'locations');path=line=None
                if locations:
                    loc=object_(locations[0],'location').get('physicalLocation',{})
                    path=object_(loc,'physicalLocation').get('artifactLocation',{}).get('uri')
                    line=loc.get('region',{}).get('startLine')
                suppressions=array(row.get('suppressions',[]),'suppressions')
                rows.append(finding(row.get('ruleId','unknown'),message,path,line,row.get('level','warning'),bool(suppressions)))
    elif format_=='infer':
        for row in array(data,'Infer report'):
            object_(row,'issue');rows.append(finding(row.get('bug_type'),row.get('qualifier'),row.get('file'),row.get('line'),row.get('severity','warning')))
    elif format_=='sonar':
        object_(data,'Sonar report');issues=array(data.get('issues'),'issues')
        paging=object_(data.get('paging'),'paging')
        if count(paging.get('total'),'paging.total')!=len(issues):raise ValueError('incomplete/paginated Sonar issues')
        for row in issues:
            object_(row,'issue');rows.append(finding(row.get('rule'),row.get('message'),row.get('component'),row.get('line'),row.get('severity','warning')))
    elif format_=='snyk':
        object_(data,'Snyk report')
        if type(data.get('ok')) is not bool or data.get('error'):raise ValueError('failed/unsupported Snyk response')
        for row in array(data.get('vulnerabilities'),'vulnerabilities'):
            object_(row,'vulnerability');rows.append(finding(row.get('id'),row.get('title'),level=row.get('severity','warning')))
        if data['ok'] and rows:raise ValueError('Snyk summary contradicts findings')
        if not data['ok'] and not rows:raise ValueError('Snyk did not establish a completed clean scan')
    elif format_=='coverage-py':
        object_(data,'coverage report');totals=object_(data.get('totals'),'totals');files=object_(data.get('files'),'files')
        covered=count(totals.get('covered_lines'),'covered_lines');total=count(totals.get('num_statements'),'num_statements')
        if covered>total or total==0 or not files:raise ValueError('empty or contradictory coverage')
        return result([],coveredStatements=covered,totalStatements=total,coveredBranches=totals.get('covered_branches'),totalBranches=totals.get('num_branches'),files=sorted(files))
    elif format_=='gcov':
        object_(data,'gcov report')
        if data.get('format_version') not in ('1','2'):raise ValueError('unsupported gcov JSON format version')
        files=array(data.get('files'),'files');lines=branches=covered_lines=covered_branches=0;identities=set()
        for file in files:
            object_(file,'file')
            name=file.get('file')
            if not isinstance(name,str) or not name:raise ValueError('missing gcov file identity')
            for row in array(file.get('lines'),'lines'):
                object_(row,'line');line=count(row.get('line_number'),'line_number');hits=count(row.get('count'),'line count')
                if line<1 or (name,line) in identities:raise ValueError('invalid/duplicate gcov source line')
                identities.add((name,line));lines+=1;covered_lines+=hits>0
                for branch in array(row.get('branches',[]),'branches'):
                    hits=count(object_(branch,'branch').get('count'),'branch count');branches+=1;covered_branches+=hits>0
        if lines==0:raise ValueError('empty gcov coverage')
        return result([],coveredLines=covered_lines,totalLines=lines,coveredBranches=covered_branches,totalBranches=branches)
    elif format_=='zap':
        object_(data,'ZAP report');sites=array(data.get('site'),'site')
        if not sites:raise ValueError('ZAP report has no sites')
        for site in sites:
            object_(site,'site')
            for row in array(site.get('alerts'),'alerts'):
                object_(row,'alert');rows.append(finding(str(row.get('pluginid','unknown')),row.get('alert') or row.get('name'),site.get('@name'),level=str(row.get('riskcode','unknown'))))
    return result(rows)

def parse(format_, raw, return_code=0):
    try:
        allowed={'mypy':(0,1,2),'tsc':(0,1,2),'compiler':(0,1),'sarif':(0,1),'spotbugs':(0,1),'checkstyle':(0,1),'infer':(0,),'sonar':(0,),'snyk':(0,1),'junit':(0,1),'coverage-py':(0,),'gcov':(0,),'jacoco':(0,),'nmap':(0,),'zap':(0,1,2)}
        if not isinstance(format_,str) or format_ not in allowed or type(return_code) is not int or return_code not in allowed[format_]:raise ValueError('unsupported or failed tool return code')
        report=_parse(format_, raw, return_code)
        if return_code and not report.get('findingCount',0) and not report.get('failed',0):raise ValueError('nonzero run without corresponding findings/test failures')
        return report
    except (TypeError,AttributeError,KeyError,OverflowError,RecursionError,UnicodeError) as error:
        raise ValueError('unsupported or malformed report structure') from error
