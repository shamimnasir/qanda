# Compose an original score for this film, shaped by the edit. Everything is synthesized here: no samples, no third-party audio.
#
# Three promises (see references/music_guide.md):
#   Soft:   warm timbres only, nothing bright or metallic. It checks itself and prints a WARNING if the 2 to 6 kHz range is too strong.
#   Unique: each film gets its own key, scale, chords, tempo, motif and instruments, derived from its slug and checked against
#           ../_Channel/score_ledger.json so no two films share a sound. In the plan, "variation": 2 asks for another one.
#   Mapped: each run writes 07_Music_SFX/music_story_arc.md, one page showing every section's mood, energy and feel.
#   Opener: a film with an opener in project.json gets the mood "flash" for those seconds: no fade in, a fast soft beat, a chord on each cut.
#   Paced:  tempo comes from the narration speed, the energy curve from the sections, narration density and cut rate. Chords land
#           on cuts, melody phrases sit in the pauses between lines, and the music lifts in every gap.
#
# "score": {
#   "mode": "minor" or "major",
#   "sections": [{"from": anchor, "to": anchor, "mood": "dread", "level": 1.0}, ...],
#   "hits":  [{"at": anchor, "size": 0.8, "riser": 3.5, "drop": 0.35}],   riser/drop are seconds before the hit
#   "drops": [{"from": anchor, "to": anchor}],                             short silences for tension
#   "variation": 1, "key": "D", "keep_key": true                           optional: re-roll, or force the key
#   each section may add "feel": one sentence on what the viewer should feel, shown in the Music Story Arc
# }
# Moods: flash (automatic), dread, tension, suspense, hush, curious, pulse, drive, light, awe, warm, silence.
# Usage: DOC_LANG=en|bn python3 build_score.py <tmp dir> [output.wav]. A custom output is a trial: the ledger is not changed.
import hashlib, json, os, subprocess, sys
import numpy as np
from common import FPS, P, ROOT, SFX_DIR, SR, Anchors, f, load_timeline, load_words

TMP = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SFX_DIR, f('score.wav'))
TRIAL = len(sys.argv) > 2
ISR = 24000
MAX_HZ = 5000          # no partial above this, which is what keeps the score from sounding harsh
TL = load_timeline()
WORDS = load_words()
A = Anchors(TL, WORDS)
T = A.T
N = int(T * ISR)
PLAN = P['score']
MODE = PLAN.get('mode', 'minor')
NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}

# Chord: (semitones above the tonic, quality). m minor, M major, s open sus2 chord.
PROGS = {
    'minor': {
        'still': [(0, 'm'), (8, 'M'), (3, 'M'), (10, 'M')],
        'turning': [(0, 'm'), (5, 'm'), (8, 'M'), (7, 's')],
        'climbing': [(0, 'm'), (10, 'M'), (8, 'M'), (10, 'M')],
        'open': [(0, 'm'), (3, 'M'), (10, 'M'), (5, 'm')],
        'searching': [(0, 's'), (8, 'M'), (5, 'm'), (10, 's')],
    },
    'major': {
        'home': [(0, 'M'), (7, 'M'), (9, 'm'), (5, 'M')],
        'lift': [(0, 'M'), (4, 'm'), (5, 'M'), (7, 's')],
        'wide': [(0, 's'), (5, 'M'), (9, 'm'), (7, 'M')],
        'step': [(0, 'M'), (5, 'M'), (2, 'm'), (7, 'M')],
    },
}
SCALES = {'minor': {'aeolian': [0, 2, 3, 5, 7, 8, 10], 'dorian': [0, 2, 3, 5, 7, 9, 10]},
          'major': {'ionian': [0, 2, 4, 5, 7, 9, 11], 'mixolydian': [0, 2, 4, 5, 7, 9, 10]}}
