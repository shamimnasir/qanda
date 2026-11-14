# Script and Retention Guide

## The hook (always, with the twist in about the first 10 seconds)
The producer's standing rule (7 Nov 2026), replacing the 6 Nov rule of 5 to 7 hard cuts of facts in 0 to 6 s. On the St. Francis film the producer found those cuts too fast and agreed the 6 second rule does not suit documentaries. Too many facts flashed past, the text said something different from the voice, and a real death toll going by like a trailer felt wrong. The 5-line opener of Situation, Desire, Conflict, Change and Result stays dropped, because the producer called it "dull and boring". Whether the slower hook lifts retention is untested, so compare the first 30 s with the fast hook on the live Picher film.

How to make it work:
- **Start at once.** The first word comes at the start, on a strong real picture at frame 0. No greeting, no slow build.
- **Voice: one to three full, natural sentences that state the twist, in about 10 s.** A complete thought sounds alive, where clipped fragments sound dull. St. Francis: "The St. Francis Dam was leaking muddy water. Its famous builder checked it, and went home. By midnight, it was gone."
- **Picture: 3 or 4 shots of about 2 to 3 s, cut on the voice, each showing what the voice says.** The 3 s limit still holds. The build warns about a hook shot under 1.5 s.
- **Text: only where it adds something, in a few words that support the voice.** One well-chosen fact is enough, such as "11:58 PM". Never run a different story in text. A fact on screen must be delivered later and be on the fact list.
- **Motion and sound: calm until the turn.** Hook shots keep a slow push and get a light swish and tap on the cut. Mark the turn with `"hit": true` in the shotlist for one soft impact: a short blur, a small shake, a soft flash, text that lands with a wiping bar, and a fuller hit. Producer's notes on 7 Nov 2026: cuts with no motion or sound looked "unnatural", and whips and hits on every fast cut were still too fast. A low thump alone does not reach phone and laptop speakers, so check the hit above 250 Hz. `sound_design.opener_hit` scales the sound. Look at the frames, and the producer checks the sound by ear.
- **Respect real tragedy.** Do not flash a death toll past for excitement. Let the voice say it, on a picture that holds.
- **Set up:** `project.json` -> `"opener": {"to": "last words of the opening lines"}`. The engine then starts the first word at once, plays the `flash` music until `to` and prints a hook check.
- **Then give a reason to stay:** the next line opens the how or why, then Promise, Proof and Plan by 0:30. The music drops back like a door opening onto the story.
- **Delivery:** keep the producer's natural clone read. `[urgent]` takes sounded unnatural and were rejected. See `references/elevenlabs_tagging_guide.md`.

Honesty:
- Every word on screen goes in `facts_to_verify.md`. A claim from one report keeps its attribution in the film, such as "NPR, 2007".
- No fake drama. For a serious topic such as death, illness or disaster, excitement comes from tension and pace, not a cheerful tone.

No source here proves this format raises retention. After each film, compare the first 30 s with the channel's other films in `./studio.sh review`.

## Four ways a hook fails (check every hook, film and Short)
A hook must give **topic clarity**, so viewers know what this is, and **targeted curiosity**, so they believe it is for them and want the answer.
1. **Delay.** The topic arrives late. "This is one of the craziest things I've ever seen" tells them nothing. Name the topic in the first sentence or first few seconds.
2. **Confusion.** Hard to take in at once. Use fewer words, about a sixth-grade reading level and direct, active sentences. Read it alone and ask whether it could be misunderstood.
3. **Irrelevance.** Clear, but not about the viewer. Frame it around what they care about or already wonder: "If you have ever driven past a town and wondered why it is empty..." Use "you" only when it is honestly about the viewer.
4. **Disinterest.** Clear and relevant, but no reason to stay. Open a loop with **contrast**: what people assume against what is true. It can be stated, or implied when the viewer already knows the usual view.

**A strong structure:** sentence 1 gives the topic, sentence 2 gives the contrast. Picher does the contrast well: "An EF4 tornado tore through this town. But that tornado isn't what killed this town." Its weak spot is that the first line says "this town", not the name. For a searched place, try saying the name early.

The contrast must be true and delivered in the film. Never exaggerate to build one, such as an unsupported "three times faster".

## Find the story within the story (decide this before the script)
A broad subject is only a starting point. Viewers connect with people more readily than with issues or statistics, and following one person's stakes helps them feel the bigger issue. For every film, look for:
- **A central person** connected to the subject. If no one is documented well enough, use a family or a small group, or follow the place as the character, and say at Gate 1 that the film has no single main person.
- **A clear conflict:** what stands in their way.
- **Meaningful stakes:** what they could lose.
- **Change:** how they, or our understanding of them, shift by the end. It can be subtle.

Four ways to find it:
1. **Follow emotion as well as facts.** In your research, note the moments that hit hardest. They are often the best way in.
2. **Look for contradictions.** Unexpected combinations stick. Picher's principal called the toxic waste piles "our friends".
3. **Choose someone capable of change,** and show the turn only if sources record it.
4. **Keep the focus narrow.** Leave out what does not serve this thread, and keep the viewer wondering what happens next. The facts that remain must still be fair, so never cut one that would change the conclusion.

