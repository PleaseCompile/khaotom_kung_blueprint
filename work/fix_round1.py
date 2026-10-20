# -*- coding: utf-8 -*-
# แก้ตามผลตรวจรอบ 1 (review_round1.md)
import json, re
from pathlib import Path
W = Path(__file__).parent
def rw(name, fn):
    p = W / name; d = json.loads(p.read_text(encoding="utf-8")); fn(d)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

# --- structure.py ---
s = (W / "structure.py").read_text(encoding="utf-8")
def sub(a, b):
    global s
    assert a in s, a[:60]; s = s.replace(a, b)
sub(' "PEELING":', ' "WATER":   ("หม้อน้ำเปล่า", "The pot holds only clear water, no prawns or any food in frame."),\n'
    ' "RAW_BOARD": ("กุ้งดิบบนเขียง", "The prawns are whole and raw, translucent grey-blue, nothing cooked."),\n "PEELING":')
sub(' "HEADS":', ' "GARLIC0": ("กระเทียมเพิ่งลงน้ำมัน", "Pale chopped garlic just starting to sizzle in hot oil in the pot, not golden yet, no prawns in the pot."),\n'
    ' "GARLICOIL": ("น้ำมันกระเทียมในหม้อ กระเทียมเจียวตักออกแล้ว", "Golden garlic oil in the pot with only a few fried garlic bits left, the fried garlic set aside in a small bowl, prawn heads and tails still raw in side bowls."),\n "HEADS":')
sub("ginger strips, cilantro, white pepper.", "ginger strips, cilantro, spring onion, white pepper.")
sub('"P02": (["COUNTER", "PRAWN"], "RAW"', '"P02": (["COUNTER", "PRAWN"], "RAW_BOARD"')
sub('"P04": (["STOVE", "COUNTER", "PRAWN"], "GARLIC"', '"P04": (["STOVE", "COUNTER", "PRAWN"], "GARLICOIL"')
sub("ปิดไฟเลย เนื้อจะเด้งค่ะ", "ยกลงจากเตาเลย เนื้อจะเด้งค่ะ")
sub('"ตักใส่ชามตราไก่ โรยกระเทียมเจียว ขิง ผักชี พริกไทยขาว"', '"ตักใส่ชามตราไก่ แล้วโรยกระเทียมเจียว ขิง ผักชี พริกไทยขาวค่ะ"')
sub('"เชฟใช้ช้อนกระเบื้องตักน้ำซุปจากหม้อขึ้นมาชิม พยักหน้าพอใจ"', '"เชฟถือช้อนกระเบื้องตักน้ำซุปไว้ระดับคาง พูดกับกล้อง แล้วพยักหน้าพอใจ"')
sub('"เชฟเป่าข้าวต้มในช้อนกระเบื้อง ชิมแล้วยิ้มกว้างมองกล้อง ชามตราไก่อยู่ด้านหน้า"', '"เชฟถือช้อนข้าวต้มที่มีไอร้อนระดับคาง พูดกับกล้อง แล้วยิ้มกว้าง ชามตราไก่อยู่ด้านหน้า"')
sub('"B02": ("CU", ["COUNTER", "PRAWN"], "RAW"', '"B02": ("CU", ["COUNTER", "PRAWN"], "RAW_BOARD"')
sub('"B03": ("CU", ["STOVE"], "RAW"', '"B03": ("CU", ["STOVE"], "WATER"')
sub('"B07": ("ECU", ["STOVE"], "GARLIC"', '"B07": ("ECU", ["STOVE"], "GARLIC0"')
sub('"B09": ("ECU", ["STOVE", "PRAWN"], "HEADS"', '"B09": ("ECU", ["STOVE", "PRAWN"], "GARLICOIL"')
sub("มือโรยขิงซอย ต้นหอม และขึ้นฉ่ายหั่นลงหม้อข้าวต้ม", "มือโรยขิงซอย ผักชี และต้นหอมหั่นลงหม้อข้าวต้ม")
sub("พริกไทยขาวโปรยบางๆ แล้วช้อนกระเบื้องตักข้าวพร้อมกุ้งหนึ่งตัวยกขึ้น ไอร้อนลอย", "ช้อนกระเบื้องตักข้าวพร้อมกุ้งหนึ่งตัวยกขึ้นจากชามที่โรยพริกไทยขาวแล้ว ไอร้อนลอย")
(W / "structure.py").write_text(s, encoding="utf-8")

# --- img.json ---
def fimg(d):
    i = d["img"]
    i["P08"] = i["P08"].rstrip() + " The bowl is still empty apart from this first pour, no toppings yet."
    i["B18"] = i["B18"].replace("fine ginger strips, sliced scallion and chopped celery leaves", "fine ginger strips, chopped cilantro and sliced spring onion")
    assert "cilantro" in i["B18"]
    d["REF3"] = d["REF3"].replace("cilantro, white pepper specks", "cilantro, sliced spring onion, white pepper specks"); assert "spring onion" in d["REF3"]
rw("img.json", fimg)

