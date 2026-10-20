# -*- coding: utf-8 -*-
"""คำสั่งสำหรับ Claude in Chrome (สั่งเจนภาพใน Gemini เว็บ ทีละ 10 ภาพ) → output/CHROME_COMMANDS_TH.html + 07_chrome_commands_TH.md
ภาพอ้างอิงดึงจาก Google Drive โฟลเดอร์ NAM/khaotom_REF (ผ่านปุ่ม 'เพิ่มจากไดรฟ์' ของ Gemini)
"""
import html
from pathlib import Path
from structure import ITEMS
from build import refs_for
from build_th import ref_th, frame_th

W = Path(__file__).parent; ROOT = W.parent; OUT = ROOT / "output"
DRIVE = "https://drive.google.com/drive/folders/1-uLoaCJUNxYiOrGnPBXMvxhtTk50CTCO"
REF_FOLDER = "NAM → khaotom_REF"

COMMON = f"""กติกาทุกภาพ:
- เปิดแท็บใหม่ที่ https://gemini.google.com/app แล้วเริ่มแชทใหม่ (1 ภาพ = 1 แชท/1 แท็บ ห้ามเจนหลายภาพในแชทเดียว)
- กดปุ่ม + ในช่องพิมพ์ → เลือก "สร้างรูปภาพ" → ตั้ง "สัดส่วนภาพ" เป็น 16:9
- ถ้ารายการนั้นระบุให้แนบภาพ: กดปุ่ม + → "เพิ่มจากไดรฟ์" → เปิดโฟลเดอร์ {REF_FOLDER} → เลือกไฟล์ตามชื่อที่ระบุ (เลือกได้หลายไฟล์พร้อมกัน) → แทรก
- วางข้อความคำสั่งของรายการนั้นทั้งหมดแบบคำต่อคำ ห้ามย่อ ห้ามแปล ห้ามเพิ่มคำ แล้วกดส่ง
- ทำแบบนี้จนครบทุกรายการในชุด (ส่งไว้ทุกแท็บก่อน ไม่ต้องรอทีละภาพ)
- จากนั้นวนกลับไปทีละแท็บตามลำดับ เมื่อภาพเสร็จให้กดดาวน์โหลดภาพขนาดเต็ม (ดาวน์โหลดตามลำดับรายการเท่านั้น เพื่อให้ชื่อไฟล์จับคู่ถูก)
- ถ้าแท็บไหนเจนไม่สำเร็จหรือขึ้นข้อผิดพลาด ให้กดลองใหม่ 1 ครั้ง ถ้ายังไม่ได้ให้ข้ามและจดไว้
- ห้ามเปลี่ยนชื่อหรือแก้อะไรใน Google Drive ห้ามลบไฟล์
- เสร็จแล้วรายงานเป็นตาราง: ลำดับ | รหัสภาพ | ดาวน์โหลดแล้ว / ไม่สำเร็จ | ลิงก์แท็บ (เพื่อให้ฉันกลับไปแก้ภาพในแชทเดิมได้)"""

def attach_names(it):
    return [Path(r).name for r in refs_for(it)]   # ชุดละ 10 ภาพพร้อมกัน จึงไม่แนบภาพก่อนหน้า ใช้เฉพาะ REF

def block(title, intro, rows):
    L = [f"คุณคือผู้ช่วยสั่งงานบนเบราว์เซอร์ งาน: {title}", "", intro, "", COMMON, "", "รายการ:"]
    for n, (rid, att, pr) in enumerate(rows, 1):
        L += ["", f"[{n}] รหัส {rid}", f"แนบ: {', '.join(att) if att else 'ไม่ต้องแนบ'}", "คำสั่ง:", pr]
    return "\n".join(L)

