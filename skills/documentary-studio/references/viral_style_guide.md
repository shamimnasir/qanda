# Viral documentary style guide

The producer asked (Nov 2026) for research into viral YouTube documentaries and for our films to apply what works. Read this before choosing a topic, before the script, and before the shotlist.

Learn the structure, never copy. Do not take another creator's words, footage, thumbnails, music or signature look. `references/rules.md` always wins.

## How strong is this evidence?
Claude read about what these creators do, and did not watch or listen to their videos. No source proves that any one technique causes views. Good story and strong demand probably matter more than any edit trick.

| Label | Meaning |
|---|---|
| **Strong** | The creator or studio describing their own process, or a working professional writing for a craft body |
| **Medium** | Third-party breakdowns that agree with each other. Their numbers are not measured |
| **Test** | One vendor blog or AI summary. Treat it as an idea to try and measure |

## Choosing the idea
1. **Must be visual, and must add something.** Before greenlighting, ask if the story can be shown and if the film gives viewers something they did not have. Johnny Harris uses this filter. (Strong)
2. **A small door into a big story.** A simple, familiar subject can open a larger system. Harris cites bread as a way into a story about America. Look for the everyday object or moment behind the big topic. (Strong)
3. **Explain the why.** Harris argues the why is what most news leaves out, and that viewers will stay for depth when it helps them understand. Offer understanding, not a list of facts. (Strong)
4. **Keep the channel's look steady across films.** When Harris's team made two matched videos, they kept the packaging and music approach the same so the subject was the variable. Consistency makes comparisons meaningful. (Strong)

## Script
5. **Narrate as a curious person.** Sound like someone explaining what they just learned, not a distant authority reading lines. Harris rejects that voice-of-God style. In `en_tts`, write for this, and only use "I" for things that are true of the producer. (Strong)
6. **Question, report, new question.** Pose a question, answer it with evidence, and let that answer raise the next question. It suits a detective story, even when the topic is not a crime. (Medium)
7. **After the hook, open on what the viewer still wants to know.** The hook states the twist in about 10 s (`references/script_and_retention_guide.md`), so the next line opens the how or why, and each section ends on the next question.
8. **Seesaw between story and explanation.** Alternate the human or visual story with the technical part, so the story pulls viewers back when things get dense. (Test)
9. **Rewrite for retention.** Label every paragraph: hook, context, proof, example, transition, payoff or filler. Cut the filler, and move energy earlier if the best moment comes late. (Test)
10. **Draft many times.** Kurzgesagt says about a dozen drafts go into balancing facts and story. Use at least 3 passes: facts, story, spoken rhythm. (Strong)
11. **Start with a bare list of key points.** LEMMiNO builds a script up from a short list of points over time. Write the beat list before searching for any footage. (Strong)

## Pictures and edit
12. **Choose a visual idea for each scene before searching.** Kurzgesagt settles the visual metaphor in sketches before making any art. Add a one-line `desc` to each shot saying what it proves or shows, before opening Pexels. (Strong)
13. **Voice first, picture to the voice.** Kurzgesagt times its animation to the narration. Our engine already does this. Keep it. (Strong)
14. **Never let stock become wallpaper.** Moody clips playing under narration are a known failure of faceless videos. Every shot should show, prove or explain something. Use graphics, maps, real photos and real examples, and use sound to mark changes. (Test, but it matches our honesty rules)
15. **Change the picture when the idea changes.** Use a graphic, map, title or big change of scene at each new idea, and before places where viewers may leave. The QA check flags long runs of only stock. (Test)
16. **Vary the pace.** Move between fast sections and slower ones where viewers can breathe. Slow down slightly when a new concept arrives. Over-editing backfires, and a strong story can hold with few cuts. (Medium)
17. **Add quiet texture where it fits.** Harris-style edits are described as using photo sequences that speed up, each with a soft camera click, plus grain and light leaks. Use your own version, sparingly, where it helps the story. (Medium)

