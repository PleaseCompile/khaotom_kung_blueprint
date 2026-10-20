# -*- coding: utf-8 -*-
# A1 ผู้กำกับ — "ข้าวต้มกุ้ง" เชฟเล่าเรื่อง (P01–P09 พูดไทยกับกล้อง) สลับภาพแทรก macro (B01–B21) · 180 วินาที · 16:9
# ฉาก: ครัวไทยบ้านๆ ตอนเช้า เตาถ่าน หม้ออะลูมิเนียม ชามตราไก่ · ภาพแทรกไม่มีใบหน้า (เห็นแค่มือ) · ใบหน้าเดียวที่อนุญาต = เชฟ
CREDITS = {4: 7, 6: 10, 8: 12, 10: 15}   # Flow Omni 1.1 Flash 720p x1

BLOCKS = {
 "LIGHT": ("Warm early-morning sunlight streaming from a window at left, soft golden key light, drifting steam catching "
           "the light, shallow depth of field, gentle film grain, warm amber grade with soft greens, photorealistic "
           "food cinematography, natural textures."),
 "STOVE": ("A black clay Thai charcoal stove with glowing orange embers, holding a dented matte aluminum pot with two "
           "small side handles and a softly worn plain surface, no markings."),
 "COUNTER": ("A weathered teak wood counter with a thick round tamarind-wood chopping board, small white enamel bowls "
             "with blue rims, faded blue-green tiled wall behind, a few banana leaves at the edge."),
 "PRAWN": ("Fresh giant river prawns, large heads with orange tomalley showing through translucent grey-blue shells, "
           "long slender blue claws, glossy and wet."),
 "BOWL": ("A white ceramic rooster bowl hand-painted with a red-and-black rooster and a green banana leaf, with a "
          "matching white ceramic spoon."),
 "HANDS": "Only the cook's clean bare hands and forearms in faded indigo rolled sleeves appear, no face.",
 "NEGATIVE": ("text, letters, numbers, logos, watermarks, labels, brand marks, faces, extra fingers, deformed hands, "
              "plastic look, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, "
              "modern appliances, cluttered background"),
}
CHEF = ("A Thai woman cook in her early fifties, black hair tied in a low bun, warm kind smile, faded indigo cotton "
        "shirt with rolled sleeves, plain cream apron without any marks, clean bare hands, in a rustic Thai "
        "home kitchen.")
NEGATIVE_CHEF = ("text, letters, numbers, logos, watermarks, labels, brand marks, embroidery, extra people, extra "
                 "fingers, deformed hands, distorted face, plastic skin, cartoon style, oversaturated colors, blown "
                 "highlights, gas stove, stainless steel, modern appliances")