def main():
    cmds = []
    cmds.append(("ชุด 0 — REF-1 ฉากครัว (3 แบบ)",
                 "ไม่ต้องแนบภาพ", block("เจนภาพ REF-1 ฉากครัว 3 แบบ (สั่งคำสั่งเดียวกัน 3 แท็บ)", "รายการทั้ง 3 ใช้คำสั่งเดียวกัน แต่ละแท็บจะได้ภาพต่างกัน",
                       [(f"REF-1_v{i}", [], ref_th(1)) for i in (1, 2, 3)])))
    cmds.append(("ชุด 1 — REF-2 กุ้งดิบ, REF-3 ชามข้าวต้ม, REF-4 แม่ครัว (อย่างละ 3 แบบ = 9 แท็บ)",
                 "แนบ REF-1.png ทุกแท็บ",
                 block("เจนภาพอ้างอิง REF-2, REF-3, REF-4 อย่างละ 3 แบบ", "ทุกแท็บแนบ REF-1.png จาก Drive",
                       [(f"REF-{n}_v{i}", ["REF-1.png"], ref_th(n)) for n in (2, 3, 4) for i in (1, 2, 3)])))
    for b in range(3):
        part = ITEMS[b * 10:(b + 1) * 10]
        rows = [(it["id"], attach_names(it), frame_th(it)) for it in part]
        cmds.append((f"ชุด {b + 2} — ภาพเริ่มต้น {b * 10 + 1:02d}–{b * 10 + 10:02d} ({part[0]['id']}–{part[-1]['id']})",
                     "แนบ REF ตามที่ระบุในแต่ละรายการ",
                     block(f"เจนภาพเริ่มต้นชุดที่ {b + 1} ({len(part)} ภาพ)", "ภาพอ้างอิงทุกไฟล์อยู่ใน Drive โฟลเดอร์ " + REF_FOLDER, rows)))
    fix = ("ในแท็บของภาพ <รหัส> (แชทเดิม) พิมพ์คำสั่งแก้นี้แล้วส่ง: \"แก้ภาพนี้: <สิ่งที่ต้องแก้ เช่น เอากุ้งออกจากหม้อ / ให้แสงอุ่นขึ้น> "
           "คงทุกอย่างที่เหลือไว้เหมือนเดิม สัดส่วน 16:9\" เมื่อเสร็จให้ดาวน์โหลดภาพใหม่ แล้วรายงานรหัสภาพที่ดาวน์โหลด")
    md = ["# 07 — คำสั่ง Claude in Chrome (เจนภาพใน Gemini ทีละ 10)", "", f"Drive: {DRIVE}", ""]
    for t, att, c in cmds: md += [f"## {t}", "", "```", c, "```", ""]
    md += ["## คำสั่งแก้ภาพ (ใช้ซ้ำได้)", "", "```", fix, "```"]
    (ROOT / "07_chrome_commands_TH.md").write_text("\n".join(md), encoding="utf-8")
    cards = "".join(f'''<article class="card"><h2>{html.escape(t)}</h2><p class="m">{html.escape(att)} · {len(c):,} ตัวอักษร</p>
<details><summary>ดูคำสั่ง</summary><pre id="c{i}">{html.escape(c)}</pre></details><button onclick="cp('c{i}',this)">Copy คำสั่งทั้งชุด</button></article>'''
                    for i, (t, att, c) in enumerate(cmds))
    cards += f'''<article class="card"><h2>คำสั่งแก้ภาพ (ใช้ซ้ำได้)</h2><pre id="cfix">{html.escape(fix)}</pre><button onclick="cp('cfix',this)">Copy</button></article>'''
    page = f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chrome Image Commands</title><style>
:root{{--bg:#f7f3ec;--fg:#1f1b16;--mut:#6d655a;--card:#fff;--line:#e4dccf;--acc:#c0562b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15120f;--fg:#eee7dd;--mut:#a69c8f;--card:#1f1b17;--line:#363029;--acc:#ef8a5a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Segoe UI","Leelawadee UI",sans-serif}}
header{{padding:20px 16px;border-bottom:1px solid var(--line)}}h1{{margin:0 0 4px;font-size:22px}}header p,header li{{color:var(--mut)}}
main{{max-width:900px;margin:0 auto;padding:16px;display:grid;gap:14px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
h2{{margin:0;font-size:18px}}.m{{margin:2px 0 8px;color:var(--mut);font-size:13px}}summary{{cursor:pointer;color:var(--acc);margin:6px 0}}
pre{{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:10px;font:13px/1.6 "Leelawadee UI",system-ui,sans-serif;max-height:420px;overflow:auto}}
button{{font:inherit;padding:6px 14px;border-radius:6px;border:1px solid var(--acc);background:transparent;color:var(--acc);cursor:pointer;margin-top:6px}}button.ok{{background:var(--acc);color:#fff}}
</style></head><body><header><h1>ข้าวต้มกุ้ง — คำสั่ง Claude in Chrome</h1>
<ol><li>กด Copy คำสั่งชุดที่ต้องการ → วางในแผง Claude ข้าง Gemini → รอ</li>
<li>ตรวจภาพเอง ไม่ถูกใจใช้ "คำสั่งแก้ภาพ" ในแท็บเดิม</li>
<li>ดาวน์โหลดครบแล้วบอก Claude Code ว่า "จัดไฟล์ชุด X" → ผมเปลี่ยนชื่อไฟล์และย้ายเข้าโปรเจกต์ให้</li>
<li>ก่อนชุด 1: อัปโหลด REF-1.png ที่เลือกแล้วเข้า Drive โฟลเดอร์ {REF_FOLDER} · ก่อนชุด 2: อัปโหลด REF-2, REF-3, REF-4</li></ol></header>
<main>{cards}</main>
<script>function cp(id,b){{const t=document.getElementById(id).innerText;const done=()=>{{const o=b.textContent;b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{{b.textContent=o;b.classList.remove('ok')}},1200)}};
if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(t).then(done)}}else{{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();done()}}}}</script>
</body></html>'''
    (OUT / "CHROME_COMMANDS_TH.html").write_text(page, encoding="utf-8")
    for t, _, c in cmds: print(t, "·", len(c), "chars")

if __name__ == "__main__":
    main()
