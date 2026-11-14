# Producer profile and defaults (template)

Copy this file for each creator and fill it in. These are defaults: anything the producer says in a brief wins.

## About the producer
- Channel name and language(s): [fill in]
- Audience: [fill in, for example Bangladeshi and English-speaking viewers]
- Typical film: retention-focused, about 5 minutes, plus a 60 s vertical Short and a Facebook post
- Comfort with code: [fill in; if not a coder, give finished files, short explanations and folder locations]
- Language review: [who has the final call on Bangla wording; use natural Bangladeshi usage]
- Working style: [fast "do it all" or careful, step by step]; always keep the 3 gates

## Voices (ElevenLabs)
- Bangla voice: [your voice or clone name]
- English voice: [library voice or your clone]
- Model: Eleven v4 or v3. Check the downloaded filename: it shows the real model and stability.
- Plan and renewal date: [fill in]. Check your plan's terms before using generated music or distributing audio.
- Claude cannot save ElevenLabs downloads through the Chrome extension: click Download yourself. To paste a script, copy it with `LANG=en_US.UTF-8 pbcopy` outside the sandbox, or Bangla turns into garbage.

## Channel decisions
They live in `_Channel/channel_strategy.md`. If it says NOT SET, ask once. Do not guess the audience, themes or offer.

## Looks
Set `"look"` in `project.json`: `"cold"` (blue grade, falling snow), `"warm"` (amber grade, drifting dust) or `"dusk"`. Pick the one that fits the place, or add a new look in `remotion/src/theme.ts`.

## Sound defaults
- Original score, shape only: dread open, driving middle, climbs into hits, a short silence before key lines, a warm close. Follow `references/music_guide.md` and never reuse a sound.
- Music level about 0.65 with duck depth 0.5; film master about -14 to -16 LUFS.
- One signature sound effect tied to the story, plus impacts on reveals.

## Edit defaults
- The twist in about 10 s over 3 or 4 shots that follow the voice; no visual over 3 s; exciting pictures.
- No "ILLUSTRATIVE FOOTAGE" text and no credits card. Credits in one place, the description.
- Energy comes from pace, cuts and music, not from forced voice delivery tags.

## Packaging
Follow `references/packaging.md`: 3 titles each for the film and the Short, every one with a virality score; 2 to 4 film thumbnails and 1 or 2 vertical Short covers. Gather the files in `10_Ready_to_Upload/` as plain text files to copy and paste.