BRIGHT_PROG = [(0, 'M'), (5, 'M'), (9, 'm'), (7, 's')]
PADS = {
    'felt_strings': ((1, 1.0), (2, 0.5), (3, 0.24), (4, 0.11), (5, 0.05)),
    'warm_choir': ((1, 1.0), (2, 0.3), (3, 0.34), (4, 0.08), (5, 0.1)),
    'soft_organ': ((1, 1.0), (2, 0.62), (3, 0.14), (4, 0.2)),
    'hollow_air': ((1, 1.0), (3, 0.3), (5, 0.1), (7, 0.03)),
}
LEADS = {  # (partials, decay per second, attack seconds)
    'felt_piano': (((1, 1.0), (2, 0.42), (3, 0.14), (4, 0.05)), 1.1, 0.012),
    'soft_mallet': (((1, 1.0), (4, 0.09)), 2.2, 0.009),
    'nylon_pluck': (((1, 1.0), (2, 0.36), (3, 0.1)), 2.8, 0.008),
    'music_box_low': (((1, 1.0), (2, 0.12), (3, 0.05)), 1.5, 0.014),
}

def signature(salt):
    r = np.random.default_rng(int.from_bytes(hashlib.sha256(f"{P.get('slug', 'film')}:{salt}".encode()).digest()[:8], 'big'))
    progs, scales = PROGS[MODE], SCALES[MODE]
    return {
        'key': PLAN['key'] if PLAN.get('keep_key') else str(r.choice(NOTES)), 'mode': MODE,
        'scale': str(r.choice(sorted(scales))), 'progression': str(r.choice(sorted(progs))),
        'pad': str(r.choice(sorted(PADS))), 'lead': str(r.choice(sorted(LEADS))),
        'tempo_shift': round(float(r.uniform(-5, 5)), 2), 'motif_seed': int(r.integers(1, 1 << 30)),
    }

def clashes(a, b):
    return (a['key'], a['progression']) == (b['key'], b['progression']) or (a['pad'], a['lead'], a['progression']) == (b['pad'], b['lead'], b['progression'])

LEDGER = os.path.join(os.path.dirname(ROOT), '_Channel', 'score_ledger.json')
others = {}
if os.path.exists(LEDGER):
    others = {k: v for k, v in json.load(open(LEDGER, encoding='utf-8')).items() if k != P.get('slug')}
salt = PLAN.get('variation', 1)
SIG = signature(salt)
while any(clashes(SIG, o) for o in others.values()):
    salt = f'{salt}+'
    SIG = signature(salt)

pc = PC[SIG['key']]
R = (36 if pc <= 6 else 24) + pc     # tonic, 65 to 98 Hz or so
rng = np.random.default_rng(SIG['motif_seed'])
PAD, LEAD = PADS[SIG['pad']], LEADS[SIG['lead']]
SCALE = SCALES[MODE][SIG['scale']]
PROG = PROGS[MODE][SIG['progression']]
RELATIVE = 3 if MODE == 'minor' else 0   # bright moods move to the relative major

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def spread(root, q):
    third = {'m': 3, 'M': 4, 's': 2}[q]
    return [root + 12, root + 19, root + 24 + third, root + 31]

MOOD = {  # energy 0 to 1, brightness of the pad, which harmony, and how the middle layer moves
    'dread': dict(e=0.28, br=0.26, harm='drone', arp=None),
    'tension': dict(e=0.42, br=0.3, harm='film', arp='slow'),
    'suspense': dict(e=0.5, br=0.32, harm='film', arp='low'),
    'hush': dict(e=0.14, br=0.28, harm='film', arp=None),
    'curious': dict(e=0.46, br=0.44, harm='film', arp='walk'),
    'pulse': dict(e=0.56, br=0.4, harm='film', arp='pulse'),
    'drive': dict(e=0.74, br=0.5, harm='film', arp='walk'),
    'light': dict(e=0.6, br=0.54, harm='bright', arp='walk'),
    'awe': dict(e=0.76, br=0.58, harm='bright', arp='slow'),
    'warm': dict(e=0.5, br=0.52, harm='bright', arp='slow'),
    'flash': dict(e=1.0, br=0.62, harm='film', arp='flash'),     # the opener: exciting and driving, still with no harsh sound
    'silence': dict(e=0.0, br=0.2, harm='film', arp=None),
}

# ---- Read the film: narration, cuts, sections, hits ----
CR = 20  # control rate, Hz
CN = int(T * CR) + 1
ct = np.arange(CN) / CR
speaking = np.zeros(CN)
starts = np.zeros(CN)
sentence_ends = []
for w in WORDS:
    try:
        s, e = A.film_t(w['s']), A.film_t(w['e'])
    except ValueError:
        continue
    speaking[int(s * CR): int(e * CR) + 1] = 1
    starts[min(CN - 1, int(s * CR))] += 1
    if w['w'].rstrip()[-1:] in ('.', '?', '!'): sentence_ends.append(e)
