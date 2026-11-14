# Documentary Studio Playbook

The fastest path from a topic to a finished, licensed, bilingual documentary plus Short. Built from the Oymyakon project.
Engine: `<skill>/assets/engine` (Python scripts + Remotion). Worked example: `<skill>/assets/examples/Oymyakon/`. `<skill>` is this skill's folder.

## 0. One-time setup per machine
`bash <skill>/scripts/setup.sh` checks and installs everything: ffmpeg, whisper-cpp and its English model, Google Chrome, Python with numpy and Pillow, Node, the Remotion packages (cached in `~/.cache/documentary-studio/`), and the Pexels key in `~/.config/documentary-studio/.env` (chmod 600, never printed). Rotate the key if it was ever pasted in chat.

## 1. Create the project (1 minute)
```bash
bash <skill>/scripts/new_project.sh "Topic Name" [parent folder, default: current folder]
```
Creates `Topic_Name_Documentary/` with the standard folders, the engine, `studio.sh`, the templates, a project `CLAUDE.md` with the rules, and the private `.env`.

## 1a. Demand check (producer about 20 min, Claude 10 min)
Follow `references/growth_system.md`. The producer fills `01_Script/demand_research.csv` by hand: at least 5 wins from 3 channels and 2 flops, in each language. Never scrape YouTube. Claude adds web search, computes the ratios, finds the patterns and writes `01_Script/demand_brief.md` with demand level A, B or C, the channel fit test and the repeat test. Read `_Channel/channel_strategy.md` and `_Channel/learned_rules.md` first. Not a gate: if the producer skips the sheet, mark the level and carry on.

## 1b. Promise first (5 min)
In the same brief: audience, one-sentence promise, proof, plan, format, next step, 3 working titles, 3 thumbnail ideas. The script delivers this promise, and final packaging still uses real moments from the film.

## 2. Research and fact base (15 to 30 min)
- Extract every claim from the source material into `01_Script/facts_to_verify.md`. Recompute every difference and conversion. (Oymyakon: "+30 to -60.5 is almost 100 degrees" was wrong; it is about 90.)
- Note names that a voice may mispronounce.

## 3. Script (20 to 40 min) -> GATE 1
Write `01_Script/script_master.tsv`: one sentence per row, columns `break, tags, en, en_tts, bn`.
- Structure for a 5-minute film (about 650 to 780 spoken words in English, 130 to 150 wpm):
  cold open hook (0:00 to 0:25, with Promise, Proof and Plan clear by 0:30, ends on an open loop), then 8 to 10 chapters of 25 to 40 s, a question hook about every 45 s, and a close with a callback to the opening image.
- `en` is what captions show (digits fine). `en_tts` spells numbers out for the voice ("minus sixty point five").
- `bn`: native Bangla, not a word-for-word translation. Numbers as words, Bangladeshi usage (পানি, গোসল). Keep the same sentence breaks as English: the engine pairs them row by row.
- Tags: see `references/elevenlabs_tagging_guide.md`. A row with only `[long pause]` marks a gap where a quote card goes.
- Quote lines from real people never go in the narration: they become `quote` cards in the shot list.
Run `./studio.sh scripts` -> `01_Script/elevenlabs_en.txt`, `elevenlabs_bn.txt` and the credit cost of each. At Gate 1, also show the demand level and the promise.

