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

## Quick start (เริ่มยังไง)

1. ติดตั้ง Claude CLI ให้เสร็จก่อน → ดู [SETUP.md](SETUP.md)
2. เปิด Terminal แล้วเข้าโฟลเดอร์นี้:
   ```
   cd ~/Downloads/unlockai-social-media
   ```
3. เริ่ม AI:
   ```
   claude
   ```
4. พิมพ์คำสั่งแรก:
   ```
   /brand
   ```
   ตอบคำถาม AI ให้ครบ — มันจะสร้างไฟล์แบรนด์ของคุณ แล้วทุก skill ที่เหลือจะเขียนงานในเสียงแบรนด์คุณอัตโนมัติ

5. ลองต่อเลย:
   ```
   /caption โพสต์เปิดตัวสินค้าใหม่อาทิตย์หน้า
   /ideas คอนเทนต์ช่วงสงกรานต์
   /calendar
   /autoreply
   ```

## Folders (โฟลเดอร์)

- `brand/` — ไฟล์แบรนด์ของคุณ (สร้างโดย `/brand`)
- `output/` — งานที่ AI เขียนให้ (แคปชั่น แผนโพสต์ ตาราง auto-reply)
- `workshop/` — แบบฝึกหัดตามคลาส

ติดปัญหา → DM [@butabuilds](https://instagram.com/butabuilds)
