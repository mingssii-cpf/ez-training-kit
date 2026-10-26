# EZ Training Kit

ชุดธีมและ skill สำหรับผลิตคลิปสอนงานภาษาไทย **“หนึ่งวันกับ EZ”** ในสไตล์ **Explainer Notebook — Style C** ด้วย HyperFrames

กระดาษตารางสีครีม ตัวอักษรหมึกน้ำเงิน สีเขียวอมฟ้าจาก EZ ไฮไลต์เหลือง ภาพหน้าจอแปะเทป และการ์ด prompt แบบ sticky note ขนาดงาน 1920×1080 / 30 fps

## สิ่งที่อยู่ใน repo

- [Skill และขั้นตอนผลิต](skills/ez-training-clip/SKILL.md)
- [สเปกธีม สี ฟอนต์ องค์ประกอบ และ motion](skills/ez-training-clip/references/frame.md)
- [CSS ที่ใช้จริง](skills/ez-training-clip/assets/style.css)
- [สคริปต์สร้างตอนใหม่](skills/ez-training-clip/scripts/new_episode.py) และ [ตัวช่วยประกอบฉาก](skills/ez-training-clip/scripts/eplib.py)
- Templates บทและฉาก ฟอนต์ มาสคอต EZ โลโก้ CPF และ SFX จากชุดต้นฉบับ

เก็บธีมและเครื่องมือไว้ที่เดียวใน `skills/ez-training-clip/` เพื่อไม่ให้ CSS หรือสเปกหลายชุดคลาดกัน การใช้งาน skill ในโปรเจกต์อื่นให้อ้างอิงไฟล์ SKILL.md พร้อม supporting files ทั้งโฟลเดอร์

## เริ่มใช้

ต้องมี Python 3, Node.js/npm และ FFmpeg/ffprobe ใน PATH ส่วน `redact.py` ใช้ Pillow และ `compose_bgm.py` ใช้ NumPy เพิ่มเติม เครื่องมือที่ไม่เรียกสองสคริปต์นี้ไม่ต้องติดตั้งสองแพ็กเกจดังกล่าว

รันจาก root ของ repo:

```powershell
python tools/check.py
python skills/ez-training-clip/scripts/new_episode.py ./episodes s1e3-email
```

คำสั่งสร้างตอนใหม่จะไม่เขียนทับโฟลเดอร์ที่มีอยู่แล้ว จากนั้น:

1. เขียน `episodes/s1e3-email/script.json` และให้เจ้าของงานตรวจบทก่อนทำเสียง
2. ทดสอบความสามารถ Copilot ที่จะสอนและบันทึกหลักฐานของตอนนั้นเอง
3. สร้างเสียงจริงเป็น `audio/gemini/<scene-id>.wav` แล้วจับเวลา:

   ```powershell
   python skills/ez-training-clip/scripts/align.py episodes/s1e3-email
   ```

4. จับภาพหน้าจอจริงและแก้ `redact.json` ให้ตรงกับตำแหน่งไฟล์และข้อมูลที่ต้องปิดบัง ตรวจภาพหลัง redact ด้วยตา
5. เขียนฉากใน `tools/build.py` ให้ครบทุก scene และรัน:

   ```powershell
   python episodes/s1e3-email/tools/build.py
   cd episodes/s1e3-email
   npm run check
   npm run render -- --fps 30 --quality standard --workers 2 --output renders/s1e3-email.mp4
   ```

6. จาก root ของ repo ตรวจไฟล์ที่ render แล้ว:

   ```powershell
   python skills/ez-training-clip/scripts/qa.py episodes/s1e3-email episodes/s1e3-email/renders/s1e3-email.mp4
   ```

Template มีเพียงสองฉากเริ่มต้น ต้องเติมเนื้อหาและเสียงก่อนผลิตจริง `tools/check.py` ใช้ timing/เสียงเงียบสมมติในโฟลเดอร์ชั่วคราวเพื่อตรวจ scaffold → HTML เท่านั้น ไม่ใช่หลักฐานว่าเสียง ภาพ หรือวิดีโอผ่าน QA

