# 01 — Style Guide & บล็อกคำล็อค

ทุก Prompt ภาพประกอบอัตโนมัติ: LIGHT + บล็อกพร็อพ + (CHEF หรือ HANDS) + แท็กสถานะอาหาร + `16:9 widescreen frame.` + ข้อความเฉพาะภาพ + ประโยคอ้างอิง REF + `Avoid:` NEGATIVE

### [LIGHT] (36 คำ)
```
Warm early-morning sunlight streaming from a window at left, soft golden key light, drifting steam catching the light, shallow depth of field, gentle film grain, warm amber grade with soft greens, photorealistic food cinematography, natural textures.
```

### [STOVE] (29 คำ)
```
A black clay Thai charcoal stove with glowing orange embers, holding a dented matte aluminum pot with two small side handles and a softly worn plain surface, no markings.
```

### [COUNTER] (31 คำ)
```
A weathered teak wood counter with a thick round tamarind-wood chopping board, small white enamel bowls with blue rims, faded blue-green tiled wall behind, a few banana leaves at the edge.
```

### [PRAWN] (21 คำ)
```
Fresh giant river prawns, large heads with orange tomalley showing through translucent grey-blue shells, long slender blue claws, glossy and wet.
```

### [BOWL] (21 คำ)
```
A white ceramic rooster bowl hand-painted with a red-and-black rooster and a green banana leaf, with a matching white ceramic spoon.
```

### [HANDS] (16 คำ)
```
Only the cook's clean bare hands and forearms in faded indigo rolled sleeves appear, no face.
```

### [NEGATIVE] (29 คำ)
```
text, letters, numbers, logos, watermarks, labels, brand marks, faces, extra fingers, deformed hands, plastic look, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, modern appliances, cluttered background
```

### [CHEF] (40 คำ)
```
A Thai woman cook in her early fifties, black hair tied in a low bun, warm kind smile, faded indigo cotton shirt with rolled sleeves, plain cream apron without any marks, clean bare hands, in a rustic Thai home kitchen.
```

### [NEGATIVE_CHEF] (31 คำ)
```
text, letters, numbers, logos, watermarks, labels, brand marks, embroidery, extra people, extra fingers, deformed hands, distorted face, plastic skin, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, modern appliances
```

## แท็กสถานะอาหาร

| แท็ก | ไทย | อังกฤษ |
|---|---|---|
| NONE | ไม่มีอาหารในภาพ |  |
| RAW | กุ้งดิบทั้งตัว | The prawns are whole and raw, translucent grey-blue, the pot holds only clear water. |
| WATER | หม้อน้ำเปล่า | The pot holds only clear water, no prawns or any food in frame. |
| RAW_BOARD | กุ้งดิบบนเขียง | The prawns are whole and raw, translucent grey-blue, nothing cooked. |
| PEELING | กำลังแกะกุ้งดิบ | Raw prawns being peeled, translucent grey flesh, heads with orange tomalley set aside, nothing cooked yet. |
| PEELED | กุ้งแกะแล้ว ยังดิบ | Peeled raw prawn tails in an enamel bowl, heads in another bowl, nothing cooked yet. |
| GARLIC | เจียวกระเทียมในหม้อ กุ้งยังดิบ | Chopped garlic frying golden in oil in the pot, prawn heads and tails still raw in side bowls. |
| GARLIC0 | กระเทียมเพิ่งลงน้ำมัน | Pale chopped garlic just starting to sizzle in hot oil in the pot, not golden yet, no prawns in the pot. |
| GARLICOIL | น้ำมันกระเทียมในหม้อ กระเทียมเจียวตักออกแล้ว | Golden garlic oil in the pot with only a few fried garlic bits left, the fried garlic set aside in a small bowl, prawn heads and tails still raw in side bowls. |
| HEADS | ผัดหัวกุ้งในน้ำมันกระเทียม | Prawn heads frying in garlic oil in the pot, shells turning bright orange, peeled tails still raw in a side bowl. |
| BROTH0 | น้ำซุปหัวกุ้ง ยังไม่ใส่ข้าว | Pale orange-tinted broth simmering with prawn heads, no rice yet, peeled tails still raw in a side bowl. |
| BROTH | น้ำซุปใส่ข้าวแล้ว กุ้งยังดิบ | Golden broth with soft jasmine rice grains simmering, orange prawn oil on the surface, peeled tails still raw in a side bowl. |
| COOKING | กุ้งเพิ่งลงหม้อ ยังใส | Peeled prawns just dropped into the simmering rice broth, still translucent grey, starting to curl. |
| COOKED | กุ้งสุกในหม้อ | The prawns are fully cooked, curled, opaque white flesh with bright orange-red stripes, in the rice broth. |
| BOWL | ข้าวต้มกุ้งในชามตราไก่ | Finished prawn rice soup in the rooster bowl: rice in golden broth, cooked orange-striped prawns, fried garlic, ginger strips, cilantro, spring onion, white pepper. |

