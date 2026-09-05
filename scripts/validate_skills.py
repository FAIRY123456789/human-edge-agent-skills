from pathlib import Path
import re, sys, yaml, json

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
NAME_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
errors = []
folders = sorted(p for p in SKILLS.iterdir() if p.is_dir())

for d in folders:
    f = d / 'SKILL.md'
    if not f.exists():
        errors.append(f'{d.name}: missing SKILL.md')
        continue
    text = f.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        errors.append(f'{d.name}: missing YAML frontmatter')
        continue
    try:
        parts = text.split('---', 2)
        fm = yaml.safe_load(parts[1])
    except Exception as e:
        errors.append(f'{d.name}: invalid YAML: {e}')
        continue
    if not isinstance(fm, dict):
        errors.append(f'{d.name}: frontmatter is not a mapping')
        continue
    if fm.get('name') != d.name:
        errors.append(f'{d.name}: name mismatch ({fm.get("name")!r})')
    if not NAME_RE.fullmatch(d.name) or len(d.name) > 64:
        errors.append(f'{d.name}: invalid name')
    desc = str(fm.get('description', '')).strip()
    if not desc or len(desc) > 1024:
        errors.append(f'{d.name}: invalid description length {len(desc)}')
    if text.count('\n') + 1 > 500:
        errors.append(f'{d.name}: SKILL.md >500 lines')
    readme = d / 'README.md'
    if not readme.exists():
        errors.append(f'{d.name}: missing human-facing README.md')
    metadata = d / 'agents' / 'openai.yaml'
    if metadata.exists():
        try:
            interface = yaml.safe_load(metadata.read_text(encoding='utf-8')).get('interface', {})
            if f'${d.name}' not in str(interface.get('default_prompt', '')):
                errors.append(f'{d.name}: agents/openai.yaml default_prompt must mention ${d.name}')
        except Exception as e:
            errors.append(f'{d.name}: invalid agents/openai.yaml: {e}')

catalog = ROOT / 'catalog.json'
try:
    items = json.loads(catalog.read_text(encoding='utf-8'))
    names = {x['name'] for x in items}
    if len(items) != len(names):
        errors.append('catalog.json contains duplicate skill names')
    if names != {d.name for d in folders}:
        errors.append('catalog.json names do not match skill folders')
except Exception as e:
    errors.append(f'catalog.json invalid: {e}')

count = len(folders)
readme_en = (ROOT / 'README.md').read_text(encoding='utf-8')
readme_zh = (ROOT / 'README.zh-CN.md').read_text(encoding='utf-8')
if f'The {count} Skills' not in readme_en:
    errors.append(f'README.md does not declare the current {count}-Skill catalog')
if f'{count} 个 Skill' not in readme_zh:
    errors.append(f'README.zh-CN.md does not declare the current {count}-Skill catalog')

try:
    eval_items = json.loads((ROOT / 'evals' / 'cases.json').read_text(encoding='utf-8'))
    eval_names = {item['skill'] for item in eval_items}
    missing_evals = {d.name for d in folders} - eval_names
    unknown_evals = eval_names - {d.name for d in folders}
    if missing_evals:
        errors.append(f'missing seed evals for: {sorted(missing_evals)}')
    if unknown_evals:
        errors.append(f'evals reference unknown skills: {sorted(unknown_evals)}')
except Exception as e:
    errors.append(f'evals/cases.json invalid: {e}')

if errors:
    print('Validation failed:')
    for e in errors:
        print('-', e)
    sys.exit(1)

print(f'OK: {len(folders)} skills passed static validation.')
