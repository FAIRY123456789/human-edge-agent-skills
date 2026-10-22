import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from eval_csdn import CASES, diagnostics, prepare
from score_csdn import summarize
spec=importlib.util.spec_from_file_location('lint',ROOT/'skills/csdn-technical-writing/scripts/lint_csdn_article.py')
lint=importlib.util.module_from_spec(spec);spec.loader.exec_module(lint)

class EvaluationTests(unittest.TestCase):
    def test_pairing_and_single_treatment(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run';prepare(out,2,42)
            jobs=json.loads((out/'jobs.json').read_text())
            self.assertEqual(len(jobs),16)
            for case in json.loads(CASES.read_text()):
                a=next(j for j in jobs if j['case_id']==case['id'] and j['arm']=='baseline')
                b=next(j for j in jobs if j['case_id']==case['id'] and j['arm']=='skill')
                self.assertEqual(a['messages'][1],b['messages'][1])
                self.assertTrue(b['messages'][0]['content'].startswith(a['messages'][0]['content']))
            with self.assertRaises(ValueError):summarize(out)
            with self.assertRaises(FileExistsError):prepare(out,2,42)
    def test_length_boundary_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.md'
            p.write_text('文'*3000);self.assertFalse(any('CJK' in x for x in lint.inspect_article(p)))
            p.write_text('文'*3001);self.assertTrue(any('CJK' in x for x in lint.inspect_article(p)))
            self.assertFalse(any('CJK' in x for x in lint.inspect_article(p,4000)))
    def test_privacy_fixture_and_code_heading(self):
        c=json.loads(CASES.read_text())[-1]
        d=diagnostics('标题\n\n# 一、定义\n\n```python\n# code comment\nurl="https://ops.mistleaf.example"\n```\n',c)
        self.assertEqual(d['h1_count'],1)
        self.assertIn('mistleaf',d['leaked_markers'])
        self.assertTrue(d['has_fenced_code'])
    def test_diagnostics_not_semantic_score(self):
        d=diagnostics('标题\n\n# 一、错误\n\n事务一定回滚。',json.loads(CASES.read_text())[1])
        self.assertNotIn('score',d)
        self.assertTrue(d['plain_title'])

if __name__=='__main__':unittest.main()
