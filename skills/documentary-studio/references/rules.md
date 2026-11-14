# Hard rules (always apply)

These come from the producer and protect a monetized YouTube channel. Breaking one can cost a copyright strike, a demonetization or the audience's trust, so they hold even when the producer says "just do it all".

## Writing
- Never write the long dash character (em dash or en dash) in any text, caption, script or file. Use commas, periods or hyphens. `qa_check.py` scans for it.

## Rights and licensing
- Only use footage, images, music and fonts whose license allows commercial YouTube use: Pexels, Pixabay (with a key), Wikimedia Commons (checked per file), public domain (US government, NPS, USFWS, NASA), the producer's own files, OFL fonts. Adobe Stock only through the producer's signed-in account, and only after stating the cost.
- Log every asset in the project's `tracker.csv` with its license. If a license is unclear, do not use the asset, and flag it.
- CC BY-SA is allowed with credit but raises a ShareAlike question: flag it for the producer.
- Never scrape or bulk download from Instagram, X, Threads, TikTok or YouTube. Never download another creator's video without written permission. If the producer wants a creator's footage, draft a permission request from `assets/templates/permission_request.template.md` for them to send.
- Adapting the ideas in someone's writing (an article, letter or book) into a film is the producer's decided approach: retell it in new words with new research, credit the source, and do not reuse their title or long passages. Do not raise permission, draft a request or mark it unclear unless the producer asks.
- Demand research follows the same limits: no scraping or bulk collection from YouTube, and no tool that pulls channel or video data outside YouTube's API policies. The producer gathers examples by hand, and we learn patterns, never copying another creator's words, thumbnail art or footage.
- Clip length does not make use legal. "Fair use" is never assumed.

## Honesty
- Never invent facts, sources, URLs, statistics or quotes. Put every claim in `facts_to_verify.md` and recompute every number (Oymyakon: "almost 100 degrees" was really about 90).
- If you are not certain about a fact, a tool's capability or a platform rule, say so.
- Never present stock or AI footage as real footage of the place or person. The producer does not want "ILLUSTRATIVE FOOTAGE" text on screen (6 Nov 2026), so honesty comes from the edit: when a line is about one specific real event, place or person (this tornado, this creek, this parade), use a real photo or a graphic. Generic stock only sits where it reads as generic (mining, kids playing, a lab, storm clouds). If no honest picture exists, use a graphic and tell the producer. Real-location photos keep their small on-screen credit with the place name, because the licenses and this rule need it. The description says plainly that other footage is illustrative stock.
- Quotes from real people go on quote cards (text plus their real audio if licensed), never re-voiced by an AI voice.
- Scenes follow the same rule: never invent a real person's thoughts, feelings, gestures or dialogue to make a story more vivid. Use only what a source records.
- Label AI-generated material as AI in the tracker and the description, including AI people on thumbnails, and set YouTube's AI use question to Yes for the cloned narration. Check YouTube's current disclosure rule before publishing.
- Thumbnails and titles follow the same honesty rules: only promise what the film shows, never imply a stock or made-up person is a real subject (an older stranger is not "a centenarian", and a made-up miner is not a named Picher resident), and add a small label when big text could mislead ("OKINAWAN MEN" above "4TH → 43RD").
- Proof and next steps are held to the same standard: never invent a credential, a result, a case study or a free resource. Say when a link is paid or sponsored. Demand never justifies a claim the evidence does not support: a popular promise such as a fast health fix must still be true, or the film says that it is not.
- Health, science and history topics: back every claim with a real source, mark contested claims as CONTESTED in `facts_to_verify.md` and say so in the script ("some scientists question..."), call observational studies a link and not proof, and put "Not medical advice" in the description. Use "odds" or "risk" exactly as the study does.
- Read every stock clip's title, not only its thumbnail, and check frames of the final render. A clip must not contradict the line it sits under (a living wolf under "this wolf did not die", a vape cloud as "breath", adults as "children"). Watch for the wrong place too: Japan film searches returned Hawaii and Maldives sunsets, hospitals in India and London, and the Itsukushima torii (Hiroshima) for "Okinawa". A staged actor looking at the camera does not belong under a line about researchers.

## Money and tools
- Before relying on a tool or connector, test it and report the result.
- Ask before spending money or credits, and state the cost first. ElevenLabs TTS v3/v4 is about 1 credit per character; ElevenLabs Marketplace music is about 7,500 credits per track. The engine's original score costs nothing.
- Never enter passwords, payment details or API keys yourself. The producer stores the Pexels key with `setup.sh --key`. Never print the key.

## The 3 gates
Always stop and wait for the producer at:
1. **Script gate:** the locked script and every translation, with the credit cost, before any voice is generated. After approval the script is locked: edit it only with the producer's approval.
2. **Voice gate:** the producer generates (or approves generating) the voiceover and downloads it.
3. **Publish gate:** the finished renders, `facts_to_verify.md` and the publish kit, before anything is uploaded or posted.

"Do it all" or FAST mode removes every other checkpoint, never these three.

## Reporting
Music: every film gets its own soft, never harsh score matched to its exact vibe and pace, with real ups and lows. See `references/music_guide.md`.

Say plainly what was verified and what was not. Claude cannot listen to audio, so the producer checks pronunciation, voice and music by ear.