# สถานะอาหาร (ไทย, แท็กอังกฤษที่ต่อหลังบล็อก) — กันความต่อเนื่องหลุด
STATES = {
 "NONE":    ("ไม่มีอาหารในภาพ", ""),
 "RAW":     ("กุ้งดิบทั้งตัว", "The prawns are whole and raw, translucent grey-blue, the pot holds only clear water."),
 "WATER":   ("หม้อน้ำเปล่า", "The pot holds only clear water, no prawns or any food in frame."),
 "RAW_BOARD": ("กุ้งดิบบนเขียง", "The prawns are whole and raw, translucent grey-blue, nothing cooked."),
 "PEELING": ("กำลังแกะกุ้งดิบ", "Raw prawns being peeled, translucent grey flesh, heads with orange tomalley set aside, nothing cooked yet."),
 "PEELED":  ("กุ้งแกะแล้ว ยังดิบ", "Peeled raw prawn tails in an enamel bowl, heads in another bowl, nothing cooked yet."),
 "GARLIC":  ("เจียวกระเทียมในหม้อ กุ้งยังดิบ", "Chopped garlic frying golden in oil in the pot, prawn heads and tails still raw in side bowls."),
 "GARLIC0": ("กระเทียมเพิ่งลงน้ำมัน", "Pale chopped garlic just starting to sizzle in hot oil in the pot, not golden yet, no prawns in the pot."),
 "GARLICOIL": ("น้ำมันกระเทียมในหม้อ กระเทียมเจียวตักออกแล้ว", "Golden garlic oil in the pot with only a few fried garlic bits left, the fried garlic set aside in a small bowl, prawn heads and tails still raw in side bowls."),
 "HEADS":   ("ผัดหัวกุ้งในน้ำมันกระเทียม", "Prawn heads frying in garlic oil in the pot, shells turning bright orange, peeled tails still raw in a side bowl."),
 "BROTH0":  ("น้ำซุปหัวกุ้ง ยังไม่ใส่ข้าว", "Pale orange-tinted broth simmering with prawn heads, no rice yet, peeled tails still raw in a side bowl."),
 "BROTH":   ("น้ำซุปใส่ข้าวแล้ว กุ้งยังดิบ", "Golden broth with soft jasmine rice grains simmering, orange prawn oil on the surface, peeled tails still raw in a side bowl."),
 "COOKING": ("กุ้งเพิ่งลงหม้อ ยังใส", "Peeled prawns just dropped into the simmering rice broth, still translucent grey, starting to curl."),
 "COOKED":  ("กุ้งสุกในหม้อ", "The prawns are fully cooked, curled, opaque white flesh with bright orange-red stripes, in the rice broth."),
 "BOWL":    ("ข้าวต้มกุ้งในชามตราไก่", "Finished prawn rice soup in the rooster bowl: rice in golden broth, cooked orange-striped prawns, fried garlic, ginger strips, cilantro, spring onion, white pepper."),
}

ACTS = [("A1", "เปิดเรื่อง · รู้จักกุ้งแม่น้ำ", 0, 30), ("A2", "เตรียมกุ้งและเจียวกระเทียม", 30, 65),
        ("A3", "ทำน้ำซุปหัวกุ้งและใส่ข้าว", 65, 120), ("A4", "ใส่กุ้ง ปรุง ตักใส่ชาม", 120, 160),
        ("A5", "ชิมและปิดเรื่อง", 160, 180)]

