# -*- coding: utf-8 -*-
"""หน้าเว็บสำหรับเปิดผ่าน Cloudflare Tunnel: output/index.html (หน้าแรก) + output/CHARACTER.html (ชุดตัวละครแม่ครัวสำหรับ Flow)"""
import html
from pathlib import Path
from build import CPIMG_JS
from structure import CHEF

OUT = Path(__file__).parent.parent / "output"
CSS = """:root{--bg:#f7f3ec;--fg:#1f1b16;--mut:#6d655a;--card:#fff;--line:#e4dccf;--acc:#c0562b}
@media (prefers-color-scheme:dark){:root{--bg:#15120f;--fg:#eee7dd;--mut:#a69c8f;--card:#1f1b17;--line:#363029;--acc:#ef8a5a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Segoe UI","Leelawadee UI",sans-serif}
header{padding:18px 16px;border-bottom:1px solid var(--line)}h1{margin:0 0 4px;font-size:22px}header p{margin:2px 0;color:var(--mut)}
nav a{color:var(--acc);margin-right:14px}main{max-width:1100px;margin:0 auto;padding:16px}h2{font-size:18px;margin:22px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:12px}
pre{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:10px;font:14px/1.6 system-ui,"Leelawadee UI",sans-serif}
button{font:inherit;padding:5px 12px;border-radius:6px;border:1px solid var(--acc);background:transparent;color:var(--acc);cursor:pointer}button.ok{background:var(--acc);color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px}
figure img{width:100%;border-radius:6px;display:block}figcaption{font-size:13px;color:var(--mut);margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}figcaption a{color:var(--acc)}
ol li{margin:4px 0}.links a{display:block;padding:14px 16px;margin-bottom:10px;background:var(--card);border:1px solid var(--line);border-radius:10px;color:var(--fg);text-decoration:none}
.links a b{color:var(--acc)}"""
NAV = '<nav><a href="index.html">หน้าแรก</a><a href="FLOW_SHEET.html">Flow Sheet</a><a href="CHARACTER.html">ตัวละคร</a><a href="STEP_BY_STEP_TH.html">เจนภาพทีละขั้น</a></nav>'
COPY_JS = """function cp(id,b){const t=document.getElementById(id).innerText;const d=()=>{const o=b.textContent;b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{b.textContent=o;b.classList.remove('ok')},1200)};
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(d)}else{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();d()}}"""

def page(title, h1, sub, body):
    return (f'<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{CSS}</style></head><body><header>{NAV}<h1>{h1}</h1><p>{sub}</p></header><main>{body}</main>'
            f'<script>{COPY_JS}\n{CPIMG_JS}</script></body></html>')

CAP = {"C01_front": "หน้าตรง", "C02_three_quarter_left": "หัน 3/4 (ขวาของเธอ)", "C03_three_quarter_right": "หัน 3/4 (ซ้ายของเธอ)",
       "C04_profile": "ด้านข้าง เห็นมวยผม", "C05_full_body": "เต็มตัว", "C06_talking": "กำลังพูดในครัว (16:9)",
       "C07_hands": "มือ + แขนเสื้อ (16:9)", "C08_closeup_smile": "ใบหน้ายิ้มระยะใกล้"}
NAME = "แม่ครัวข้าวต้มกุ้ง"
DESC_EN = (CHEF + " Warm, kind and calm; speaks Thai to camera in a gentle mid-pitched voice with a natural central Thai "
           "accent, ending sentences politely with 'ค่ะ'. Moves slowly and naturally like an experienced home cook.")
DESC_TH = ("หญิงไทยวัยห้าสิบต้นๆ ผมดำเกล้ามวยต่ำ ยิ้มอบอุ่นใจดี สวมเสื้อผ้าฝ้ายสีครามซีดพับแขน ผ้ากันเปื้อนสีครีมเรียบไม่มีลาย มือเปล่าสะอาด "
           "พูดภาษาไทยกับกล้องด้วยน้ำเสียงนุ่ม ระดับเสียงกลาง สำเนียงภาคกลาง ลงท้ายด้วย 'ค่ะ' เคลื่อนไหวช้าๆ เป็นธรรมชาติแบบแม่ครัวบ้านๆ")

