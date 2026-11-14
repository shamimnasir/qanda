# Gather everything the producer needs for the upload into one top-level folder, 10_Ready_to_Upload/:
# the films and Shorts, SRT files, thumbnails, and plain text files to paste (titles, description,
# Short text, hooks, Facebook caption), taken from youtube_publish_kit.md.
# Run after `docs`, `render` and the publish kit. Safe to re-run: it rebuilds the folder.
# Usage: python3 build_upload.py
import glob, os, re, shutil, subprocess
from common import P, ROOT

EXP = os.path.join(ROOT, '08_Timeline_and_Exports')
LIC = os.path.join(ROOT, '09_Permissions_and_Licenses')
OUT = os.path.join(ROOT, '10_Ready_to_Upload')
LANGS = list(P['languages'])
NAME = {'en': 'English', 'bn': 'Bangla'}
SLUG, LIMIT = P['slug'], 5000  # YouTube description limit, in characters
warn = []

def copy(src, dst):
    """APFS clone when possible (no extra disk space), else a normal copy."""
    if os.path.exists(dst): os.remove(dst)
    if subprocess.run(['cp', '-c', src, dst], capture_output=True).returncode != 0:
        shutil.copy2(src, dst)

def write(name, text):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(text.strip() + '\n')

def tag(lang):
    """File-name suffix, only when the film has more than one language."""
    return f'_{NAME.get(lang, lang)}' if len(LANGS) > 1 else ''

# Publish kit: split into "## " sections and label each by kind and (optional) language.
kit_path = os.path.join(EXP, 'youtube_publish_kit.md')
kit = open(kit_path, encoding='utf-8').read() if os.path.exists(kit_path) else ''
if not kit: warn.append('no youtube_publish_kit.md yet: only the videos, subtitles and thumbnails were copied')
sections = []
for block in re.split(r'^## ', kit, flags=re.M)[1:]:
    head, _, body = block.partition('\n')
    h = head.lower()
    kind = ('short' if 'short' in h else 'title' if 'title' in h else 'thumb' if 'thumbnail' in h else
            'description' if 'description' in h else 'next' if 'next step' in h else 'hooks' if 'hook' in h else 'facebook' if 'facebook' in h else None)
    lang = 'bn' if re.search(r'bangla|bengali|বাংলা', h) else 'en' if 'english' in h else None
    if kind: sections.append((kind, lang, body.strip()))

def section(kind, lang):
    """The section for this language, else the one with no language, else none."""
    for want in (lang, None):
        for k, l, b in sections:
            if k == kind and l == want: return b
    return ''

def plain(s):
    """Markdown to plain text: drop ** and `, and turn table rows into lines like "1. Title (Score: 92, ...)"."""
    out, head = [], None
    for line in s.splitlines():
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '): continue
            if head is None: head = cells; continue
            extra = ', '.join(f'{h}: {c}' for h, c in zip(head[2:], cells[2:]))
            out.append(f'{cells[0]}. {cells[1]}' + (f'  ({extra})' if extra else ''))
        else:
            head = None; out.append(line)
    return re.sub(r'\*\*|`', '', '\n'.join(out)).strip()

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'Thumbnails'))

# Videos and subtitles
for lang in LANGS:
    for n, part in ((1, 'film'), (2, 'short')):
        src = os.path.join(EXP, 'renders', f'{SLUG}_{lang}_{part}.mp4')
        if os.path.exists(src): copy(src, os.path.join(OUT, f"{n}_{'Film' if part == 'film' else 'Short'}{tag(lang)}_{SLUG}.mp4"))
        else: warn.append(f'missing render: {os.path.relpath(src, ROOT)}')
    srt = os.path.join(EXP, f'{SLUG}_captions_{lang}.srt')
    if os.path.exists(srt): copy(srt, os.path.join(OUT, f'3_Subtitles_{NAME.get(lang, lang)}.srt'))
    else: warn.append(f'missing subtitles: {os.path.relpath(srt, ROOT)}')

thumbs = sorted(p for p in glob.glob(os.path.join(ROOT, '05_Motion_Graphics', 'thumbnails', '*.*'))
                if os.path.isfile(p) and not os.path.basename(p).startswith('phone_size_check'))
for t in thumbs: copy(t, os.path.join(OUT, 'Thumbnails', os.path.basename(t)))
if not thumbs: warn.append('no thumbnails in 05_Motion_Graphics/thumbnails')

# Text to paste
short_credits = os.path.join(LIC, 'credits_short_for_description.txt')
credits = open(short_credits, encoding='utf-8').read().strip() if os.path.exists(short_credits) else ''
for lang in LANGS:
    t = tag(lang)
    titles, thumb = section('title', lang), section('thumb', lang)
    if titles:
        write(f'4_Titles_and_thumbnails{t}.txt', 'TITLE OPTIONS (pick one, 100 characters at most)\n' + plain(titles)
              + ('\n\nTHUMBNAILS (in the Thumbnails folder)\n' + plain(thumb) if thumb else ''))
    desc = section('description', lang)
    m = re.search(r'```[a-z]*\n(.*?)```', desc, flags=re.S)
    if m:
        text = m.group(1)
        # The kit's "[Paste ... credits ...]" line becomes the short credits.
        text = re.sub(r'^\[Paste[^\]]*credits[^\]]*\]\s*$', credits, text, flags=re.M | re.I) if credits else text
        write(f'5_Description_paste_into_YouTube{t}.txt', text)
        n = len(text.strip())
        if n > LIMIT: warn.append(f'description{t} is {n} characters, over the YouTube limit of {LIMIT}: shorten it')
        if re.search(r'\[[A-Z][^\]]*\]', text): warn.append(f'description{t} still has a [bracket] to fill in')
        if '<' in text or '>' in text: warn.append(f'description{t} has < or >, which YouTube does not allow')
    elif kit: warn.append(f'no description code block found for {lang}')
    for n, kind, label in ((7, 'short', 'Short_title_and_description'), (8, 'facebook', 'Facebook_caption'), (9, 'hooks', 'Hooks'), (10, 'next', 'Next_step_and_end_screen')):
        b = section(kind, lang)
        if b: write(f'{n}_{label}{t}.txt', (f'FOR THE SHORT (2_Short{t}_{SLUG}.mp4)\n\n' if kind == 'short' else '') + plain(b))
        elif kit and kind == 'next': warn.append(f'no "Next step and end screen" section in the kit for {lang}')

bad = [os.path.basename(p) for p in glob.glob(os.path.join(OUT, '*.txt'))
       if re.search('[\u2013\u2014]', open(p, encoding='utf-8').read())]
if bad: warn.append('long dash found in: ' + ', '.join(bad))
print(f'10_Ready_to_Upload: {len(os.listdir(OUT)) - 1} files and {len(thumbs)} thumbnails')
for w in warn: print('  WARNING:', w)
