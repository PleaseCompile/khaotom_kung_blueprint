# -*- coding: utf-8 -*-
"""เจนภาพเริ่มต้นผ่าน Gemini API (Nano Banana 2.1) แบบยิงพร้อมกัน
python gen_api.py [--ids P03,B01,...] [--tag a1] [--count] [--workers 30]
- Prompt = Prompt อังกฤษที่ผ่านผู้ตรวจ (jobs/prompts/<id>.txt) + ประโยคนำกันคัดลอก REF (บันทึกไว้ใน shot_status note)
- REF ย่อเหลือ 1024px ก่อนแนบ · ขนาดผลลัพธ์ 1K · 16:9
- เพดานเงิน BUDGET_USD · บันทึกโทเคน/ค่าใช้จ่ายทุกครั้งลง api_usage.csv
- key อ่านจากไฟล์นอกโปรเจกต์ (env GEMINI_KEY_FILE) ไม่เขียนลง log
"""
import base64, csv, io, json, os, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
import requests
from PIL import Image
from structure import ITEMS
from build import refs_for

W = Path(__file__).parent; OUT = W.parent / "output"; FR = OUT / "01_frames"; CAND = FR / "_candidates"
MODEL = "gemini-nano-banana-2.1"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:"
PRICE_IN, PRICE_OUT = 1.50 / 1e6, 30.0 / 1e6
BUDGET_USD = 150 / 35          # 150 บาท
USAGE = W / "api_usage.csv"
LEAD = ("Create a NEW photograph exactly as described below. The attached images are references only for materials, "
        "colors, lighting and the cook's face; do not copy their framing, composition or camera angle.")
LOCK = threading.Lock()

def key():
    return Path(os.environ["GEMINI_KEY_FILE"]).read_text().strip()

def spent():
    if not USAGE.exists(): return 0.0
    with USAGE.open(encoding="utf-8") as f: return sum(float(r["usd"]) for r in csv.DictReader(f))

_cache = {}
def img_part(p):
    if p not in _cache:
        im = Image.open(p).convert("RGB"); im.thumbnail((1024, 1024)); b = io.BytesIO(); im.save(b, "JPEG", quality=88)
        _cache[p] = {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}
    return _cache[p]

DROP = set()   # รหัสที่เจนแล้วได้ภาพซ้ำกับ REF → รอบใหม่ไม่แนบ REF-2/REF-3 (คุมหน้าตาด้วย REF-1 + ข้อความ)

def attachments(it):
    r = [Path(x) for x in refs_for(it)]
    if it["id"] in DROP: r = [x for x in r if x.name not in ("REF-2.png", "REF-3.png")]
    if it["kind"] == "chef" and it["id"] != "P01" and (FR / "P01.png").exists(): r.append(FR / "P01.png")   # ล็อกใบหน้าแม่ครัว
    return r

def body(it, extra=""):
    pr = (OUT / "jobs" / "prompts" / f"{it['id']}.txt").read_text(encoding="utf-8")
    return {"contents": [{"parts": [{"text": " ".join(x for x in (LEAD, extra, pr) if x)}] + [img_part(p) for p in attachments(it)]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9", "imageSize": "1K"}}}

def log(row):
    with LOCK:
        new = not USAGE.exists()
        with USAGE.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(row)); new and w.writeheader(); w.writerow(row)

def gen(it, tag, extra=""):
    t0 = time.time(); last = ""
    for attempt in range(6):
        if spent() > BUDGET_USD: return it["id"], "BUDGET", 0
        try:
            r = requests.post(URL + "generateContent", headers={"x-goog-api-key": key()}, json=body(it, extra), timeout=180)
        except requests.RequestException as e:
            last = type(e).__name__; time.sleep(2 ** attempt); continue
        if r.status_code in (429, 500, 503):
            last = str(r.status_code); time.sleep(min(60, 3 * 2 ** attempt)); continue
        d = r.json()
        if r.status_code != 200: return it["id"], f"ERR {r.status_code} {d.get('error', {}).get('message', '')[:120]}", time.time() - t0
        um = d.get("usageMetadata", {}); pin, pout = um.get("promptTokenCount", 0), um.get("candidatesTokenCount", 0)
        usd = pin * PRICE_IN + pout * PRICE_OUT
        log(dict(time=datetime.now().strftime("%H:%M:%S"), id=it["id"], tag=tag, in_tok=pin, out_tok=pout, usd=f"{usd:.5f}"))
        parts = [p for c in d.get("candidates", []) for p in c.get("content", {}).get("parts", []) if "inlineData" in p or "inline_data" in p]
        if not parts: return it["id"], "NOIMG " + str(d.get("candidates", [{}])[0].get("finishReason")), time.time() - t0
        data = (parts[0].get("inlineData") or parts[0].get("inline_data"))["data"]
        CAND.mkdir(parents=True, exist_ok=True); dst = CAND / f"{it['id']}_{tag}.png"
        Image.open(io.BytesIO(base64.b64decode(data))).save(dst)
        return it["id"], f"OK {dst.name} in={pin} out={pout} ${usd:.4f}", time.time() - t0
    return it["id"], f"FAIL after retries ({last})", time.time() - t0

def main():
    a = sys.argv[1:]; get = lambda k, d: a[a.index(k) + 1] if k in a else d
    st = json.loads((W / "shot_status.json").read_text(encoding="utf-8"))
    ids = get("--ids", "").split(",") if "--ids" in a else [i["id"] for i in ITEMS if st.get(i["id"], {}).get("status") not in ("PASS", "WARN")]
    its = [i for i in ITEMS if i["id"] in ids]; tag = get("--tag", "a1")
    DROP.update(x for x in get("--drop", "").split(",") if x)
    extra = json.loads((W / "api_extra.json").read_text(encoding="utf-8")) if (W / "api_extra.json").exists() else {}
    if "--count" in a:
        it = its[0]; r = requests.post(URL + "countTokens", headers={"x-goog-api-key": key()}, json={"contents": body(it)["contents"]}).json()
        print(it["id"], "input tokens:", r.get("totalTokens"), r.get("error", "")); return
    print(f"{len(its)} images · spent so far ${spent():.3f} · budget ${BUDGET_USD:.2f}")
    t0 = time.time()
    with ThreadPoolExecutor(int(get("--workers", "30"))) as ex:
        futs = [ex.submit(gen, it, tag, extra.get(it["id"], "")) for it in its]
        for f in as_completed(futs):
            i, msg, dt = f.result(); print(f"{i:4s} {dt:5.1f}s {msg}", flush=True)
    print(f"done in {time.time() - t0:.0f}s · total spent ${spent():.3f} (≈{spent() * 35:.1f} บาท)")

if __name__ == "__main__":
    main()