cut_times = sorted({x['from'] / FPS for x in TL['items']})
cuts = np.zeros(CN)
for c in cut_times:
    cuts[min(CN - 1, int(c * CR))] += 1

def box(x, secs):
    k = max(1, int(secs * CR))
    return np.convolve(x, np.ones(k) / k, mode='same')

spoken = max(1.0, speaking.sum() / CR)
WPS = max(0.5, starts.sum() / spoken)
BPM = float(np.clip(WPS * 26 + SIG['tempo_shift'], 54, 98))   # faster narration, faster music
BEAT = 60 / BPM
BAR = BEAT * 4

OPENER_END = TL.get('opener_end')
SECTIONS = [dict(s) for s in PLAN['sections']]
sections = [(A(s['from']), A(s['to']), s['mood'], s.get('level', 1.0)) for s in SECTIONS]
if OPENER_END:      # the opener always gets its own burst of music, and the plan's first section starts after it
    sections = [(max(a, OPENER_END), b, m, L) for a, b, m, L in sections if b > OPENER_END]
    sections.insert(0, (0.0, OPENER_END, 'flash', 1.0))
    SECTIONS = [{'feel': 'Exciting: the whole story in a few seconds, on hard cuts'}] + SECTIONS[-(len(sections) - 1):]
def section_at(t):
    for a, b, m, L in sections:
        if a <= t < b: return m, L
    return (sections[-1][2], sections[-1][3]) if t >= sections[-1][0] else (sections[0][2], sections[0][3])

base = np.array([(lambda m, L: MOOD[m]['e'] * L)(*section_at(x)) for x in ct])
pace = np.clip(box(starts, 6) * CR / WPS - 1, -1, 1)
rate = np.clip(box(cuts, 8) * CR / max(1e-3, cuts.sum() / T) - 1, -1, 1)
energy = base + 0.09 * pace + 0.07 * rate
hits = [(A(h['at']), h) for h in PLAN.get('hits', [])]
for at, h in hits:
    size, lead = h.get('size', 0.8), max(h.get('riser', 0) or 0, 1.5)
    energy += 0.3 * size * np.clip((ct - (at - lead * 1.6)) / (lead * 1.6), 0, 1) ** 2 * (ct < at)   # climb into it
    energy += 0.26 * size * np.exp(-np.clip(ct - at, 0, None) / 3.5) * (ct >= at)                    # settle after it
k = int(1.2 * CR)
energy = np.convolve(energy, np.hanning(2 * k + 1) / np.hanning(2 * k + 1).sum(), mode='same')
lo, hi = np.percentile(energy, 5), np.percentile(energy, 97)   # use the whole range: real lows and real peaks in every film
energy = np.clip(0.1 + 0.9 * (energy - lo) / max(0.05, hi - lo), 0.04, 1)
if OPENER_END: energy[ct < OPENER_END] = 1.0
def E(t): return float(np.interp(t, ct, energy))

# ---- Instruments ----
M = np.zeros(N)
air = np.fft.rfft(rng.standard_normal(N))
fq = np.fft.rfftfreq(N, 1 / ISR)
air *= 1 / (1 + (fq / 700) ** 2) / np.sqrt(np.maximum(fq, 40))
air = np.fft.irfft(air, N)
air /= np.abs(air).max() + 1e-9

def span(a, b):
    i, j = max(0, int(a * ISR)), min(N, int(b * ISR))
    return i, j, np.arange(i, j) / ISR

def pad(notes, a, b, amp, br, att=1.4, rel=1.6):
    i, j, tt = span(a, b + rel)
    if j <= i: return
    env = np.clip((tt - a) / att, 0, 1) ** 2 * np.clip((b + rel - tt) / rel, 0, 1) ** 2
    out = np.zeros(j - i)
    for m in notes:
        fr = hz(m)
        for det in (-0.0028, 0.0, 0.0031):
            ph, drift = rng.uniform(0, 6.28), rng.uniform(0.04, 0.11)
            for n, w in PAD:
                if fr * n > MAX_HZ: continue
                out += np.sin(2 * np.pi * fr * n * (1 + det) * tt + ph * n) * w * br ** (n - 1) * (0.86 + 0.14 * np.sin(2 * np.pi * drift * tt + ph))
    M[i:j] += out / (len(notes) * 3) * env * amp

