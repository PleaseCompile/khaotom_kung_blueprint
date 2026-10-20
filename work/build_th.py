# -*- coding: utf-8 -*-
"""คำสั่งเจนภาพภาษาไทย (สำหรับวางใน Gemini บนเว็บ) — ประกอบแบบเดียวกับ build.py แต่ใช้ข้อความจาก img_th.json
ผลลัพธ์: output/IMAGE_SHEET_TH.html (มีปุ่ม Copy) · output/jobs/prompts_th/<id>.txt · 06_image_prompts_TH.md
"""
import html, json
from pathlib import Path
from structure import ITEMS, STATES
from build import refs_for, FLASH_FWD, NO_PREV, J

W = Path(__file__).parent; ROOT = W.parent; OUT = ROOT / "output"
T = J("img_th.json"); B = T["blocks"]
ORDER = [i["id"] for i in ITEMS]

def join(*p):
    return " ".join(x.strip() for x in p if x and x.strip())

def ref_th(n):
    body = T[f"REF{n}"]
    if n == 1: return join(B["LIGHT"], B["STOVE"], B["COUNTER"], T["frame"], body, T["avoid"] + " " + B["NEGATIVE"])
    if n == 2: return join(B["LIGHT"], B["COUNTER"], B["PRAWN"], T["states"]["RAW_BOARD"], T["frame"], body, T["avoid"] + " " + B["NEGATIVE"])
    if n == 3: return join(B["LIGHT"], B["COUNTER"], B["BOWL"], T["states"]["BOWL"], T["frame"], body, T["avoid"] + " " + B["NEGATIVE"])
    return join(B["LIGHT"], B["COUNTER"], B["CHEF"], T["frame"], body, T["avoid"] + " " + B["NEGATIVE_CHEF"])

LEAD = ("สร้างภาพใหม่ตามคำอธิบายนี้ ห้ามคัดลอกภาพที่แนบมา ภาพที่แนบใช้ดูหน้าตาของวัสดุ สี แสง และตัวละครเท่านั้น "
        "ต้องจัดเฟรม ระยะภาพ และมุมกล้องใหม่ตามที่เขียนไว้ด้านล่าง:")

def frame_th(it):
    chef = it["kind"] == "chef"
    props = [B[k] for k in ("STOVE", "COUNTER", "PRAWN", "BOWL") if k in it["props"]]
    who = B["CHEF"] if chef else (B["HANDS"] if "HANDS" in it["props"] else "")
    return join(LEAD, T["img"][it["id"]], T["frame"], T["states"][it["state"]], B["LIGHT"], *props, who,
                T["ref_sent_chef"] if chef else T["ref_sent"], T["avoid"] + " " + (B["NEGATIVE_CHEF"] if chef else B["NEGATIVE"]))

def attach_th(it):
    i = ORDER.index(it["id"])
    prev = None if it["id"] in NO_PREV else next((ORDER[j] for j in range(i - 1, -1, -1)
             if ITEMS[j]["kind"] == it["kind"] and ORDER[j] not in FLASH_FWD), None)
    names = [Path(r).name for r in refs_for(it)] + ([f"{prev}.png (ภาพก่อนหน้า)"] if prev else [])
    return names

