# Growth system: choosing, packaging and learning

Every film runs through this system: research what the audience already watches, choose a topic with shown demand, make a clear promise, deliver it quickly, offer a useful next step, measure, then improve the next film.

Source: a summary of Jake Trinder's YouTube strategy, pasted by the producer on 4 Nov 2026. The original video was not viewed and its case studies were not checked. Treat it as one practitioner's method, not proof. `references/rules.md` always wins over anything here.

## Where each point lives in the workflow
| # | Point | What we do | Where |
|---|---|---|---|
| 1 | Find topics people already want | Demand check before any script: search phrases, videos far above their channel's usual views, several channels | Step 3, `01_Script/demand_research.csv` |
| 2 | Package so people choose it | Promise, working titles and thumbnail ideas written before the script, in the audience's words | Step 4, `01_Script/demand_brief.md` |
| 3 | Understood at a glance | One-glance test, and at least one thumbnail that shows the promise plainly | `references/packaging.md`, rules 10 to 12 |
| 4 | Deliver the promise immediately | Promise, Proof, Plan in the first 30 s, and a promise match check before Gate 3 | `references/script_and_retention_guide.md`, `references/quality_bar.md` |
| 5 | Turn views into a next step | One next step per film, tied to the film's problem | Step 4 choice, script if natural, kit section "Next step and end screen" |
| 6 | Let data guide the next video | Check-ins at 48 hours, 7 days and 28 days, full funnel, one change for the next film | Step 10, `./studio.sh review` |
| 7 | Study wins and failures | The research sheet needs flops too, and notes structure rather than only titles | Step 3 |
| 8 | Match production to the video | Format choice in the brief, and editing must clarify | Demand brief, `references/quality_bar.md` |
| 9 | One coherent channel | Channel strategy, a fit test for each topic, a repeat test for each win | `_Channel/channel_strategy.md`, Steps 3 and 10 |
| 10 | The whole loop | This file, repeated for every film | All steps |

## Step 3: Demand check (about 20 minutes for the producer, then Claude analyses)
Run it after the project is created and before the fact work. A topic that fails this check should change before any voice credits are spent.

**Rights and platform limits.** Never scrape YouTube, and never download its videos or transcripts in bulk. Do not build a tool that pulls this from the YouTube Data API: its developer policies, read on 4 Nov 2026, restrict scraped data, storing public statistics past 30 days and new derived metrics, and our outlier ratio is a derived metric. So the producer gathers the examples by hand. Claude may use ordinary web search for public signals, and may analyse whatever the producer pastes.

**What the producer does**
1. Search YouTube for the problem in the audience's words, in every language of the film. Follow the results, the channels and the recommendations until the same videos start repeating.
2. Add rows to `01_Script/demand_research.csv`, at least 5 wins from at least 3 channels and at least 2 flops. A win is a video well above that channel's usual views. A flop is the same topic or format well below them. Our working line for a win is 2x or more, which is our own number, not a study. Views vary with video age, so note the age and compare with similar-age videos where possible.
3. For the best 2 or 3 wins and 1 flop, watch the opening and skim the rest, then note the structure: opening, delivery, scripting, editing, visual explanations and transitions.

Tools such as YouTube Studio's inspiration or research features, vidIQ and ViewStats may speed this up. Their current features and prices are not checked here: test them first, and ask before paying.