def note(m, at, amp, length=None):
    parts, decay, att = LEAD
    dur = length or min(4.0, 4.5 / decay)
    i, j, tt = span(at, at + dur)
    if j <= i: return
    x, fr = tt - at, hz(m)
    out = np.zeros(j - i)
    for n, w in parts:
        if fr * n <= MAX_HZ:
            out += np.sin(2 * np.pi * fr * n * x) * w * np.exp(-x * decay * (1 + 0.35 * (n - 1)))
    M[i:j] += out * np.clip(x / att, 0, 1) * np.clip((dur - x) / 0.2, 0, 1) * amp

def sub(m, a, b, amp):
    i, j, tt = span(a, b + 0.6)
    if j <= i: return
    env = np.clip((tt - a) / 0.5, 0, 1) * np.clip((b + 0.6 - tt) / 0.6, 0, 1)
    M[i:j] += np.sin(2 * np.pi * hz(m) * tt) * env * amp

def soft_beat(at, amp):
    i, j, tt = span(at, at + 0.55)
    x = tt - at
    M[i:j] += np.sin(2 * np.pi * (46 * x + 3.2 * (1 - np.exp(-x * 26)))) * np.clip(x / 0.012, 0, 1) * np.exp(-x * 7.5) * amp

def swell_hit(at, amp, chord, root):
    """A low bloom on the key line, in place of a loud braam."""
    i, j, tt = span(at, at + 3.4)
    x = tt - at
    M[i:j] += np.sin(2 * np.pi * hz(root - 12 if hz(root) > 70 else root) * x) * np.clip(x / 0.07, 0, 1) * np.exp(-x * 1.25) * amp * 0.85
    pad(chord, at, at + 0.9, amp * 0.8, 0.5, att=0.14, rel=2.2)

def rise(a, b, amp, chord):
    i, j, tt = span(a, b)
    if j <= i: return
    x = np.clip((tt - a) / (b - a), 0, 1)
    M[i:j] += air[i:j] * x ** 2.4 * amp * 1.1
    pad(chord, a, b, amp * 0.8, 0.46, att=(b - a) * 0.8, rel=0.15)

# ---- A motif that belongs to this film ----
def make_motif():
    deg, out = int(rng.integers(0, 5)), []
    for _ in range(int(rng.integers(5, 8))):
        out.append(deg)
        deg = int(np.clip(deg + rng.choice([-2, -1, -1, 1, 1, 2, 3]), 0, 9))
    return out, [float(x) for x in rng.choice([1, 1, 1.5, 2, 0.5], len(out))]
MOTIF, RHYTHM = make_motif()

