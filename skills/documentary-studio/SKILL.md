---
name: documentary-studio
description: Make a complete, retention-focused YouTube documentary (about 5 minutes) plus a 60 s vertical Short, in English and/or Bangla, with licensed stock and photos, AI narration from ElevenLabs, an original synthesized score with rises and drops, burned-in captions, SRT files, a license tracker and a publish kit (titles, thumbnails, description, hooks, Facebook caption), plus demand research before the script and a performance review after publishing. Bundles a config-driven Python plus Remotion engine. Use this whenever the user wants to make, script, remake, translate, re-cut or publish a documentary, explainer or faceless story video, a Bangla version of a video, a YouTube Short from a film, or says things like "make a documentary about X", "new video on X", "ডকুমেন্টারি বানাও", even if they don't say "documentary studio".
---

# Documentary Studio

A full production pipeline: topic and sources in, finished films, Shorts and a publish kit out. It was built on the Oymyakon film ("The Place Where Standing Still Can Kill You", Bangla and English, cold look) and extended on "Why Japanese People Live Longer" (English, warm look, data graphics, health topic) and "One Day to Fix Your Life" (English and Bangla, an idea film adapted from a written source, dusk look, story graphics). All three are worked examples in `assets/examples/`.

`<skill>` below means this skill's folder (the folder holding this SKILL.md).

## Before anything else
1. Read `references/rules.md`. Those rules always apply: no long dash characters, licensing, honesty, costs, and the 3 gates.
2. Read `references/producer_profile.md` for the producer's voices, preferences and the look that worked.
3. Follow `references/playbook.md` step by step. It holds every command, the time budget, the costs and the known traps.

## Where this works
- **Claude Code on a Mac (full pipeline).** It needs ffmpeg, whisper-cpp, Google Chrome, Node, and Python with numpy and Pillow. Run `bash <skill>/scripts/setup.sh` to check them. If something is missing, tell the producer and, with their OK, run `setup.sh --install`. The Pexels key is stored by the producer running `bash <skill>/scripts/setup.sh --key` in their own Terminal. Never ask them to paste the key into chat.
- **Claude.ai project or another chat with no local Mac tools.** Do the parts that need no rendering: research, `facts_to_verify.md`, the script in English and Bangla, the ElevenLabs tagged paste files, the shot list, the score plan in `project.json`, the publish kit, hooks and captions. Say plainly that rendering needs Claude Code on the Mac.

## Workflow

### 1. Brief
If the producer pasted the brief from `references/master_prompt.md`, use it. Otherwise ask once, in one message, for only what is missing:
- topic and source material
- the original-source credit
- languages
- length
- voices
- mode (FAST or CAREFUL)
- credit budget

### 2. Create the project
Run `bash <skill>/scripts/new_project.sh "<Topic>" [parent folder]`. It creates `<Topic>_Documentary/` in the current folder by default, with the engine, `studio.sh`, the templates, a project `CLAUDE.md` and the private `.env`, and creates `_Channel/` beside it if missing. Work inside the project folder.

### 3. Demand check
Follow `references/growth_system.md`. Read `_Channel/channel_strategy.md` and `_Channel/learned_rules.md`. Use the producer's `01_Script/demand_research.csv` (wins and flops, gathered by hand, never scraped) plus web search, then write the demand level, the patterns, and the channel fit and repeat tests in `01_Script/demand_brief.md`. If the evidence is weak, recommend a change and carry on with the producer's choice. This is not a gate.

### 4. Promise first
In `01_Script/demand_brief.md`, write the story within the story (central person, conflict, stakes, change), audience, promise, proof, plan, format, next step, 3 working titles and 3 thumbnail ideas. The script must deliver this promise. If the facts do not support it, change the promise.

### 5. Research
- Build `01_Script/facts_to_verify.md` from the source material, and recompute every number. Mark each claim SOURCED, CHECK (one detail still needs a primary source) or CONTESTED (experts disagree, and the script says so). For health or science topics, follow the honesty rules in `references/rules.md`.
- Test the tools before relying on them:
  - `ffmpeg -version`
  - `whisper-cli --help`
  - one Pexels API call
  - the ElevenLabs balance, if a voice is needed

  Report the result.

