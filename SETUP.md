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

## 3. เข้าโฟลเดอร์นี้ แล้วเริ่ม

```
cd ~/Downloads/unlockai-social-media
claude
```

- ครั้งแรกจะให้ล็อกอิน → ทำตามหน้าจอ (ใช้บัญชี Claude ของคุณ)
- ถามว่า trust folder นี้ไหม → ตอบ **Yes**
- เห็นหน้าจอ Claude Code = สำเร็จ ✅ ("มันมาอยู่ในคอมเราแล้ว")

## 4. ทดสอบ

พิมพ์:
```
สวัสดี แนะนำตัวหน่อย
```
ถ้า AI ตอบ = พร้อมเรียน 🎉 กลับไปที่ [README.md](README.md) แล้วเริ่ม `/brand`

---

## ติดปัญหาบ่อย ๆ

| อาการ | ทางแก้ |
|---|---|
| `command not found: claude` | ปิด Terminal เปิดใหม่ แล้วลองอีกครั้ง |
| Windows ฟ้อง execution policy | เปิด PowerShell แบบ "Run as Administrator" แล้วรันคำสั่งติดตั้งใหม่ |
| ล็อกอินไม่ผ่าน | ลองเปิดลิงก์ล็อกอินใน Chrome แทน browser เดิม |
| ช้า/ค้าง | เช็คเน็ต แล้วพิมพ์ `/quit` เปิด `claude` ใหม่ |