def scale_note(deg, root, top):
    return root + 12 * top + SCALE[deg % 7] + 12 * (deg // 7)

# ---- Lay chords on the edit ----
forced = sorted({a for a, *_ in sections} | {at for at, _ in hits} | ({c for c in cut_times if c < OPENER_END} if OPENER_END else set()))
counts = {'film': 0, 'bright': 0}
t0, segs = 0.0, []
while t0 < T - 0.05:
    e = E(t0)
    length = BAR * (1 if e > 0.74 else 2 if e > 0.34 else 4)
    nominal = t0 + length
    nf = next((x for x in forced if x > t0 + 0.6), None)
    if nf is not None and nf < nominal + 0.5 * BAR:
        t1 = nf
    else:
        near = [c for c in cut_times if abs(c - nominal) <= 0.3 * length and c > t0 + 0.6]
        t1 = min(near, key=lambda c: abs(c - nominal)) if near else nominal
    segs.append((t0, min(t1, T)))
    t0 = t1

for a, b in segs:
    mid = (a + b) / 2
    mood, _ = section_at(a + 0.01)
    if mood == 'silence': continue
    cfg, e = MOOD[mood], E(mid)
    if cfg['harm'] == 'drone':
        offset, q = 0, 'm' if MODE == 'minor' else 'M'
    elif cfg['harm'] == 'bright':
        offset, q = BRIGHT_PROG[counts['bright'] % 4]; offset += RELATIVE; counts['bright'] += 1
    else:
        offset, q = PROG[counts['film'] % 4]; counts['film'] += 1
    root = R + offset
    while root > R + 7: root -= 12
    chord = spread(root, q)
    flash = mood == 'flash'
    pad(chord, a, b, 0.2 + 0.26 * e, cfg['br'] * (0.72 + 0.56 * e), att=0.03 if flash else min(1.6, (b - a) * 0.5), rel=0.3 if flash else 1.6)
    if e > 0.22: sub(root, a, b, 0.11 + 0.1 * e)
    tones = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[3], chord[2] + 12, chord[1] + 12]
    arp = cfg['arp']
    if arp:
        step = {'slow': BEAT * 2, 'low': BEAT, 'pulse': BEAT / 2, 'walk': BEAT if e < 0.62 else BEAT / 2, 'flash': 60 / max(BPM * 1.5, 112) / 2}[arp]
        for n_, at in enumerate(np.arange(a + 0.03, b - 0.05, step)):
            talking = float(np.interp(at, ct, box(speaking, 0.6)))
            if step < BEAT and n_ % 2 and talking > 0.6 and not flash: continue   # fewer notes under words, not only quieter ones
            quiet = 1 - 0.35 * talking                                        # step back while a line is spoken
            pitch = root + 12 if arp == 'low' else (chord[0] + 12 if arp == 'pulse' else tones[n_ % len(tones)])
            note(pitch, at, (0.06 + 0.11 * e) * quiet)
    if flash:
        soft_beat(a, 0.32)
        for at in np.arange(a + 60 / max(BPM * 1.5, 112), b - 0.05, 60 / max(BPM * 1.5, 112)):
            soft_beat(at, 0.2)
    if mood in ('drive', 'pulse') and e > 0.6:
        for at in np.arange(a, b - 0.05, BEAT * 2):
            soft_beat(at, 0.08 + 0.1 * (e - 0.6) / 0.4)
    if mood == 'dread' and e > 0.3:
        for at in np.arange(a + BEAT, b - 0.1, BEAT * 4):
            soft_beat(at, 0.09)

# ---- Melody phrases in the pauses, never over the words ----
pockets, x = [], 0
quiet_mask = box(speaking, 0.15) < 0.05
while x < CN:
    if quiet_mask[x]:
        y = x
        while y < CN and quiet_mask[y]: y += 1
        if (y - x) / CR >= 0.25: pockets.append((x / CR, y / CR))
        x = y
    else:
        x += 1
# Narration often runs without a real pause, so a sentence end is also a place for the music to answer.
pockets = sorted(pockets + [(e, e + 0.35) for e in sentence_ends])
last_end, phrase = -9.0, 0
for a, b in pockets:
    mood, _ = section_at(a + 0.01)
    if mood in ('silence', 'hush', 'flash') or a < last_end + BAR * 1.5: continue
    at, e, shift = a + 0.04, E(a), phrase % 3
    room = max(b, a + 1.5 * BEAT)        # a short phrase may lean into the next line, where the music is already ducked
    for d, r in zip(MOTIF[shift:], RHYTHM[shift:]):
        if at > room: break
        tonic = R + (RELATIVE if MOOD[mood]['harm'] == 'bright' else 0)
        note(scale_note(d, tonic, 3), at, 0.11 + 0.11 * e)
        at += r * BEAT
    last_end, phrase = at, phrase + 1
for a, b, m, _ in sections:      # in a warm close the melody may simply sing
    if m == 'warm':
        at, n_ = a + 1.0, 0
        while at < b - 3:
            d, r = MOTIF[n_ % len(MOTIF)], RHYTHM[n_ % len(RHYTHM)]
            quiet = 1 - 0.55 * float(np.interp(at, ct, box(speaking, 0.5)))
            note(scale_note(d, R + RELATIVE, 3), at, 0.11 * quiet)
            at += r * BEAT * 2; n_ += 1

# ---- Rises and hits ----
if OPENER_END:      # the Result line lands, then the music opens out into the film
    swell_hit(OPENER_END, 0.34, spread(R, 'm' if MODE == 'minor' else 'M'), R)
for at, h in hits:
    size, d = h.get('size', 0.8), h.get('drop', 0.3)
    mood, _ = section_at(at + 0.01)
    root = R + (RELATIVE if MOOD[mood]['harm'] == 'bright' else 0)
    while root > R + 7: root -= 12
    q = 'M' if MOOD[mood]['harm'] == 'bright' or MODE == 'major' else 'm'
    if h.get('riser'): rise(at - h['riser'], at - d, 0.2 * size, spread(root, 's'))
    swell_hit(at, 0.36 * size, spread(root, q), root)

