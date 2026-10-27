# Explainer Notebook Kit

ธีมสำหรับสื่ออธิบายและสอนงาน: กระดาษตารางสีครีม ตัวอักษรหมึกน้ำเงิน ไฮไลต์เหลือง sticky notes และการ์ดอธิบายเป็นขั้นตอน **ใช้กับแบรนด์หรือมาสคอตอะไรก็ได้ และไม่ใส่มาสคอตก็ได้**

## ใช้ง่ายที่สุด: ส่งลิงก์นี้ให้ AI

คัดลอกข้อความนี้ เปลี่ยนโจทย์ในวงเล็บ แล้วส่งพร้อมเนื้อหา/ภาพที่ต้องการใช้:

```text
อ่าน README.md และ PROMPT.md ใน https://github.com/mingssii-cpf/ez-training-kit
แล้วใช้ธีม Explainer Notebook สร้าง [ประเภทสื่อ เช่น สไลด์ / ภาพ / HTML / วิดีโอ]
เรื่อง [หัวข้อ] จากเนื้อหาที่ฉันให้ ใช้ภาษาไทย
ใช้โลโก้หรือมาสคอตที่ฉันแนบ ถ้าไม่มีให้ทำโดยไม่ใส่
ดูภาพอ้างอิงใน docs เพื่อรักษาสไตล์ แล้วสร้างผลลัพธ์ตามโจทย์นี้
ถ้าอ่าน repo ไม่ได้ ให้บอกตรง ๆ และขอไฟล์ที่จำเป็นแทน
```

**สำหรับ AI:** อ่าน [PROMPT.md](PROMPT.md) เป็น brief หลัก เปิด [ภาพธีม](docs/preview.png) และ [ภาพใช้ตัวละครอื่น](docs/custom-preview.png) เมื่อเครื่องมือรองรับ แล้วลงมือทำสื่อชนิดที่ผู้ใช้ขอ จำนวนหน้า/ฉากขึ้นกับเนื้อหา ไม่จำกัดตามสามฉากของ starter

การใช้ธีมแบบนี้ไม่ต้องติดตั้ง skill, clone หรือรัน npx; เครื่องมือที่ต้องใช้ผลิตไฟล์ขึ้นกับประเภทสื่อ ส่วนโค้ดด้านล่างเป็นทางเลือกเมื่อต้องการเริ่มจาก template ที่มีอยู่

### ถ้า AI อ่าน GitHub ไม่ได้

Repo นี้ยังเป็น **private** ตามที่เจ้าของกำหนด คนและเครื่องมือ AI ที่อ่านต้องมีสิทธิ์เข้าถึงบัญชีที่เชื่อมต่อ การเปิดลิงก์เองได้ไม่ได้แปลว่า AI ในทุกแอปจะอ่านได้ด้วย

ทางสำรอง: ดาวน์โหลดแล้วแนบ **PROMPT.md + docs/preview.png** ให้ AI ในแชต ถ้าจะใช้ตัวละครให้แนบภาพของตนเองเพิ่ม หากต้องการรายละเอียดโค้ด ให้แนบไฟล์ที่เกี่ยวข้องหรือชุด repo ด้วย วิธีนี้ไม่ต้องเปลี่ยน repo เป็น public

## ใน repo มีอะไรให้เลือกใช้

| ต้องการ | อ่าน/ใช้ |
|---|---|
| ให้ AI ทำสื่อตามธีม | [PROMPT.md](PROMPT.md) พร้อม [ภาพ reference](docs/preview.png) |
| เห็นตัวอย่างเปลี่ยนตัวละคร | [ภาพ custom mascot](docs/custom-preview.png) |
| สร้าง HTML ให้ตรง CSS เดิม | [style.css](skills/explainer-notebook/assets/style.css) |
| ใช้ generator / ทำวิดีโอจาก template | ขั้นตอนด้านล่าง และ [SKILL.md](skills/explainer-notebook/SKILL.md) |

![ตัวอย่างธีมแบบไม่มีมาสคอต](docs/preview.png)

## สร้างไฟล์จาก template (ทางเลือกสำหรับคนใช้โค้ด)

Repo นี้เป็น **private** คนที่จะ clone ต้องได้รับสิทธิ์เข้าถึงจากเจ้าของ `mingssii-cpf` ก่อน เมื่อมีสิทธิ์แล้ว:

```powershell
git clone https://github.com/mingssii-cpf/ez-training-kit.git
cd ez-training-kit
python skills/explainer-notebook/scripts/new_episode.py ./episodes my-lesson --title "ประชุมให้ได้ข้อสรุป" --preview
```

