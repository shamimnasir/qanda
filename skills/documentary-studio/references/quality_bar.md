# Quality Bar (check before Gate 3)

## Picture
- [ ] No visual over 3 s (the build prints a shot check), and the pictures are exciting
- [ ] Cohesive grade: cold tint on cold scenes, warm in the close, vignette on footage
- [ ] Cross-fades of about 8 frames; hard cuts only on hits
- [ ] No clip contradicts its line (2 frames per stock shot checked in the final render)
- [ ] Real-location photos carry an on-screen credit with the place name
- [ ] Graphics: nothing touches the frame edges, and no caption sits on top of a graphic's text (check the vertical Short too: wide graphics are scaled into a band and can crop)
- [ ] Each number on a graphic appears when the narration says it (use `at` on `rank` steps)

## Captions
- [ ] One line, phrase-level breaks, never shown over the title or quote cards
- [ ] Bangla shapes correctly (conjuncts, no letter-spacing)
- [ ] SRT per language matches the burned-in captions

## Sound
- [ ] Film about -14 to -16 LUFS integrated, true peak at or below -1.5 dB. Short about -14 LUFS
- [ ] Music ducks under the voice and rises between lines; a drop of silence before the key hits
- [ ] Music follows `references/music_guide.md`: soft, unique to this film, matched to its vibe and pace, real ups and lows. No score WARNING. The producer has heard a mix
- [ ] Pronunciation of names checked by ear (the user)

- [ ] Read the Music Story Arc: enough contrast, a strong opening, at least one moment considered for silence

## Honesty and rights
- [ ] Every asset in tracker.csv with a license; no "unclear"
- [ ] AI voice disclosed in the description, and YouTube's AI use question set to Yes
- [ ] No "ILLUSTRATIVE FOOTAGE" text and no credits card. Illustrative-footage line in the description. No stock under a line about one specific real event or place
- [ ] facts_to_verify.md reviewed; no unprovable superlatives in titles
- [ ] No long dash characters anywhere (qa_check.py)
- [ ] Credits in one place, the description, with no credits pinned comment. Real photos of named places listed as real, illustrative ones as illustrative

## Promise match
- [ ] Watch the title, the thumbnail and the first 30 s together: same promise, and Promise, Proof and Plan are clear
- [ ] The film delivers everything the title and thumbnail promise
- [ ] Each graphic and cut helps understanding or feeling; none is movement for its own sake

## Packaging (see references/packaging.md)
- [ ] 3 film thumbnails (2 to 4) from moments inside the film, 0 to 3 words, none repeating the recommended title; all readable in phone_size_check.jpg
- [ ] 1 or 2 vertical Short covers, plus a fallback frame time
- [ ] 3 titles each for the film and the Short, scored, one recommended, at or under about 60 characters, none ending in a question
- [ ] No thumbnail or title rests on a CHECK fact or implies a stock person is a real subject
- [ ] Description at or under 5,000 characters (the upload step checks), with "Not medical advice" on health topics
- [ ] One-glance test passed, and at least one thumbnail shows the promise plainly
- [ ] One next step chosen, truthful and ready: the resource exists, paid links are disclosed, and the end screen is decided
- [ ] Demand level stated, and any B or C level or channel fit flag reported to the producer
- [ ] `./studio.sh upload` ran with no WARNING, and the report points the producer to 10_Ready_to_Upload/ first

## Style check
- [ ] Went through `references/viral_style_guide.md`, and read the `Style:` lines from `./studio.sh qa`

## Shorts and Reels
- [ ] Follows `references/shorts_guide.md`, with `short.brief` filled and no unresolved Short check
- [ ] Frame 0 is clear at phone size with the sound off, matches the title and cover, and the first word comes at once
- [ ] An early line sets the expectation, and the ending pays it off
- [ ] Each beat causes the next, in simple accurate words, with no wasted seconds
- [ ] The last 3 seconds end cleanly (the producer checks by ear)
- [ ] A line in the publish kit for each platform used

## Hook
- [ ] Passes the four checks: no delay, no confusion, relevant to the viewer, and a true contrast or open loop
- [ ] The twist is stated in about 10 s, over 3 or 4 shots of about 2 to 3 s that show what the voice says, starting on a strong picture at frame 0
- [ ] Text in the hook supports the voice and never tells a different story. One soft hit on the turn, which reaches phone speakers (at least about 4 dB above the sound just before, above 250 Hz)
- [ ] One or two full, natural spoken sentences stating the twist, with no fragment lines
- [ ] Every fact on screen is on the fact list and delivered later in the film
- [ ] Exciting music through the hook, then a clear drop back

## Render check
- [ ] Look at one frame of every shot in the final render, including graphics, not only the stock. QA now fails on "missing media", but other faults only show to the eye
- [ ] Counters land on the right number before the cut

## Sound and cuts
- [ ] Score check: stereo correlation 0.5 to 0.9, harshness under the limit, real ups and lows
- [ ] Pause check: no stretch over about 30 s without a pause of 1 s or more
- [ ] Sound design is present but never busy. The producer judges this by ear
- [ ] `cut_style` is `hard` unless the producer asked for fades

## Scenes
- [ ] A tracking object returns at least 3 times, and each setup has a payoff
- [ ] The film has a planned color arc and 2 or 3 real drops in the sound
- [ ] Any `hold` past 3 s was approved by the producer
- [ ] The film follows a central person or group from start to end, or Gate 1 recorded why not
- [ ] One story is not presented as proof: the wider numbers are in the film
- [ ] Care taken with private people, children, illness and grief
- [ ] At least 2 or 3 moments are told as scenes, not summaries
- [ ] No invented thought, feeling, gesture or dialogue about a real person
