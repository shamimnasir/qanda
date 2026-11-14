# Build the edit timeline (shots, captions, gaps, chapters) from data/shotlist.json and the aligned voiceover words.
# Usage: DOC_LANG=en|bn python3 build_timeline.py
import json, os, re
from common import DATA, FPS, LANG, P, f, load_words, timeline_path

OPENER = P.get('opener')       # the hook: {"to": last word of the opening lines}. Fast music and hard cuts run until then. See the script guide
MAX_SHOT = P.get('max_shot_seconds', 3.0)   # the producer's rule: no visual on screen longer than this
LEAD = 0.0 if OPENER else P.get('lead', 1.2)      # seconds of picture and ambience before the first word (an opener starts at once)
TAIL = P.get('tail', 0.8)      # after the last word, before the end cards
W = load_words()
W_EN = load_words('en')
shots = json.load(open(os.path.join(DATA, 'shotlist.json'), encoding='utf-8'))
assets = json.load(open(os.path.join(DATA, 'assets.json'), encoding='utf-8')) if os.path.exists(os.path.join(DATA, 'assets.json')) else {}

norm = lambda s: re.sub(r"[^a-z0-9']", '', s.lower())
EN_NORM = [norm(w['w']) for w in W_EN]

def find_phrase(phrase, last=False):
    """Index of the first (or last) word of a phrase in the English narration."""
    toks = [norm(x) for x in phrase.split() if norm(x)]
    for i in range(len(EN_NORM) - len(toks) + 1):
        if EN_NORM[i:i + len(toks)] == toks:
            return i + len(toks) - 1 if last else i
    raise SystemExit(f'phrase not found in narration: "{phrase}"')

def word_index(x, last=False):
    return x if isinstance(x, int) else find_phrase(x, last)

def shot_anchor(s):
    """('word', i) | ('after', i) | ('end', n)."""
    w = s.get('w', s.get('at'))
    if 'after' in s: return ('after', word_index(s['after'], last=True))
    if isinstance(w, str) and w.startswith('after:'): return ('after', word_index(int(w[6:]) if w[6:].isdigit() else w[6:], last=True))
    if w in ('end', 'end2'): return ('end', 1 if w == 'end' else 2)
    if 'end' in s: return ('end', s['end'])
    return ('word', word_index(w))

anchors = [shot_anchor(s) for s in shots]

# Gaps opened in the voiceover: cards that sit between lines, extra room for sound moments, chapter breathers.
inserts = {}   # word index the gap follows -> seconds
for s, (kind, i) in zip(shots, anchors):
    if kind == 'after':
        inserts[i] = s['dur']
for g in P.get('gaps', []):
    inserts[word_index(g['after'], last=True)] = g['seconds']
breather = P.get('chapter_gap', 0.7)
if breather:
    prev_ch = None
    for s, (kind, i) in sorted(zip(shots, anchors), key=lambda x: (x[1][0] != 'word', x[1][1])):
        if (kind == 'word' and prev_ch is not None and s['ch'] != prev_ch and i > 0 and s['ch'] not in P.get('chapter_gap_skip', [])
                and not any(abs(i - 1 - k) <= 1 for k in inserts)):
            inserts[i - 1] = breather
        if kind == 'word':
            prev_ch = s['ch']

cuts = sorted(inserts)
cut_t = {k: (W[k]['e'] + W[k + 1]['s']) / 2 for k in cuts}

def tl(t):
    """Voiceover time to film time."""
    return LEAD + t + sum(inserts[k] for k in cuts if cut_t[k] <= t)

def tl_end(t):
    """Like tl(), for the end of a sound: a gap that opens exactly at t comes after it."""
    return LEAD + t + sum(inserts[k] for k in cuts if cut_t[k] < t)

def gap_start(k):
    return LEAD + cut_t[k] + sum(inserts[j] for j in cuts if cut_t[j] < cut_t[k])

vo_end = W[-1]['e']
end_cards = sorted([(i, s) for s, (kind, i) in zip(shots, anchors) if kind == 'end'], key=lambda x: x[0])
total = tl(vo_end) + TAIL + sum(s['dur'] for _, s in end_cards)

pieces, prev = [], 0.0
for k in cuts + [None]:
    end = cut_t[k] if k is not None else vo_end + 0.5
    pieces.append({'from': round(tl(prev) if prev else LEAD, 3), 'voStart': round(prev, 3), 'voEnd': round(end, 3)})
    prev = end

starts = []
for s, (kind, i) in zip(shots, anchors):
    if kind == 'word':
        t = 0.0 if i == 0 else tl(W[i]['s']) - 0.12 - s.get('lead', 0)   # "lead": cut this many seconds before the word
    elif kind == 'after':
        t = gap_start(i)
    else:
        t = tl(vo_end) + TAIL + sum(x['dur'] for n, x in end_cards if n < i)
    starts.append(t)

