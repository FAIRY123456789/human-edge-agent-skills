from pathlib import Path
import json, html, sys

src = Path(sys.argv[1])
out = Path(sys.argv[2] if len(sys.argv) > 2 else "todo.html")
data = json.loads(src.read_text(encoding="utf-8"))
if isinstance(data, dict):
    tasks = data.get("tasks", [])
    title = data.get("title", "Todo")
else:
    tasks = data
    title = "Todo"

payload = json.dumps(tasks, ensure_ascii=False).replace("</", "<\\/")
page = """<!doctype html>
<html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>__TITLE__</title>
<style>
body{font-family:system-ui,-apple-system,'Segoe UI','PingFang SC',sans-serif;max-width:900px;margin:36px auto;padding:0 18px;background:#fafafa;color:#171717}
h1{font-size:28px}.bar{display:flex;gap:12px;align-items:center;margin:18px 0;flex-wrap:wrap}.card{background:white;border:1px solid #ddd;border-radius:12px;padding:14px 16px;margin:10px 0;display:grid;grid-template-columns:auto 1fr;gap:12px}.done .main{opacity:.48;text-decoration:line-through}.meta{font-size:13px;color:#666;margin-top:6px}.p{font-weight:700}button{padding:8px 12px;border:1px solid #bbb;border-radius:8px;background:white;cursor:pointer}progress{width:220px}
</style></head><body><h1>__TITLE__</h1>
<div class='bar'><progress id='prog' max='100' value='0'></progress><span id='count'></span><button onclick='resetAll()'>Reset</button><button onclick='exportState()'>Export JSON</button></div><div id='app'></div>
<script>
const seed=__PAYLOAD__; const key='joyt-todo:'+location.pathname; let state=JSON.parse(localStorage.getItem(key)||'null')||seed;
function esc(s){return String(s).replace(/[&<>\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[m]))}
function render(){const app=document.getElementById('app');app.innerHTML='';state.forEach((t,i)=>{const d=document.createElement('div');d.className='card '+(t.status==='done'?'done':'');d.innerHTML=`<input type='checkbox' ${t.status==='done'?'checked':''} onchange='toggle(${i})'><div class='main'><div><span class='p'>${esc(t.priority||'')}</span> ${esc(t.title||'')}</div><div>${esc(t.details||'')}</div><div class='meta'>${t.due?'Due: '+esc(t.due)+' · ':''}${t.uncertainty?'⚠ '+esc(t.uncertainty):''}</div></div>`;app.appendChild(d)});const done=state.filter(x=>x.status==='done').length;document.getElementById('count').textContent=`${done} / ${state.length} done`;document.getElementById('prog').value=state.length?done/state.length*100:0;localStorage.setItem(key,JSON.stringify(state))}
function toggle(i){state[i].status=state[i].status==='done'?'todo':'done';render()}
function resetAll(){if(confirm('Reset all task states?')){state=JSON.parse(JSON.stringify(seed));render()}}
function exportState(){const b=new Blob([JSON.stringify(state,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='todo-state.json';a.click();URL.revokeObjectURL(a.href)}
render();
</script></body></html>"""
page = page.replace("__TITLE__", html.escape(title)).replace("__PAYLOAD__", payload)
out.write_text(page, encoding="utf-8")
print(out)
