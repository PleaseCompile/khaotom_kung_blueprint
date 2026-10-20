# -*- coding: utf-8 -*-
"""ข้าวต้มกุ้ง — ประกอบ Prompt, ไฟล์งาน agy, โฟลเดอร์ไทม์ไลน์, progress, FLOW_SHEET, contact sheet, เอกสาร
output/
  00_REF/        REF-1..4.png (+ candidates/)
  01_frames/     ภาพเริ่มต้นทุกภาพ (<id>.png) — agy บันทึกที่นี่ที่เดียว
  02_timeline/   A1_opening/01_P01_0000-0008/ (<id>.png + _flow_prompt.txt + _info.txt) เรียงตามลำดับตัดต่อ
  jobs/          ไฟล์งานสำหรับ agy (+ prompts/)
ใช้: python build.py --check | --jobs | --deliver | --docs
"""
import base64, html, io, json, re, shutil, sys
from pathlib import Path
from structure import BLOCKS, CHEF, NEGATIVE_CHEF, STATES, ACTS, ITEMS, CREDITS, ts

W = Path(__file__).parent; ROOT = W.parent; OUT = ROOT / "output"
REF_DIR, FRAMES, TL, JOBS = OUT / "00_REF", OUT / "01_frames", OUT / "02_timeline", OUT / "jobs"
ACT_DIR = {"A1": "A1_opening", "A2": "A2_prep", "A3": "A3_broth", "A4": "A4_prawns_bowl", "A5": "A5_taste"}
STATUS_FILE = W / "shot_status.json"
REF_SENT = ("Use the attached reference images as the exact look for the kitchen, stove, pot, board and bowls. "
            "Keep identical materials, colors and lighting, and follow the food state described here.")
REF_SENT_CHEF = ("Use the attached reference images as the exact look for the cook, kitchen, stove, pot, board and "
                 "bowls. Keep identical face, clothing, materials, colors and lighting, and follow the food state described here.")
FORBIDDEN = re.compile(r"\b(text|logo|logos|label|labels|brand|letters|writing|sign|bottle|gas|stainless|music)\b", re.I)
RAW_STATES = {"RAW", "RAW_BOARD", "GARLIC0", "GARLICOIL", "PEELING", "PEELED", "GARLIC", "HEADS", "BROTH0", "BROTH", "COOKING"}

def J(name, default=None):
    p = W / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def load():
    return J("img.json", {}), J("vid.json", {}), J("edit.json", {}), J("prompt_overrides.json", {}), J("shot_status.json", {})

def join(*parts):
    return " ".join(p.strip() for p in parts if p and p.strip())

def item(fid):
    return next(i for i in ITEMS if i["id"] == fid)

def still_prompt(fid, img, ov):
    if fid in ov: return ov[fid]
    it = item(fid); chef = it["kind"] == "chef"
    blocks = [BLOCKS[k] for k in ("STOVE", "COUNTER", "PRAWN", "BOWL") if k in it["props"]]
    who = CHEF if chef else (BLOCKS["HANDS"] if "HANDS" in it["props"] else "")
    return join(BLOCKS["LIGHT"], *blocks, who, STATES[it["state"]][1], "16:9 widescreen frame.", img["img"][fid],
                REF_SENT_CHEF if chef else REF_SENT, "Avoid: " + (NEGATIVE_CHEF if chef else BLOCKS["NEGATIVE"]))

def ref_prompt(n, img, ov):
    if f"REF{n}" in ov: return ov[f"REF{n}"]
    body = img[f"REF{n}"]
    if n == 1: return join(BLOCKS["LIGHT"], BLOCKS["STOVE"], BLOCKS["COUNTER"], "16:9 widescreen frame.", body, "Avoid: " + BLOCKS["NEGATIVE"])
    if n == 2: return join(BLOCKS["LIGHT"], BLOCKS["COUNTER"], BLOCKS["PRAWN"], STATES["RAW_BOARD"][1], "16:9 widescreen frame.", body, "Avoid: " + BLOCKS["NEGATIVE"])
    if n == 3: return join(BLOCKS["LIGHT"], BLOCKS["COUNTER"], BLOCKS["BOWL"], STATES["BOWL"][1], "16:9 widescreen frame.", body, "Avoid: " + BLOCKS["NEGATIVE"])
    return join(BLOCKS["LIGHT"], BLOCKS["COUNTER"], CHEF, "16:9 widescreen frame.", body, "Avoid: " + NEGATIVE_CHEF)