def main():
    pd = OUT / "jobs" / "prompts_th"; pd.mkdir(parents=True, exist_ok=True)
    rows = []   # (key, title, save, attach, prompt, note)
    what = {1: "ฉากครัว (ไม่มีคนและอาหาร)", 2: "กุ้งแม่น้ำดิบ", 3: "ข้าวต้มกุ้งในชามตราไก่", 4: "ตัวแม่ครัว"}
    for n in (1, 2, 3, 4):
        rows.append((f"REF-{n}", f"REF-{n} · {what[n]}", f"00_REF/candidates/REF-{n}_v1.png, _v2.png, _v3.png → เลือกภาพดีที่สุดเซฟเป็น 00_REF/REF-{n}.png",
                     [] if n == 1 else ["REF-1.png"], ref_th(n), "เจน 3 แบบ"))
    for k, it in enumerate(ITEMS, 1):
        rows.append((it["id"], f"{k:02d} · {it['id']} · {'แม่ครัวพูด' if it['kind'] == 'chef' else 'ภาพแทรก'} · {STATES[it['state']][0]}",
                     f"01_frames/{it['id']}.png", attach_th(it), frame_th(it), it["action_th"]))
    for key, *_, pr, _n in rows: (pd / f"{key}.txt").write_text(pr, encoding="utf-8")
    md = ["# 06 — คำสั่งเจนภาพภาษาไทย (วางใน Gemini บนเว็บ)", "",
          "ขั้นตอน: แนบภาพอ้างอิงตามที่ระบุ → วางคำสั่ง → เลือกสัดส่วน 16:9 → ดาวน์โหลดแล้วเซฟตามชื่อไฟล์ (โฟลเดอร์ `output/`)",
          "ลำดับ: REF-1 ก่อน → REF-2, 3, 4 → ภาพเริ่มต้นเรียงตามลำดับ", ""]
    cards = []
    for key, title, save, att, pr, note in rows:
        md += [f"## {title}", f"- เซฟเป็น: `{save}`", f"- แนบ: {', '.join(att) if att else 'ไม่ต้องแนบ'}", "", "```", pr, "```", ""]
        cards.append(f'''<article class="card"><h2>{html.escape(title)}</h2><p class="m">{html.escape(note)}</p>
<p><b>เซฟเป็น:</b> <code>{html.escape(save)}</code></p><p><b>แนบภาพ:</b> {html.escape(', '.join(att)) if att else 'ไม่ต้องแนบ'}</p>
<pre id="t{key}">{html.escape(pr)}</pre><button onclick="cp('t{key}',this)">Copy</button></article>''')
    (ROOT / "06_image_prompts_TH.md").write_text("\n".join(md), encoding="utf-8")
    page = f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Khao Tom Image Prompts</title><style>
:root{{--bg:#f7f3ec;--fg:#1f1b16;--mut:#6d655a;--card:#fff;--line:#e4dccf;--acc:#c0562b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15120f;--fg:#eee7dd;--mut:#a69c8f;--card:#1f1b17;--line:#363029;--acc:#ef8a5a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Segoe UI","Leelawadee UI",sans-serif}}
header{{padding:20px 16px;border-bottom:1px solid var(--line)}}h1{{margin:0 0 4px;font-size:22px}}header p{{margin:2px 0;color:var(--mut)}}
main{{max-width:900px;margin:0 auto;padding:16px;display:grid;gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}h2{{margin:0;font-size:18px}}
.m{{margin:2px 0 8px;color:var(--mut);font-size:13px}}.card p{{margin:4px 0}}code{{font-size:13px}}
pre{{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:10px;font:14px/1.6 "Leelawadee UI",system-ui,sans-serif;margin:8px 0}}
button{{font:inherit;padding:6px 14px;border-radius:6px;border:1px solid var(--acc);background:transparent;color:var(--acc);cursor:pointer}}button.ok{{background:var(--acc);color:#fff}}
</style></head><body><header><h1>ข้าวต้มกุ้ง — คำสั่งเจนภาพภาษาไทย</h1>
<p>แนบภาพอ้างอิงตามที่ระบุ → กด Copy → วางใน Gemini → เลือก 16:9 → เซฟตามชื่อไฟล์ในโฟลเดอร์ output/</p>
<p>ทำ REF-1 ก่อน แล้วจึง REF-2 ถึง REF-4 จากนั้นภาพเริ่มต้นตามลำดับ (ต้องใช้ภาพก่อนหน้าแนบต่อ)</p></header>
<main>{''.join(cards)}</main>
<script>function cp(id,b){{const t=document.getElementById(id).innerText;const done=()=>{{b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{{b.textContent='Copy';b.classList.remove('ok')}},1200)}};
if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(t).then(done)}}else{{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();done()}}}}</script>
</body></html>'''
    (OUT / "IMAGE_SHEET_TH.html").write_text(page, encoding="utf-8")
    print("th ok ·", len(rows), "prompts")

if __name__ == "__main__":
    main()
