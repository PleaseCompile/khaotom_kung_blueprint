# -*- coding: utf-8 -*-
"""แผนเจนภาพแบบก๊อปวางเอง ทีละภาพ แบ่งเฟส → output/STEP_BY_STEP_TH.html + 08_step_by_step_TH.md
ผู้ใช้เจนใน Gemini เว็บ แล้วส่งภาพกลับมาในแชทพร้อมรหัส → save_image.py จัดเข้าโฟลเดอร์
"""
import base64, html, io, json
from pathlib import Path
from structure import ITEMS, ACTS, STATES, ts
from build import refs_for, J
from build_th import ref_th, frame_th

W = Path(__file__).parent; ROOT = W.parent; OUT = ROOT / "output"
REF_WHAT = {1: "ฉากครัวเปล่า (ไม่มีคน ไม่มีอาหาร)", 2: "กุ้งแม่น้ำดิบบนเขียง", 3: "ข้าวต้มกุ้งในชามตราไก่", 4: "ตัวแม่ครัว"}

def phases():
    P = [("เฟส 1 · ภาพอ้างอิง (REF)", "ทำก่อนทุกอย่าง · REF-1 ก่อน แล้วค่อย REF-2 ถึง 4 (แนบ REF-1)",
          [dict(key=f"REF-{n}", title=f"REF-{n} · {REF_WHAT[n]}", attach=[] if n == 1 else ["REF-1.png"],
                prompt=ref_th(n), note="เจนได้หลายรอบจนพอใจ แล้วส่งภาพที่เลือกมาภาพเดียว") for n in (1, 2, 3, 4)])]
    for k, (aid, name, a0, a1) in enumerate(ACTS, 2):
        rows = []
        for it in ITEMS:
            if it["act"] != aid: continue
            n = ITEMS.index(it) + 1
            rows.append(dict(key=it["id"], title=f"{n:02d} · {it['id']} · {'🎙 แม่ครัวพูด' if it['kind'] == 'chef' else 'ภาพแทรก'} · {ts(it['start'])}",
                             attach=[Path(r).name for r in refs_for(it)], prompt=frame_th(it),
                             note=f"{it['action_th']} · สถานะ: {STATES[it['state']][0]}"))
        P.append((f"เฟส {k} · องก์ {aid} {name}", f"{ts(a0)}–{ts(a1)} · {len(rows)} ภาพ", rows))
    return P

