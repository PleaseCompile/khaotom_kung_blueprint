# -*- coding: utf-8 -*-
"""จัดไฟล์ที่ Claude in Chrome ดาวน์โหลดจาก Gemini: เอาภาพใหม่สุด N ไฟล์ใน Downloads เรียงตามเวลาดาวน์โหลด แล้วตั้งชื่อตามรหัสในชุด
คัดลอกเท่านั้น (ไม่ลบไฟล์ใน Downloads) · ใช้: python organize_downloads.py <ชุด 0-4> [--dry]
"""
import shutil, sys
from pathlib import Path
from structure import ITEMS

OUT = Path(__file__).parent.parent / "output"
DL = Path.home() / "Downloads"
BATCH = {0: [f"REF-1_v{i}" for i in (1, 2, 3)],
         1: [f"REF-{n}_v{i}" for n in (2, 3, 4) for i in (1, 2, 3)],
         **{b + 2: [it["id"] for it in ITEMS[b * 10:(b + 1) * 10]] for b in range(3)}}

def main():
    b = int(sys.argv[1]); ids = BATCH[b]
    files = sorted([p for p in DL.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")], key=lambda p: p.stat().st_mtime)[-len(ids):]
    if len(files) < len(ids): sys.exit(f"พบภาพแค่ {len(files)} ไฟล์ ต้องการ {len(ids)}")
    dest = OUT / "00_REF" / "candidates" if b < 2 else OUT / "01_frames"
    up = OUT / "drive_upload" / f"batch{b}"; dest.mkdir(parents=True, exist_ok=True); up.mkdir(parents=True, exist_ok=True)
    for rid, src in zip(ids, files):
        name = rid + ".png"
        print(f"{src.name} → {name}")
        if "--dry" in sys.argv: continue
        if src.suffix.lower() == ".png": shutil.copy2(src, dest / name)
        else:
            from PIL import Image; Image.open(src).convert("RGB").save(dest / name)
        shutil.copy2(dest / name, up / name)
    print("ok →", dest, "· สำเนาสำหรับอัปโหลด Drive:", up)

if __name__ == "__main__":
    main()