# คลิปเชฟ: id -> (props, state, cam_th, cam_en, line_th, gesture_th)  · ทุกคลิป MCU, ไทม์ไลน์ 8 วิ, เจน 10 วิ
P = {
 "P01": (["STOVE", "COUNTER", "PRAWN"], "RAW", "ดันกล้องเข้าช้าๆ", "Slow push in",
         "เช้านี้มาทำข้าวต้มกุ้งกันค่ะ สูตรบ้านๆ แต่หอมไปทั้งซอย",
         "เชฟยืนหลังเคาน์เตอร์ไม้ ยิ้มมองกล้อง มือผายไปที่กุ้งแม่น้ำดิบบนเขียง หม้อน้ำบนเตาถ่านด้านหลังมีไอบางๆ"),
 "P02": (["COUNTER", "PRAWN"], "RAW_BOARD", "กล้องนิ่ง", "Static",
         "กุ้งแม่น้ำหัวมันเยอะ มันสีส้มในหัวนี่แหละ คือหัวใจของน้ำซุปค่ะ",
         "เชฟหยิบกุ้งดิบหนึ่งตัวขึ้นมาระดับอก หันหัวกุ้งเข้ากล้องให้เห็นมันกุ้งสีส้ม"),
 "P03": (["COUNTER", "PRAWN"], "PEELED", "กล้องนิ่ง", "Static",
         "กระเทียมไทยสับหยาบๆ เจียวให้เหลืองหอม เก็บไว้โรยตอนท้าย",
         "เชฟถือมีดอีโต้บนเขียงที่มีกองกระเทียมสับ ชามกุ้งแกะแล้วและชามหัวกุ้งวางข้างๆ พูดกับกล้อง"),
 "P04": (["STOVE", "COUNTER", "PRAWN"], "GARLICOIL", "โค้งกล้องไปขวาช้าๆ", "Slow arc right",
         "น้ำมันกระเทียมอย่าทิ้งนะคะ เอาหัวกุ้งลงไปผัดให้มันกุ้งออกมา",
         "เชฟยืนข้างเตาถ่าน ถือชามหัวกุ้งดิบเหนือหม้อที่น้ำมันกระเทียมกำลังเดือด"),
 "P05": (["STOVE"], "BROTH0", "ดันกล้องเข้าช้าๆ", "Slow push in",
         "เคี่ยวสักสิบห้านาที น้ำซุปจะหวานจากกุ้งล้วนๆ เลยค่ะ",
         "เชฟถือทัพพีไม้ช้อนฟองออกจากหม้อน้ำซุปสีส้มอ่อน ไอน้ำลอยตัดแสงเช้า"),
 "P06": (["STOVE"], "BROTH", "กล้องนิ่ง", "Static",
         "ปรุงแค่น้ำปลากับซีอิ๊วขาวนิดเดียว ชิมดู ต้องกลมกล่อม",
         "เชฟถือช้อนกระเบื้องตักน้ำซุปไว้ระดับคาง พูดกับกล้อง แล้วพยักหน้าพอใจ"),
 "P07": (["STOVE"], "COOKED", "กล้องนิ่ง", "Static",
         "ใส่กุ้งทีหลังสุด พอเป็นสีส้มปุ๊บ ยกลงจากเตาเลย เนื้อจะเด้งค่ะ",
         "เชฟใช้ทัพพีตักกุ้งสุกสีส้มขึ้นมาให้กล้องดู ไอร้อนลอยจากหม้อ"),
 "P08": (["STOVE", "COUNTER", "BOWL"], "COOKED", "ดันกล้องเข้าช้าๆ", "Slow push in",
         "ตักใส่ชามตราไก่ แล้วโรยกระเทียมเจียว ขิง ผักชี พริกไทยขาวค่ะ",
         "เชฟตักข้าวต้มจากหม้อใส่ชามตราไก่บนเคาน์เตอร์ ถ้วยเครื่องโรยวางเรียงข้างชาม"),
 "P09": (["COUNTER", "BOWL"], "BOWL", "ดอลลี่ถอยออกช้าๆ", "Slow dolly out",
         "หอม ร้อน คล่องคอ ข้าวต้มกุ้งตอนเช้าแบบนี้ อร่อยที่สุดค่ะ",
         "เชฟถือช้อนข้าวต้มที่มีไอร้อนระดับคาง พูดกับกล้อง แล้วยิ้มกว้าง ชามตราไก่อยู่ด้านหน้า"),
}

