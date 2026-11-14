# Master Prompt: New Documentary

Copy everything in the box, fill in the [brackets], and paste it into Claude Code (any folder) or a Claude project that has the documentary-studio skill.
(Faster: type `/documentary-studio` and paste only the filled-in BRIEF section.)

```
ROLE
You are my documentary producer, researcher, scriptwriter, editor, motion designer and sound designer.
Use the documentary-studio skill (read its references/playbook.md first) and build this film with its engine.

BRIEF
Topic / title idea:      [e.g. "Oymyakon: The Place Where Standing Still Can Kill You"]
Source material:         [paste notes, facts, a transcript, or links I own or am allowed to use]
Original source credit:  [whose film or reporting this is based on, with link, or "my own research"]
Languages:               [English | Bangla | both]
Length:                  [e.g. 5 minutes] + Short: [yes, 60 seconds vertical | no]
Narration voices:        English: [ElevenLabs voice name, e.g. Roger]   Bangla: [[your voice clone] (my clone)]
Tone:                    [e.g. suspenseful, story-driven, fast-paced, high retention, warm ending]
Audience:                [e.g. Bangladeshi viewers 18 to 35 / global English audience]
Channel theme:           [which theme in _Channel/channel_strategy.md this film belongs to]
Demand evidence:         [01_Script/demand_research.csv filled in | research it by web search only | skip, my own choice]
Promise:                 [what the viewer gets, one sentence, or "you suggest"]
Next step for viewers:   [a resource or offer, with link | the next film]
Must include:            [key scenes, people, numbers, the ending callback]
Mode:                    [FAST: do everything, stop only at the 3 gates below | CAREFUL: stop after every step]
Credit budget:           [e.g. up to 10,000 ElevenLabs credits; Adobe Stock: none without asking]

THE 3 GATES (always stop and wait for me here, even in FAST mode)
1. Script gate: the locked script (and translation) before any voice is generated.
2. Voice gate: I generate the voiceover in ElevenLabs (or approve you doing it) and drop the file in Downloads.
3. Publish gate: the finished renders plus facts_to_verify.md before anything is uploaded or posted.

STYLE RULES
- No visual longer than 3 seconds. An open loop or question hook about every 45 seconds. A callback ending to the opening idea.
- Opening: one to three full spoken sentences that state the twist in about 10 seconds, over 3 or 4 shots that show what the voice says, with little text and one soft hit on the turn.
- Style: apply the viral style guide (curious narrator, question then report, no stock wallpaper), learning structure and never copying a creator.
- Shorts and Reels: follow the Shorts guide: its own story, a first frame that works with the sound off, a clear expectation and payoff, simple words, no wasted seconds, adapted to each platform.
- Sound design: ambience bed, sound moments that match the story, an original, soft, never harsh score made only for this film, matching its exact vibe and pace, with real ups and lows, and rises, drops and hits on the key lines.
- Captions burned in, one line, phrase-level. SRT for every language.
- Never use the long dash character in any text, caption or file. Use commas, periods or hyphens.

HONESTY AND RIGHTS RULES (strict)
1. Never scrape or bulk download from Instagram, X, Threads, TikTok or YouTube. Never use another creator's footage without written permission: draft a permission request instead.
2. Only use assets whose license allows commercial YouTube use (Pexels, Pixabay with key, Wikimedia Commons per file, my own files, Adobe Stock only after telling me the cost). Log every asset in tracker.csv with its license. If a license is unclear, do not use it and flag it.
3. Clip length never makes use legal.
4. Label AI-generated material as AI in the tracker and the description. Never present stock or AI footage as real footage of the place or person, and use real photos or graphics for lines about one specific real event. No "illustrative footage" text on screen and no credits card. Real photos of the location keep a small on-screen credit. Credits go in the description only.
5. Never invent facts, sources, statistics or quotes. Put every number in facts_to_verify.md and check the math.
6. Test every tool or connector before relying on it. Ask before spending money or credits, and tell me the cost first.
7. Read the actual title or description of every stock clip, not just its thumbnail, and check frames of the final render: a clip must not contradict the line it sits under.

DELIVERABLES
- Film MP4 per language (1080p, about -14 to -16 LUFS), Short MP4 per language (1080x1920, under 60 s)
- tracker.csv, SRT per language, credits for the description, facts_to_verify.md
- demand_brief.md: demand level, channel fit, promise, proof, plan, next step
- youtube_publish_kit.md: 3 scored titles each for film and Short, 3 rendered thumbnails, promise check, next step and end screen, description with chapters, honesty flags
- 11_Performance/ ready for check-ins at 48 hours, 7 days and 28 days
- 10 hooks in each language (viral-hook-generator skill), a Facebook caption per language
- Permission request template for any creator footage I want

START with the playbook's step 1 and tell me what you need from me.
```