opener_end = None
if OPENER and OPENER.get('to') is not None:
    opener_end = tl_end(W[word_index(OPENER['to'], last=True)]['e']) + 0.12
QUOTES = P.get('quotes', {}).get(LANG, {})
order = sorted(range(len(shots)), key=lambda i: starts[i])
items = []
for n, i in enumerate(order):
    s = shots[i]
    st = starts[i]
    en = starts[order[n + 1]] if n + 1 < len(order) else total
    if s['kind'] == 'reuse' and s['of'] not in assets:
        # Reusing a graphic: copy it, because a reuse with no media would render a black "missing media" card.
        src = next((x for x in shots if x['id'] == s['of']), None)
        while src and src['kind'] == 'reuse': src = next((x for x in shots if x['id'] == src['of']), None)
        if not src or not src.get('mg'): raise SystemExit(f"shot {s['id']} reuses {s['of']}, which has no picture and no graphic")
        s = {**s, 'kind': src['kind'], 'mg': src['mg'], 'props': src.get('props', {})}
    a = assets.get(s['id']) or (assets.get(s['of']) if s['kind'] == 'reuse' else None)
    props = dict(s.get('props', {}))
    props.update(s.get('props_' + LANG, {}))
    if s.get('mg') == 'credits':
        props.setdefault('lines', P.get('credits', {}).get(LANG) or P.get('credits', {}).get('en', []))
    item = {'id': s['id'], 'kind': s['kind'], 'ch': s['ch'], 'desc': s.get('desc', ''),
            'from': round(st * FPS), 'dur': round(en * FPS) - round(st * FPS),
            'overlay': (s.get('overlay_' + LANG) or s.get('overlay')), 'mg': s.get('mg'), 'props': props, 'lines': s.get('lines')}
    if s.get('hold'): item['hold'] = True    # an approved long moment, allowed past the 3 s limit
    if s.get('tone'): item['tone'] = s['tone']   # gray, cool, night, warm or vivid: plan the film's color arc
    if s.get('cut') == 'hard' or (opener_end is not None and st < opener_end):
        item['hard'] = item['boom'] = True   # no fade in
        if opener_end is not None and st < opener_end:
            item['opener'] = True            # a light sound on the cut, and text that eases in
            if s.get('hit'): item['punch'] = True   # "hit": true on the hook's turn: one soft impact, in picture and sound
    elif P.get('cut_style') == 'hard' and s['kind'] != 'quote':
        item['hard'] = True          # project.json "cut_style": "hard": no soft fades anywhere
    if LANG != 'en' and item['lines']:
        item['lines'] = [[QUOTES.get(who, who), QUOTES.get(what, what)] for who, what in item['lines']]
    if a:
        src_id = s['of'] if s['kind'] == 'reuse' else s['id']
        item['src'] = os.path.basename(a['path']) if a['type'] in ('commons', 'image') else f'clip_{src_id}.mp4'
        item['srcType'] = 'image' if a['type'] in ('commons', 'image') else 'video'
        if a.get('credit'):
            item['credit'] = a['credit']
        elif a['type'] == 'commons':
            item['credit'] = f"{a.get('place', P.get('place', ''))}. Photo: {a['creator']}, {a['license']}".lstrip('. ')
    items.append(item)

# Captions. English: whole sentences when short, else split at natural phrase breaks, never across a gap.
MAX_CHARS = 46
FUNC = {'a', 'an', 'the', 'in', 'of', 'to', 'from', 'and', 'with', 'for', 'on', 'at', 'by', 'our', 'your', 'their',
        'is', 'was', 'be', 'it', 'its', 'that', 'this', 'these', 'one', 'into', 'onto', 'like', 'but', 'so', 'or', 'we', 'you', "you'll", 'he', 'his'}

def chars(g):
    return len(' '.join(W[i]['w'] for i in g))

def split_phrase(g):
    if chars(g) <= MAX_CHARS or len(g) < 2:
        return [g]
    best = None
    for k in range(1, len(g)):
        word = W[g[k - 1]]['w']
        score = abs(chars(g[:k]) - chars(g[k:]))
        if re.search(r'[,:;]$|\.\.\.$', word): score -= 25
        if word.lower().strip(',.?!:') in FUNC: score += 40
        if best is None or score < best[0]: best = (score, k)
    return split_phrase(g[:best[1]]) + split_phrase(g[best[1]:])

captions = []
if LANG == 'en':
    sentences, cur = [], []
    for i, w in enumerate(W):
        cur.append(i)
        nxt = W[i + 1] if i + 1 < len(W) else None
        if (nxt is None or i in inserts or (re.search(r'[.?!]$', w['w']) and not w['w'].endswith('a.m.') and not w['w'].endswith('..'))
                or nxt['s'] - w['e'] > 0.45):
            sentences.append(cur); cur = []
    caps = [p for s in sentences for p in split_phrase(s)]
    for n, g in enumerate(caps):
        st = tl(W[g[0]]['s'])
        en = tl_end(W[g[-1]]['e']) + (0.0 if g[-1] in inserts else 0.2)
        if n + 1 < len(caps): en = min(en, tl(W[caps[n + 1][0]]['s']))
        captions.append({'from': round(st * FPS), 'dur': max(6, round(en * FPS) - round(st * FPS)), 'text': ' '.join(W[i]['w'] for i in g)})