# ภาพแทรก: id -> (size, props, state, cam_th, cam_en, scene_th, highlight)
B = {
 "B01": ("ECU", ["BOWL"], "BOWL", "ดันกล้องเข้าช้ามาก", "Very slow push in",
         "ภาพตัวอย่างตอนจบ (flash-forward): ไอร้อนลอยจากผิวข้าวต้มกุ้งในชามตราไก่ แสงเช้าส่องผ่านไอ", True),
 "B02": ("CU", ["COUNTER", "PRAWN"], "RAW_BOARD", "เลื่อนกล้องไปขวาช้าๆ", "Slow truck right",
         "กุ้งแม่น้ำดิบเรียงบนเขียงไม้มะขาม หยดน้ำเกาะเปลือก ก้ามยาวสีฟ้าทอดยาว", False),
 "B03": ("CU", ["STOVE"], "WATER", "กล้องนิ่ง", "Static",
         "ถ่านในเตาถ่านเรืองแดง ประกายไฟลอยขึ้น หม้อน้ำใสเริ่มมีไอ", False),
 "B04": ("ECU", ["COUNTER", "PRAWN", "HANDS"], "PEELING", "กล้องนิ่ง", "Static",
         "มือบิดหัวกุ้งออกจากตัว มันกุ้งสีส้มเยิ้มเงาที่รอยต่อ", True),
 "B05": ("CU", ["COUNTER", "PRAWN", "HANDS"], "PEELED", "ก้มกล้องลงช้าๆ", "Slow tilt down",
         "มือวางกุ้งแกะเปลือกแล้วลงชามเคลือบ หางกุ้งยังติดครีบหาง เนื้อใสสีเทา", False),
 "B06": ("ECU", ["COUNTER", "HANDS"], "PEELED", "กล้องนิ่ง", "Static",
         "มีดอีโต้สับกระเทียมไทยบนเขียง ชิ้นกระเทียมกระเด็นเล็กน้อย", False),
 "B07": ("ECU", ["STOVE"], "GARLIC0", "ดันกล้องเข้าช้าๆ", "Slow push in",
         "กระเทียมสับเจียวในน้ำมันในหม้อ ฟองน้ำมันเล็กๆ กระเทียมเปลี่ยนเป็นสีเหลืองทอง", True),
 "B08": ("CU", ["STOVE", "HANDS"], "GARLIC", "ยกกล้องขึ้นช้าๆ", "Slow tilt up",
         "กระชอนตักกระเทียมเจียวสีทองขึ้นจากหม้อ น้ำมันหยดกลับลงหม้อ", False),
 "B09": ("ECU", ["STOVE", "PRAWN"], "GARLICOIL", "กล้องนิ่ง", "Static",
         "หัวกุ้งร่วงลงน้ำมันกระเทียมร้อน น้ำมันกระเซ็นเป็นฟอง เปลือกเริ่มเปลี่ยนเป็นสีส้มสด", True),
 "B10": ("CU", ["STOVE", "PRAWN", "HANDS"], "HEADS", "กล้องนิ่ง", "Static",
         "ตะหลิวไม้กดหัวกุ้งในหม้อ มันกุ้งสีส้มแผ่ซึมออกมาในน้ำมัน", False),
 "B11": ("MS", ["STOVE", "HANDS"], "HEADS", "กล้องนิ่ง", "Static",
         "มือเทน้ำจากขันอะลูมิเนียมลงหม้อ ไอน้ำพวยพุ่งขึ้นตัดแสงเช้า", True),
 "B12": ("CU", ["STOVE", "HANDS"], "BROTH0", "ก้มกล้องลงช้าๆ", "Slow tilt down",
         "มือเทข้าวหอมมะลิสุกจากชามลงน้ำซุปสีส้มอ่อนที่เดือดเบาๆ เม็ดข้าวกระจายตัว", False),
 "B13": ("ECU", ["STOVE", "HANDS"], "BROTH", "กล้องนิ่ง", "Static",
         "มือรินน้ำปลาจากถ้วยกระเบื้องเล็กลงหม้อข้าวต้ม เป็นสายเรียวสีอำพัน", False),
 "B14": ("ECU", ["STOVE"], "BROTH", "กล้องนิ่ง", "Static",
         "ผิวข้าวต้มเดือดปุดๆ ฟองแตกช้าๆ คราบน้ำมันกุ้งสีส้มลอยบนผิว", False),
 "B15": ("CU", ["STOVE", "PRAWN", "HANDS"], "BROTH", "กล้องนิ่ง", "Static",
         "มือเทกุ้งแกะแล้วจากชามเคลือบลงหม้อข้าวต้มที่เดือด", False),
 "B16": ("ECU", ["STOVE", "PRAWN"], "COOKING", "ดันกล้องเข้าช้าๆ", "Slow push in",
         "กุ้งในน้ำซุปค่อยๆ เปลี่ยนจากสีเทาใสเป็นขาวขุ่นลายส้มแดง และงอตัวเป็นรูปตัว C", True),
 "B17": ("CU", ["STOVE", "PRAWN", "HANDS"], "COOKED", "ยกกล้องขึ้นช้าๆ", "Slow tilt up",
         "ทัพพีไม้ช้อนกุ้งสุกตัวอวบขึ้นจากหม้อ น้ำซุปไหลออกจากทัพพี ไอร้อนลอย", True),
 "B18": ("CU", ["STOVE", "HANDS"], "COOKED", "กล้องนิ่ง", "Static",
         "มือโรยขิงซอย ผักชี และต้นหอมหั่นลงหม้อข้าวต้ม สีเขียวกระจายบนผิว", False),
 "B19": ("ECU", ["BOWL", "HANDS"], "BOWL", "กล้องนิ่ง", "Static",
         "นิ้วโรยกระเทียมเจียวสีทองลงบนข้าวต้มในชามตราไก่", False),
 "B20": ("ECU", ["BOWL", "HANDS"], "BOWL", "ยกกล้องตามช้อน", "Slow tilt up following the spoon",
         "ช้อนกระเบื้องตักข้าวพร้อมกุ้งหนึ่งตัวยกขึ้นจากชามที่โรยพริกไทยขาวแล้ว ไอร้อนลอย", True),
 "B21": ("WS", ["COUNTER", "BOWL"], "BOWL", "ดอลลี่ถอยออกช้าๆ", "Slow dolly out",
         "ภาพปิด: ชามข้าวต้มกุ้งบนเคาน์เตอร์ไม้ แสงเช้าลอดหน้าต่าง ไอร้อนลอย ใบตองข้างชาม", True),
}