### 6. Script -> GATE 1 (stop)
- Write `01_Script/script_master.tsv`, one sentence per row, with the columns `break, tags, en, en_tts, bn`. Follow `references/script_and_retention_guide.md` and `references/elevenlabs_tagging_guide.md`. Apply the storytelling techniques in that guide: write the ending first, pick a story lens, alternate context and conflict, join beats with "therefore" and "but", vary sentence rhythm, talk to one person, hook with sound and picture together, give Promise, Proof and Plan by 0:30, deliver the promise, and place any next step naturally. Go through its checklist before showing the script.
- Check the script against `references/viral_style_guide.md`: curious narrator, question then report then new question, every paragraph labelled and filler cut.
- Open every film with the hook in about the first 10 s, per `references/script_and_retention_guide.md`: one to three full spoken sentences with the twist, over 3 or 4 shots that show what the voice says, with little text. Set `opener` in `project.json`.
- Write Bangla as native Bangla, row by row, with the same sentence breaks as the English. The engine pairs the rows.
- Run `./studio.sh scripts`, then show the producer the script, the translation, the credit cost, the demand level and the promise. Wait for approval. After approval, the script is locked.

### 7. Voice -> GATE 2 (stop)
- Give the producer the paste files and the settings.
- After they download, check each filename (voice, stability, model) and copy it into `06_Audio_Voiceover/` with the name in `project.json`.
- Say if the settings differ from the plan.

### 8. Build
- Run `./studio.sh align`.
- Write `08_Timeline_and_Exports/data/shotlist.json`: decide what each shot shows or proves before searching (no stock wallpaper, a new picture when the idea changes), no visual over 3 s, about 130 shots for 5 minutes, quote cards for real people, title, map and graphics, end cards.
- Fill `project.json`: the look (`cold`, `warm` or `dusk`), score sections and hits planned for this film per `references/music_guide.md` (never copied from another film), sfx, gaps, Short segments and `short.brief` per `references/shorts_guide.md`, map, quotes per language, credits, tracker_extra. Copy patterns from `assets/examples/Oymyakon/` (story, map, quotes) `assets/examples/Japan_Longevity/` (data graphics: `count`, `bars`, `rank`, `bowl`) or `assets/examples/Fix_Your_Life/` (idea film, story graphics: `flip`, `rec`, `course`, `steps`, `alert`, `range`, with Bangla text in `props_bn`) or `assets/examples/Picher/` (the current fast edit: fact hook, 3 s shots, `strata` cross-section, reuse and `lead`).
- Run `./studio.sh media`, and `./studio.sh pool` for themed pools of exciting clips from `media_pool` in `project.json`. View every contact sheet and read every clip title, then write `data/picks.json`. Run `./studio.sh download`.
- Run `./studio.sh build && ./studio.sh sound && ./studio.sh docs`, never piped to `head`. Fix what the hook, shot and pause checks print. Read `07_Music_SFX/music_story_arc.md` and the opener, score and Short checks. Fix what looks wrong.
- Run `./studio.sh stills en <frames>`, then look at the stills. Fix what you see and repeat.
- Run `./studio.sh render` outside the sandbox, in the background (about 15 min per film, with a watchdog). Use `./studio.sh render-film` for a re-cut that keeps the live Short.
- Extract a frame of every shot, graphics included, from each render, and look at all of them.