Return to this person at the start, middle and end, so the broad facts hang on a thread the viewer cares about. A film can use the hook's facts first, then enter through the person.

**Honesty and care:**
- The person must be real, and their story sourced. No composite characters or invented people. Never imply they stand for more people than the evidence supports.
- One story is an example, not proof. Give the wider numbers as well, so a single case does not mislead.
- Do not change their words or the order of events to build a neater arc. If no change is documented, do not claim one.
- For private people, use what they shared publicly or through reporting. Take special care with children, illness and grief. Do not name or expose more than the story needs, and raise any doubt with the producer at Gate 1.

## Show the change: objects, payoffs, color and silence
Learned from a near-wordless animated film the producer admired (7 Nov 2026). It tells its story mostly through things changing, and its alarm, calendar and shop all change meaning by the end.
- **A tracking object.** Find one real object or number that changes across the film, and return to it at least three times, so the viewer sees the story move. Picher could use the population count or the water tower. Plan it in the shotlist.
- **Setup and payoff.** Show or say something early that matters later: a sign, a date, a place, a line. Before Gate 1, list each setup and the time of its payoff. A setup with no payoff gets cut.
- **Show the failure or turn without words where a real picture can.** A real before and after, a date passing or a document can say more than a sentence. In a documentary, the picture must be real or plainly generic.
- **Return to where it began.** End in the same place or on the same question, now changed. This strengthens the callback ending.
- **Color arc.** Plan how the film's colors move with the story, then set `"tone"` (`gray`, `cool`, `night`, `warm` or `vivid`) on shots. Picher's arc might run from warm boomtown photos to gray. Tone is a mood treatment: never use it to fake a date, season or place, and keep real archive images recognizable.
- **Hold for one big moment.** The 3 s limit stays. With the producer's approval at Gate 1, one or two big emotional moments can run longer with `"hold": true` on the shot. The build lists them, so none slip through.

This film was fiction, so its characters could be made up. Documentary rules do not change: no invented people, scenes or events.

## Zoom in on one moment (at least 2 or 3 scenes per film)
Summaries keep the viewer at a distance. Facts earn trust, but a scene makes them care. Pick the moments that carry the most feeling, often where a chapter turns, and bring the viewer into each one, using as many of these five as the sources support:
1. **Place and time.** Say where we are and when, in a few words: "In February 2008, the EPA signed the plan." Skip scenery that does not matter.
2. **Specific actions.** Say who did what, with clear, active verbs, and get moving. Avoid long background first.
3. **Thoughts.** Real thoughts make a story feel human. Use them only when a person said them in a source, or when they are the producer's own true experience. Otherwise, ask the question the viewer is thinking: "So why stay?"
4. **Emotion through behavior.** Show what people did instead of naming the feeling. Only use a physical detail a source records. Without one, let the facts carry the emotion, because a stated fact can land harder than a claimed feeling.
5. **Dialogue.** Use the exact, short, memorable words people said, on a quote card with the speaker named, never in the AI voice.

**Never invent any of it.** A made-up thought, gesture or line of dialogue about a real person is a fabrication, however natural it sounds. Every scene detail goes in `facts_to_verify.md` with its source. Do not write "she must have felt". If a scene is imagined, for example "Imagine you are a parent here", the narration must say so plainly and it must be about the viewer, not a real person.

A sourced example, from Picher: "Vicky Phillips stood on the empty lot where the family home used to be." Then the quote card: "We didn't want to move." That line has a place, an action and her real words, with nothing added.

Check each scene: can the viewer picture where they are and what is happening? Does one specific moment replace a broad summary? Can every detail be traced to a source?

## Storytelling techniques (always apply, in this order of work)
These are standing rules from the producer. Check every script against them before Gate 1.

1. **Write the ending first.** Decide the last line and the takeaway before anything else, then work backward to the conflicts and setup that earn it. A strong ending is memorable, worth sharing, and ideally loops back to the opening.
2. **Pick a story lens.** A topic alone is not enough, because anyone can cover it. Choose the angle others are not taking and state it in one line (Oymyakon: standing still can kill you. Fix Your Life: a viral promise put on trial). The same topic through a fresh lens is a different film.
3. **Dance between context and conflict.** Alternate: context (who, what, the goal), then conflict (a problem or an unexpected turn). Each conflict opens a question the viewer wants answered. When one resolves, the next must arise.
4. **Connect beats with "therefore" and "but", never "and then".** This is the Matt Stone and Trey Parker test: each event must cause the next. Read the beats aloud with those words between them. If "and then" fits, the beat is a list, so rebuild it so that each step solves the problem the last one left.
5. **Vary the sentence rhythm.** Mix short lines for emphasis, medium lines for explanation, and longer lines for detail or buildup. Put each sentence on its own line: if they all end at about the same point, rewrite. In script_master.tsv every row is one sentence, so check the spread of lengths. Avoid long runs of very short sentences as well, because staccato gets monotonous too.
6. **Talk to one person.** Write as if speaking to a close friend: "you", plain words, questions, "try this with me". It should not feel like a lecture or a pitch. This also applies to Bangla: চলিত ভাষা, written to be spoken. Keep the honesty limits, but say them in spoken words.
7. **Hook with sound and picture together (show and tell).** The hook does this. The first spoken line says immediately what the video is about, in words that match the title, while the pictures show how much is coming.
8. **Promise, Proof, Plan in the first 30 s, right after the opener.** After clicking, the viewer needs three answers. Promise: restate what they clicked for, in the words of the title and thumbnail. Proof: why trust this film, using something real, such as the study, the method or the producer's true experience. Never invent a credential, and do not imply the AI voice is an expert. Plan: one spoken line on what the film will cover. Reveal the route, and keep back how and why, so the open loop stays open even though the opener stated the result. Weave these into the story without a greeting or a list of contents.
9. **Deliver what the promise said.** Read the demand brief's promise before writing and again after. Everything in the film should serve it. If the title promises a method, the viewer gets the method, not a summary of one. If the facts do not support the promise, change the promise.
10. **A next step only where it helps.** If the film's next step belongs in the narration, place it after the film has raised the problem it solves, or in the close, never in the first 30 s. It should sound like more help, not an advert.

