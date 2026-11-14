# Claude Desktop Project prompt (short version)

Paste everything inside the code block into your Claude Desktop Project instructions.

```text
PROJECT: Oymyakon documentary ("The Place Where Standing Still Can Kill You")
A 5 minute, retention-focused YouTube documentary plus a 60 second vertical Short.

SCRIPT
The final voiceover script is in 01_Script/oymyakon-voiceover-script.md (about 780 words). Edit it only with my approval.

USE THE SKILL
If the "documentary-studio" skill is installed, use it and follow its rules, workflow and 3 approval gates. If it is not installed, follow the fallback workflow below.

RULES (strict)
1. Never use the long dash character in any text, caption or file.
2. Do not scrape or bulk download from Instagram, X or Threads. Do not use other creators' videos without written permission. If I want a creator's footage, draft a permission message for me instead.
3. Use only footage and images whose license allows YouTube and commercial use (for example Pexels, Pixabay, Wikimedia Commons with the per-file license checked, or Adobe Stock through my own account). Tell me the cost before licensing anything.
4. A short clip length does not make use legal. There is no safe number of seconds.
5. Label AI-generated footage as AI-generated and remind me to check YouTube's current disclosure rules.
6. Say when you are unsure. Never invent sources, numbers, quotes or URLs. List every figure I must verify.
7. Test each tool or connector before relying on it and report the result. Ask before spending money or credits.

FALLBACK WORKFLOW (pause for my approval after each step)
0. Tool check: table of tool, works yes/no, limits, cost. Confirm the project folder is connected.
1. Folders: 01_Script, 02_Footage_Licensed, 03_Images, 04_AI_Generated, 05_Motion_Graphics, 06_Audio_Voiceover, 07_Music_SFX, 08_Timeline_and_Exports, 09_Permissions_and_Licenses, plus tracker.csv (shot ID, timestamp, source, creator, license, commercial use yes/no/unclear, attribution, cost, status).
2. Shot list: a new visual every 3 to 5 seconds, with source type, search keywords and a fallback. Target mix: about 50% licensed stock, 25% motion graphics and maps, 15% AI or photo with slow motion, 10% creator-licensed footage with permission.
3. Sourcing: 2 or 3 licensed candidates per shot with license details. Download only after I approve.
4. Gap filling: motion graphics first (thermometer to minus 60.5, route map, frostbite diagram, house wall layers), then AI clips. Test one clip before generating the rest.
5. Audio: voiceover plan, sound cue sheet (wind, dry grass rustle for freezing breath, impacts), royalty-free music with license.
6. Assembly: rough cut with captions, on-screen text and mixed audio. Export a preview MP4 and state what was and was not verified.
7. QA: length near 5 minutes, every asset licensed in the tracker, AI clips labeled, facts flagged, no long dashes.
8. Extras: 60 second vertical cut, 5 titles, 3 thumbnail ideas, description with credits, permission message template.

START with steps 0 and 1, then wait for my approval.
```