def ref_data(name, w=1280):
    from PIL import Image
    f = OUT / "00_REF" / name
    if not f.exists(): return None
    im = Image.open(f).convert("RGB"); im.thumbnail((w, w)); b = io.BytesIO(); im.save(b, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def ref_html(names):
    out = []
    for a in names:
        d = (OUT / "00_REF" / a).exists()
        if d: out.append(f'<figure><img data-ref="{a}" alt="{a}" draggable="true"><figcaption>{a} <button onclick="cpi(this)">Copy ภาพ</button></figcaption></figure>')
        else: out.append(f'<figure class="miss"><div>{a}<br>ยังไม่มีภาพ</div></figure>')
    return '<div class="refs">' + "".join(out) + "</div>" if out else '<p class="m">ไม่ต้องแนบภาพ</p>'

def main():
    st = J("shot_status.json", {})
    P = phases(); total = sum(len(r) for _, _, r in P)
    md = ["# 08 — เจนภาพทีละขั้น (ก๊อปวางเอง)", "",
          "ทุกภาพ: Gemini → แชทใหม่ → + → สร้างรูปภาพ → สัดส่วน 16:9 → แนบภาพ (+ → อัปโหลดไฟล์ จาก `output/00_REF/`) → วางคำสั่ง → ส่ง",
          "ได้ภาพที่พอใจแล้ว: ส่งภาพมาในแชท Claude Code พร้อมพิมพ์รหัส เช่น `P01` → ผมจัดเข้าโฟลเดอร์และบอกภาพถัดไป", ""]
    sec = []
    for title, sub, rows in P:
        md += [f"## {title}", sub, ""]
        cards = []
        for r in rows:
            ok = r["key"] in st and st[r["key"]].get("status") in ("PASS", "WARN")
            att = ", ".join(f"output/00_REF/{a}" for a in r["attach"]) or "ไม่ต้องแนบ"
            md += [f"### {'✅' if ok else '⬜'} {r['title']}", f"- แนบ: {att}", f"- {r['note']}", "", "```", r["prompt"], "```", ""]
            res = (f'<p><b>ภาพที่ได้:</b></p><img class="res" src="{("00_REF" if r["key"].startswith("REF") else "01_frames")}/{r["key"]}.png">' if ok else '')
            cards.append(f'''<article class="card{' done' if ok else ''}" id="k{r['key']}"><div class="top"><label><input type="checkbox" data-k="{r['key']}"{' checked' if ok else ''}> <b>{html.escape(r['title'])}</b></label>
<span class="tag">{'✅ ได้ภาพแล้ว' if ok else 'ยังไม่มีภาพ'}</span></div>
<p class="m">{html.escape(r['note'])}</p><p><b>1) แนบภาพ</b> (กด Copy ภาพ แล้ว Ctrl+V ในช่องพิมพ์ Gemini หรือลากภาพไปวาง):</p>{ref_html(r['attach'])}{res}<p><b>2) คำสั่ง</b></p>
<details><summary>ดูคำสั่ง</summary><pre id="p{r['key']}">{html.escape(r['prompt'])}</pre></details>
<button onclick="cp('p{r['key']}',this)">Copy คำสั่ง</button> <button onclick="cpt('{r['key']}',this)">Copy รหัส {r['key']}</button></article>''')
        sec.append(f'<section><h2>{html.escape(title)}</h2><p class="sub">{html.escape(sub)}</p>{"".join(cards)}</section>')
    (ROOT / "08_step_by_step_TH.md").write_text("\n".join(md), encoding="utf-8")
    done_n = sum(1 for _, _, rows in P for r in rows if st.get(r["key"], {}).get("status") in ("PASS", "WARN"))
    page = f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Khao Tom Step by Step</title><style>
:root{{--bg:#f7f3ec;--fg:#1f1b16;--mut:#6d655a;--card:#fff;--line:#e4dccf;--acc:#c0562b;--ok:#2f7d4f}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15120f;--fg:#eee7dd;--mut:#a69c8f;--card:#1f1b17;--line:#363029;--acc:#ef8a5a;--ok:#6fcf97}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Segoe UI","Leelawadee UI",sans-serif}}
header{{padding:18px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:2}}
h1{{margin:0 0 4px;font-size:21px}}header p{{margin:2px 0;color:var(--mut);font-size:14px}}
.bar{{height:8px;background:var(--line);border-radius:9px;overflow:hidden;margin-top:8px}}.bar i{{display:block;height:100%;background:var(--ok)}}
main{{max-width:900px;margin:0 auto;padding:16px}}section{{margin-bottom:26px}}h2{{font-size:19px;margin:0}}.sub{{margin:0 0 10px;color:var(--mut)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin-bottom:10px}}.card.done{{opacity:.6;border-color:var(--ok)}}
.top{{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}}.tag{{font-size:12px;color:var(--mut)}}.card.done .tag{{color:var(--ok)}}
.m{{margin:2px 0;color:var(--mut);font-size:13px}}.card p{{margin:3px 0}}summary{{cursor:pointer;color:var(--acc)}}
pre{{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:10px;font:14px/1.6 "Leelawadee UI",system-ui,sans-serif}}
button{{font:inherit;padding:5px 12px;border-radius:6px;border:1px solid var(--acc);background:transparent;color:var(--acc);cursor:pointer;margin-top:6px}}button.ok{{background:var(--acc);color:#fff}}
input{{width:18px;height:18px;vertical-align:-3px}}
.refs{{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0}}figure{{margin:0;width:220px}}figure img{{width:100%;border-radius:6px;display:block;cursor:grab}}
figcaption{{font-size:12px;color:var(--mut);display:flex;justify-content:space-between;align-items:center;gap:4px}}figcaption button{{margin:4px 0 0;padding:2px 8px;font-size:12px}}
.miss div{{aspect-ratio:16/9;border:1px dashed var(--line);border-radius:6px;display:grid;place-items:center;text-align:center;font-size:12px;color:var(--mut)}}
.res{{width:320px;max-width:100%;border-radius:6px;border:2px solid var(--ok)}}
</style></head><body><header><h1>ข้าวต้มกุ้ง — เจนภาพทีละขั้น</h1>
<p>Gemini → แชทใหม่ → + → สร้างรูปภาพ → 16:9 → แนบภาพจาก <code>output/00_REF/</code> → Copy คำสั่ง → ส่ง</p>
<p>ได้ภาพที่พอใจ → ส่งภาพมาในแชท Claude Code พร้อมรหัส (เช่น <b>P01</b>) · ติ๊กช่องได้เองเพื่อกันลืม</p>
<p>เสร็จแล้ว {done_n}/{total} ภาพ</p><div class="bar"><i style="width:{100 * done_n // total}%"></i></div></header>
<main>{''.join(sec)}</main>
<script>
const R={json.dumps({f'REF-{n}.png': ref_data(f'REF-{n}.png') for n in (1, 2, 3, 4) if ref_data(f'REF-{n}.png')})};
document.querySelectorAll('img[data-ref]').forEach(i=>i.src=R[i.dataset.ref]);
const K='khaotom-steps';let s={{}};try{{s=JSON.parse(localStorage.getItem(K)||'{{}}')}}catch(e){{}}
document.querySelectorAll('input[data-k]').forEach(c=>{{if(s[c.dataset.k])c.checked=true;c.onchange=()=>{{s[c.dataset.k]=c.checked;try{{localStorage.setItem(K,JSON.stringify(s))}}catch(e){{}}}}}});
function put(t,b){{const o=b.textContent;const d=()=>{{b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{{b.textContent=o;b.classList.remove('ok')}},1200)}};
if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(t).then(d)}}else{{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();d()}}}}
function cp(id,b){{put(document.getElementById(id).innerText,b)}}
async function cpi(b){{const img=b.closest('figure').querySelector('img');const c=document.createElement('canvas');c.width=img.naturalWidth;c.height=img.naturalHeight;c.getContext('2d').drawImage(img,0,0);
c.toBlob(async bl=>{{try{{await navigator.clipboard.write([new ClipboardItem({{'image/png':bl}})]);b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{{b.textContent='Copy ภาพ';b.classList.remove('ok')}},1200)}}catch(e){{b.textContent='ลากภาพแทน'}}}},'image/png')}}function cpt(k,b){{put(k,b)}}
</script></body></html>'''
    (OUT / "STEP_BY_STEP_TH.html").write_text(page, encoding="utf-8")
    print("steps ok ·", done_n, "/", total)

if __name__ == "__main__":
    main()