## Prompt ภาพ REF

### REF-1
```
Warm early-morning sunlight streaming from a window at left, soft golden key light, drifting steam catching the light, shallow depth of field, gentle film grain, warm amber grade with soft greens, photorealistic food cinematography, natural textures. A black clay Thai charcoal stove with glowing orange embers, holding a dented matte aluminum pot with two small side handles and a softly worn plain surface, no markings. A weathered teak wood counter with a thick round tamarind-wood chopping board, small white enamel bowls with blue rims, faded blue-green tiled wall behind, a few banana leaves at the edge. 16:9 widescreen frame. Wide shot, eye-level, establishing view of the empty kitchen set. Charcoal stove with the aluminum pot at centre-left, teak counter with round board and white enamel bowls at right, tiled wall behind, a window at far left pouring golden morning light across the room. No people, no food, a thin wisp of steam rising from the pot. Avoid: text, letters, numbers, logos, watermarks, labels, brand marks, faces, extra fingers, deformed hands, plastic look, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, modern appliances, cluttered background
```

### REF-2
```
Warm early-morning sunlight streaming from a window at left, soft golden key light, drifting steam catching the light, shallow depth of field, gentle film grain, warm amber grade with soft greens, photorealistic food cinematography, natural textures. A weathered teak wood counter with a thick round tamarind-wood chopping board, small white enamel bowls with blue rims, faded blue-green tiled wall behind, a few banana leaves at the edge. Fresh giant river prawns, large heads with orange tomalley showing through translucent grey-blue shells, long slender blue claws, glossy and wet. The prawns are whole and raw, translucent grey-blue, nothing cooked. 16:9 widescreen frame. Close-up, slightly high angle, hero shot of five raw giant river prawns lying side by side on the round tamarind-wood chopping board, wet and glossy with water droplets, orange tomalley glowing through the translucent grey-blue head shells, long blue claws stretched forward. Soft window light from the left, blurred kitchen behind. No people, nothing cooked. Avoid: text, letters, numbers, logos, watermarks, labels, brand marks, faces, extra fingers, deformed hands, plastic look, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, modern appliances, cluttered background
```

### REF-3
```
Warm early-morning sunlight streaming from a window at left, soft golden key light, drifting steam catching the light, shallow depth of field, gentle film grain, warm amber grade with soft greens, photorealistic food cinematography, natural textures. A weathered teak wood counter with a thick round tamarind-wood chopping board, small white enamel bowls with blue rims, faded blue-green tiled wall behind, a few banana leaves at the edge. A white ceramic rooster bowl hand-painted with a red-and-black rooster and a green banana leaf, with a matching white ceramic spoon. Finished prawn rice soup in the rooster bowl: rice in golden broth, cooked orange-striped prawns, fried garlic, ginger strips, cilantro, spring onion, white pepper. 16:9 widescreen frame. Close-up, slightly high three-quarter angle, hero shot of the finished prawn rice soup in the rooster bowl on the teak counter: golden broth, soft rice, three curled orange-striped prawns, fried garlic, thin ginger strips, cilantro, sliced spring onion, white pepper specks. Gentle steam drifts upward through morning window light, ceramic spoon resting beside. No people. Avoid: text, letters, numbers, logos, watermarks, labels, brand marks, faces, extra fingers, deformed hands, plastic look, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, modern appliances, cluttered background
```

### REF-4
```
Warm early-morning sunlight streaming from a window at left, soft golden key light, drifting steam catching the light, shallow depth of field, gentle film grain, warm amber grade with soft greens, photorealistic food cinematography, natural textures. A weathered teak wood counter with a thick round tamarind-wood chopping board, small white enamel bowls with blue rims, faded blue-green tiled wall behind, a few banana leaves at the edge. A Thai woman cook in her early fifties, black hair tied in a low bun, warm kind smile, faded indigo cotton shirt with rolled sleeves, plain cream apron without any marks, clean bare hands, in a rustic Thai home kitchen. 16:9 widescreen frame. Medium close-up, eye-level, frontal portrait of the Thai woman cook standing behind the teak counter, shoulders and head framed centrally, relaxed upright posture, hands out of frame. Neutral friendly expression, mouth relaxed and slightly open, eyes looking straight ahead. Soft window light on her face, tiled wall and blurred charcoal stove behind her. Avoid: text, letters, numbers, logos, watermarks, labels, brand marks, embroidery, extra people, extra fingers, deformed hands, distorted face, plastic skin, cartoon style, oversaturated colors, blown highlights, gas stove, stainless steel, modern appliances
```
