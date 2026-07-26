---
name: brand
description: Interview the user about their business/brand and create brand/brand.md — the brand voice file every other skill uses. Use when user wants to set up, update, or fix their brand profile.
---

Interview the user to create the brand file `brand/brand.md`.
**Talk to the user in Thai. Write `brand.md` itself in Thai** (it feeds Thai content generation).

## Steps

1. Ask **one question at a time** (don't dump all 10 at once — act like a consultant). Cover:
   - What the business/page does and sells
   - Who the customer/audience is (age, interests, pain points)
   - What makes them different from competitors
   - Brand voice: casual or formal? Which Thai particles (ครับ/ค่ะ/จ้า)? Jokes OK? How much emoji?
   - Primary platform (IG / Facebook / TikTok) + a posting frequency they can realistically keep
   - What NOT to say/do (forbidden words, retired promos, drama to avoid)
   - Example posts the user likes (ask them to paste any)
2. While asking, if an answer is too broad, ask ONE short follow-up — then move on, don't stall.
3. Write the summary to `brand/brand.md` (in Thai) using this structure:

```markdown
# Brand: <name>
## ธุรกิจ (Business)
## ลูกค้า (Audience)
## จุดขาย (Differentiators)
## เสียงแบรนด์ (Voice — tone, pronouns, emoji, sample sentences)
## แพลตฟอร์ม + ความถี่ (Platform + frequency)
## ข้อห้าม (Never do / never say)
## ตัวอย่างโพสต์อ้างอิง (Reference posts)
```

4. Show the file, ask what to change, revise until the user is happy.
5. Close by telling them every other skill uses this file automatically — suggest trying `/caption`.

If `brand/brand.md` already exists → read it and ask which section to update.
