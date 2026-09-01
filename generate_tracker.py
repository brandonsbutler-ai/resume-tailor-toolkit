"""Build a self-contained interactive application tracker -> out/tracker.html

A single HTML file: search box, status filter, and an "applied" checkbox per role that
persists in the browser (localStorage) behind a progress bar. Theme-aware. Nothing is
submitted -- it just tracks your own progress. Edit ROLES, or wire it to tailorings.py.
"""
import os
import html
from datetime import date
import tailorings as T

def esc(s):
    return html.escape(str(s), quote=True)

# Seed from the tailorings you've prepared, plus any leads you're still chasing.
ROLES = [{"company": t["company"], "role": t["job_title"], "status": "READY", "key": k}
         for k, t in T.TAILORINGS.items()]
ROLES += [
    {"company": "Example Startup", "role": "Security Engineer", "status": "TODO", "key": "lead1"},
    {"company": "Example Bank", "role": "Cloud Security Architect", "status": "TODO", "key": "lead2"},
]

STYLE = r"""
:root{--bg:#F7F8FA;--panel:#fff;--surface:#EEF1F6;--ink:#141821;--ink3:#6B7688;--rule:#D7DCE6;
  --accent:#2F4A7C;--go:#1F6F5C;--go-bg:#E2EFEA;--warn:#8F5A12;--warn-bg:#F6EBDA}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0D1015;--panel:#161B22;
  --surface:#1B212B;--ink:#E9ECF2;--ink3:#7F8A9A;--rule:#2A313C;--accent:#8FAEDD;--go:#6FC3AA;
  --go-bg:#15261F;--warn:#D6A45C;--warn-bg:#2A2115}}
:root[data-theme="dark"]{--bg:#0D1015;--panel:#161B22;--surface:#1B212B;--ink:#E9ECF2;--ink3:#7F8A9A;
  --rule:#2A313C;--accent:#8FAEDD;--go:#6FC3AA;--go-bg:#15261F;--warn:#D6A45C;--warn-bg:#2A2115}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,sans-serif;font-size:15px}
.wrap{max-width:820px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:24px;margin:0 0 4px}.sub{color:var(--ink3);font-size:13px;margin-bottom:18px}
.prog{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.bar{flex:1;height:8px;background:var(--surface);border-radius:99px;overflow:hidden}
.fill{height:100%;width:0;background:var(--go);transition:width .3s}
.lbl{font-size:13px;color:var(--ink3);white-space:nowrap}
.ctl{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
input[type=search]{flex:1;min-width:180px;font:inherit;font-size:13px;padding:7px 12px;border:1px solid var(--rule);border-radius:8px;background:var(--panel);color:var(--ink)}
.pill{font:inherit;font-size:12px;padding:5px 11px;border:1px solid var(--rule);background:var(--surface);color:var(--ink3);border-radius:99px;cursor:pointer}
.pill.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.row{display:flex;align-items:center;gap:12px;background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:12px 14px;margin-bottom:8px}
.row.applied{opacity:.55}
.row .who{flex:1}.row .co{font-weight:600}.row .ro{font-size:13px;color:var(--ink3)}
.badge{font-size:11px;font-weight:600;padding:3px 8px;border-radius:6px}
.badge.READY{background:var(--go-bg);color:var(--go)}.badge.TODO{background:var(--warn-bg);color:var(--warn)}
.row input{width:17px;height:17px;accent-color:var(--go);cursor:pointer}
.hidden{display:none}
"""
SCRIPT = r"""
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const KEY='rtk_applied';
const load=()=>{try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return{}}};
const save=s=>{try{localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}};
let st=load();
function prog(){const b=$$('.row input'),n=b.filter(x=>x.checked).length;
  $('#fill').style.width=(n/b.length*100||0)+'%';$('#lbl').textContent=n+' of '+b.length+' applied';}
$$('.row input').forEach(b=>{b.checked=!!st[b.dataset.k];b.closest('.row').classList.toggle('applied',b.checked);
  b.onchange=()=>{st[b.dataset.k]=b.checked;save(st);b.closest('.row').classList.toggle('applied',b.checked);prog();};});
prog();
let flt=null;
function apply(){const q=($('#q').value||'').toLowerCase();
  $$('.row').forEach(r=>{let ok=true;if(flt&&r.dataset.status!==flt)ok=false;
    if(q&&!r.textContent.toLowerCase().includes(q))ok=false;r.classList.toggle('hidden',!ok);});}
$$('.pill').forEach(p=>p.onclick=()=>{const v=p.dataset.v,on=flt===v;$$('.pill').forEach(x=>x.classList.remove('active'));
  flt=on?null:v;if(!on)p.classList.add('active');apply();});
$('#q').oninput=apply;
"""

def build():
    rows = "".join(
        f'<div class="row" data-status="{esc(r["status"])}">'
        f'<input type="checkbox" data-k="{esc(r["key"])}">'
        f'<div class="who"><div class="co">{esc(r["company"])}</div><div class="ro">{esc(r["role"])}</div></div>'
        f'<span class="badge {esc(r["status"])}">{esc(r["status"])}</span></div>'
        for r in ROLES)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Application Tracker</title><style>{STYLE}</style></head><body>
<div class="wrap">
  <h1>Application Tracker</h1>
  <div class="sub">Generated {date.today().isoformat()} &middot; progress saves in your browser &middot; nothing is submitted here</div>
  <div class="prog"><div class="bar"><div class="fill" id="fill"></div></div><div class="lbl" id="lbl"></div></div>
  <div class="ctl"><input id="q" type="search" placeholder="Search company or role...">
    <button class="pill" data-v="READY">Ready</button><button class="pill" data-v="TODO">To do</button></div>
  {rows}
</div><script>{SCRIPT}</script></body></html>"""
    os.makedirs("out", exist_ok=True)
    with open("out/tracker.html", "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote out/tracker.html  ({len(ROLES)} roles)")


if __name__ == "__main__":
    build()
