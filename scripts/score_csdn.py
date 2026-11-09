#!/usr/bin/env python3
"""Validate human evidence and summarize complete paired ratings; no auto judging."""
import argparse
import json
from pathlib import Path
from eval_csdn import DIMENSIONS


def summarize(out):
    jobs=json.loads((out/'jobs.json').read_text())
    ratings=json.loads((out/'ratings.json').read_text())
    key=lambda r:(r['case_id'],r['repeat'],r['arm'])
    expected={key(j) for j in jobs}
    if len(ratings)!=len(expected) or {key(r) for r in ratings}!=expected:
        raise ValueError('Missing, duplicate or unexpected ratings')
    by_key={key(r):r for r in ratings}
    for r in ratings:
        if not r['reviewer'].strip(): raise ValueError('Reviewer required')
        for d in DIMENSIONS:
            score=r['scores'].get(d)
            if type(score) is not int or score not in (0,1,2) or not r['evidence'].get(d,'').strip():
                raise ValueError('Each score requires 0/1/2 and quoted/located evidence')
    # Require an actual complete response for every scored output.
    for i,j in enumerate(jobs):
        folder=out/f'{i:03d}-{j["case_id"]}-{j["repeat"]}-{j["arm"]}'
        if (folder/'failure.json').exists() or not (folder/'article.md').is_file():
            raise ValueError('Missing/failed output cannot be scored')
    pairs=[]
    for case,repeat,arm in sorted(expected):
        if arm!='baseline':continue
        a=by_key[(case,repeat,'baseline')];b=by_key[(case,repeat,'skill')]
        pairs.append({'case_id':case,'repeat':repeat,'delta':{d:b['scores'][d]-a['scores'][d] for d in DIMENSIONS},
                      'baseline_critical_errors':a['critical_errors'],'skill_critical_errors':b['critical_errors']})
    return {'status':'human_scored_small_sample','pairs':pairs,
            'mean_paired_delta':{d:sum(p['delta'][d] for p in pairs)/len(pairs) for d in DIMENSIONS},
            'regressions':[p for p in pairs if any(v<0 for v in p['delta'].values()) or p['skill_critical_errors']]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);a=p.parse_args()
    result=summarize(a.out)
    path=a.out/'summary.json'
    with path.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
