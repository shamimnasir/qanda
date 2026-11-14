# Shorts and Reels guide

The producer's standing rule (Nov 2026): every Short and Reel follows this guide. A Short is its own story with a simple visual hook, a clear expectation, cause and effect, tight editing and a satisfying payoff. It is not a trailer or a summary of the film.

Source: the producer's summary of a video about how Jenny Hoyos approaches Shorts. The original was not viewed and its examples were not checked. Her channel and audience are not ours, so treat her numbers as one creator's targets. `references/rules.md` always wins, and the channel's own numbers beat this guide.

## Honesty comes first
- A story needs a goal, a problem or a contrast, but never invent a personal goal, challenge or reaction. Use a true one, such as the film's real question.
- Simple words must stay accurate. If a simple version would be false, keep the harder word and show what it means.
- Never promise what the Short does not deliver. Facts still go in `facts_to_verify.md`.

## Write the brief first
Fill `project.json` -> `short.brief` before choosing any lines:

| Field | The question |
|---|---|
| `story` | What goal, problem, irony or contrast makes someone care? |
| `first_frame` | What does a viewer see and read at the very first frame, with the sound off? |
| `hook_line` | The first spoken line, in simple words, matching the title and cover |
| `foreshadow` | One brief early line saying what they will get, without giving it away |
| `mechanism` | What pushes it forward: a test, countdown, three steps, a reveal or a problem to solve |
| `ending` | The last line, written first. It closes the loop, with a twist if one is true |
| `why_share` | Why would someone send this to a friend? |

## The process
1. List many possible angles from the film's story, and from daily life if the topic fits.
2. Keep the ones that are true, clear and worth making.
3. Write the ending first, then work backward.
4. Write at least 5 hooks. Choose by clarity and how well they show on screen. `viral-hook-generator` can help.
5. Write one foreshadowing line that appears early and is brief.
6. Join every beat with "so", "but" or "therefore", so each event causes the next. Never use "and then".
7. Choose film segments that tell this story, in that order, then edit hard.
8. After publishing, read the retention graph and change the next Short.

A Short cut from the film costs no credits. If the film's lines cannot tell the story, say so before Gate 2 and offer new Short lines with their credit cost. The engine now builds Shorts from the film's narration only, so new lines need a small engine change first.

## The opening
Use the same idea as the film's hook: a full spoken sentence with the twist, and strong pictures with big text from frame 0. Do not use fragment lines. The producer rated the old 5-line formula dull.

Check the opening against the four ways a hook fails: delay, confusion, irrelevance and disinterest (`references/script_and_retention_guide.md`). Topic in the first sentence, contrast in the next.

## The rules
1. **The first frame hooks by itself.** Clear with the sound off, with big readable text on it from frame 0 and no fade in.
2. **Simple words.** Aim for roughly a fifth-grade reading level, with short sentences. The check prints the English score. Write Bangla in everyday চলিত ভাষা. Use the same plain style for every audience, and do not mark films as made for kids because of it.
3. **Set the expectation early and pay it off.** Viewers should know what they are waiting for. Close that loop, and add a twist only if it is true.
4. **Every second earns its place.** Remove pauses and spare frames. Use only the length the story needs. 60 s is a limit, not a target.
5. **Protect the ending.** End when the last line lands. The engine trims silence before the first word and after the last. One example in the source had a sharp drop in the last second, and removing that second helped.
6. **Cause and effect.** Each beat should cause the next one.
7. **Think about sharing.** Retention alone may not explain why a Short spreads. Satisfaction and sharing may matter too.
8. **Keep music, face and honesty rules.** `references/music_guide.md` and `references/packaging.md` still apply. A hard cut in the audio at the end needs a quick listen.

## Platforms
The same video can do very well on one platform and poorly on another. Plan for each one instead of assuming that vertical video travels. These are one creator's impressions, so test them.

| Platform | Described as favoring | What to adapt |
|---|---|---|
| YouTube Shorts | Slower storytelling, a more mature audience | The default version |
| Instagram or Facebook Reels | Visually clear, subtitle-heavy, shareable | Bigger clear captions, a first frame that needs no sound, a caption written for sharing |
| TikTok | Shorter, denser videos with faster information | A tighter cut with fewer beats |

Write a line in the publish kit for each platform used. Check each platform's rules before posting.

## Checks
`./studio.sh sound` prints a Short check for each language. Fix what it flags where you can:
- Length, delay before the first word, long pauses, and silent tail
- English reading level and the hardest words
- Which `short.brief` fields are empty

Check by eye and ear too:
- Look at the frame at 0:00 at phone size, with the sound off. Does it say what this is about?
- Read the words without the picture: does each beat cause the next?
- Play the last 3 seconds. Does it end cleanly?

## After publishing
Add a row with `video` set to `short` to `11_Performance/metrics.csv`. It includes:
- `shorts_stayed_to_watch_percent`: viewers who watched instead of swiping away, from YouTube Studio. The name in Studio may differ, such as viewed versus swiped away.
- `average_percent_viewed`
- `biggest_drop_time`: especially the opening and final seconds.

Jenny Hoyos reportedly aims for about 85% or more staying and about 95% viewed, and some of her videos with average retention still reached millions. Use those as ambitious references only, and judge against the channel's own Shorts. A short audience also does not automatically become a long-form audience, so measure both.