def refs_for(it):
    r = [REF_DIR / "REF-1.png"]
    if "PRAWN" in it["props"] and it["state"] in RAW_STATES: r.append(REF_DIR / "REF-2.png")
    if "BOWL" in it["props"]: r.append(REF_DIR / "REF-3.png")             # ชามเสร็จแนบเฉพาะเฟรมที่มีชาม (ผู้ตรวจรอบ 1)
    if it["kind"] == "chef": r.append(REF_DIR / "REF-4.png")
    return [str(x) for x in r]

FLASH_FWD = {"B01"}   # ภาพตัวอย่างตอนจบ ห้ามใช้เป็นเฟรมก่อนหน้า
NO_PREV = {"B03"}     # หม้อน้ำเปล่า ห้ามแนบเฟรมกุ้งก่อนหน้า

def done(fid, st):
    return st.get(fid, {}).get("status") in ("PASS", "WARN")

# ---------- ตรวจกลไก ----------
def check():
    img, vid, ed, ov, st = load(); errs = []
    ids = [i["id"] for i in ITEMS]
    for k in ("REF1", "REF2", "REF3", "REF4"):
        if k not in img: errs.append(f"img missing {k}")
    for fid in ids:
        it = item(fid)
        b = img.get("img", {}).get(fid); v = vid.get(fid); e = ed.get("items", {}).get(fid)
        if not b: errs.append(f"{fid}: no still body"); continue
        if not v: errs.append(f"{fid}: no video prompt")
        if not e: errs.append(f"{fid}: no edit note")
        n = len(b.split())
        if not 25 <= n <= 80: errs.append(f"{fid}: still body {n} words")
        for t, s in (("still", b), ("video", v or "")):
            m = FORBIDDEN.search(s.replace("no on-screen text", ""))
            if m: errs.append(f"{fid}: forbidden '{m.group(0)}' in {t}")
        if re.search(r"same as|as above|ditto", b + (v or ""), re.I): errs.append(f"{fid}: ditto phrase")
        if it["kind"] == "chef" and v:
            if it["line_th"] not in v: errs.append(f"{fid}: Thai line not verbatim")
            if "No subtitles" not in v: errs.append(f"{fid}: missing no-subtitles")
            if not v.rstrip().endswith("camera stable, no morphing, face and food shape unchanged."): errs.append(f"{fid}: bad ending")
        elif v and not v.rstrip().endswith("camera stable, no morphing, food shape unchanged."): errs.append(f"{fid}: bad ending")
    print("\n".join(errs) if errs else "check ok"); return not errs

# ---------- ไฟล์งาน agy ----------
HEAD = ["Use your image generation tool. Landscape 16:9. Use each prompt file's text EXACTLY as the prompt "
        "(no shortening, keep the long style prefix)."]
TAIL = "Reply one line per file: output path + DONE or FAILED + reason. On quota/rate limit stop and reply QUOTA + item id."

def write_ref_jobs(img, ov):
    JOBS.mkdir(parents=True, exist_ok=True); (REF_DIR / "candidates").mkdir(parents=True, exist_ok=True)
    pd = JOBS / "prompts"; pd.mkdir(exist_ok=True)
    for n in (1, 2, 3, 4): (pd / f"REF-{n}.txt").write_text(ref_prompt(n, img, ov), encoding="utf-8")
    c = REF_DIR / "candidates"
    L = ["# Job 1 — REF-1 kitchen set (3 variants)", "", *HEAD, f"- prompt file: {pd / 'REF-1.txt'}",
         "- no attachments", "- generate 3 separate variants, save as:", *[f"  - {c / f'REF-1_v{i}.png'}" for i in (1, 2, 3)], "", TAIL]
    (JOBS / "job1_REF-1.md").write_text("\n".join(L), encoding="utf-8")
    L = ["# Job 2 — REF-2 raw prawns, REF-3 finished bowl, REF-4 cook (3 variants each)", "", *HEAD,
         f"Attach {REF_DIR / 'REF-1.png'} to every image as the look of the kitchen, light and props.", ""]
    for n, what in ((2, "raw prawns"), (3, "finished bowl"), (4, "the cook")):
        L += [f"## REF-{n} ({what})", f"- prompt file: {pd / f'REF-{n}.txt'}", "- 3 separate variants, save as:",
              *[f"  - {c / f'REF-{n}_v{i}.png'}" for i in (1, 2, 3)], ""]
    L.append(TAIL); (JOBS / "job2_REF-2-4.md").write_text("\n".join(L), encoding="utf-8")