# A breath of air under everything, following the energy.
env = np.interp(np.arange(N) / ISR, ct, energy)
M += air * (0.012 + 0.03 * env)

# ---- Room, tone and shape ----
ir_n = int(2.8 * ISR)
ix = np.arange(ir_n) / ISR
ir = np.random.default_rng(29).standard_normal(ir_n) * np.exp(-ix * 2.3) * np.clip(ix / 0.018, 0, 1)
size = N + ir_n
spec_ir = np.fft.rfft(ir, size)
fq2 = np.fft.rfftfreq(size, 1 / ISR)
spec_ir *= 1 / (1 + (fq2 / 2300) ** 2)
spec = np.fft.rfft(M, size)
wet = np.fft.irfft(spec * spec_ir, size)[:N]
wet *= np.sqrt((M ** 2).mean() / ((wet ** 2).mean() + 1e-12))
# Stereo: a second room for the other side, plus a short delay, kept only in the side signal. Left plus right still equals the mono score.
WIDTH = PLAN.get('width', 1.0)
ir2 = np.random.default_rng(31).standard_normal(ir_n) * np.exp(-ix * 2.3) * np.clip(ix / 0.018, 0, 1)
wet2 = np.fft.irfft(spec * np.fft.rfft(ir2, size) * (1 / (1 + (fq2 / 2300) ** 2)), size)[:N]
wet2 *= np.sqrt((M ** 2).mean() / ((wet2 ** 2).mean() + 1e-12))
SIDE = WIDTH * (0.32 * (wet - wet2) + 0.22 * np.roll(M, int(0.013 * ISR)))
M = 0.8 * M + 0.42 * wet
spec = np.fft.rfft(M)
fq = np.fft.rfftfreq(N, 1 / ISR)
BR = PLAN.get('brightness', 1.0)   # 1: detail up to about 9 kHz. 0: the older, darker score
db = -(22 - 8 * BR) * np.clip(np.log2(np.maximum(fq, 1) / (2200 + 1000 * BR)) / np.log2((6500 + 2500 * BR) / (2200 + 1000 * BR)), 0, 1)   # a soft tilt
db -= 18 * np.clip(np.log2(34 / np.maximum(fq, 1)), 0, 2)                            # no rumble
M = np.fft.irfft(spec * 10 ** (db / 20), N)
SIDE = np.fft.irfft(np.fft.rfft(SIDE) * 10 ** ((db - 24 * np.clip(np.log2(220 / np.maximum(fq, 1)), 0, 2)) / 20), N)   # bass stays centered

# Lift in the gaps between lines, dip under the voice, and shape with the energy curve.
lift = np.convolve(1 - box(speaking, 0.4), np.hanning(int(1.0 * CR)) / np.hanning(int(1.0 * CR)).sum(), mode='same')
breath = sum(np.exp(-((ct - e - 0.15) / 0.4) ** 2) for e in sentence_ends) if sentence_ends else 0   # lifts as each sentence lands
shape = (0.4 + 0.6 * energy) * (0.9 + 0.3 * lift + 0.1 * np.clip(breath, 0, 1))
shape *= np.clip(np.minimum(ct / (0.02 if OPENER_END else 2.0), (T - ct) / 3.5), 0, 1)
tt = np.arange(N) / ISR
M *= np.interp(tt, ct, shape)
SIDE *= np.interp(tt, ct, shape)
G = np.ones(N)
drops = [(A(d['from']), A(d['to'])) for d in PLAN.get('drops', [])]
drops += [(at - h['drop'], at - 0.02) for at, h in hits if h.get('drop')]
drops += [(a, b) for a, b, m, _ in sections if m == 'silence']
for a, b in drops:
    fade = 0.09
    G *= 1 - np.clip((tt - (a - fade)) / fade, 0, 1) * np.clip(((b + 0.03) - tt) / 0.03, 0, 1)
M *= G
SIDE *= G
LEVEL = 10 ** (-23 / 20) / (np.sqrt((M ** 2).mean()) + 1e-9)
M *= LEVEL
SIDE *= LEVEL
ST = np.stack([M + SIDE, M - SIDE], axis=1)
ST = 0.92 * np.tanh(ST / 0.92)     # rounds any peak instead of clipping it
M = ST.mean(axis=1)

