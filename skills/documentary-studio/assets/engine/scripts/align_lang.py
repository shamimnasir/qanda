# Time a non-English voiceover (for example Bangla) against the English shot anchors, without speech recognition.
# Whisper cannot reliably transcribe languages like Bangla, so sentences are fitted to the take's pauses by dynamic
# programming: each sentence's speaking time should match its letter count at the take's average rate, and sentence
# breaks should land in pauses. Check: every [long pause] tag in the script should land on a long silence.
# Usage: DOC_LANG=bn python3 align_lang.py
# Writes data/vo_words_virtual_<lang>.json (English word indices timed to this audio) and data/captions_<lang>.json.
import json, os, re, subprocess
from common import DATA, LANG, P, duration, vo_path

assert LANG != 'en', 'run with DOC_LANG set to the other language, for example DOC_LANG=bn'
VO = vo_path()
S = json.load(open(os.path.join(DATA, 'sentences.json'), encoding='utf-8'))
W_EN = json.load(open(os.path.join(DATA, 'vo_words_en.json')))
PUNCT = r'[\s.,:;?!।"“”\'‘’]'
sentences = [{'en': s['en_word'], 'text': s[LANG], 'L': max(1, len(re.sub(PUNCT, '', s[LANG])))} for s in S]

dur = duration(VO)
NOISE = P.get('languages', {}).get(LANG, {}).get('silence_db', -38)
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', VO, '-af', f'silencedetect=noise={NOISE}dB:d=0.3', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', log)]
en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', log)]
sil = [(a, b) for a, b in zip(st, en) if b > a]
onset = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
sil = [x for x in sil if x[0] >= 0.05 and x[1] < dur - 0.05]
nodes = [(onset, onset)] + sil + [(dur, dur)]
pre = [0.0]
for a, b in nodes:
    pre.append(pre[-1] + (b - a))
total_L = sum(s['L'] for s in sentences)
rate = total_L / ((nodes[-1][0] - nodes[0][1]) - sum(b - a for a, b in nodes[1:-1]))

def span_cost(i, j, group):
    t0, t1 = nodes[i][1], nodes[j][0]
    if t1 <= t0:
        return None
    inner = pre[j] - pre[i + 1]
    speech = (t1 - t0) - inner
    exp = sum(sentences[k]['L'] for k in group) / rate
    c = ((speech - exp) / (0.22 * exp + 0.35)) ** 2
    soft = any(re.search(r'\.\.\.|,|:', sentences[k]['text']) for k in group)
    return c + (0.6 if soft else 2.5) * inner + 0.4 * (j - i - 1) + 3.0 * (len(group) - 1)

K, J, INF = len(sentences), len(nodes), float('inf')
best = [[INF] * J for _ in range(K + 1)]
back = [[None] * J for _ in range(K + 1)]
best[0][0] = 0.0
for k in range(1, K + 1):
    for j in range(1, J):
        for g in (1, 2, 3):
            k0 = k - g
            if k0 < 0: break
            for i in range(j):
                if best[k0][i] == INF: continue
                c = span_cost(i, j, list(range(k0, k)))
                if c is not None and best[k0][i] + c < best[k][j]:
                    best[k][j] = best[k0][i] + c; back[k][j] = (k0, i)
if best[K][J - 1] == INF:
    raise SystemExit('no alignment found: does the audio match the script?')
groups, k, j = [], K, J - 1
while k > 0:
    k0, i = back[k][j]; groups.append((k0, k, i, j)); k, j = k0, i
groups.reverse()

def speech_map(t0, t1):
    pieces, cur = [], t0
    for a, b in [(a, b) for a, b in sil if a > t0 and b < t1]:
        pieces.append((cur, a)); cur = b
    return pieces + [(cur, t1)]

def at_fraction(pieces, frac):
    target = frac * sum(b - a for a, b in pieces)
    for a, b in pieces:
        if target <= b - a: return a + target
        target -= b - a
    return pieces[-1][1]

for k0, k1, i, j in groups:
    pieces = speech_map(nodes[i][1], nodes[j][0])
    L, acc = sum(sentences[k]['L'] for k in range(k0, k1)), 0
    for k in range(k0, k1):
        s = sentences[k]
        s['s'] = at_fraction(pieces, acc / L); acc += s['L']; s['e'] = at_fraction(pieces, acc / L)
        s['pieces'] = speech_map(s['s'], s['e'])

virtual = []
for k, snt in enumerate(sentences):
    a = snt['en']; b = sentences[k + 1]['en'] if k + 1 < len(sentences) else len(W_EN)
    words = [W_EN[i]['w'] for i in range(a, b)]
    total, off = len(' '.join(words)), 0
    for wd in words:
        virtual.append({'w': wd, 's': round(at_fraction(snt['pieces'], off / total), 3),
                        'e': round(at_fraction(snt['pieces'], (off + len(wd)) / total), 3)})
        off += len(wd) + 1
json.dump(virtual, open(os.path.join(DATA, f'vo_words_virtual_{LANG}.json'), 'w'), indent=0)

# Captions: whole sentences up to MAX characters, else split at commas or ellipses, timed by letter share.
MAX = 40
def split(text):
    if len(text) <= MAX: return [text]
    best = None
    for m in re.finditer(r'[,:]\s|\.\.\.\s|\s', text):
        left, right = text[:m.end()].strip(), text[m.end():].strip()
        if not left or not right: continue
        score = abs(len(left) - len(right)) - (25 if m.group().strip() else 0)
        if best is None or score < best[0]: best = (score, m.end())
    return [text] if best is None else split(text[:best[1]].strip()) + split(text[best[1]:].strip())
caps = []
for snt in sentences:
    parts, done = split(snt['text']), 0
    for n, ptxt in enumerate(parts):
        L = len(re.sub(PUNCT, '', ptxt))
        s0 = at_fraction(snt['pieces'], done / snt['L']); done += L
        s1 = snt['e'] if n == len(parts) - 1 else at_fraction(snt['pieces'], min(1, done / snt['L']))
        caps.append({'s': round(s0, 3), 'e': round(max(s1, s0 + 0.4), 3), 'text': ptxt, 'en': snt['en']})
json.dump(caps, open(os.path.join(DATA, f'captions_{LANG}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

long_sil = [(a, b) for a, b in sil if b - a >= 0.9]
starts_after_long = sum(1 for s in sentences if any(abs(b - s['s']) < 0.15 for a, b in long_sil))
print(f'[{LANG}] rate {rate:.1f} letters/s, {len(sil)} pauses ({len(long_sil)} long), {len(sentences)} sentences in {len(groups)} spans, '
      f'{starts_after_long} sentences start right after a long pause, {len(caps)} captions')
