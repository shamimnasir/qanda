# Prompt: install the Documentary Studio template on banglacodes.com

Paste everything inside the code block into a Claude session that has access to the banglacodes.com codebase (and its deployment tools, if you want it to deploy).

```text
ROLE
You are a senior full-stack engineer and product designer. You will add a "Documentary Studio" template to the Templates section of banglacodes.com so that people on the platform can make retention-focused YouTube documentaries and Shorts.

SOURCE MATERIAL
The skill and engine are in the GitHub repo shamimnasir/qanda, folder skills/documentary-studio (start with SKILL.md, references/rules.md and references/playbook.md). Docs are in docs/documentary-studio. The worked example is skills/documentary-studio/assets/examples/Oymyakon. Read them before designing anything.
What the engine is: a config-driven Python plus Remotion pipeline that turns a topic and sources into a script, ElevenLabs narration, licensed stock, an original score, burned-in captions, a 5 minute film, a 60 second Short and a publish kit, in English and Bangla.

IMPORTANT UNKNOWNS
I have not described the banglacodes.com stack to you. Do not assume it. Discover it in Phase 0.

PHASE 0: DISCOVERY (read only, then stop)
Report: framework and language, how the Templates section is built and how a template is defined (data file, CMS, database or code), authentication, billing and plans, file storage, background jobs or queues, hosting limits (CPU, memory, execution time, disk), how Bangla text and fonts are handled, and how existing templates are installed or used by visitors.
Then list the delivery options below with a recommendation and wait for my choice.

DELIVERY OPTIONS (recommend one, explain why)
A. Download template: a zip users run in their own Claude Code with their own tools. Lowest cost and risk. The engine needs ffmpeg, whisper-cpp, Google Chrome, Node and Python (numpy, Pillow), and about 15 minutes of rendering per film.
B. Hosted app: users submit a brief in the browser and our servers render the video. Needs render workers, queues, storage, per-user cost control and abuse protection.
C. Hybrid: the browser guides research, script, translation, shot list and publish kit; rendering happens by download (A) now, and hosted rendering (B) later.
My expectation is that A or C is the right first release, but verify against what Phase 0 finds.

PHASE 1: PRODUCT DESIGN (propose, then wait for approval)
- Template card: Bangla and English title and description, preview image or video, difficulty, time needed, requirements, cost notes (ElevenLabs credits, stock licenses).
- Template page: step by step guide following the skill's 3 approval gates (script, voice, final QA), a requirements checker, the download, and the Oymyakon example.
- Brief form that produces a ready-to-paste master prompt from references/master_prompt.md (topic, source credit, languages, length, voices, mode, credit budget).
- Per-user profile instead of the personal producer_profile.md. Remove all personal data (voice clone names, plan details, private preferences) from anything published to users.

PHASE 2: BUILD (after approval)
- Implement the template using the existing Templates section conventions. Match existing code style, components and design system.
- Bangla first: native Bangla UI copy, correct conjunct rendering (use Noto Sans Bengali or the site's font), and ask me to review all Bangla wording before launch.
- Responsive and accessible (keyboard, contrast, alt text).
- Keep the engine changes minimal and documented. Do not rewrite it without asking.

NON-NEGOTIABLE RULES
1. No secrets in the repo, the zip, logs, client code or analytics. Users bring their own ElevenLabs and Pexels keys, entered only on their own machine (see the skill's setup.sh --key flow). If the hosted option is chosen later, store keys encrypted server-side and never return them to the browser.
2. Licensing. The template must tell users that only licensed footage may be used (Pexels, Pixabay, Wikimedia Commons per file, paid libraries), that there is no safe number of seconds for unlicensed clips, and that scraping Instagram, X or Threads is not supported. Show a license tracker in the template.
3. Third party terms. Before launch, verify and report, with the official source for each: Remotion's license terms for a hosted multi-user service or commercial template; ElevenLabs terms for use on a platform and for each user's plan (the skill notes that Starter terms restrict some music uses); Pexels and Pixabay API terms; font licenses (Oswald, Inter, Noto Sans Bengali). If you cannot confirm something, say so plainly. Do not guess.
4. AI disclosure. The template must remind users to follow YouTube's current disclosure rules for realistic AI content, and to label AI-generated footage. Tell users to verify the current rules themselves.
5. Honesty. State what you tested and what you did not. Never claim a feature works without running it. Never invent sources, numbers or quotes.
6. Writing style: never use the long dash character in any copy, code comment or document.
7. No production deploy, payment change, database migration or data deletion without my explicit approval. Work on a branch and open a pull request.

PHASE 3: TEST
- Install the template on a staging or local copy. Run the Oymyakon example through the skill's checks as far as the environment allows (setup.sh check, studio.sh qa, a still frame render). Report any step you could not run and why.
- Test the Templates page on mobile and desktop, in Bangla and English, and with a user who is signed out.
- Check that no personal data or secrets appear in the published files (search the diff).

PHASE 4: HAND OFF
Open a pull request with: what was added, screenshots, how to roll back, the list of third party terms still to confirm, the list of Bangla copy needing my review, and known limits (for example render time and tool requirements).

CHECKPOINTS
Stop and wait for my approval after Phase 0, Phase 1 and before any deploy.
Begin with Phase 0 now.
```