raw = os.path.join(TMP, f('score_dry.f32'))
ST.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(ISR), '-ac', '2', '-i', raw, '-ar', str(SR), OUT], check=True)

# ---- Check it: nothing here can listen, so measure what makes music harsh ----
w, hop = 4096, 2048
win = np.hanning(w)
S = np.array([np.abs(np.fft.rfft(M[i:i + w] * win)) ** 2 for i in range(0, max(1, N - w), hop)])
fw = np.fft.rfftfreq(w, 1 / ISR)
total = S.sum(1) + 1e-15
loud = total > 10 ** (-5) * total.max()
share = S[:, (fw >= 2000) & (fw < 6000)].sum(1) / total
worst = float(np.percentile(share[loud], 99)) if loud.any() else 0.0
rms = np.sqrt(np.convolve(M ** 2, np.ones(ISR * 3) / (ISR * 3), mode='same')[::ISR])
rms_db = 20 * np.log10(np.maximum(rms, 1e-5))
moving = rms_db[int(4): max(5, len(rms_db) - 4)]
swing = float(np.percentile(moving, 95) - np.percentile(moving, 10))
print(f"score: {T:.1f}s, {SIG['key']} {SIG['mode']} ({SIG['scale']}), {SIG['progression']} chords, {SIG['pad']} with {SIG['lead']}, {BPM:.0f} BPM from {WPS:.2f} words per second")
print(f"score: {len(segs)} chord changes on the edit, {len(sections)} sections, {len(hits)} hits, {phrase} melody phrases in the pauses")
print(f"score check: stereo correlation {np.corrcoef(ST[::50, 0], ST[::50, 1])[0, 1]:.2f} (want 0.5 to 0.9)")
print(f"score check: 2-6 kHz share at the harshest moments {worst * 100:.1f}% (limit 6%), loud to quiet range {swing:.1f} dB (want 8 to 18)")
if worst > 0.06: print('WARNING: the score may sound harsh. Lower the brightness of the moods used here.')
if swing < 8: print('WARNING: the score is flat. Vary the sections, levels and hits so it has real ups and lows.')
if swing > 18: print('WARNING: the quiet parts may disappear under the voice. Raise the levels of the quietest sections.')
rests = [b - a for a, b in drops if b - a >= 1.5]
opening = float(energy[: int(min(25, T) * CR)].mean())
if not OPENER_END: print('Reminder: no opener. Every new film should open with exciting music over the hook.')
if opening < 0.25: print(f'Reminder: the first 25 s have low music energy ({opening:.2f}). The hook is where viewers decide, so check that the opening does not feel empty.')
if not rests: print('Reminder: no moment of 1.5 s or more without music. Ask whether one strong moment would hit harder with silence or ambience.')
arc = ['# Music Story Arc', '', f"{SIG['key']} {SIG['mode']}, {SIG['scale']}, {SIG['pad']} with {SIG['lead']}, {BPM:.0f} BPM. Check for too much or too little music, and whether the rises fall where the story turns.", '',
       '| Time | Length | Mood | Energy | Feel |', '|---|---|---|---|---|']
for s, (a, b, m, _) in zip(SECTIONS, sections):
    keep = (ct >= a) & (ct < b)
    level = float(energy[keep].mean()) if keep.any() else 0.0
    arc.append(f"| {int(a // 60)}:{int(a % 60):02d} | {b - a:.0f} s | {m} | {'#' * max(1, round(level * 10))} {level:.2f} | {s.get('feel', 'not written')} |")
arc += ['', '| Hit | Size | Rise |', '|---|---|---|'] + [f"| {int(at // 60)}:{int(at % 60):02d} | {h.get('size', 0.8)} | {h.get('riser') or 'none'} |" for at, h in hits]
if not TRIAL:
    open(os.path.join(SFX_DIR, f('music_story_arc.md')), 'w', encoding='utf-8').write('\n'.join(arc) + '\n')
    if os.path.isdir(os.path.dirname(LEDGER)):
        book = dict(others); book[P.get('slug', 'film')] = SIG
        json.dump(book, open(LEDGER, 'w', encoding='utf-8'), indent=1)
    json.dump({**SIG, 'bpm': round(BPM, 1), 'energy_every_second': [round(float(x), 2) for x in energy[::CR]]},
              open(os.path.join(SFX_DIR, f('score_notes.json')), 'w', encoding='utf-8'), indent=1)