### 9. QA and publish kit -> GATE 3 (stop)
- Run `./studio.sh qa`, then go through `references/quality_bar.md`.
- Write `08_Timeline_and_Exports/youtube_publish_kit.md`:
  - packaging, following `references/packaging.md` (always):
    - 3 film thumbnails (2 to 4), each from a moment inside the film, with a big human face (the producer's or a made-up person related to the film) and 0 to 3 words that do not repeat the title, plus 1 or 2 vertical Short covers. Write `data/thumbnails.json`, run `./studio.sh thumbs`, look at every image and at `phone_size_check.jpg`.
    - 3 titles for the film and 3 for the Short, each with its virality score from the rubric, one recommendation, and which thumbnail it pairs with. No unprovable superlatives.
  - a promise check for each title and thumbnail pair, and the section "Next step and end screen"
  - the description in a ``` block, with chapters, sources, "Not medical advice" for health topics, and the `[Paste ... credits ...]` line
  - the Short: titles, covers, description, its brief, and how it adapts for each platform used
  - the honesty flags
- Add hooks in each language (use the viral-hook-generator skill if it is available) and a Facebook caption per language.
- Run `./studio.sh upload`. It builds `10_Ready_to_Upload/` at the top of the project: the films, Shorts, SRT files and thumbnails, plus plain text files to paste (titles, the description with the credits, which go only there and fit YouTube's 5,000-character limit, Short text, hooks, Facebook caption). Fix every WARNING it prints. Point the producer to this folder first.
- Report to the producer:
  - `10_Ready_to_Upload/` first, then every other file, with its location
  - the recommended title and thumbnail pairing, and the scores
  - what was verified
  - what was not verified (audio by ear, facts)
  - every open decision

### 10. After publishing
At 48 hours, 7 days and 28 days, the producer adds YouTube Studio numbers to `11_Performance/metrics.csv`. Run `./studio.sh review`, then agree one main change for the next film, add evidence to `_Channel/learned_rules.md`, and test any win with another film in the same theme. See `references/growth_system.md`.

## Extending the engine
When a film needs something new, add it to the engine instead of writing one-off scripts. For example:
- a topic-specific diagram goes in `remotion/src/graphics.tsx` as a new `mg` kind with props
- a new music mood goes in `build_score.py`

The engine files are copied into each project, so edit the project's copy. If the change is reusable, offer to copy it back into `<skill>/assets/engine/`.

## Files in this skill

| Path | Contents |
|---|---|
| `references/rules.md` | The hard rules |
| `references/producer_profile.md` | The producer's defaults |
| `references/playbook.md` | The full step-by-step workflow |
| `references/master_prompt.md` | The fill-in brief |
| `references/script_and_retention_guide.md` | How to write the script for retention |
| `references/elevenlabs_tagging_guide.md` | How to tag the script for ElevenLabs |
| `references/quality_bar.md` | The checks before Gate 3 |
| `references/viral_style_guide.md` | Read before the topic, script and shotlist: what successful YouTube documentary creators do, with how strong the evidence is |
| `references/shorts_guide.md` | Read before planning any Short or Reel: story, first-frame hook, payoff, simple words, tight edit, each platform |
| `references/music_guide.md` | Read before planning a score: soft, unique to each film, matched to its vibe and pace, real ups and lows, stereo, pauses and sound design |
| `references/packaging.md` | Thumbnail and title research, rules and the virality score |
| `references/growth_system.md` | Demand check, promise first, next step, channel fit and the review after publishing |
| `assets/producer/` | The producer's cutout photos, one option for thumbnails alongside made-up people, with a table of which face suits which moment |
| `scripts/setup.sh` | Checks and installs the tools; stores the Pexels key |
| `scripts/new_project.sh` | Creates a new project folder |
| `assets/engine/` | `studio.sh`, the Python pipeline scripts, and the Remotion project (fonts included; `node_modules` cached by setup) |
| `assets/templates/` | Templates for project.json, the script, the shot list, the facts list, the demand research and brief, the channel files, the publish kit and the permission request |
| `assets/examples/README.md` | Read first: what to copy from the example films, and which older habits not to copy |
| `assets/examples/Oymyakon/` | A complete project.json, script_master.tsv (English and Bangla) and shotlist.json |
| `assets/examples/Japan_Longevity/` | An English health-topic film: project.json (warm look), script, shotlist with data graphics, thumbnails.json, facts_to_verify.md and the publish kit with scored titles |
| `assets/examples/Picher/` | The current house style: fact hook, every visual 3 s or less, no labels or credits card, `strata` graphic, project and shot files, fact list and publish kit |
| `assets/examples/Fix_Your_Life/` | A bilingual idea film adapted from a written letter: project.json (dusk look), script, shotlist with `props_bn`, picks and thumbnails.json |