def write_frames_job(img, ov, st, ids=None, name="job3_frames"):
    order = [i["id"] for i in ITEMS]; ids = ids or [f for f in order if not done(f, st)]
    pd = JOBS / "prompts"; pd.mkdir(parents=True, exist_ok=True)
    L = [f"# {name} — start frames ({len(ids)} images)", "", *HEAD,
         "Work IN ORDER, one image per item. Attach the reference images listed for each item. "
         f"Save to the output path (folder {FRAMES}); overwrite if it exists.", ""]
    for fid in ids:
        i = order.index(fid); it = item(fid)
        prev = None if fid in NO_PREV else next((order[j] for j in range(i - 1, -1, -1) if item(order[j])["kind"] == it["kind"] and order[j] not in FLASH_FWD), None)  # ภาพแทรกห้ามแนบภาพเชฟ
        r = refs_for(it) + ([str(FRAMES / f"{prev}.png") + " (previous frame, for continuity)"] if prev else [])
        (pd / f"{fid}.txt").write_text(still_prompt(fid, img, ov), encoding="utf-8")
        L += [f"## {fid}", f"- prompt file: {pd / f'{fid}.txt'}", f"- attach: {', '.join(r)}", f"- output: {FRAMES / (fid + '.png')}", ""]
    L.append(TAIL); jf = JOBS / f"{name}.md"; jf.write_text("\n".join(L), encoding="utf-8"); return jf

# ---------- ส่งมอบ ----------
def tl_dir(it, n):
    return TL / ACT_DIR[it["act"]] / f"{n:02d}_{it['id']}_{ts(it['start']).replace(':', '')}-{ts(it['end']).replace(':', '')}"

LAB = {"PASS": "✅ ผ่าน", "WARN": "⚠️ ใช้ภาพดีที่สุด", "REDO": "🔁 ต้องเจนใหม่", "PENDING": "⏳ ยังไม่มี"}

def info_text(it, img, vid, ed, ov, st):
    e = ed.get("items", {}).get(it["id"], {}); s = st.get(it["id"], {})
    L = [f"{it['id']} · {'เชฟพูด' if it['kind'] == 'chef' else 'ภาพแทรก macro'} · องก์ {it['act']}" + (" · ⭐ ไฮไลต์" if it["highlight"] else ""),
         f"เวลาในไทม์ไลน์: {ts(it['start'])}–{ts(it['end'])} ({it['dur']} วินาที)",
         f"เจนใน Flow: วิดีโอ → เฟรม · 16:9 · Omni 1.1 Flash · 720p · {it['gen']} วินาที · x1 ({CREDITS[it['gen']]} เครดิต)",
         f"ภาพในช่อง 'เริ่ม': {it['id']}.png (ไม่ใช้ช่อง 'สิ้นสุด')",
         f"กล้อง: {it['size']} · {it['cam_th']} / {it['cam_en']}", f"สถานะอาหาร: {STATES[it['state']][0]}"]
    if it["kind"] == "chef": L.append(f"บทพูด (ไทย): {it['line_th']}")
    L += [f"ฉาก: {it['action_th']}", f"ช่วงที่ใช้: {e.get('trim', '-')}", f"การตัดต่อ: {e.get('cut', '-')}", f"เสียง: {e.get('sound', '-')}",
          "", f"สถานะภาพเริ่มต้น: {LAB[s.get('status', 'PENDING')]} (เจน {s.get('attempts', 0)} ครั้ง) {s.get('review', '')}"]
    if s.get("note"): L.append(f"หมายเหตุการปรับ Prompt: {s['note']}")
    L += ["", "Prompt ภาพเริ่มต้น:", still_prompt(it["id"], img, ov), ""]
    return "\n".join(L)