## ขอบเขตและข้ออ้างอิงเดิม

- Repo นี้แพ็ก skill เดิมจาก `D:/ai_clip/.claude/skills/ez-training-clip` โดยคงไฟล์ต้นฉบับไว้ครบและไม่แก้ installed copies
- ไม่รวมภาพอีเมล ไฟล์ capture บทของตอนจริง เสียงบรรยาย เพลง Corporate Calm หรือวิดีโอสำเร็จของซีรีส์
- Reference episode, capability matrix และโฟลเดอร์ style-gate ที่เอกสารเดิมอ้างถึงอยู่ในโปรเจกต์ต้นทาง ไม่ได้รวมใน kit นี้ แต่สร้างสองฉากเริ่มต้นได้ด้วยไฟล์ใน repo
- รายละเอียดบัญชีที่ sign in แล้ว ตำแหน่ง download/browser tools และชื่อโมเดลเสียงในเอกสารเดิมเป็นบริบทของเครื่องต้นทาง ต้องตรวจใหม่บนเครื่องที่ใช้งาน
- HyperFrames ปักไว้ที่ `0.8.143` ตามชุดเดิม ไม่มีการอัปเกรดหรือยืนยันบริการภายนอกใหม่ในการแพ็กครั้งนี้
- กรณี `frame.md` ยังกล่าวถึง DRAFT ให้ยึดการตัดสินใจล่าสุดใน SKILL.md ว่าไม่มี DRAFT tag
- โลโก้ CPF และมาสคอตเป็นทรัพย์สินแบรนด์เดิม ไม่ได้ให้สิทธิ์ใช้กับแบรนด์อื่น; SFX ใช้เครดิตที่มากับต้นฉบับ ไม่ได้ประกาศ open-source license ครอบไฟล์ทั้งหมด

## สถานะและการดูแล

เจ้าของ: `mingssii-cpf` · งาน `KIT-001` · แพ็กเมื่อ 2026-10-26 · เป้าหมาย: private GitHub repo `mingssii-cpf/ez-training-kit`

การอนุญาต: ผู้ใช้ขอขึ้น GitHub หลังเลือกแนวทาง repo รวมธีมและ skill เดิม และยืนยันล่าสุดให้ใช้บัญชี `mingssii-cpf` เป็น private repo

แหล่งต้นฉบับและ SHA-256 รายไฟล์อยู่ใน [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) คู่มือเริ่มใช้/สถานะอยู่ใน README นี้ ขั้นตอนผลิตอยู่ใน SKILL.md ส่วน theme tokens อยู่ใน frame.md และ CSS ให้แก้เมื่อเปลี่ยนพฤติกรรมหรือรูปลักษณ์ที่เกี่ยวข้อง

เกณฑ์ส่งมอบ: ไฟล์ skill ตรงกับต้นฉบับ, scaffold และ HTML build ผ่าน `python tools/check.py`, ตรวจรายการไฟล์ก่อน commit และตรวจ SHA ของ branch main บน GitHub หลัง push การแพ็กนี้ไม่เปลี่ยนสถานะอนุมัติตอน S1E2 หรืออ้างว่าผลิตวิดีโอตอนใหม่แล้ว

หลักฐาน local วันที่ 2026-10-26: `python tools/check.py` ผ่าน — SHA-256 ครบ 39 ไฟล์, Python/JSON parse, scaffold, ปฏิเสธการเขียนทับ, HTML build และไฟล์ assets ที่อ้างถึง; ตรวจรายการไฟล์และรูปแบบ token/private key ก่อน commit แล้ว ไม่ได้รัน TTS, capture, render หรือ visual QA

ขั้นถัดไป: ใช้ kit สร้างตอนใหม่และตรวจเสียง/ภาพ/render ตาม workflow ก่อนส่งคลิปจริง
