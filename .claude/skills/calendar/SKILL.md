---
name: calendar
description: Build a 7-day posting plan (content calendar) as a saved file — what to post, when, on which platform, with ready hooks. Use when user wants a posting schedule or weekly content plan.
---

Plan 7 days of posts, every decision made up front, all in one file. **Write hooks/topics in Thai.** Talk to the user in Thai.

## Steps

1. Read `brand/brand.md` (if missing → invite them to run `/brand`) — use the platform + frequency from the brand file.
2. **Ask everything up front, then produce it all at once** (this is the whole point: make every decision now so the user isn't back asking daily):
   - Anything special this week? (promo? launch? holiday/festival?)
   - How many posts can they realistically make (don't over-plan)?
   - Do they already have photos/videos on hand?
3. Create `output/calendar-<start-date>.md`:

```markdown
# แผนโพสต์ <date>–<date>
| วัน | เวลา | แพลตฟอร์ม | ฟอร์แมต | Hook/หัวข้อ | CTA | ต้องเตรียม |
|---|---|---|---|---|---|---|
```

   - Posting times: when Thai users are actually online (midday 11:30–13:00 / evening 19:00–21:30) unless the brand knows its own timing.
   - Simple content mix: value ~60% / sell ~30% / trend or behind-the-scenes ~10%.
   - The "ต้องเตรียม" (to-prepare) column must be detailed enough to act on directly (e.g. "shoot the product from 3 angles on a white background").
4. End of file: roll every shoot/prep item for the week into a single checklist (batch it all in one session).
5. Offer: want the caption for any given day? Continue straight into `/caption`.
