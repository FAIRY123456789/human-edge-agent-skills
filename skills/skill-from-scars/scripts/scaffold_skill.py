from pathlib import Path
import json, re, sys

src = Path(sys.argv[1])
out = Path(sys.argv[2] if len(sys.argv) > 2 else '.')
data = json.loads(src.read_text(encoding='utf-8'))
name = data['name'].strip().lower()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
    raise SystemExit('name must use lowercase letters/numbers/hyphens')
root = out / name
(root / 'references').mkdir(parents=True, exist_ok=True)
(root / 'evals').mkdir(parents=True, exist_ok=True)
desc = data['description'].replace('"', '\\"')
body = data.get('workflow', ['Define the workflow.'])
lines = '\n'.join(f'{i+1}. {x}' for i,x in enumerate(body))
skill_text = "---\nname: {}\ndescription: \"{}\"\n---\n\n# {}\n\n## Workflow\n\n{}\n".format(name, desc, data.get('title', name), lines)
(root/'SKILL.md').write_text(skill_text, encoding='utf-8')
(root/'evals'/'seed.json').write_text(json.dumps(data.get('eval', {}), ensure_ascii=False, indent=2), encoding='utf-8')
print(root)
