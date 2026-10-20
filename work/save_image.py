# -*- coding: utf-8 -*-
"""รับภาพที่ผู้ใช้ส่งมา: python save_image.py <รหัส เช่น REF-1 / P01> <ไฟล์ภาพ>
คัดลอกเข้าโฟลเดอร์ที่ถูกต้อง (แปลงเป็น PNG) · บันทึกสถานะ PASS (ผู้ใช้ตรวจเอง) · อัปเดต timeline/progress/หน้า step · บอกภาพถัดไป
"""
import json, sys
from datetime import datetime
from pathlib import Path
from PIL import Image
from structure import ITEMS

W = Path(__file__).parent; OUT = W.parent / "output"
ORDER = [f"REF-{n}" for n in (1, 2, 3, 4)] + [i["id"] for i in ITEMS]

def main():
    rid, src = sys.argv[1].upper(), Path(sys.argv[2])
    assert rid in ORDER, f"ไม่รู้จักรหัส {rid}"
    dest = (OUT / "00_REF" if rid.startswith("REF") else OUT / "01_frames") / f"{rid}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src); im.convert("RGB").save(dest)
    p = W / "shot_status.json"; st = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    s = st.get(rid, {}); s.update(status="PASS", attempts=s.get("attempts", 0) + 1, review="ผู้ใช้ตรวจเอง",
                                  saved=datetime.now().strftime("%Y-%m-%d %H:%M"), size=f"{im.width}x{im.height}")
    st[rid] = s; p.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    import build, build_phases
    build.deliver(); build_phases.main()
    left = [r for r in ORDER if st.get(r, {}).get("status") not in ("PASS", "WARN")]
    print(f"saved {rid} → {dest} ({im.width}x{im.height}, ratio {im.width / im.height:.2f})")
    print("next:", left[0] if left else "ครบแล้ว", "· เหลือ", len(left))

if __name__ == "__main__":
    main()