# --- vid.json ---
def fvid(v):
    v["P06"] = ('Static camera, medium close-up. She holds the ceramic spoon of steaming broth near her chin and speaks to camera, then gives a small satisfied nod. '
                'Soft simmer, a faint spoon clink, birds outside the window. She says in Thai, warmly: "ปรุงแค่น้ำปลากับซีอิ๊วขาวนิดเดียว ชิมดู ต้องกลมกล่อม" '
                'Speech starts at about 0.5 seconds and finishes by 7.5 seconds, then she holds a gentle smile. No subtitles, no captions, no on-screen text. '
                'camera stable, no morphing, face and food shape unchanged.')
    v["P09"] = ('Slow dolly out, medium close-up. She holds a steaming spoonful of rice soup near her chin and speaks warmly to camera, rooster bowl in front, then breaks into a wide smile. '
                'Soft spoon clink, birds outside the window, quiet morning ambience. She says in Thai, warmly: "หอม ร้อน คล่องคอ ข้าวต้มกุ้งตอนเช้าแบบนี้ อร่อยที่สุดค่ะ" '
                'Speech starts at about 0.5 seconds and finishes by 7.5 seconds, then she holds a gentle smile. No subtitles, no captions, no on-screen text. '
                'camera stable, no morphing, face and food shape unchanged.')
    v["B20"] = ('Slow tilt up following the spoon, extreme close-up. The ceramic spoon lifts rice and one curled orange-striped prawn out of the white-pepper-dusted soup, '
                'broth dripping back into the bowl, steam trailing as the view tilts up with it. Soft spoon clink, gentle steam hush, birds outside the window. '
                'No speech, no faces. camera stable, no morphing, food shape unchanged.')
    v["P07"] = v["P07"].replace("ปิดไฟเลย", "ยกลงจากเตาเลย")
    v["P08"] = v["P08"].replace("She ladles rice soup from the pot into the rooster bowl on the counter, small topping cups lined up beside it.",
                                "She pours the ladle of rice soup into the rooster bowl on the counter, small topping cups lined up beside it.")
    v["P08"] = v["P08"].replace('"ตักใส่ชามตราไก่ โรยกระเทียมเจียว ขิง ผักชี พริกไทยขาว"', '"ตักใส่ชามตราไก่ แล้วโรยกระเทียมเจียว ขิง ผักชี พริกไทยขาวค่ะ"')
    v["B18"] = v["B18"].replace("shredded ginger, sliced spring onion and chopped celery", "shredded ginger, chopped cilantro and sliced spring onion")
    assert "ยกลงจากเตา" in v["P07"] and "pours the ladle" in v["P08"] and "แล้วโรย" in v["P08"] and "cilantro" in v["B18"]
rw("vid.json", fvid)

# --- edit.json ---
def fed(e):
    it = e["items"]
    it["P01"]["trim"] = "ต้นทาง 0.3–8.3 วิ (คำพูด ~0.5–7.5 วิ ครบ)"
    it["P01"]["sound"] = "เก็บเสียงเชฟ+ไอน้ำเดือดเบาๆ+นกเช้า; ห้ามเลื่อนเสียงพูด (ลิปซิงก์ต้องตรง); ภาพเฟดจากดำ 0.5 วิ (00:00–00:00.5) เฉพาะภาพ เสียงพูดไม่เฟด มีแค่ ambience เฟดอิน"
    it["P01"]["cut"] = "[L-cut] ambience/ไอน้ำของ P01 ต่อทับหัว B01 ~0.2 วิ"
    it["B01"]["sound"] = it["B01"]["sound"].replace("เสียงเชฟ P01 ต่อ 0.2 วิแล้วหาย", "ambience P01 ต่อ 0.2 วิแล้วหาย")
    it["P02"]["cut"] = "[J-cut] ambience ของคลิปเชฟนำภาพ ~0.3 วิ; ปลายคัทตรงเข้า B04 ตอนเชฟลดกุ้งลง"
    for k in ("P04", "P06", "P08"): it[k]["cut"] = it[k]["cut"].replace("[J-cut] เสียงเชฟนำภาพ ~0.3 วิ", "[J-cut] ambience ของคลิปเชฟนำภาพ ~0.3 วิ")
    it["P05"]["sound"] = "เสียงเชฟ+น้ำซุปเดือดเบาๆ; ห้ามเลื่อนเสียงพูด; ดนตรี -12 dB"
    it["P05"]["cut"] = "[L-cut] เสียงเดือด/ambience ของ P05 ค้างทับหัว B12 ~0.2 วิ"
    it["P06"]["sound"] = "เสียงเชฟ+ช้อนกระเบื้องแตะหม้อเบาๆ; ดนตรี -12 dB"
    it["P09"]["sound"] = "เสียงเชฟ+ช้อนแตะชามเบาๆ; ห้ามเลื่อนเสียงพูด; ดนตรี -12 dB แล้วดีดกลับขึ้นตอนจบประโยค"
    it["P09"]["cut"] = "[L-cut] ambience ของ P09 ค้างทับหัว B21 ~0.2 วิ"
    it["B20"]["sound"] = it["B20"]["sound"].replace("เสียงพริกไทยโปรย+", "")
    for k in ("P04", "P06", "P08"): assert "ambience ของคลิปเชฟ" in it[k]["cut"], k
    assert "ambience P01" in it["B01"]["sound"] and "พริกไทยโปรย" not in it["B20"]["sound"]
rw("edit.json", fed)
print("fixed")