**What Claude does**
1. Compute `outlier_ratio` (views divided by the channel's typical views), and check the math.
2. Find the patterns across channels: repeated topics, words, title frames, thumbnail ideas and structures.
3. Say why a format may have worked by naming the audience motive, and why the flops failed. Treat every cause as a guess unless it repeats. One viral video is a signal, not an explanation.
4. Write `01_Script/demand_brief.md`, including its demand level:
   - **A, demonstrated:** the minimum sheet is met, and the wins share the topic and the audience.
   - **B, weak:** fewer examples, or only web search and press signals.
   - **C, unvalidated:** no evidence, for example a source the producer simply wants to adapt.
5. Run the channel fit test and the repeat test below. State the level at Gate 1. If the level is B or C, or a test fails, recommend a change, but the producer decides.

The Short and each language can have different demand. Bangla viewers may use different words or want a different angle, so do not assume English results carry over.

Also note how the music behaves and where the first big turn comes, because Claude cannot watch or listen. `references/viral_style_guide.md` has the general patterns, and this film's own winners come first.

Copy what the pattern teaches, never another creator's words, thumbnail art or footage.

**FAST mode.** Ask for the sheet once with the brief. If the producer skips it, run the web search, mark the film B or C, and carry on. This check is not a fourth gate.

Before recommending a topic, check it has a human way in: a documented person or group with a conflict, stakes and change. A popular subject with no documented human story is harder to make gripping, so say so in the recommendation. Fill in "Story within the story" in the brief (`references/script_and_retention_guide.md`).

## Step 4: Promise first
Write these in `01_Script/demand_brief.md` before the script:
- **Promise:** one sentence, the result or answer the viewer clicks for.
- **Audience:** as broad as possible while still clearly speaking to the core audience. Specific enough that the right viewer feels understood.
- **3 working titles and 3 thumbnail ideas:** using the audience's words. These are drafts. Final packaging still comes from real moments in the film.
- **Proof:** the real reason to trust this film (a named study, the method, the producer's real experience). Never an invented credential.
- **Plan:** what the film will cover, in one spoken line.
- **Next step:** see below.
- **Format:** the production style that suits the idea. Our default is a tightly scripted narrated film. Use a loose screen recording for a walkthrough or natural reactions for a real challenge only if the producer really films one.

The script is written to deliver this promise. If the script finds that the promise is false, change the promise, never the facts.

## Next step, not interruption
Every film gets exactly one next step, chosen from `_Channel/channel_strategy.md`, in this order of preference:
1. A real resource or offer that solves the problem the film raises: a free checklist, a template or a guide.
2. The next film on the same theme, when there is no fitting offer. This is a real goal too.

Rules:
- It continues the film's subject. If it needs a forced transition, use the next film instead.
- Never in the first 30 s. Best after the film has raised the problem it solves, or in the close.
- Say plainly when something is paid or sponsored, and follow YouTube's paid promotion rule. Never promise a result the offer cannot show.
- A resource must really exist before the film promises it. If collecting emails, the producer chooses the service and is responsible for its privacy terms.
- A script line for the next step is part of the locked script at Gate 1. Do not add one after approval without asking.

The kit's "Next step and end screen" section holds the description line, an optional pinned comment that starts a conversation (never credits) and the end screen choice.

## Channel fit and repeat tests
`_Channel/` sits beside the film folders and holds what no single film owns: `channel_strategy.md`, `video_ledger.csv` and `learned_rules.md`.

- **Fit test:** would a viewer of the channel's recent films want this one, and would a viewer of this film want the others? A topic outside the theme can win views and still weaken the channel. Flag that clearly and let the producer decide.
- **Repeat test:** can you name 3 more films for the same audience with the same promise style? If not, treat it as a one-off.
- **After a win:** test it again with another film in the same theme before calling it a strategy.
- If the strategy file is not filled in yet, ask once. Never guess the producer's audience or offer.

## Step 10: After publishing
Run a check-in at 48 hours, 7 days and 28 days. The producer adds one row per video and language to `11_Performance/metrics.csv` from YouTube Studio, then Claude runs `./studio.sh review`. It writes `11_Performance/review.md` and updates `_Channel/video_ledger.csv`. It compares only against the channel's own earlier films and needs at least 3 before it judges high or low.

| What you see | Look first at | Try next |
|---|---|---|
| Few impressions | Topic demand and audience fit | Choose from stronger demand, stay in the theme |
| Good impressions, low click rate | Title and thumbnail | Test another thumbnail, clearer promise |
| Good clicks, viewers leave in the first 30 s | The opening does not match the packaging | Fix Promise, Proof, Plan and the match |
| Good first 30 s, low average viewed | The story's middle, at the biggest drop | Add a turn before that moment, cut slow context |
| Strong views, few next step clicks | The next step or where it appears | Better fit, better moment |
| Clicks but no leads | The page or the resource | Simplify the page, check the promise |
| Leads but no customers | The offer or sales process | Review the offer, not the film |

Rules:
- Change one main thing per film, and write it in the review, so the next result teaches something.
- Do not chase click rate or retention alone. A title that gets clicks from the wrong people and disappoints them is a loss.
- Add to `_Channel/learned_rules.md` only with evidence. One film is a **signal**. Two or more films showing the same thing is a **rule**. Failures count as evidence too.
- Read `learned_rules.md` before every demand brief and every script.
- Say plainly when numbers are too few to conclude anything. New channels may need many films before a pattern is real.