## 4. Voice (5 min, the user does it) -> GATE 2
- ElevenLabs, Eleven v4 (or v3), paste the whole file, one generation. Cost is about 1 credit per character. Check the balance first.
- Bangla: voice "[your voice clone]" (the user's own clone). English: a library narrator such as Roger.
- **Check the filename** after download: it shows the real stability (`s50`) and model (`v4`). The slider in the UI did not always apply.
- Claude cannot save downloads from ElevenLabs through the Chrome extension: ask the user to click Download. If Claude pastes text into ElevenLabs, copy with `LANG=en_US.UTF-8 pbcopy` outside the sandbox, or Bangla turns into garbage.
- Copy the files into `06_Audio_Voiceover/` with the names in `project.json` -> `languages`.

## 5. Align (1 min)
`./studio.sh align`
- English: Whisper word timings (expect 95%+ matched). It prints every sentence with its first word index: use them in the shot list.
- Bangla (or any language Whisper handles badly): sentences are fitted to the take's pauses. Trust check printed at the end: most sentences after a `[long pause]` should start right after a long silence.

## 6. Shot list (20 to 30 min)
`08_Timeline_and_Exports/data/shotlist.json`, no shot over 3 s (about 130 shots for 5 minutes, or 8 spoken words a shot at most). See `<skill>/assets/templates/shotlist.template.json` and the `Picher` example, the first film cut this way.
- `"tone"`: `gray`, `cool`, `night`, `warm` or `vivid`, for the color arc. `"hold": true`: an approved long moment past 3 s.
- `"w"`: a word index or a phrase from the narration where the shot starts. `"lead"`: seconds to cut before that word, for a pause in the voice. `"after"` + `"dur"`: a card inserted between lines (title, quotes), 3 s at most. `"w": "end"`, `"end2"`: end cards, 3 s each and about 6 s in all so the YouTube end screen fits. No credits card. `"kind": "reuse"` + `"of"`: show an earlier picture or graphic again. `"after"` + `"dur"` is also how to add a pause: a strong picture over a moment of music and sound. Follow the build's pause check.
- `kind`: `pexels` (with `"q"` search list), `commons` (with `"q"` and `"place"`), `mg` (motion graphic), `quote`, `reuse` (`"of"` another shot).
- Graphics (`"mg"` + `"props"`): `title`, `map` (from `project.json` -> `map`), `thermo`, `timer`, `stat`, `stack`, `compare`, `card`, `scale`, `endcard`, `credits`, plus Oymyakon-specific examples to adapt (`vessels`, `permafrost`, `wall`, `boiler`).
- Data graphics (added for the Japan film), with their props:
  - `count`: a number counting up. `{"from": 153, "to": 107677, "fromLabel": "1963", "label": "PEOPLE OVER 100", "sub": "Japan, 1 September 2026"}`
  - `bars`: two bars, before and after, values 0 to 100. `{"title": "...", "left": {"label": "1965", "value": 100, "text": "100"}, "right": {"label": "1990", "value": 20, "text": "about 20"}, "note": "Index, 1965 = 100"}`
  - `rank`: a place falling down a ladder. `{"title": "...", "of": 47, "steps": [{"year": "1995", "rank": 4, "at": 0}, {"year": "2000", "rank": 26, "at": 5.9}]}`. Set `"at"` (seconds into the shot) so each step appears when the narration says it; without it the steps are evenly spaced.
  - `bowl`: a bowl filling up and stopping at a percent. `{"percent": 80, "label": "HARA HACHI BU", "sub": "Stop at 80% full"}`
  - An `mg` shot that also has a pick in `picks.json` gets that footage dimmed behind it (`count` uses it).
- Story graphics (added for the Fix Your Life film), with their props:
  - `flip`: one word struck through and replaced. `{"from": "FAILING", "to": "SUCCEEDING", "sub": "AT A GOAL YOU NEVER CHOSE"}`
  - `rec`: a camera viewfinder over footage. `{"label": "NO SOUND"}`. Needs a pick (give the shot its own `"q"`).
  - `course`: a ship drifting and correcting along a straight line. `{"target": "YOUR COURSE", "wind": "WIND", "note": "CHECK. CORRECT. AGAIN."}`
  - `steps`: rows that appear one by one. `{"steps": [{"k": "1 YEAR", "v": "THE MISSION"}]}`
  - `alert`: a phone alarm banner holding one question. `{"kicker": "RANDOM ALARM", "text": "What am I avoiding right now?"}`
  - `range`: values along one scale. `{"title": "...", "max": 254, "note": "...", "points": [{"value": 66, "text": "ABOUT 66", "at": 0.1, "main": true}]}`, where `at` is a fraction of the shot.
  - `portrait`: a small photo beside a name, for images too small to fill the frame. `{"name": "...", "sub": "..."}`. Needs a pick.
- Bangla text on graphics: add `"props_bn"` beside `"props"`. It overrides those props in the Bangla film (the same works for any language code), as `"overlay_bn"` does for overlays. Thumbnail text in Bangla is drawn through Chrome, so conjuncts shape correctly.
- An `mg` shot with its own `"q"` gets stock candidates in the contact sheets, for footage behind the graphic.
- Sound effect `alarm`: four quick digital beeps, twice, with an optional `"gain"`. For a story with an alarm clock or phone.
- Look: `"look"` in `project.json` is `"cold"` (default: blue grade, falling snow) `"warm"` (amber grade, warm palette, slow drifting dust, made for the Japan film) or `"dusk"` (grey-blue with no snow, for inner stories; the `Close` chapter still turns warm). It recolours every graphic, the grade and the captions.
- Mix target: about 55% stock, 25% graphics, 15% real photos of the place, 5 to 10% creator-licensed (only with permission).
- `"overlay"`: a big text line over footage, for example "ABOUT 800 RESIDENTS".

## 7. Media (15 to 30 min)
`./studio.sh media` -> contact sheets in `08_Timeline_and_Exports/review/`. View them, then write `data/picks.json`.
- Read the clip title under each thumbnail. Oymyakon lessons: "breath steam" was a vape cloud, "children walking" was two adults, "wolf" was a living wolf under "this wolf did not die", and "door opening" turned into a man in a VOLUNTEER T-shirt on a warm doorstep once trimmed.
- Prefer real, correctly licensed photos of the place (Commons). Check each license; CC BY-SA means ShareAlike, so flag it. Public domain (US government, NPS, USFWS) is cleanest.
- `./studio.sh download` downloads, logs licenses and deletes anything no longer picked.

## 8. Build, sound, stills (5 to 10 min)
```bash
./studio.sh build && ./studio.sh sound && ./studio.sh docs
./studio.sh stills en 120 900 2300
```
- `build`: a timeline per language, the map, and trimmed clips (long enough for every language).
- `sound`: an original score, unique to this film, from `project.json` -> `score` (see the music guide; moods: flash (automatic for the opener), dread, drive, tension, pulse, curious, hush, awe, suspense, light, warm, silence; hits get a soft rise, a short drop and a low bloom), ambience, sound effects (`sfx`), ducking, a -14 LUFS master, and the Short's audio.
- Look at the stills: caption collisions, letter-spaced Bangla, text running off-screen.

## 9. Render (about 17 min per 5-minute film, 4 min per Short)
`./studio.sh render en` / `./studio.sh render bn` (outside the Claude sandbox). Outputs go to `08_Timeline_and_Exports/renders/`.
To fix one shot without a full render: render only its frames (`--frames=a-b`) and overlay them with ffmpeg (see the Oymyakon history).

## 10. QA -> GATE 3
`./studio.sh qa`, then:
- Grab 2 frames of every stock shot from the final render and look at them all (wrong-content clips hide here).
- Listen for pronunciation and music balance. Claude cannot listen: the user must.
- facts_to_verify.md reviewed by the user.
- Promise match: the title, the thumbnail and the first 30 s make the same promise, and the film delivers it.

## 11. Publish kit (15 min)
`youtube_publish_kit.md`: packaging per `references/packaging.md` (3 scored titles each for the film and the Short; 3 film thumbnails from moments inside the film with a big human face, the producer's or a made-up person's, and 0 to 3 words that do not repeat the title, plus 1 or 2 Short covers, built with `./studio.sh thumbs`), a promise check, the section `Next step and end screen` (one next step, tied to the film's problem), description with chapters and credits, Short titles, honesty flags. Hooks: the `viral-hook-generator` skill in each language. Facebook caption per language. Upload the SRT files. Check YouTube's current "altered or synthetic content" rule. Then `./studio.sh upload` gathers everything into `10_Ready_to_Upload/`. In the kit, keep the description in a ``` block with the line `[Paste 09_Permissions_and_Licenses/credits_for_description.txt]`: the step swaps it for the short credits. Label sections for a second language with its name, for example `## 3. Description (Bangla)`.

## 12. After publishing (5 min per check-in)
At 48 hours, 7 days and 28 days the producer adds YouTube Studio numbers to `11_Performance/metrics.csv`. `./studio.sh review` writes `11_Performance/review.md` and updates `_Channel/video_ledger.csv`. Agree one main change for the next film, add signals and rules to `_Channel/learned_rules.md`, and test any win with another film in the theme. See `references/growth_system.md`.

---

## Time budget for a 5-minute bilingual film
| Step | Claude | User |
|---|---|---|
| Demand check, promise | 10 min | 20 min |
| Project, research, script, translation | 45 to 70 min | review: 10 min |
| Voice generation | | 5 to 10 min |
| Align, shot list, media picks | 40 to 60 min | |
| Build, sound, stills, fixes | 10 to 20 min | |
| Render 2 films + 2 Shorts | about 45 min (unattended) | |
| QA, publish kit, hooks | 20 min | listen: 15 min |
| Check-ins after publishing | 5 min each | 5 min each |

## Costs and licenses (as of Nov 2026)
- ElevenLabs TTS v3/v4: about 1 credit per character. A 5-minute script is about 4,300 to 4,400 characters per language.
- ElevenLabs Music Marketplace: 7,500 credits per track for the Social Media license. The original engine score costs nothing and carries no Content ID risk.
- Pexels: free, commercial use allowed, no attribution required (credit anyway). Not allowed: implying endorsement by people shown, or showing identifiable people in a bad light.
- Wikimedia Commons: per file. Public domain or CC BY is easiest. CC BY-SA needs credit and raises a ShareAlike question.
- Fonts: Oswald, Inter, Noto Sans Bengali (SIL OFL).

## Known traps
| Trap | Fix |
|---|---|
| Remotion's bundled headless Chrome crashes (GPU) | studio.sh renders through installed Chrome; run outside the sandbox |
| Whisper skips or garbles Bangla | `align_lang.py` pause fitting; check its long-pause score |
| Captions show over title or quote cards | built in: captions never cross a gap |
| Bangla letters pulled apart | no letter-spacing on Bangla text; Noto Sans Bengali fallback in TITLE and BODY |
| Wikimedia 429 Too Many Requests | the scripts batch requests and retry |
| A clip's thumbnail lies | read the title, and check frames of the render |
| Bangla runs about 15% longer | the Short drops segments in `drop_order` automatically |
| A shot holds longer than 6 s | the build prints it; split it or add a graphic |
| English-only (or Bangla-only) film | list only that language in `project.json` `languages`. Keep `remotion/src/timeline_bn.json` and `short_bn.json` as placeholders (Root.tsx imports them); docs and upload skip unused languages |
| The voice file is in a different language than its name says | check the downloaded file with Whisper before filing it (the Japan film's English take was first filed as Bangla) |
| `align_lang.py` fails with no `vo_words_en.json` | other languages are timed against the English alignment: run the English align first, or make the film English only |
| A graphic shows a number before the narration says it | give `rank` steps an `at` (seconds into the shot); check stills at each step |
| Commons photos credited as "illustrative" | set `place` on every shot that shows a real named place: it marks the photo as real in the credits and tracker |
| A win is copied by its title alone | Note the structure, delivery and editing too, and study flops; one viral video is a signal, not a cause |
| The description runs over YouTube's 5,000 characters | the credits belong in the description only, so set `credits_public_domain_summary` in `project.json` to name public domain sources in one line. Never add a credits comment |
| A render hangs with no error and no file | Chrome died, usually from low disk or other Remotion jobs. `./studio.sh render` now has a watchdog. Free space and rerun |
| New clips 404 at render ("clip_X.mp4") | the build was cut off before trimming. Never pipe `./studio.sh build` to `head`. Rerun it in full |
| A tall portrait crops to legs or a torso | check a frame of every photo. Crop a 16:9 file with the face, pick it as `file:path`, and give it `local_assets` with credit, creator, license, page, title and place |
| Long names run off a stat card | keep the `value` to about 15 characters, and put the name in `label` |
| "missing media" black card in a render | a reuse of a graphic. The build now copies the graphic, and QA fails on any shot with no picture |
| Align fails with a whisper error | the speech model was removed by a disk cleanup. Run `setup.sh --install` |
| Commons has a place with the right name but the wrong location | read the description and coordinates. "Tar Creek" photos were from California, not Oklahoma |
| Chrome is on the producer's other channel | confirm [your channel handle] in Studio before any upload. Chrome can default to the main [your voice clone] channel, so switch, and tell the producer you switched |
| The film is over 10 MB, so browser tools cannot upload it | open the upload box, reveal the file with `open -R`, and ask the producer to drag it. Then find the draft in the content list, because it may be in another tab |
| A film folder is about to be deleted to free disk | warn first: git holds no video, voice or music. Uncommitted edits die with the folder. ElevenLabs files stay in ~/Downloads and in the site's history |
| ElevenLabs API says "key ID used as API key" | the real secret starts with `sk_` and is shown when the key is created or rotated |
