#!/usr/bin/env python3
"""Paired CSDN generation harness. Heuristics are diagnostics, never semantic scores."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import re
import subprocess
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/csdn-technical-writing/SKILL.md'
CASES = ROOT / 'evals/csdn/cases.json'
DIMENSIONS = ['concept_accuracy', 'technical_detail', 'structure', 'code_clarity', 'privacy']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def diagnostics(text, case):
    # Exclude code from prose statistics; total CJK length includes code/comments.
    prose = re.sub(r'(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$', '', text)
    blocks = [x.strip() for x in re.split(r'\n\s*\n', prose) if x.strip()]
    paragraphs = [x for x in blocks[1:] if not re.match(r'^(#|>|[-*+] |\d+[.)] |\|)', x)]
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
    return {'cjk_characters': cjk, 'target_range': case['length']['target'],
            'over_max': cjk > case['length']['max'] and not case['length']['explicit_override'],
            'plain_title': bool(blocks) and not blocks[0].startswith('#'),
            'h1_count': len(re.findall(r'^# ', prose, re.M)),
            'unnumbered_h1': re.findall(r'^# (?![一二三四五六七八九十]+[、.．\s])(.+)', prose, re.M),
            'short_paragraph_ratio': sum(len(re.sub(r'\s','',p)) < 45 for p in paragraphs) / max(1,len(paragraphs)),
            'has_fenced_code': bool(re.search(r'^(```|~~~)',text,re.M)),
            'leaked_markers': [x for x in case['forbidden_literals'] if x.casefold() in text.casefold()]}

def dump(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def prepare(out, repeats, seed):
    out.mkdir(parents=True,exist_ok=False)
    skill=SKILL.read_text(); cases=json.loads(CASES.read_text())
    dump(out/'manifest.json', {'status':'prepared_not_executed','created_utc':datetime.now(timezone.utc).isoformat(),
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'skill_sha256':sha(SKILL.read_bytes()),'cases_sha256':sha(CASES.read_bytes()),'order_seed':seed,'repeats':repeats})
    (out/'skill.md').write_text(skill)
    (out/'eval_csdn.py').write_bytes(Path(__file__).read_bytes())
    (out/'score_csdn.py').write_bytes((ROOT/'scripts/score_csdn.py').read_bytes())
    dump(out/'cases.json', cases)
    jobs=[]
    for case in cases:
        for repeat in range(repeats):
            for arm in ['baseline','skill']:
                jobs.append({'case_id':case['id'],'repeat':repeat,'arm':arm,'messages':[
                    {'role':'system','content':'请准确回答用户的技术写作请求。'+ ('\n\n'+skill if arm=='skill' else '')},
                    {'role':'user','content':case['prompt']}]})
    random.Random(seed).shuffle(jobs)
    dump(out/'jobs.json',jobs)
    dump(out/'ratings.json',[{'case_id':j['case_id'],'repeat':j['repeat'],'arm':j['arm'],
        'scores':{d:None for d in DIMENSIONS},'evidence':{d:'' for d in DIMENSIONS},
        'critical_errors':[],'reviewer':'','notes':''} for j in jobs])

def run(out, model, endpoint, max_tokens):
    key=os.environ.get('OPENAI_API_KEY')
    if not key:
        raise SystemExit('OPENAI_API_KEY unavailable; prepared fixtures remain unexecuted.')
    manifest=json.loads((out/'manifest.json').read_text())
    if manifest['status'] != 'prepared_not_executed':
        raise SystemExit('Use a fresh prepared directory; existing runs are immutable.')
    manifest.update(status='running',model=model,endpoint=endpoint,max_tokens=max_tokens,temperature=0)
    dump(out/'manifest.json',manifest)
    cases={c['id']:c for c in json.loads((out/'cases.json').read_text())}
    failures=0
    for i,job in enumerate(json.loads((out/'jobs.json').read_text())):
        folder=out/f'{i:03d}-{job["case_id"]}-{job["repeat"]}-{job["arm"]}'
        folder.mkdir()
        payload={'model':model,'messages':job['messages'],'temperature':0,'max_tokens':max_tokens}
        dump(folder/'request.json',payload)
        try:
            req=urllib.request.Request(endpoint,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=180) as response:
                raw=response.read()
            (folder/'response.json').write_bytes(raw)
            result=json.loads(raw); choice=result['choices'][0]
            content=choice['message']['content']
            if not isinstance(content,str) or not content.strip():
                raise ValueError('Empty/non-text output')
            (folder/'article.md').write_text(content)
            dump(folder/'diagnostics.json',dict(diagnostics(content,cases[job['case_id']]),finish_reason=choice.get('finish_reason'),usage=result.get('usage')))
            if choice.get('finish_reason') != 'stop':
                raise ValueError('Incomplete generation: review raw response; do not score as complete')
        except Exception as exc:
            failures+=1
            # Avoid logging provider error bodies, headers or credentials.
            dump(folder/'failure.json',{'error_type':type(exc).__name__,'status':'unscorable'})
    manifest.update(status='completed_with_failures' if failures else 'generated_unscored',failures=failures)
    dump(out/'manifest.json',manifest)

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True)
    prep=sub.add_parser('prepare'); prep.add_argument('out',type=Path); prep.add_argument('--repeats',type=int,default=2); prep.add_argument('--seed',type=int,default=42)
    execute=sub.add_parser('run'); execute.add_argument('out',type=Path); execute.add_argument('--model',required=True); execute.add_argument('--endpoint',default='https://api.openai.com/v1/chat/completions'); execute.add_argument('--max-tokens',type=int,default=6500)
    a=p.parse_args()
    if a.command=='prepare':
        if a.repeats<1: p.error('repeats must be positive')
        prepare(a.out,a.repeats,a.seed)
    else: run(a.out,a.model,a.endpoint,a.max_tokens)

if __name__=='__main__': main()