else:
    CB = json.load(open(os.path.join(DATA, f'captions_{LANG}.json'), encoding='utf-8'))
    ends_at_gap = {round(W[k]['e'], 3) for k in inserts}
    for n, c in enumerate(CB):
        st = tl(c['s'])
        en = tl_end(c['e']) + (0.0 if round(c['e'], 3) in ends_at_gap else 0.2)
        if n + 1 < len(CB): en = min(en, tl(CB[n + 1]['s']))
        captions.append({'from': round(st * FPS), 'dur': max(6, round(en * FPS) - round(st * FPS)), 'text': c['text']})

chapters, seen = [], set()
for it in items:
    if it['ch'] not in seen:
        seen.add(it['ch']); chapters.append({'ch': it['ch'], 'from': round(it['from'] / FPS, 3)})
gaps = [{'after_word': k, 'from': round(gap_start(k), 3), 'dur': inserts[k]} for k in cuts]

json.dump({'fps': FPS, 'durationInFrames': round(total * FPS), 'vo': pieces, 'items': items, 'captions': captions,
           'gaps': gaps, 'chapters': chapters, 'opener_end': round(opener_end, 3) if opener_end else None}, open(timeline_path(), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'look': P.get('look', 'cold')}, open(os.path.join(os.path.dirname(timeline_path()), 'look.json'), 'w'))  # film look (theme.ts)
lens = [x['dur'] / FPS for x in items]
print(f"[{LANG}] total {total:.2f}s ({int(total // 60)}:{total % 60:04.1f}), {len(items)} visuals, avg {sum(lens) / len(lens):.2f}s, "
      f"max {max(lens):.2f}s, {len(captions)} captions, {len(gaps)} gaps")

# Hook check (script guide, "The hook").
if not OPENER:
    print(f'[{LANG}] hook check: no opener in project.json. Every new film should state its twist in about the first 10 s, over 3 or 4 shots that follow the voice')
elif opener_end is None:
    print(f'[{LANG}] hook check: set "to" to the last word of the opening lines')
else:
    inside = [x for x in items if x['from'] / FPS < opener_end]
    print(f'[{LANG}] hook check: {opener_end:.1f}s, {len(inside)} hard cuts, first word at {tl(W[0]["s"]):.2f}s')
    if opener_end > 12: print(f'[{LANG}] hook check: longer than about 10 s. Shorten the opening lines or tell the producer')
    fast = [x['id'] for x in inside if x['dur'] / FPS < 1.5 and x['from'] + x['dur'] <= opener_end * FPS]
    if fast: print(f'[{LANG}] hook check: too fast to take in, under 1.5 s: {fast}')
    if items[0]['kind'] == 'mg': print(f"[{LANG}] hook check: the first shot is an animated graphic. Use a strong picture at frame 0")
# Pause check: music and sound need moments alone, where they can actually be heard.
real_pauses = sorted(cut_t[k] for k in cuts if inserts[k] >= 1.0)
marks = [0.0] + real_pauses + [vo_end]; stretch = max(b - a for a, b in zip(marks, marks[1:]))
print(f'[{LANG}] pause check: {len(real_pauses)} pauses of 1 s or more, longest stretch without one {stretch:.0f} s (aim for 30 s or less)')
if stretch > 30 and LANG == 'en':
    ends = [i for i, x in enumerate(W[:-1]) if x['w'].rstrip('"').endswith(('.', '?', '!'))]
    want, ideas = 25.0, []
    while want < vo_end - 10:
        i = min(ends, key=lambda e: abs(W[e]['e'] - want)); ideas.append(i); want = W[i]['e'] + 25
    print(f'[{LANG}] pause check: add shots with "after": N and "dur": 1.2 (a strong picture and a sound moment). Sentence ends to try: {ideas}')
held = [(x['id'], round(x['dur'] / FPS, 2)) for x in items if x.get('hold')]
if held: print(f'[{LANG}] shot check: approved holds past the limit: {held}. The producer must have agreed to each')
over = [(x['id'], round(x['dur'] / FPS, 2)) for x in items if x['dur'] / FPS > MAX_SHOT + 0.01 and not x.get('hold')]
if over: print(f'[{LANG}] shot check: {len(over)} visuals over {MAX_SHOT} s (add a cut at a word, or "lead" on the next shot): {over}')
else: print(f'[{LANG}] shot check: every visual is {MAX_SHOT} s or less')
