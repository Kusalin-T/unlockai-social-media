# Setup — ติดตั้ง Claude CLI

ทำครั้งเดียว ใช้ได้ตลอด ใช้เวลา ~10 นาที

## 1. เปิด Terminal

- **Mac**: กด `⌘ + Space` → พิมพ์ `Terminal` → Enter
- **Windows**: กดปุ่ม Windows → พิมพ์ `PowerShell` → Enter

## 2. ติดตั้ง Claude CLI

คัดลอกบรรทัดนี้ วางใน Terminal แล้วกด Enter:

**Mac:**
```
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**
```
irm https://claude.ai/install.ps1 | iex
```

รอจนขึ้นว่าติดตั้งสำเร็จ แล้ว**ปิด Terminal เปิดใหม่ 1 ครั้ง**

## 3. เปิด Claude แล้วล็อกอิน

พิมพ์:
```
claude
```
- ครั้งแรกจะให้ล็อกอิน → ทำตามหน้าจอ (ใช้บัญชี Claude ของคุณ)
- ถามว่า trust folder นี้ไหม → ตอบ **Yes**
- เห็นหน้าจอ Claude Code = สำเร็จ ✅

## 4. ให้ AI โหลดชุดเครื่องมือให้ (วางคำสั่งเดียว)

วางข้อความนี้ลงใน Claude แล้วกด Enter — ไม่ต้องดาวน์โหลดอะไรเอง:

```
ตั้งค่าเวิร์กช็อป UnlockAI: Social Media ให้หน่อย — อ่านและทำตามขั้นตอนใน https://raw.githubusercontent.com/Kusalin-T/unlockai-social-media/master/BOOTSTRAP.md ให้ครบ ถ้าติดปัญหาให้ดู DEBUG.md ใน repo เดียวกัน
```

- ถ้ามันขออนุญาตรันคำสั่ง / เข้าเน็ต → กด **อนุญาต (Yes)**
- AI จะโหลด repo ลงโฟลเดอร์ `Downloads/unlockai-social-media` แล้วตรวจไฟล์ให้ครบ
- เสร็จแล้วมันจะบอกให้คุณ **เปิด `claude` ใหม่ในโฟลเดอร์นั้น** — ทำตามที่มันบอก แล้วพิมพ์ `/brand`

ถ้า AI ตอบและโหลดครบ = พร้อมเรียน 🎉 กลับไปที่ [README.md](README.md) แล้วเริ่ม `/brand`

---

## (ทางเลือก) โหลดเองแบบ manual — ถ้าไม่อยากผ่าน AI

**มี git อยู่แล้ว:**
```
git clone https://github.com/Kusalin-T/unlockai-social-media.git ~/Downloads/unlockai-social-media
cd ~/Downloads/unlockai-social-media
claude
```
**ไม่มี git (Mac):**
```
curl -fsSL https://codeload.github.com/Kusalin-T/unlockai-social-media/tar.gz/refs/heads/master | tar -xz -C ~/Downloads
mv ~/Downloads/unlockai-social-media-master ~/Downloads/unlockai-social-media
cd ~/Downloads/unlockai-social-media && claude
```
แล้วพิมพ์ `/brand`

---

## ติดปัญหาบ่อย ๆ

| อาการ | ทางแก้ |
|---|---|
| `command not found: claude` | ปิด Terminal เปิดใหม่ แล้วลองอีกครั้ง |
| Windows ฟ้อง execution policy | เปิด PowerShell แบบ "Run as Administrator" แล้วรันคำสั่งติดตั้งใหม่ |
| ล็อกอินไม่ผ่าน | ลองเปิดลิงก์ล็อกอินใน Chrome แทน browser เดิม |
| ช้า/ค้าง | เช็คเน็ต แล้วพิมพ์ `/quit` เปิด `claude` ใหม่ |