### Check before Gate 1
- [ ] Checked against `references/viral_style_guide.md`: sounds like a curious person, each answer opens the next question, filler cut
- [ ] Last line written first, and it pays off the opening
- [ ] Story lens stated in one line
- [ ] Every beat joins the next with "therefore" or "but"
- [ ] A new conflict or question at least every 45 s
- [ ] Sentence lengths clearly vary
- [ ] Reads like talking to one friend
- [ ] The first line names the topic, and the first picture shows it
- [ ] Central person, conflict, stakes and change are stated in the demand brief, or the brief says why the film has none
- [ ] A tracking object appears at least 3 times, and each setup has a payoff
- [ ] At least 2 or 3 scenes zoom in on one moment, and every place, action, thought, behavior and quote in them is sourced
- [ ] The hook: one to three full spoken sentences with the twist in about 10 s, over 3 or 4 shots that show what the voice says
- [ ] The next line gives a reason to stay: the opener reveals what happened, and the film keeps back how and why
- [ ] Promise, Proof and Plan are all clear by 0:30
- [ ] The film delivers the promise in the demand brief
- [ ] Any spoken next step is natural, truthful and after 0:30

## Length math
- English narration: 130 to 150 words per minute with pauses. 5 minutes is about 650 to 780 words.
- Bangla takes about 15% more time for the same content.
- Add about 15 to 25 s for the title card, quote cards and chapter breathers.

## Skeleton (5 minutes)
| Time | Beat | Job |
|---|---|---|
| 0:00 to 0:10 | The hook | One to three full spoken sentences with the twist, 3 or 4 shots that follow the voice, little text, one soft hit on the turn |
| 0:05 to 0:25 | Cold open | The topic in the first line and the first picture, then the strongest image (no greeting, no logo). Promise, Proof and Plan by 0:30. End on an open loop: "by the end you'll understand why..." |
| 0:25 | Title card | 3 s, over a real photo of the place |
| 0:28 to 1:00 | Journey / setup | Map, numbers, arrival moment |
| every 30 to 40 s | Chapter | Each opens with a concrete image and closes with a question or a turn |
| about every 45 s | Question hook | "Why?" / "And if the skin turns black?" / "That sound?" |
| 3:45 to 4:30 | Payoff | Answer the cold open's loop. Callback to the opening image ("Remember the wolf?") |
| last 25 s | Close | Turn from fear to meaning. Warm music, slow last line, location card |

## Line craft
- One idea per sentence. Short sentences at moments of tension.
- Specific beats vague: "Fifteen minutes." beats "very quickly".
- Every number goes in facts_to_verify.md, and the math gets checked.
- Quotes from real people go on quote cards, never in an AI voice.
- First person ("we arrived") is only for footage you filmed. Otherwise say "one crew", or credit the source.

## Visual rhythm
- Decide what each shot shows or proves before searching. Change the picture when the idea changes, and never let stock become wallpaper (`references/viral_style_guide.md`).
- No visual longer than 3 s, about 130 shots for 5 minutes. Graphics carry numbers. Real photos carry "this is the place". Stock carries energy, so look for exciting pictures rather than calm wallpaper.
- Never let a clip contradict its line. No "ILLUSTRATIVE FOOTAGE" text on screen and no credits card: stock is disclosed in the description. So stock never sits under a line about one specific real event or place, see `references/rules.md`.
- Editing should clarify or carry feeling, not add movement for its own sake. A visual that is explaining something may hold longer, up to the 6 s limit in the build check, or be split into steps.

## Shorts
- Follow the Shorts and Reels guide (`references/shorts_guide.md`): its own story with a visual first frame, a clear expectation, cause and effect, and a payoff. Fill `short.brief` and write the ending first. Under 60 s, using only the length the story needs. A header on screen from frame 0, and an ending that loops into the first shot when it can.
- Hooks: use the viral-hook-generator skill for 10 options per language, then A/B test two.
