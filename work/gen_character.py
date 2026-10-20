# -*- coding: utf-8 -*-
"""ชุดภาพตัวละครแม่ครัว (character sheet) สำหรับเมนู 'ตัวละคร' ใน Google Flow — เจนผ่าน API แบบยิงพร้อมกัน
ผลลัพธ์: output/03_character/C01..png · ใช้ REF-4 + P01 ล็อกใบหน้า · เพดานเงินเดียวกับ gen_api
"""
import base64, io, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image
from structure import CHEF
import gen_api as G

OUT = G.OUT / "03_character"
BASE = ("Character reference photo of the same Thai home cook shown in the attached images: keep her identical face, "
        "age, hairstyle, skin tone, faded indigo cotton shirt and plain cream apron. " + CHEF +
        " Photorealistic, soft even daylight, natural skin texture. No text, no logos, no watermark, one person only.")
SHOTS = {
 "C01_front": "Head-and-shoulders portrait facing straight ahead, neutral friendly expression, mouth closed, plain warm light-grey studio background.",
 "C02_three_quarter_left": "Head-and-shoulders portrait, face turned three-quarter to her right side, gentle smile, plain warm light-grey studio background.",
 "C03_three_quarter_right": "Head-and-shoulders portrait, face turned three-quarter to her left side, gentle smile, plain warm light-grey studio background.",
 "C04_profile": "Head-and-shoulders side profile, looking to the side, calm expression, low bun clearly visible, plain warm light-grey studio background.",
 "C05_full_body": "Full-body standing pose, arms relaxed, showing the full cream apron, simple dark trousers and sandals, plain warm light-grey studio background.",
 "C06_talking": "Medium close-up in the rustic Thai kitchen with blue-green tiles and morning window light, mid-sentence talking warmly, natural open mouth, one hand gesturing.",
 "C07_hands": "Close-up of her clean bare hands with short nails and the rolled indigo sleeves, holding a white ceramic spoon over a teak counter, no face in frame.",
 "C08_closeup_smile": "Tight close-up of her face with a warm wide smile, fine smile lines, soft morning window light from the left, shallow depth of field.",
}

def run(cid, text):
    refs = [G.OUT / "00_REF" / "REF-4.png", G.FR / "P01.png", G.FR / "P02.png"]
    body = {"contents": [{"parts": [{"text": BASE + " " + text}] + [G.img_part(p) for p in refs]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9" if cid in ("C06_talking", "C07_hands") else "3:4", "imageSize": "1K"}}}
    for a in range(5):
        if G.spent() > G.BUDGET_USD: return cid, "BUDGET"
        r = requests.post(G.URL + "generateContent", headers={"x-goog-api-key": G.key()}, json=body, timeout=180)
        if r.status_code in (429, 500, 503): time.sleep(3 * 2 ** a); continue
        d = r.json()
        if r.status_code != 200: return cid, f"ERR {r.status_code}"
        um = d.get("usageMetadata", {}); pin, pout = um.get("promptTokenCount", 0), um.get("candidatesTokenCount", 0)
        usd = pin * G.PRICE_IN + pout * G.PRICE_OUT
        G.log(dict(time=time.strftime("%H:%M:%S"), id=cid, tag="char", in_tok=pin, out_tok=pout, usd=f"{usd:.5f}"))
        parts = [p for c in d.get("candidates", []) for p in c.get("content", {}).get("parts", []) if "inlineData" in p]
        if not parts: return cid, "NOIMG"
        OUT.mkdir(parents=True, exist_ok=True)
        Image.open(io.BytesIO(base64.b64decode(parts[0]["inlineData"]["data"]))).save(OUT / f"{cid}.png")
        return cid, f"OK ${usd:.4f}"
    return cid, "FAIL"

if __name__ == "__main__":
    ids = sys.argv[1].split(",") if len(sys.argv) > 1 else list(SHOTS)
    with ThreadPoolExecutor(len(ids)) as ex:
        for cid, msg in ex.map(lambda k: run(k, SHOTS[k]), ids): print(cid, msg)
    print(f"total spent ${G.spent():.3f} (≈{G.spent() * 35:.1f} บาท)")