เปิด `episodes/my-lesson/preview.html` ในเบราว์เซอร์ จะเห็นตัวอย่างนิ่ง 3 ฉากทันที **ขั้นนี้ใช้แค่ Python ไม่ต้องมีเสียงหรือ render วิดีโอก่อน** ส่วน `index.html` เป็น composition สำหรับ HyperFrames ไม่ใช่ player

## ใส่แบรนด์และตัวละครของตัวเอง

```powershell
python skills/explainer-notebook/scripts/new_episode.py ./episodes team-lesson --title "สื่อสารงานให้ชัดเจน" --brand "ทีมของเรา" --logo ./my-assets/logo.png --mascot ./my-assets/character.webp --preview
```

- ไม่ส่ง `--mascot`: ใช้การ์ด notebook แทนตัวละคร
- ไม่ส่ง `--logo`: ไม่มีโลโก้
- ส่งเฉพาะ `--logo` หรือเฉพาะ `--mascot` ก็ได้ รองรับ PNG, JPEG, WebP และ SVG
- รูปตัวละครพื้นหลังโปร่งใสจะวางกับกระดาษได้ง่าย ระบบรักษาสัดส่วนภาพ
- หากต้องการ EZ/CPF แบบเดิม เพิ่ม `--preset ez`; ภาพที่ส่งเองจะ override preset นั้น
- คำสั่งไม่เขียนทับตอนที่มีอยู่แล้ว ให้แก้ไฟล์ในตอนเดิมหรือใช้ชื่อโฟลเดอร์ใหม่

ดู [ตัวอย่างเปลี่ยนเป็นตัวละครอื่น](docs/custom-preview.png) — ยังคงธีมเดียวกันโดยไม่ใช้ EZ

| อยากเปลี่ยนอะไร | แก้ที่ไฟล์ในโฟลเดอร์ตอน |
|---|---|
| ชื่อเรื่อง เนื้อหา prompt และ 3 ขั้นตอน | `script.json` |
| ชื่อแบรนด์ โลโก้ มาสคอต | `brand.json` และไฟล์ใน `public/` |
| สี ฟอนต์ และหน้าตาองค์ประกอบ | `tools/style.css` |
| จัดวางภาพและการเคลื่อนไหว | `tools/build.py` |

ใน `brand.json` ตั้ง `logo` หรือ `mascot` เป็น `null` เพื่อนำออก เปลี่ยนแล้วรัน:

```powershell
python episodes/team-lesson/tools/build.py
```

ไฟล์ build และ assets ถูกคัดลอกไปในตอนแล้ว ย้ายโฟลเดอร์ตอนทั้งก้อนไปเครื่องอื่นแล้ว build ต่อได้ ไม่ผูกกับ path เครื่องผู้สร้าง

## ใช้กับ AI เป็น skill

ตัว skill อยู่ที่ [skills/explainer-notebook/SKILL.md](skills/explainer-notebook/SKILL.md) พร้อม supporting files ในโฟลเดอร์เดียวกัน ให้ AI อ่านไฟล์นี้จาก repo ได้เลย ตัวอย่างคำสั่ง:

> อ่าน skills/explainer-notebook/SKILL.md แล้วทำคลิปสอนเรื่องการส่งต่องาน ใช้ธีม notebook นี้ ใช้โลโก้และมาสคอตของฉันจาก my-assets ให้ดู preview ก่อน เลือกเสียงผู้บรรยายให้เข้ากับงานนี้

หากต้องการให้ agent ค้นพบเป็น skill ที่ติดตั้ง ให้ใช้ตัวติดตั้ง skill ของ agent นั้นกับ **ทั้งโฟลเดอร์ explainer-notebook** ไม่ใช่คัดลอกแค่ SKILL.md การอัปเดต repo นี้ไม่ได้ติดตั้ง skill ลงเครื่องให้อัตโนมัติ

## จาก preview เป็นวิดีโอจริง

1. ปรับบทและฉากให้ตรงเรื่อง เลือกเสียงบรรยายและเพลงตามงาน ไม่ได้บังคับ Copilot, HR, EZ หรือผู้ให้บริการเสียง
2. ใส่เสียงจริงเป็น `audio/voice/<scene-id>.wav` ในโฟลเดอร์ตอน
3. จาก root ของ repo รัน:

   ```powershell
   python skills/explainer-notebook/scripts/align.py episodes/my-lesson
   python episodes/my-lesson/tools/build.py
   cd episodes/my-lesson
   npm run check
   npm run render -- --fps 30 --quality standard --workers 2 --output renders/my-lesson.mp4
   ```

