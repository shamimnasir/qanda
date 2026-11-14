# Music guide

The producer's standing rule (Nov 2026): the old music sounded harsh. Every film gets its own unique background music that matches the exact vibe and pace of that video, with real ups and lows. The narration always comes first.

`build_score.py` does this. It runs with `./studio.sh sound`, needs no samples and no credits, and carries no third-party rights.

## The rules
1. **Never harsh.** Warm, soft instruments only. No sawtooth buzz, metallic braams, white noise risers, trembling high notes or minor-second clusters. Nothing is synthesized above about 3.4 kHz, and a soft tilt removes the rest.
2. **Unique to the film.** Key, scale, chord progression, instruments, tempo and motif come from the film's slug. `_Channel/score_ledger.json` records every film, and a clash picks another sound. Never reuse one film's score on another.
3. **Matches the pace.** Tempo comes from the narration's words per second. The energy curve comes from the sections, the narration density and the cut rate. Chord changes land on cuts where possible.
4. **Real ups and lows.** Choose sections that climb and fall with the story. Hits get a slow climb, a short silence, then a low bloom. Every film should have clear quiet moments and clear peaks.
5. **Serves the voice.** Melody answers at sentence ends and in pauses, not over the words. Middle-layer notes step back during a line, and the music lifts as a sentence lands. Ducking in `build_audio.py` still applies.

## Exciting opener
Every new film's hook gets the mood `flash`, added automatically from `project.json` -> `opener`: music at full level from frame 0, a fast soft beat, a chord on each hard cut and a low hit on each cut. Exciting comes from pace and energy, and rule 1 still applies, so it is never harsh. Plan the next section lower, so the contrast feels like a door opening.

## How to plan a score
Fill `project.json` -> `score` after reading the script, section by section:
- Name what the viewer should feel, then choose the mood. Do not paste another film's plan.
- `mode`: `minor` for a serious or questioning film, `major` for a bright one. Key is chosen for you, so leave `key` out. Use `keep_key` only for a reason, and a clash with another film still changes the sound.
- Give a section a `level` under 1 to pull it back, so the peaks have room.
- Use few hits, about 5 to 8 in 5 minutes, only on lines that deserve one. Use `size` 0.4 to 0.9.
- `variation: 2` (then 3 and so on) re-rolls the film's sound if the producer does not like it.

| Mood | Feels like | Energy |
|---|---|---|
| `flash` | The opener: fast, driving, full energy. Automatic | highest |
| `hush` | A held breath, a soft pad alone | very low |
| `dread` | Low drone, slow soft pulse | low |
| `tension` | Slow notes over dark chords | medium low |
| `suspense` | A low repeated note, moving chords | medium |
| `curious` | Gentle walking notes | medium |
| `pulse` | Steady soft eighth notes | medium high |
| `light` | Brighter chords, walking notes | medium high |
| `warm` | Bright chords, the motif sings, a resolution | medium |
| `drive` | Walking notes and a soft low beat | high |
| `awe` | Wide, bright, open chords | high |
| `silence` | Nothing | none |

## One-page map
Each run writes `07_Music_SFX/music_story_arc.md`, listing each section's time, mood, energy and feel, plus the hits. Add `"feel"` to each section in the plan. Read the map to spot too much music, too little contrast, or an empty opening.

## Checks
Each run prints the film's sound and two measurements:
- **2 to 6 kHz share at the harshest moments:** the limit is 6%. The old engine measured about 47% on Fix Your Life.
- **Loud to quiet range:** want 8 to 18 dB. Below that the music is flat, and above it quiet parts may vanish under the voice.

Fix every WARNING. These numbers and the waveform cannot judge taste, and Claude cannot listen. Before Gate 3, give the producer a mix to hear, say plainly it was not checked by ear, and adjust with what they say: `variation` for a different sound, moods and levels for the shape, `music_level` for the balance.

## Stereo, detail and space (added 7 Nov 2026)
Measuring a successful narrated video against Picher showed where our sound was thinner. These are defaults now, and the score must still never be harsh.
- **Stereo.** The score is stereo, with the bass and voice centered. It adds a second room and a short delay only in the side signal, so it still sums cleanly to mono. The score check prints the correlation, which should be 0.5 to 0.9. `score.width` adjusts it.
- **Detail.** Partials now reach 5 kHz, and the tilt keeps some air up to about 9 kHz. `score.brightness` set to 0 returns the older, darker sound. The harshness check still applies, with its 6% limit.
- **Give the music moments alone.** Narration wall to wall leaves nowhere to hear it. Aim for a pause of 1 s or more at least every 30 s. Add a shot with `"after": N` and `"dur": 1.2`: a strong picture, and usually a hit or riser. The score already lifts in every gap. The build prints a pause check with sentence ends to try. Pauses use the voice already recorded, so they cost no credits.
- **Sound design.** `project.json` -> `"sound_design": {"level": 1.0, "swish_every": 3}` adds a soft thud on graphics and on-screen text, and a soft stereo swish on every third cut. For big reveals, add `riser`, `thud` or `impact` in `sfx`. Level 0 switches the automatic sounds off. If they ever feel busy, lower the level before removing any.
- **Voice.** `"voice_presence_db": 2.0` gently lifts around 4 kHz. Set 0 if the voice sounds thin or sharp.

Nothing here can listen. These numbers show differences, not whether it sounds good, so the producer always checks by ear at Gate 3.

## Real silence (added 7 Nov 2026)
That wordless film's loudness range was about 13 LU, against about 3.8 for Picher, and its sound level dropped sharply after its busy first minute. Sound stays interesting when it can fall away.
- Plan at least 2 or 3 real drops per film with `score.drops` or the `silence` mood, usually just before or after a big reveal or quote.
- A drop only works in a pause, so pair it with the pause check.
- `qa_check.py` prints the film's loudness range. Narrated films will measure lower than a wordless film, so use the number to compare and do not chase 13. The narration must stay easy to hear, and the producer judges this by ear.