## Sound and music
See `references/music_guide.md` for the engine. These rules shape how to plan each film:
18. **Compose for the film.** Kurzgesagt gets each video its own score, made to fit its mood. Our score engine does the same. (Strong)
19. **Map the whole film on one page.** Composer Miriam Cutler suggests a one-page Music Story Arc listing each cue's emotion, intensity, tempo, place and length, so too much or too little music is easy to spot. The engine writes `07_Music_SFX/music_story_arc*.md`. Read it before rendering. (Strong)
20. **Ask if each section needs music.** Cutler treats music like an edit, asking if each sequence needs it and if it supports that sequence's intent. Try silence or plain ambience for at least one or two strong moments. (Strong)
21. **Write one sentence on what each section should feel like,** using `"feel"` in the score plan. Then choose the mood. (Test)
22. **Fewer layers under speech.** Lower the density of the music under words, not only its volume. The engine does this. (Test)
23. **Change at structural moments.** Let music move when the place, time or argument changes, not run as one bed. Chapter changes are natural points. (Test)
24. **Punctuate with sound.** Use effects to mark moments, with near silence after a big reveal, rather than a constant noise. (Medium)
25. **Be careful with heartbeats and ticking clocks.** They can push a viewer's feelings beyond the evidence in a serious investigative film. Use them only if the story earns them. (Test)

## Study real wins for each film
This guide is general. The strongest lesson comes from the winners in this film's own niche:
- In the demand check (`references/growth_system.md`), the producer watches the opening of the best 2 or 3 wins and 1 flop and fills in `opening_structure` and `delivery_and_editing`.
- Also note how the music behaves and where the first big turn comes, since Claude cannot watch or listen. Claude then finds the patterns and puts them in the demand brief.
- After publishing, compare the retention graph with the Music Story Arc and the script labels. Keep what the channel's own numbers support in `_Channel/learned_rules.md`. **Our own data beats this guide.**

## Sources (read Nov 2026)
- Johnny Harris, Colin and Samir interview, auto-captioned transcript: https://rosetta.to/u/colinandsamir/an-honest-conversation-with-johnny-harris
- Johnny Harris channel video list and summaries: https://rosetta.to/u/johnnyharris/topic/storytelling
- LEMMiNO, Q&A, auto-captioned transcript: https://rosetta.to/u/lemmino/3-000-000-q-a
- Kurzgesagt, their own process page: https://kurzgesagt.org/youtube/
- Miriam Cutler, Documentary magazine (2014): https://www.documentary.org/index%2Ephp/node/35962
- Third-party Harris breakdowns: https://blog.editorduel.com/blog/johnny-harris-detective-story-formula-explainer-videos and https://motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/
- Paddy Galloway interview summary: https://recapio.com/digest/meet-the-youtube-expert-behind-10-billion-views-paddy-galloways-full-story-by-karat
- Vendor and AI sources: https://www.overseeros.com/blog/youtube-retention-architecture-2026, https://sonilo.com/ai-music/documentary-music, https://gist.ly/youtube-summarizer/the-secrets-behind-veritasiums-viral-success

Not found: a reliable ranking of the most-viewed YouTube documentaries, a study of what makes them viral, or useful first-hand sources on Fern, Nick Crowley or Magnates Media. Do not claim these were studied.

## Learning from a reference video
`./studio.sh reference file.mp4` measures a video against the current film: stereo, loudness, voice clarity, pauses, sound hits, cuts and shot length. It writes `review/reference_report.md` and a frame sheet. Use only a video you have the right to analyze, such as your own or one with permission, and do not download other creators' videos for this. When a video is only on YouTube, watch it there and write notes by hand. Take the technique, never the footage, music or words. One video proves nothing, so test a change on our own films and let our own numbers decide.

## A format to test: the wordless idea film
A short animated story with no narrator, a little on-screen dialogue, simple characters, one small idea and a strong sound arc. It suits idea films such as habits and life lessons, not factual films about real events.
- It is fiction, so characters can be made up. Say so in the description, and label any AI animation or images as AI.
- Learn its structure and never copy its story, characters or look. Quotes from real people must be accurate and credited.
- It may cost no voice credits. The engine does not support it yet: it expects a narration track, and it has no character animation. Tell the producer this and agree on a plan before promising one.
- One film is not proof. Fast facts and slow stories may suit different topics, so test and let the channel's numbers decide.