4. กลับมาที่ root ของ repo แล้วรัน `python skills/explainer-notebook/scripts/qa.py episodes/my-lesson episodes/my-lesson/renders/my-lesson.mp4` และตรวจภาพ/เสียงของไฟล์จริง

Preview เป็นภาพตัวอย่างพร้อม timing สมมติ ไม่มีเสียงบรรยาย ต้องใช้ `align.py` จับเวลาจากเสียงจริงก่อนผลิตคลิปที่มีเสียง ขั้นผลิตใช้ Node.js/npm และ FFmpeg/ffprobe เพิ่มเติม; Pillow ใช้เฉพาะ redact และ NumPy ใช้เฉพาะ compose_bgm

ดู [ขั้นตอนผลิต](skills/explainer-notebook/references/workflow.md), [สเปกธีม](skills/explainer-notebook/references/frame.md) และ [scene helpers](skills/explainer-notebook/references/eplib.md)

## ขอบเขตและการดูแล

เจ้าของ `mingssii-cpf` · งานล่าสุด `KIT-003` · 2026-10-27 · repo ยังคงเป็น private ชื่อ ez-training-kit; ใช้ README เป็นจุดเริ่มต้นและ PROMPT.md เป็น brief ที่อ่านได้โดยไม่ต้องติดตั้ง

คำสั่งเดิมใน skills/ez-training-clip เปลี่ยนเป็น skills/explainer-notebook; ไฟล์เสียงใช้ audio/voice แทน audio/gemini; ส่วน branding เดิมเลือกด้วย --preset ez ตัว skill ต้นฉบับบนเครื่องผู้ใช้ไม่ได้ถูกแก้

[Source manifest](SOURCE-MANIFEST.json) เป็นประวัติของชุด EZ เริ่มต้นใน commit bc25671 ไม่ใช่ checksum ของรุ่นที่ปรับแล้ว โลโก้ CPF/EZ เป็นทรัพย์สินแบรนด์เดิมและอยู่ใน preset เท่านั้น ไม่มีการให้สิทธิ์นำไปใช้กับแบรนด์อื่น; ไฟล์ SFX/ฟอนต์คงเครดิตเดิม ชุดนี้ไม่ได้ประกาศ open-source license ครอบทุกไฟล์

คำสั่งตรวจ: `python tools/check.py` ครอบคลุม default ไม่มีแบรนด์, โลโก้อย่างเดียว, มาสคอตอย่างเดียว, custom branding, EZ preset, ปฏิเสธข้อมูลไม่ถูกต้อง/การเขียนทับ, HTML build และย้ายโฟลเดอร์ตอน การตรวจนี้ไม่แทนการ render และ QA วิดีโอจริง

สถานะ KIT-002: template และ preview ทั่วไปตรวจผ่านแล้ว รวม skill validator และตรวจภาพใน Chrome ที่ไม่มีแบรนด์, custom character, EZ preset และชื่อเรื่องยาว ไม่พบภาพหายหรือองค์ประกอบล้นกรอบ; ภาพใน docs มาจาก starter รุ่นนี้ ไม่ได้ render/ตรวจวิดีโอจริงในงานนี้

KIT-003 เพิ่มทางใช้งานผ่านลิงก์ GitHub และ brief แบบครบในไฟล์เดียวตามคำขอผู้ใช้ โค้ด generator และภาพอ้างอิงไม่เปลี่ยน การอ่าน repo private จาก AI ภายนอกขึ้นกับสิทธิ์และความสามารถของเครื่องมือนั้น จึงมีทางแนบ PROMPT.md กับภาพแทน ไม่ได้อ้างว่าทดสอบการอ่านผ่าน AI ทุกแอปแล้ว

หลักฐาน KIT-003: ตรวจลิงก์ภายใน README/PROMPT/AGENTS/SKILL ทั้ง 23 จุดและค่าหลักใน brief ผ่าน; skill frontmatter validator ผ่าน การแก้ครั้งนี้เป็นเอกสารและคำแนะนำการใช้งาน ไม่เปลี่ยน generator หรือ templates

README นี้เป็นคู่มือและสถานะหลัก รุ่นที่เผยแพร่คือ branch main บน GitHub; ขั้นถัดไปสำหรับผู้ใช้คือส่งลิงก์พร้อมประเภทสื่อ/หัวข้อ/เนื้อหาให้ AI หรือแนบ brief กับภาพหากไม่มีสิทธิ์อ่านลิงก์