def character():
    figs = []
    for f in sorted((OUT / "03_character").glob("C0*.png")):
        src = f"03_character/{f.name}"
        figs.append(f'<figure><img src="{src}" alt="{f.stem}" loading="lazy"><figcaption><b>{f.stem[:3]}</b> {CAP.get(f.stem, "")}'
                    f'<button data-src="{src}" onclick="cpimg(this,this.dataset.src)">Copy ภาพ</button><a href="{src}" download>ดาวน์โหลด</a></figcaption></figure>')
    refs = "".join(f'<figure><img src="{s}" alt="{n}" loading="lazy"><figcaption><b>{n}</b><a href="{s}" download>ดาวน์โหลด</a></figcaption></figure>'
                   for n, s in (("REF-4 ต้นแบบ", "00_REF/REF-4.png"), ("P01 ในฉาก", "01_frames/P01.png"), ("P02 ในฉาก", "01_frames/P02.png")))
    body = f"""<div class="card"><b>ตั้งตัวละครใน Flow (ทำครั้งเดียว ใช้ได้ทุกคลิป)</b><ol>
<li>Flow → เมนูซ้าย <b>ตัวละคร</b> → <b>ตัวละครใหม่</b></li>
<li>กด <b>อัปโหลด</b> แล้วเลือกภาพ C01, C02, C04, C05, C08 (ดาวน์โหลดจากด้านล่าง) — หน้าตรง/ข้าง/เต็มตัวช่วยให้หน้าไม่เพี้ยน</li>
<li>ตั้งชื่อ: <b>{NAME}</b> แล้ววางคำอธิบาย (อังกฤษ แนะนำ) ในช่อง "อธิบายตัวละครของคุณ" · รุ่น Nano Banana 2.1</li>
<li>ตอนเจนคลิปเชฟ P01–P09: ใส่ภาพเริ่มต้นจาก Flow Sheet ในช่อง 'เริ่ม' และเลือกตัวละครนี้แนบด้วย</li></ol></div>
<h2>คำอธิบายตัวละคร</h2>
<div class="card"><b>English (แนะนำ)</b><pre id="den">{html.escape(DESC_EN)}</pre><button onclick="cp('den',this)">Copy</button></div>
<div class="card"><b>ภาษาไทย</b><pre id="dth">{html.escape(DESC_TH)}</pre><button onclick="cp('dth',this)">Copy</button></div>
<h2>ชุดภาพตัวละคร (03_character)</h2><div class="grid">{''.join(figs)}</div>
<h2>ภาพต้นแบบที่ใช้ล็อกหน้า</h2><div class="grid">{refs}</div>"""
    (OUT / "CHARACTER.html").write_text(page("Khao Tom Character", "ตัวละคร — แม่ครัวข้าวต้มกุ้ง",
                                             "ชุดภาพอ้างอิง + คำอธิบาย สำหรับเมนู 'ตัวละคร' ใน Google Flow ให้หน้าไม่หลุดโทนทุกคลิป", body), encoding="utf-8")

def index():
    body = """<div class="links">
<a href="FLOW_SHEET.html"><b>Flow Sheet</b><br>30 คลิป · ภาพเริ่มต้น + Prompt วิดีโอ · Copy ภาพ / Copy Prompt / ดาวน์โหลด</a>
<a href="CHARACTER.html"><b>ตัวละคร</b><br>ชุดภาพแม่ครัว 8 มุม + คำอธิบาย สำหรับตั้งตัวละครใน Flow</a>
<a href="STEP_BY_STEP_TH.html"><b>เจนภาพทีละขั้น (ไทย)</b><br>คำสั่งภาพภาษาไทยแบ่งเฟส</a>
<a href="contact_sheet.png"><b>Contact sheet</b><br>ภาพรวม 30 ภาพ</a>
<a href="khaotom_timeline.zip"><b>ดาวน์โหลดโฟลเดอร์ไทม์ไลน์ (.zip)</b><br>ภาพ + Prompt + info ทีละคลิปตามลำดับตัดต่อ</a></div>
<div class="card">ขั้นตอนใน Flow: ตั้งตัวละครครั้งเดียว → แต่ละคลิป: วิดีโอ → เฟรม · ใส่ภาพเริ่มต้นช่อง 'เริ่ม' · 16:9 · Omni 1.1 Flash · 720p · x1 → วาง Prompt → สร้าง</div>"""
    (OUT / "index.html").write_text(page("Khao Tom Project", "ข้าวต้มกุ้ง — โปรเจกต์วิดีโอ", "180 วินาที · 30 คลิป · แม่ครัวพูด 9 คลิป + ภาพแทรก 21 คลิป", body), encoding="utf-8")

if __name__ == "__main__":
    character(); index(); print("web ok")
