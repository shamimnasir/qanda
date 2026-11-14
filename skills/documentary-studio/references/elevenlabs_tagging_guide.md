# ElevenLabs Tagging Guide (English and Bangla)

Model: Eleven v4 (or v3). Tags go in [square brackets] in the `tags` column of script_master.tsv. SSML `<break>` tags do not work on v3/v4.

## How the narration stays human, not AI
- Tag only about 1 line in 3. Plain lines carry the information; tags mark the turns: reveal, danger, wonder, callback.
- Never more than 2 tags together, and never two that conflict ([whispers] with [excited]).
- Pace comes from punctuation: an ellipsis is a breath, a line break is a beat, a blank line is a paragraph pause.
- Short punchy sentences create excitement better than [excited] does: "Eighteen hours. Nine hundred kilometers."
- Avoid [whispers], [laughs] and [excited] on narrator voices. They read as gimmicky or like an advert.
- Never tag sound effects ([wind], [explosion]). Sound design is added in the edit, where it can be controlled.
- End each paragraph on an ellipsis or a pause so the last word is not clipped.

## Tag set that works for documentary narration
| Feel | Tags |
|---|---|
| Low, ominous | [quietly] [low voice] [hushed] [slowly] |
| Tension | [tense] [serious] [grave] [measured] |
| Rise | [building intensity] |
| Wonder, warmth | [in awe] [softly] [warmly] [gently] |
| Question hooks | [curious] |
| Human texture | [exhales] (once or twice per film) |
| Timing | [short pause] [long pause] |

## Chapter arc
Calm (plain) -> turn (one tag) -> beat (pause) -> next chapter. Energy should rise and fall, not stay flat.

## Bangla specifics
- Native Bangla, written to be spoken: চলিত ভাষা, Bangladeshi usage (পানি, গোসল), short sentences.
- Numbers as words: "মাইনাস সাড়ে ষাট", "রাত দুটোয়", "প্রায় আটশো".
- Keep the tags in English; v4 understands them for Bangla text.
- If a name is mispronounced, regenerate that line with a hyphenated respelling (Oy-myah-KON).
- Bangla runs about 15% longer than English, so the film and the Short get longer too.
- Voice: "[your voice clone]" (the user's own clone). Language: Auto (Recommended).

## Generation checklist
1. Check the balance: cost is about 1 credit per character (studio.sh scripts prints it).
2. Voice, model and stability: confirm them in the downloaded filename (`..._s50_..._v4.mp3`).
3. Pick the better take if two are generated. Download, then rename to the file name in project.json.

## The producer's clone
Avoid `[urgent]` on "[your voice clone]": on Picher (6 Nov 2026) it sounded unnatural and the producer chose the plain take. If a line lacks energy, make the sentence more direct, generate plain takes, and let the cuts and music lift it. Each Generate makes 2 takes and is charged once.
