# Build the vertical Short from story segments of the full film, plus its audio cut from the final mix.
# project.json "short": {"max_seconds": 59.5, "segments": [{"name": "hook", "from": anchor, "to": anchor}, ...],
#                        "drop_order": ["frostbite", "arrival"],   segments dropped (in this order) if a language runs long
#                        "brief": {"story": "", "first_frame": "", "hook_line": "", "foreshadow": "", "mechanism": "", "ending": "", "why_share": ""}}
# It trims silence before the first word and after the last word, and prints the Short check. See references/shorts_guide.md.
# Usage: DOC_LANG=en|bn python3 build_short.py
import json, os, re, subprocess
from common import FPS, LANG, P, REM, Anchors, f, load_timeline, load_words

TL = load_timeline()
A = Anchors(TL, load_words())
cfg = P['short']
segs = [(s['name'], A(s['from']), A(s['to'])) for s in cfg['segments']]
for name in cfg.get('drop_order', []):
    if sum(b - a for _, a, b in segs) <= cfg.get('max_seconds', 59.5):
        break
    segs = [s for s in segs if s[0] != name]
    print(f'[{LANG}] dropped segment "{name}" to fit {cfg.get("max_seconds", 59.5)}s')

# Where the words fall, for the ending trim and the check.
WORDS = []
for w in load_words():
    try: WORDS.append((A.film_t(w['s']), A.film_t(w['e']), w['w']))
    except ValueError: pass
def spoken_in(a, b): return [w for w in WORDS if w[1] > a and w[0] < b]

MAX_TAIL, MAX_LEAD = 0.3, 0.15
name, a, b = segs[0]
inside = spoken_in(a, b)
if inside and inside[0][0] - a > MAX_LEAD:
    print(f'[{LANG}] trimmed {inside[0][0] - MAX_LEAD - a:.2f}s of silence from the start')
    segs[0] = (name, inside[0][0] - MAX_LEAD, b)
name, a, b = segs[-1]
inside = spoken_in(a, b)
if inside and b - inside[-1][1] > MAX_TAIL:
    trimmed = inside[-1][1] + MAX_TAIL
    print(f'[{LANG}] trimmed {b - trimmed:.2f}s of silent tail from the end')
    segs[-1] = (name, a, trimmed)

out, at = [], 0
for name, a, b in segs:
    fa, fb = round(a * FPS), round(b * FPS)
    out.append({'name': name, 'filmFrom': fa, 'shortFrom': at, 'dur': fb - fa}); at += fb - fa

parts, filt = [], []
for n, s in enumerate(out):
    a, d = s['filmFrom'] / FPS, s['dur'] / FPS
    filt.append(f"[0:a]atrim={a:.4f}:{a + d:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={d - 0.03:.4f}:d=0.03[s{n}]")
    parts.append(f'[s{n}]')
filt.append(''.join(parts) + f'concat=n={len(out)}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', os.path.join(REM, 'public', f('final_mix.wav')),
                '-filter_complex', ';'.join(filt), '-map', '[out]', '-ar', '48000', '-ac', '2', os.path.join(REM, 'public', f('short_mix.wav'))], check=True)
header = cfg.get(f'header_{LANG}') or cfg.get('header', {})   # {"title": "...", "sub": "..."} shown for the first 5 s
json.dump({'durationInFrames': at, 'segments': out, 'header': header},
          open(os.path.join(REM, 'src', f('short.json')), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# Short check (references/shorts_guide.md).
def syllables(word):
    w = re.sub(r'[^a-z]', '', word.lower())
    if not w: return 0
    n = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and not w.endswith('le') and n > 1: n -= 1
    return max(1, n)

said, pauses = [], []
for _, a, b in segs:
    inside = spoken_in(a, b)
    said += inside
    pauses += [x[0] - y[1] for y, x in zip(inside, inside[1:])]
notes = []
first = next((w[0] - segs[0][1] for w in spoken_in(*segs[0][1:])), None)
if first is None: notes.append('no words in the first segment')
elif first > 0.3: notes.append(f'first word comes at {first:.1f}s. Start sooner')
if pauses and max(pauses) > 0.6: notes.append(f'longest pause is {max(pauses):.1f}s. Cut it if it is not a deliberate beat')
if at / FPS > 50: notes.append(f'{at / FPS:.0f}s long. Is every beat earning its place?')
if LANG == 'en' and said:
    tokens = [w[2] for w in said]
    sentences = max(1, sum(1 for w in tokens if w.rstrip()[-1:] in '.?!'))
    syl = sum(syllables(w) for w in tokens)
    grade = 0.39 * len(tokens) / sentences + 11.8 * syl / len(tokens) - 15.59
    hard = sorted({re.sub(r'[^A-Za-z-]', '', w) for w in tokens if syllables(w) >= 3})[:8]
    print(f"[{LANG}] short check: reading grade about {grade:.1f}. Longer words: {', '.join(hard) or 'none'}")
    if grade > 6.5: notes.append('reading level is above the fifth-grade aim. Choose plainer lines if they stay accurate')
empty = [k for k in ('story', 'first_frame', 'hook_line', 'foreshadow', 'mechanism', 'ending', 'why_share') if not cfg.get('brief', {}).get(k)]
if empty: notes.append('short.brief is missing: ' + ', '.join(empty))
for n in notes: print(f'[{LANG}] short check: {n}')
if not notes: print(f'[{LANG}] short check: nothing flagged. Still look at frame 0 with the sound off, and play the last 3 seconds')
print(f"[{LANG}] short: {at / FPS:.1f}s from {len(out)} segments: " + ', '.join(f"{s['name']} {s['dur'] / FPS:.1f}s" for s in out))
