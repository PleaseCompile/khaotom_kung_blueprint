# -*- coding: utf-8 -*-
"""นำผลตรวจ review_api_*.json มาใช้: python apply_review.py <tag เช่น a1>
PASS → คัดลอก _candidates/<id>_<tag>.png เป็น 01_frames/<id>.png · FAIL → ใส่ประโยคแก้ใน api_extra.json สำหรับรอบถัดไป
ไม่แก้ไฟล์แผน — การปรับ Prompt บันทึกไว้ใน shot_status (โชว์ใน info.txt)
"""
import json, shutil, sys
from pathlib import Path

W = Path(__file__).parent; FR = W.parent / "output" / "01_frames"
LEAD_NOTE = "เจนผ่าน API (Nano Banana 2.1) · เติมประโยคนำกันคัดลอกภาพอ้างอิงไว้หน้า Prompt"

def main():
    tag = sys.argv[1]; maxtry = 3
    st = json.loads((W / "shot_status.json").read_text(encoding="utf-8"))
    ex_p = W / "api_extra.json"; extra = json.loads(ex_p.read_text(encoding="utf-8")) if ex_p.exists() else {}
    fails, passes = [], []
    for f in sorted(W.glob(sys.argv[2] if len(sys.argv) > 2 else "review_api_A*.json")):
        for rid, r in json.loads(f.read_text(encoding="utf-8")).items():
            cand = FR / "_candidates" / f"{rid}_{tag}.png"
            if not cand.exists() or st.get(rid, {}).get("status") == "PASS" and st[rid].get("tag") == tag: continue
            s = st.get(rid, {}); s["attempts"] = s.get("attempts", 0) + 1
            if r["verdict"] == "PASS" or s["attempts"] >= maxtry:
                shutil.copy2(cand, FR / f"{rid}.png")
                s.update(status="PASS" if r["verdict"] == "PASS" else "WARN", tag=tag, review=r.get("notes_th", ""),
                         note=LEAD_NOTE + (f" · ประโยคแก้: {extra[rid]}" if rid in extra else ""))
                passes.append(rid)
            elif cand.exists():
                s.update(status="REDO", tag=tag, review=r.get("notes_th", "")); extra[rid] = r.get("fix_en", "").strip(); fails.append(rid)
            st[rid] = s
    (W / "shot_status.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    ex_p.write_text(json.dumps(extra, ensure_ascii=False, indent=1), encoding="utf-8")
    print("pass/warn:", ",".join(passes) or "-"); print("redo:", ",".join(fails) or "-")

if __name__ == "__main__":
    main()