ORDER = [
 ("P01", 8), ("B01", 4), ("B02", 5), ("B03", 5), ("P02", 8),                                   # A1 30
 ("B04", 5), ("B05", 5), ("P03", 8), ("B06", 5), ("B07", 6), ("B08", 6),                      # A2 35
 ("P04", 8), ("B09", 6), ("B10", 5), ("B11", 5), ("P05", 8), ("B12", 6), ("B13", 5), ("P06", 8), ("B14", 4),  # A3 55
 ("B15", 5), ("B16", 6), ("P07", 8), ("B17", 5), ("B18", 5), ("P08", 8), ("B19", 3),          # A4 40
 ("B20", 6), ("P09", 8), ("B21", 6),                                                          # A5 20
]
GEN10 = {"B16", "B20"}   # ภาพแทรกที่ต้องเห็นการเปลี่ยนแปลงยาว (กุ้งเปลี่ยนสี / ช้อนยก) เจน 10 วิ ที่เหลือ 8 วิ

def ts(s):
    return f"{int(s) // 60:02d}:{int(s) % 60:02d}"

def build():
    items, t = [], 0
    act_of = lambda s: next(a for a in ACTS if a[2] <= s < a[3])[0]
    for cid, dur in ORDER:
        if cid.startswith("P"):
            props, state, cam_th, cam_en, line, gest = P[cid]
            it = dict(id=cid, kind="chef", size="MCU", props=props, state=state, cam_th=cam_th, cam_en=cam_en,
                      line_th=line, action_th=gest, highlight=False, gen=10)
        else:
            size, props, state, cam_th, cam_en, scene, hl = B[cid]
            it = dict(id=cid, kind="broll", size=size, props=props, state=state, cam_th=cam_th, cam_en=cam_en,
                      action_th=scene, highlight=hl, gen=10 if cid in GEN10 else 8)
        it.update(start=t, end=t + dur, dur=dur, act=act_of(t))
        items.append(it); t += dur
    return items

ITEMS = build()

if __name__ == "__main__":
    for a in ACTS:
        e = [i for i in ITEMS if i["act"] == a[0]]
        assert e[0]["start"] == a[2] and e[-1]["end"] == a[3], a
    for k, v in list(BLOCKS.items()) + [("CHEF", CHEF), ("NEGATIVE_CHEF", NEGATIVE_CHEF)]:
        n = len(v.replace(",", " ").split()); print(f"{k}: {n} words"); assert n <= 40, k
    for i in ITEMS:
        print(i["id"], ts(i["start"]), ts(i["end"]), i["dur"], i["act"], i["kind"], i["state"], "gen", i["gen"])
    print(len(ITEMS), "items ·", ITEMS[-1]["end"], "s · chef", sum(i["dur"] for i in ITEMS if i["kind"] == "chef"),
          "s · credits", sum(CREDITS[i["gen"]] for i in ITEMS), "· highlights", sum(i["highlight"] for i in ITEMS))
