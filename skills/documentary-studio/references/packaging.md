# Packaging: thumbnails and titles

The producer's standing rule: every film gets 2 to 4 eye-catching, click-driven thumbnails with minimal text, built from a moment inside the video (never the title copied onto the image), and a few titles per video (film and Short), each with a virality score. Research gathered on 4 Nov 2026; sources at the end. Most of it is observational, from tool vendors: treat it as patterns that amplify a good idea, not proof.

## What the research says
- Packaging decides the click. Paddy Galloway (strategist for MrBeast and others): a thumbnail is "80, maybe 90% the psychology of the click", only a little design.
- The title and thumbnail are one idea told twice, never repeated. The title carries the topic (YouTube reads it; it does not read thumbnail text), and the thumbnail carries the hook or emotion. Ask: what does the thumbnail say that the title does not? In one study of about 16,000 videos with over a million views, 75% of thumbnails with text did not repeat the title.
- Less text. In vidIQ's 500 breakout thumbnails (2026), 140 had no text and 120 had 1 to 3 words; the numbers drop as the word count rises. Aim for 0 to 3 words, never more than 4.
- One idea, one focal point, readable in under a second at about 160 px wide (over 70% of viewing is on phones). Strong contrast: two contrasting colours plus one base, text contrast at least 4.5:1.
- Faces with emotion are common on breakout thumbnails (69% overall, 80% of the biggest). So the producer's own face goes on the thumbnails by default (standing request, Nov 2026). Never imply a stock person is the real subject.
- The promise must be in the video (MrBeast production guide): the thumbnail sets an expectation the video has to meet, or retention drops and YouTube stops showing it. YouTube's Test & Compare tests up to 3 thumbnails and picks the winner by watch time, not clicks.
- Titles: specific story promises win. vidIQ's 2026 study of over 4 million videos, frames against the average (1.0x): caught on camera over 4x; turning X into Y over 3x; nobody knows over 2.5x; inside X 2.5x; age or tenure over 2x; banned or forbidden over 2x; do not, stop or never nearly 2x; how X did a surprising thing nearly 2x; a specific superlative over 1.5x; X days, hours or years nearly 1.5x. Titles ending in a question did 0.82x; "I was wrong" under 0.5x; a plain how-to 1.07x.
- Familiar but unexpected (Galloway): a known format with a twist. Intriguing and concrete beats vague: Veritasium's "Why Are 96,000,000 Black Balls on This Reservoir?"
- Clear promise (Jake Trinder, one practitioner's view): the title and thumbnail should make the result or problem clear at once, in words the audience already uses, matched to what motivates them. The same format can work in one niche and fail in another, so learn why it worked instead of copying its wording.
- Keep titles at or under about 60 characters so they are not cut off on phones (100 is the hard limit).

## Thumbnail rules for every film
1. Make 3 for the film (the most Test & Compare can test), 4 at most, each a different click reason: shock or twist, a rule to try, a mystery word or object, a before and after.
2. Build each one from a moment that is in the film, named with its time in the publish kit. Use licensed source media for the background (the shot's original clip or photo, not a render frame with burned-in captions).
3. 0 to 3 big words, plus at most a small 1 to 2 word label when needed for honesty (for example "OKINAWAN MEN" so a rank is not read as the whole island). The words must not repeat the recommended title.
4. Pass the 50% TV test. YouTube on a TV often shows only the top of a recommended video, so cover the lower half and ask: is the subject still clear, can a viewer roughly tell the topic, and is there a reason to scroll down? `./studio.sh thumbs` writes `tv_half_check.jpg` for this. Put the face's eyes and the main words in the top half, and stay away from the bottom-right corner, where YouTube shows the video length.
5. Real-place photos keep their credit line on the image. CC BY-SA photos carry the ShareAlike flag.
6. Never present a stock person as a real subject, and never promise what the film does not show.
7. Check `phone_size_check.jpg`. If a thumbnail does not read at 160 px, simplify it.
8. For the Short, make 1 or 2 vertical covers (1080x1920) from moments in the Short, and name a fallback frame (custom Short covers are desktop-only and still rolling out).
9. Use a big human face, but it does not have to be the producer's (6 Nov 2026). Choose per thumbnail: the producer's cutout (table in `05_Motion_Graphics/producer/README.md`), or a **made-up man or woman related to the film**, such as a miner, a mother or a scientist. For a made-up person: generate them with an AI image tool (state the credit cost first and ask), cut them out with `./studio.sh cutout in.jpg out.png`, keep them in `05_Motion_Graphics/people/` and use the path as `{"face": ...}`. Log them in `tracker_extra` as AI generated with the tool's license, and add "The person on the thumbnail is an AI illustration" to the description. Never make them look like a real named person, and never caption them as one. Whichever you use: big face, eyes in the upper half and clear of the text, soft dark background, a coloured rim light, and an expression that matches the words.
10. Start from the demand brief. Use its audience words and promise, and replace any working idea that no real moment in the film supports.
11. One-glance test, for each thumbnail: in one second at phone size, can a viewer say what this is about and what they get? At least one of the 3 must show the promise plainly, for example a real before and after, rather than a mystery. Use high contrast, short words and a cue that identifies the audience. Show authority cues, such as a lab coat or equipment, only if they are true.
12. Start from the reaction, not the picture. Before designing, write for each thumbnail: what should the viewer **wonder**, what should they **feel**, and which visual choice causes that? It must create interest even without the title, because titles often show small. Ways in: an unusual view, vulnerability, credibility, or a broken expectation.
13. Do not start from scratch. Collect 10 to 15 references: our own best films, outliers from other channels, channels with our format on other subjects, saved examples, and films, posters, album covers or ads. Gather them by hand or with connected research tools, never by scraping. For each, note the question, the emotion and the visual mechanism. Use the mechanism on our own idea and never copy a design.
14. Remove clutter. Every element must help the idea or the click, and anything else goes.
15. Make the main subject obvious. It should be the first thing seen, using contrast, a distinct color, clear placement or a small label.
16. Try the words. For any thumbnail with text, write 2 or 3 wordings and test them, since small changes can matter. Test & Compare takes up to 3 thumbnails. Then read its result and our retention, not only the clicks.
17. Read each pair together. The title should clarify the exact problem or promise that the thumbnail shows, and the first 30 s of the film should confirm it. Add that check to the publish kit.

Build them with `./studio.sh thumbs` from `08_Timeline_and_Exports/data/thumbnails.json` (format at the top of `scripts/make_thumbnails.py`), then look at every image.

## Title rules and the virality score
Give 3 titles for the film and 3 for the Short, ranked, with one recommendation and which thumbnail each pairs with. Score each out of 100:

| Part | Points | How to judge |
|---|---|---|
| Frame | 30 | vidIQ multiplier: 2.5x or more = 28 to 30; about 2x = 22 to 26; about 1.5x = 16 to 20; plain description = 10; ends in a question = minus 8 |
| Specific | 20 | a real number, name, place or year from the film |
| Curiosity | 20 | an open loop the film closes |
| Clarity | 15 | the topic is clear in one second, without jargon |
| Length | 5 | 60 characters or fewer = 5, 61 to 70 = 3, longer = 0 |
| Honesty | 10 | every word is true and the film delivers it. Any false or unprovable word means the title is rejected, whatever its score |

**Nine ways into a title.** Draft from several of these, and give the producer titles from at least 2 different ways:
| Way | For a documentary | Example shape |
|---|---|---|
| Benefit | What the viewer will finally understand | "The Real Reason This Town Emptied" |
| Fresh language | A new angle or distinct word, nothing that sounds like every other result | "The Town That Was Dug Out From Under Itself" |
| Viewer desire | Tie to safety, money, health, family or free time, only when the film truly does | "What Lead Did to a Town's Children" |
| Specific audience | Call out a group when the film is really for them. Fewer clicks can still mean better ones | "If You Grew Up Near a Mine, Watch This" |
| Problem and solution | Name a real problem and what the film shows about it | Use only when it gives a real answer |
| Curiosity | Promise a surprise the film has | "Nobody Rebuilt This Town. Here's Why." |
| Open loop | Hint at it without telling it all | "They Signed the Buyout Before the Tornado Hit" |
| Specific question | A concrete question with a place or number, answered in the film | "Why Did 14,252 People Leave Picher, Oklahoma?" |
| Fear or pain | A real concern with a specific place and threat, never scare tactics | "Will This Town's Ground Cave In?" |

These are shapes only. Check each against the film before using it. Hype words such as "secrets" or "must know" need to be literally true, or they fail the Honesty score. Fear titles must match a real, sourced risk, and must not frighten people about health or safety beyond the evidence. Our research found titles ending in a question averaged 0.82x, so the question penalty stays in the score. A specific question can still be tried in Test & Compare, and our own numbers decide.

Use a borrowed frame only when it is true of this film. "Get X fast, it feels like cheating" fits only if the film really gives a fast, unusually effective method, and health or money promises also have to pass `references/rules.md`.

Say plainly that the score is an estimate for ranking options, not a view prediction. Also say when a title covers only one section of the film (a retention risk), and when it rests on an unsettled fact.

## Sources
- vidIQ, YouTube title formulas study (July 2026): https://vidiq.com/research/youtube-title-formulas-study/
- vidIQ, YouTube thumbnail study (500 breakout thumbnails, 2026): https://vidiq.com/research/youtube-thumbnail-study/
- vidIQ, How to improve your thumbnail CTR: https://vidiq.com/blog/post/youtube-custom-thumbnails-ctr/
- Colin and Samir, The new rules of YouTube from Paddy Galloway: https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway
- Tubefilter, MrBeast's leaked production guide (authenticity unconfirmed): https://www.tubefilter.com/2024/09/17/mrbeast-internal-production-guide-leaked-key-points/
- OverseerOS, thumbnail text vs title study: https://www.overseeros.com/blog/youtube-thumbnail-text-vs-title-study
- Netinfluencer, thumbnail study of 1,043 channels: https://www.netinfluencer.com/youtube-thumbnail-study-of-100k-channels-finds-shocked-faces-on-just-1-in-10-covers/
- Jake Trinder, YouTube growth strategy, as summarized by the producer on 4 Nov 2026 (original video not viewed): see `references/growth_system.md`
- Producer-supplied summaries on hooks, thumbnails and titles, 7 Nov 2026 (original videos not viewed, so treat them as one creator's advice)
- PPC Land, custom thumbnails for Shorts: https://ppc.land/youtube-ends-2-year-wait-for-shorts-thumbnails-but-blocks-a-b-testing/
