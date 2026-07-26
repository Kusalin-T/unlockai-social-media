# UnlockAI: Social Media 🔓

Starter kit สำหรับใช้ AI ทำงาน social media จริง — จากเวิร์กช็อป **UnlockAI: Social Media**

## What's inside (ข้างในมีอะไร)

| Skill | พิมพ์ | ทำอะไร |
|---|---|---|
| Brand Setup | `/brand` | AI สัมภาษณ์คุณ แล้วสร้างไฟล์แบรนด์ของคุณ — **ทำอันนี้ก่อน** |
| Caption Writer | `/caption` | เขียนแคปชั่นตามแบรนด์ 3 แบบ + แฮชแท็ก |
| Content Ideas | `/ideas` | ไอเดียคอนเทนต์/hook 10 อัน จากหัวข้อเดียว |
| Content Calendar | `/calendar` | แผนโพสต์ 7 วัน เป็นไฟล์เก็บไว้ใช้ต่อ |
| Comment-to-DM Campaign | `/autoreply` | ออกแบบแคมเปญ "คอมเมนต์คำนี้ รับของทาง DM" — CTA, ข้อความตอบใต้คอมเมนต์, ข้อความ DM พร้อมติดตั้ง |

## Quick start (เริ่มยังไง) — 2 ขั้น

**ขั้น 1 — ติดตั้ง Claude Code ครั้งเดียว** (Mac/Windows) → ทำตาม [SETUP.md](SETUP.md) (~10 นาที)
พอเปิด `claude` ขึ้นมาได้แล้ว ไปขั้น 2 เลย

**ขั้น 2 — วางคำสั่งเดียวนี้** ลงใน Claude แล้วกด Enter — AI จะโหลดชุดเครื่องมือลงเครื่องให้เอง (ไม่ต้องดาวน์โหลดเอง):

```
ตั้งค่าเวิร์กช็อป UnlockAI: Social Media ให้หน่อย — อ่านและทำตามขั้นตอนใน https://raw.githubusercontent.com/Kusalin-T/unlockai-social-media/master/BOOTSTRAP.md ให้ครบ ถ้าติดปัญหาให้ดู DEBUG.md ใน repo เดียวกัน
```

AI จะโหลด repo, ตรวจไฟล์ให้ครบ, แล้วบอกคุณให้เปิด `claude` ใหม่ในโฟลเดอร์นี้ จากนั้นพิมพ์คำสั่งแรก:

```
/brand
```
ตอบคำถาม AI ให้ครบ — มันจะสร้างไฟล์แบรนด์ของคุณ แล้วทุก skill ที่เหลือจะเขียนงานในเสียงแบรนด์คุณอัตโนมัติ

แล้วลองต่อเลย — เป้าหมายวันนี้คือ `/autoreply`:
```
/caption โพสต์เปิดตัวสินค้าใหม่อาทิตย์หน้า
/ideas คอนเทนต์ช่วงสงกรานต์
/calendar
/autoreply
```

> ถ้าอยากโหลดเองแบบไม่ผ่าน AI ก็ได้ — ดูวิธี manual ท้าย [SETUP.md](SETUP.md)

## Folders (โฟลเดอร์)

- `brand/` — ไฟล์แบรนด์ของคุณ (สร้างโดย `/brand`)
- `output/` — งานที่ AI เขียนให้ (แคปชั่น แผนโพสต์ ตาราง auto-reply)
- `workshop/` — แบบฝึกหัดตามคลาส

ติดปัญหา → DM [@butabuilds](https://instagram.com/butabuilds)