def deliver():
    img, vid, ed, ov, st = load()
    if TL.exists(): shutil.rmtree(TL)                       # สร้างใหม่ทุกครั้ง (อยู่ใน output/ เท่านั้น)
    for n, it in enumerate(ITEMS, 1):
        d = tl_dir(it, n); d.mkdir(parents=True, exist_ok=True)
        src = FRAMES / f"{it['id']}.png"
        if src.exists(): shutil.copy2(src, d / f"{it['id']}.png")
        (d / f"{it['id']}_flow_prompt.txt").write_text(vid[it["id"]] + "\n", encoding="utf-8")
        (d / f"{it['id']}_info.txt").write_text(info_text(it, img, vid, ed, ov, st), encoding="utf-8")
    L = ["# Progress — ข้าวต้มกุ้ง (ภาพ REF + ภาพเริ่มต้น)", "", "| ภาพ | เวลา | สถานะ | เจน (ครั้ง) | หมายเหตุ |", "|---|---|---|---|---|"]
    for n in (1, 2, 3, 4):
        s = st.get(f"REF-{n}", {}); L.append(f"| REF-{n} | - | {LAB[s.get('status', 'PENDING')]} | {s.get('attempts', 0)} | {s.get('review', '-')} |")
    for it in ITEMS:
        s = st.get(it["id"], {})
        L.append(f"| {it['id']} | {ts(it['start'])} | {LAB[s.get('status', 'PENDING')]} | {s.get('attempts', 0)} | {s.get('review', '-')} |")
    need = [i["id"] for i in ITEMS if not done(i["id"], st)]
    L += ["", f"ภาพเริ่มต้น {len(ITEMS)} ภาพ · เสร็จ {len(ITEMS) - len(need)} · ยังต้องเจน {len(need)}"]
    if st.get("_log"): L += ["", "## บันทึก", *[f"- {x}" for x in st["_log"]]]
    (OUT / "progress.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    write_flow_sheet(vid, st); write_contact_sheet(st)
    print("deliver ok ·", len(ITEMS) - len(need), "/", len(ITEMS), "frames")

def thumb_b64(p, w=480):
    from PIL import Image
    im = Image.open(p).convert("RGB"); im.thumbnail((w, w))
    b = io.BytesIO(); im.save(b, "JPEG", quality=78); return base64.b64encode(b.getvalue()).decode()

def write_flow_sheet(vid, st):
    cards = []
    for n, it in enumerate(ITEMS, 1):
        p = FRAMES / f"{it['id']}.png"; s = st.get(it["id"], {})
        im = f'<img src="data:image/jpeg;base64,{thumb_b64(p)}" alt="{it["id"]}">' if p.exists() else '<div class="noimg">ยังไม่มีภาพ</div>'
        bd = f'<span class="b">{"🎙 เชฟพูด" if it["kind"] == "chef" else "ภาพแทรก"}</span><span class="b">{it["gen"]} วิ · {CREDITS[it["gen"]]} เครดิต</span>'
        if it["highlight"]: bd += '<span class="b hl">⭐ ไฮไลต์ — ถ้าเหลือเครดิต เจนซ้ำ x2 เลือกอันดีสุด</span>'
        if s.get("status") == "WARN": bd += '<span class="b warn">⚠️ ภาพตรวจไม่ผ่านครบ</span>'
        if not done(it["id"], st): bd += '<span class="b warn">⏳ ภาพยังไม่พร้อม</span>'
        line = f'<p class="line">“{html.escape(it["line_th"])}”</p>' if it["kind"] == "chef" else ""
        src = f"01_frames/{it['id']}.png"
        tools = (f'<div class="tools"><button data-src="{src}" onclick="cpimg(this,this.dataset.src)">Copy ภาพ</button> <a href="{src}" download="{it["id"]}.png">ดาวน์โหลดภาพเต็ม</a></div>' if p.exists() else '')
        cards.append(f'''<article class="card{' is-hl' if it['highlight'] else ''}"><div class="thumb">{im}{tools}</div>
<div class="meta"><h2>{n:02d} · {it['id']} <small>{ts(it['start'])}–{ts(it['end'])} · ใช้ {it['dur']} วิ · {it['act']}</small></h2>
<p class="st">{html.escape(STATES[it['state']][0])} · {it['size']} · {html.escape(it['cam_th'])}</p>{line}
<div class="badges">{bd}</div><pre id="p{it['id']}">{html.escape(vid[it['id']])}</pre>
<button onclick="cp('p{it['id']}',this)">Copy Prompt</button></div></article>''')
    page = f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Khao Tom Flow Sheet</title><style>
:root{{--bg:#f7f3ec;--fg:#1f1b16;--mut:#6d655a;--card:#fff;--line:#e4dccf;--acc:#c0562b;--warn:#b42318}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15120f;--fg:#eee7dd;--mut:#a69c8f;--card:#1f1b17;--line:#363029;--acc:#ef8a5a;--warn:#f97066}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,"Segoe UI","Leelawadee UI",sans-serif}}
header{{padding:20px 16px;border-bottom:1px solid var(--line)}}h1{{margin:0 0 4px;font-size:22px}}header p{{margin:0;color:var(--mut)}}
main{{max-width:1100px;margin:0 auto;padding:16px;display:grid;gap:14px}}
.card{{display:grid;grid-template-columns:320px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.card.is-hl{{border-color:var(--acc)}}.thumb img{{width:100%;border-radius:6px;display:block}}
.noimg{{aspect-ratio:16/9;display:grid;place-items:center;border:1px dashed var(--line);color:var(--mut);border-radius:6px}}
h2{{margin:0;font-size:18px}}h2 small{{font-weight:400;color:var(--mut);font-size:13px}}.st{{margin:2px 0 6px;color:var(--mut);font-size:13px}}
.line{{margin:0 0 6px;font-size:16px}}
.b{{display:inline-block;font-size:12px;padding:2px 8px;border-radius:99px;border:1px solid var(--line);margin:0 6px 4px 0}}
.b.hl{{background:var(--acc);color:#fff;border-color:var(--acc)}}.b.warn{{color:var(--warn);border-color:var(--warn)}}
pre{{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;font:13px/1.45 ui-monospace,Consolas,monospace;margin:8px 0}}
button{{font:inherit;padding:6px 14px;border-radius:6px;border:1px solid var(--acc);background:transparent;color:var(--acc);cursor:pointer}}
button.ok{{background:var(--acc);color:#fff}}
@media (max-width:700px){{.card{{grid-template-columns:1fr}}}}
.tools{{display:flex;gap:10px;align-items:center;margin-top:8px;flex-wrap:wrap}}.tools a{{color:var(--acc);font-size:14px}}nav a{{color:var(--acc);margin-right:14px}}
</style></head><body><header><nav><a href="index.html">หน้าแรก</a><a href="CHARACTER.html">ตัวละคร</a><a href="STEP_BY_STEP_TH.html">เจนภาพทีละขั้น</a></nav><h1>ข้าวต้มกุ้ง — Flow Sheet</h1>
<p>{len(ITEMS)} คลิป · 180 วินาที · 16:9 · วิดีโอ → เฟรม (ใส่ภาพช่อง 'เริ่ม') · Omni 1.1 Flash · 720p · x1 · รวม {sum(CREDITS[i['gen']] for i in ITEMS)} เครดิต</p></header>
<main>{''.join(cards)}</main>
<script>function cp(id,b){{const t=document.getElementById(id).innerText;const done=()=>{{b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{{b.textContent='Copy';b.classList.remove('ok')}},1200)}};
if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(t).then(done)}}else{{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();done()}}}}
{CPIMG_JS}</script>
</body></html>'''
    (OUT / "FLOW_SHEET.html").write_text(page, encoding="utf-8")

CPIMG_JS = """async function toPng(src){const r=await fetch(src);const b=await r.blob();if(b.type==='image/png')return b;const bm=await createImageBitmap(b);const c=document.createElement('canvas');c.width=bm.width;c.height=bm.height;c.getContext('2d').drawImage(bm,0,0);return await new Promise(ok=>c.toBlob(ok,'image/png'))}
async function fromThumb(btn){const img=btn.closest('article,figure').querySelector('img');const c=document.createElement('canvas');c.width=img.naturalWidth;c.height=img.naturalHeight;c.getContext('2d').drawImage(img,0,0);return await new Promise(ok=>c.toBlob(ok,'image/png'))}
async function cpimg(btn,src){const o=btn.textContent;try{let b;try{b=await toPng(src)}catch(e){b=await fromThumb(btn)}await navigator.clipboard.write([new ClipboardItem({'image/png':b})]);btn.textContent='Copied';}catch(e){btn.textContent='ใช้ปุ่มดาวน์โหลดแทน'}setTimeout(()=>btn.textContent=o,1500)}"""

def write_contact_sheet(st):
    from PIL import Image, ImageDraw, ImageFont
    cols, tw, th, pad, lab = 6, 320, 180, 8, 26
    rows = (len(ITEMS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), (16, 15, 14))
    dr = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
    except OSError: font = ImageFont.load_default()
    for i, it in enumerate(ITEMS):
        x = pad + (i % cols) * (tw + pad); y = pad + (i // cols) * (th + lab + pad); p = FRAMES / f"{it['id']}.png"
        if p.exists():
            im = Image.open(p).convert("RGB"); r = max(tw / im.width, th / im.height)
            im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1)); l, t = (im.width - tw) // 2, (im.height - th) // 2
            sheet.paste(im.crop((l, t, l + tw, t + th)), (x, y))
        else: dr.rectangle([x, y, x + tw, y + th], outline=(90, 90, 90))
        mark = (" *" if it["highlight"] else "") + (" !" if st.get(it["id"], {}).get("status") == "WARN" else "")
        dr.text((x + 2, y + th + 4), f"{it['id']} {ts(it['start'])}{mark}", fill=(230, 225, 218), font=font)
    sheet.save(OUT / "contact_sheet.png")

# ---------- เอกสาร ----------
def docs():
    img, vid, ed, ov, st = load()
    cred = sum(CREDITS[i["gen"]] for i in ITEMS)
    L = ["# 02 — Clip List ข้าวต้มกุ้ง (180 วินาที · 30 คลิป)", "",
         "| # | คลิป | เวลา | ใช้ | เจน | ชนิด | กล้อง | สถานะอาหาร | ฉาก / บทพูด |", "|---|---|---|---|---|---|---|---|---|"]
    for n, it in enumerate(ITEMS, 1):
        what = f"🎙 “{it['line_th']}” — {it['action_th']}" if it["kind"] == "chef" else it["action_th"]
        L.append(f"| {n} | {it['id']}{' ⭐' if it['highlight'] else ''} | {ts(it['start'])}–{ts(it['end'])} | {it['dur']} | {it['gen']} | "
                 f"{'เชฟ' if it['kind'] == 'chef' else 'แทรก'} | {it['size']} · {it['cam_th']} | {STATES[it['state']][0]} | {what} |")
    for a in ACTS: L.insert(3, "") if False else None
    (ROOT / "02_cliplist.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    E = ["# 03 — Editing & Sound Flow", "", "## ดนตรี", ed.get("music", "-"), "", "## มิกซ์เสียง", ed.get("mix", "-"), "",
         "## ทีละคลิป", "", "| คลิป | เวลา | ช่วงที่ใช้ | การตัดต่อ | เสียง |", "|---|---|---|---|---|"]
    for it in ITEMS:
        e = ed.get("items", {}).get(it["id"], {})
        E.append(f"| {it['id']} | {ts(it['start'])}–{ts(it['end'])} | {e.get('trim', '-')} | {e.get('cut', '-')} | {e.get('sound', '-')} |")
    (ROOT / "03_editing_flow.md").write_text("\n".join(E) + "\n", encoding="utf-8")
    C = ["# 05 — Copy Sheet (วาง Prompt ใน Flow)", "", "ตั้งค่าทุกคลิป: วิดีโอ → เฟรม · 16:9 · Omni 1.1 Flash · 720p · x1", ""]
    for n, it in enumerate(ITEMS, 1):
        C += [f"## {n:02d} · {it['id']} · {ts(it['start'])}–{ts(it['end'])} · เจน {it['gen']} วิ", f"ภาพเริ่ม: `01_frames/{it['id']}.png`", "",
              "```", vid[it["id"]], "```", ""]
    (ROOT / "05_copy_sheet.md").write_text("\n".join(C), encoding="utf-8")
    S = ["# 01 — Style Guide & บล็อกคำล็อค", "", "ทุก Prompt ภาพประกอบอัตโนมัติ: LIGHT + บล็อกพร็อพ + (CHEF หรือ HANDS) + แท็กสถานะอาหาร + `16:9 widescreen frame.` + ข้อความเฉพาะภาพ + ประโยคอ้างอิง REF + `Avoid:` NEGATIVE", ""]
    for k, v in list(BLOCKS.items()) + [("CHEF", CHEF), ("NEGATIVE_CHEF", NEGATIVE_CHEF)]:
        S += [f"### [{k}] ({len(v.replace(',', ' ').split())} คำ)", "```", v, "```", ""]
    S += ["## แท็กสถานะอาหาร", "", "| แท็ก | ไทย | อังกฤษ |", "|---|---|---|"] + [f"| {k} | {v[0]} | {v[1]} |" for k, v in STATES.items()]
    S += ["", "## Prompt ภาพ REF", ""] + sum([[f"### REF-{n}", "```", ref_prompt(n, img, ov), "```", ""] for n in (1, 2, 3, 4)], [])
    (ROOT / "01_style_guide.md").write_text("\n".join(S), encoding="utf-8")
    R = ["# 00 — README ข้าวต้มกุ้ง", "",
         "วิดีโอทำอาหาร 180 วินาที 16:9 · แม่ครัวไทยพูดกับกล้อง 9 คลิป (72 วินาที) สลับภาพแทรก macro 21 คลิป · ครัวไทยบ้านๆ ตอนเช้า เตาถ่าน ชามตราไก่", "",
         f"- งบ Flow: {cred} เครดิต (Omni 1.1 Flash 720p x1 · เชฟ 10 วิ = 15 · ภาพแทรก 8 วิ = 12 · B16/B20 10 วิ) — ไฮไลต์ ⭐ 9 คลิป ถ้าเหลือเครดิตให้เจนซ้ำ",
         "- เปิด `output/FLOW_SHEET.html` → กด Copy → วางใน Flow พร้อมภาพเริ่มต้นจาก `output/01_frames/`",
         "- หรือเปิดโฟลเดอร์ `output/02_timeline/` เรียงตามลำดับตัดต่อ มีภาพ + Prompt + info ทุกคลิป",
         "- ไฟล์: 01_style_guide · 02_cliplist · 03_editing_flow · 04_review_report · 05_copy_sheet · output/progress.md · output/contact_sheet.png", "",
         "## องก์", ""] + [f"- {a[0]} {ts(a[2])}–{ts(a[3])} {a[1]}" for a in ACTS] + [
         "", "## ข้อควรรู้", "- คลิปเชฟ: Flow สร้างเสียงพูดไทยในคลิป ถ้าปากไม่ตรงหรือออกเสียงผิด ให้เจนซ้ำคลิปนั้น (15 เครดิต) หรือพากย์ทับ",
         "- ภาพแทรกห้ามมีใบหน้า ใบหน้าเดียวในเรื่องคือแม่ครัว (REF-4)"]
    (ROOT / "00_README.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    print("docs ok")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--check" in a: check()
    if "--jobs" in a:
        img, vid, ed, ov, st = load(); write_ref_jobs(img, ov); print(write_frames_job(img, ov, st))
    if "--deliver" in a: deliver()
    if "--docs" in a: docs()
