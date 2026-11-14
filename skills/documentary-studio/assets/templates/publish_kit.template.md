# YouTube Publish Kit: __TITLE__

## 1. Title options (film)
Score with `references/packaging.md`. Avoid superlatives you cannot prove ("the coldest", "the first"). Prefer "one of the".

| # | Title | Chars | Frame | Score |
|---|---|---|---|---|
| 1 | ... | | | |

**Use title 1.** Why, and which thumbnail it pairs with.

## 2. Thumbnails (film, 1280x720), in `05_Motion_Graphics/thumbnails/`
3 thumbnails (2 to 4), each a different moment inside the film with its time, 0 to 3 words, not repeating the title. Built from `data/thumbnails.json` with `./studio.sh thumbs`.
- `A_....jpg`: moment (m:ss), text, what the viewer should wonder and feel, the visual mechanism, 2 or 3 wording options, and whether it passes the 50% TV test.

**Promise check:** in one sentence, what each title and thumbnail pair promises, and the time in the film where it is delivered.

## 2b. Next step and end screen
One next step, from the demand brief. Say what it is, why it continues this film, and whether it is free or paid.
- Description line:
- Pinned comment (optional, to start a conversation, never credits):
- End screen: which video or playlist, and why that viewer would want it

## 3. Description
```
[Hook line from the cold open]

[Next step line, if there is a link]

[Two sentences of context with the key facts]

CHAPTERS
0:00 ...

ABOUT THIS VIDEO
The story is based on [ORIGINAL SOURCE with link]. Real photos are labelled with their location; other footage is illustrative stock.
Narration uses an AI-generated voice (ElevenLabs). Music and sound design are original.

[Paste 09_Permissions_and_Licenses/credits_short_for_description.txt]
```

## 4. Short
Per `references/shorts_guide.md`. Story, hook, expectation and ending in one line each. Platform notes: YouTube Shorts; Reels (captions, sharing); TikTok only if used.
| # | Title | Chars | Frame | Score |
|---|---|---|---|---|
| 1 | ... | | | |

Covers (1080x1920): 1 or 2 from moments in the Short, plus a fallback frame time. A 2-line description, and the "Related video" link to the full film.

## 4b. Hooks (English)

## 4c. Facebook caption (English)

## 5. Footage honesty flags
Stock clips whose content does not match the line they sit under.

## 6. Before publishing
- Set the end screen, and add the check-in dates (48 hours, 7 days, 28 days) to your calendar. Then add the numbers to `11_Performance/metrics.csv`.
- Upload the SRT for every language.
- Check YouTube's current "altered or synthetic content" rules.
- Fill in every [bracket].
