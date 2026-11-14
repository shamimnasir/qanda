# Example films: read this before copying

These are records of real films. Their scripts, shots and picks are kept as they were made, so they show the older way in places. **Current rules win over any example.**

## Copy these
- The file formats: `project.json`, `script_master.tsv`, `shotlist.json`, `picks.json`, `thumbnails.json`.
- Graphics and their props, how anchors are written, and how shots are timed to words.
- `facts_to_verify.md` and `youtube_publish_kit.md` in `Japan_Longevity`, as models for structure.

## Updated to the new rules (Nov 2026)
Each `project.json` now shows:
- `opener`: a draft of the 5 lines. These were not voiced, are not in the scripts, and were not timed. Numbers take longer to say, so let on-screen text carry them.
- `short.brief`: written from the film's own lines.
- `feel` on every score section. The key is gone, because the engine now chooses one for each film.

## Do not copy
| Old pattern | Do this instead | Rule |
|---|---|---|
| Shots of 3 to 8 s, "ILLUSTRATIVE FOOTAGE" text, the credits card and full credits in a pinned comment | No visual over 3 s, no label text, no credits card, credits in the description only, as in `Picher` | `references/rules.md` |
| The opening of these scripts, the draft 5-line `opener` text, a slow hook, and animated title cards at frame 0 | The hook: hard cuts of facts in 0 to 6 s, as in `Picher` | `references/script_and_retention_guide.md` |
| Another film's mood plan or `feel` lines | Plan the music from this film's script | `references/music_guide.md` |
| Shorts cut as film highlights, with a very long hook | A story of its own, starting from `short.brief` | `references/shorts_guide.md` |
| Stock clips under narration in long runs | Decide what each shot shows or proves first | `references/viral_style_guide.md` |
| Oymyakon's "we arrived", "I felt it" and similar lines | First person only for what is true of the producer and footage they filmed. Otherwise credit the source | `references/rules.md` |
| Oymyakon's Celsius, and the Bangla columns and `props_bn` | The channel is English only for the USA, so use US units such as Fahrenheit, and write only English unless the producer asks | `_Channel/channel_strategy.md` |

## The films
| Folder | Good for learning |
|---|---|
| `Picher` | **Start here.** The current house style, approved by the producer: fact hook, 3 s shots, honest pictures without labels, `strata` graphic, `lead`, reuse. |
| `Oymyakon` | A story film, a map, quote cards, a signature sound moment |
| `Japan_Longevity` | Data graphics, real-place photos, fact lists, a scored publish kit |
| `Fix_Your_Life` | An idea film with no real location, and thumbnails with the producer's face. It retells a writer's ideas in new words with new research, so check `references/rules.md` before adapting a source |
