from pathlib import Path
import re, sys

path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')
lines = text.splitlines()
issues=[]

nonempty=[x for x in lines if x.strip()]
if nonempty and nonempty[0].lstrip().startswith('#'):
    issues.append('Overall article title should be plain text, not a Markdown heading.')

h1=[x for x in lines if re.match(r'^# ',x)]
h3=[x for x in lines if re.match(r'^#{3,} ',x)]
if not (4 <= len(h1) <= 7):
    issues.append(f'H1 count is {len(h1)}; normal target is roughly 4–7.')
if h3:
    issues.append('Found H3+ headings. This house style normally uses overall title + H1 + H2.')

# Remove fenced code before paragraph analysis.
clean=[]; in_code=False
for line in lines:
    if line.strip().startswith('```'):
        in_code=not in_code; continue
    if not in_code: clean.append(line)
plain='\n'.join(clean)
paragraphs=[re.sub(r'\s+','',p) for p in re.split(r'\n\s*\n',plain) if p.strip() and not p.lstrip().startswith('#')]
short=sum(1 for p in paragraphs if len(p) < 45)
if paragraphs and short/len(paragraphs) > 0.45:
    issues.append(f'{short}/{len(paragraphs)} prose paragraphs are under 45 characters; check for excessive micro-paragraphs.')

cjk=len(re.findall(r'[\u4e00-\u9fff]',text))
if cjk > 5000:
    issues.append(f'Article contains about {cjk} CJK characters; consider splitting into a series.')

if issues:
    print('Style review:')
    for x in issues: print('-',x)
    sys.exit(1)
print('No obvious CSDN house-style issues found.')
