# Place the voiceover pieces, add ambience and sound effects, lay in the score, duck under the voice, and master.
# Sound effects come from project.json "sfx": [{"type": "impact", "at": anchor}, {"type": "fire", "from": anchor, "to": anchor}, ...]
# Types: impact, crack, rustle, rustle_soft, whoosh, swish, thud, riser (ends on its anchor), fire (range), tick (range). Whooshes are also added at every chapter breather.
# project.json "sound_design": {"level": 1.0, "swish_every": 3}: soft automatic sounds on cuts, graphics and on-screen text. Level 0 switches them off.
# project.json "voice_presence_db": 2.0: gentle lift around 4 kHz so the voice is clear. 0 switches it off. Check by ear.
# Ambience: project.json "ambience": {"wind": 0.22} (0 to switch off). Usage: DOC_LANG=en|bn python3 build_audio.py <tmp dir>
import os, subprocess, sys
import numpy as np
from common import P, REM, SFX_DIR, SR, Anchors, f, load_timeline, load_words, vo_path

TMP = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
TL = load_timeline()
A = Anchors(TL, load_words())
T = A.T
N = int(T * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

def ff_noise(name, color, filters, secs):
    path = os.path.join(TMP, name + '.raw')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i',
                    f'anoisesrc=d={secs}:c={color}:r={SR}:a=0.8:s={rng.integers(1, 1 << 30)},{filters}', '-f', 'f32le', '-ac', '1', path], check=True)
    x = np.fromfile(path, dtype=np.float32)
    return x / (np.abs(x).max() + 1e-9)

def smooth(x, ms):
    k = max(1, int(SR * ms / 1000))
    c = np.cumsum(np.insert(x, 0, 0.0))
    y = (c[k:] - c[:-k]) / k
    return np.concatenate([y, np.full(len(x) - len(y), y[-1] if len(y) else 0)])

def place(track, clip, at, gain=1.0):
    i = int(at * SR)
    if 0 <= i < len(track):
        n = min(len(clip), len(track) - i); track[i:i + n] += clip[:n] * gain

def load(path, channels=1, af=None):
    raw = os.path.join(TMP, os.path.basename(path) + '.raw')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', path, *(['-af', af] if af else []), '-ar', str(SR), '-ac', str(channels), '-f', 'f32le', raw], check=True)
    x = np.fromfile(raw, dtype=np.float32)
    return x.reshape(-1, 2) if channels == 2 else x

# Voiceover, split at every gap.
presence = P.get('voice_presence_db', 0)
src = load(vo_path(), af=f'equalizer=f=4000:t=o:w=1.6:g={presence}' if presence else None)
vo = np.zeros(N, np.float32)
for p in TL['vo']:
    seg = src[int(p['voStart'] * SR): int(min(p['voEnd'], len(src) / SR) * SR)].copy()
    fade = min(len(seg) // 4, int(0.012 * SR))
    if fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    place(vo, seg, p['from'])
vo *= 0.89 / (np.abs(vo).max() + 1e-9)
duck = smooth(1 - 0.5 * np.clip(smooth(np.abs(vo), 250) / 0.05, 0, 1), 120)
OPENER_END = TL.get('opener_end')
if OPENER_END:      # the opener's music stays exciting under the voice, then hands over to normal ducking
    keep = np.clip((OPENER_END + 0.4 - t) / 0.4, 0, 1)
    duck = np.maximum(duck, 0.7 * keep.astype(np.float32))

quotes = [(x['from'] / TL['fps'], (x['from'] + x['dur']) / TL['fps']) for x in TL['items'] if x['kind'] == 'quote']
warm_from = next((A(s['from']) for s in P.get('score', {}).get('sections', []) if s['mood'] == 'warm'), T)

# Ambience: wind, loud at the open, settling under narration, swelling under quote cards, calmer in a warm close.
wind_level = P.get('ambience', {}).get('wind', 0.22)
wind = 0.7 * ff_noise('wind_low', 'brown', 'highpass=f=40,lowpass=f=420', T + 1)[:N]
wind += 0.35 * ff_noise('wind_hi', 'pink', 'bandpass=f=900:width_type=h:w=500', T + 1)[:N] * (0.5 + 0.5 * np.sin(2 * np.pi * t / 5.3) ** 2)
pts = [(0, 1.0), (1.2, 0.8), (min(24, T), 0.55), (min(60, T), 0.35), (max(0, warm_from - 1), 0.35), (min(T, warm_from + 6), 0.18), (T, 0.0)]
for a, b in quotes:
    pts += [(a - 0.3, 0.35), (a + 0.4, 0.9), (b - 0.4, 0.9), (b + 0.3, 0.35)]
if OPENER_END:      # no wind over the opener: it fades in afterward
    pts = [(x, 0.0 if x <= OPENER_END else y) for x, y in pts] + [(OPENER_END, 0.0), (OPENER_END + 1.5, 0.5)]
xs, ys = zip(*sorted(pts))
wind *= (0.6 + 0.4 * np.sin(2 * np.pi * t / 9.1) * np.sin(2 * np.pi * t / 4.3 + 1)) * np.interp(t, xs, ys) * wind_level

# Sound effects.
sfx = np.zeros(N, np.float32)
sfx_side = np.zeros(N, np.float32)
hiss = ff_noise('hiss', 'white', 'highpass=f=2500,lowpass=f=9000', 6)
def rustle(secs, density):
    n = int(secs * SR)
    grains = np.zeros(n, np.float32)
    grains[rng.integers(0, n, int(secs * density))] = rng.uniform(0.3, 1.0, int(secs * density))
    return hiss[:n] * np.clip(smooth(grains, 6) * 40, 0, 1) * np.sin(np.linspace(0, np.pi, n)) ** 0.7
bt = np.arange(int(2.2 * SR)) / SR
boom = np.sin(2 * np.pi * (35 + 45 * np.exp(-bt * 6)) * bt) * np.exp(-bt * 2.2)
wh = ff_noise('whoosh', 'pink', 'bandpass=f=700:width_type=h:w=900', 2)[:int(1.1 * SR)]
whoosh = wh * np.sin(np.linspace(0, np.pi, len(wh))) ** 2
ct = np.arange(int(0.9 * SR)) / SR
crack = hiss[:len(ct)] * np.exp(-ct * 25) + 0.6 * np.sin(2 * np.pi * 70 * ct) * np.exp(-ct * 8)
fire_bed = ff_noise('fire', 'brown', 'highpass=f=150,lowpass=f=1800', 12)
beep = np.sin(2 * np.pi * 1760 * np.arange(int(0.09 * SR)) / SR) * np.sin(np.linspace(0, np.pi, int(0.09 * SR))) ** 0.3
click = hiss[:int(0.03 * SR)] * np.exp(-np.arange(int(0.03 * SR)) / SR * 200)

sw = ff_noise('swish', 'pink', 'highpass=f=350,lowpass=f=4200', 1)[:int(0.32 * SR)]
swish = sw * np.sin(np.linspace(0, np.pi, len(sw))) ** 2
thud = boom[:int(0.55 * SR)] * np.linspace(1, 0, int(0.55 * SR)) ** 2
rs = ff_noise('riser', 'pink', 'highpass=f=250,lowpass=f=5000', 3)[:int(2.2 * SR)]
riser = rs * np.linspace(0, 1, len(rs)) ** 2.4
def swish_at(at, gain, side):
    """A soft swish that travels across the stereo field."""
    place(sfx, swish, at - 0.14, gain)
    place(sfx_side, swish * np.linspace(-side, side, len(swish)), at - 0.14, gain)
# The hook: a light whoosh and tap on each cut, and one fuller hit on the turn. Built to reach phone and laptop speakers, not only subwoofers.
hit_duck = np.ones(N, np.float32)
hit_level = (P.get('sound_design') or {}).get('opener_hit', 1.0)
def cut_hit(pitch, tail):
    ht = np.arange(int(0.9 * SR)) / SR
    sub_ = np.sin(2 * np.pi * pitch * (62 + 70 * np.exp(-ht * 30)) * ht) * np.exp(-ht * 8)
    body = np.tanh(2.2 * np.sin(2 * np.pi * pitch * (185 + 170 * np.exp(-ht * 45)) * ht)) * np.exp(-ht * 20)
    snap = ff_noise('hit_snap', 'white', 'highpass=f=900,lowpass=f=4800', 1)[:len(ht)] * np.exp(-ht * 95)
    room = ff_noise('hit_room', 'pink', 'highpass=f=180,lowpass=f=1500', 1)[:len(ht)] * np.exp(-ht * tail)
    return 0.6 * sub_ + 0.95 * body + 0.5 * snap + 0.3 * room
def into_cut(secs):
    n = int(secs * SR)
    low = ff_noise('in_low', 'pink', 'highpass=f=200,lowpass=f=900', 1)[:n]
    high = ff_noise('in_high', 'pink', 'highpass=f=1000,lowpass=f=5200', 1)[:n]
    ramp = np.linspace(0, 1, n)
    return (low * (1 - ramp) + high * ramp) * ramp ** 2.2
for x in TL['items']:
    at = x['from'] / TL['fps']
    if x.get('opener'):
        if at <= 0: continue
        hit = x.get('punch')
        place(sfx, cut_hit(0.82 if hit else 1.0, 5 if hit else 12), at, hit_level * (0.6 if hit else 0.2))
        wh_in = into_cut(0.34 if hit else 0.24)
        place(sfx, wh_in, at - len(wh_in) / SR, hit_level * (0.3 if hit else 0.14))
        if hit:      # the music steps back for a moment, so the hit lands
            a_, b_ = int(at * SR), int((at + 0.16) * SR)
            hit_duck[a_:b_] = np.minimum(hit_duck[a_:b_], 1 - 0.45 * np.linspace(1, 0, b_ - a_))
    elif x.get('boom') and x['from'] > 0: place(sfx, boom, at, 0.14)   # a soft low hit on a chosen hard cut
SD = P.get('sound_design') or {}
sd_level, sd_every, sd_count = SD.get('level', 0), SD.get('swish_every', 3), 0
if sd_level:
    for n, x in enumerate(TL['items']):
        at = x['from'] / TL['fps']
        if at <= (OPENER_END or 0) or x.get('boom'): continue
        if x['kind'] == 'mg' or x['kind'] == 'quote': place(sfx, thud, at, 0.11 * sd_level); sd_count += 1
        elif x.get('overlay'): place(sfx, thud, at, 0.09 * sd_level); swish_at(at, 0.05 * sd_level, 0.7); sd_count += 1
        elif n % sd_every == 0: swish_at(at, 0.06 * sd_level, 0.7 if n % 2 else -0.7); sd_count += 1
for e in P.get('sfx', []):
    kind = e['type']
    if kind == 'impact': place(sfx, boom, A(e['at']), 0.3)
    elif kind == 'crack': place(sfx, crack, A(e['at']), 0.5); place(sfx, crack, A(e['at']) + 0.13, 0.25)
    elif kind == 'rustle': place(sfx, rustle(1.2, 260), A(e['at']), 0.55)
    elif kind == 'rustle_soft': place(sfx, rustle(3.2, 120), A(e['at']), 0.18)
    elif kind == 'whoosh': place(sfx, whoosh, A(e['at']) - 0.5, 0.2)
    elif kind == 'swish': swish_at(A(e['at']), e.get('gain', 0.1), 0.7)
    elif kind == 'thud': place(sfx, thud, A(e['at']), e.get('gain', 0.18))
    elif kind == 'riser': place(sfx, riser, A(e['at']) - len(riser) / SR, e.get('gain', 0.1))
    elif kind == 'fire':
        a, b = A(e['from']), A(e['to']); n = int((b - a) * SR)
        pops = np.zeros(n, np.float32); k = int((b - a) * 14)
        pops[rng.integers(0, n, k)] = rng.uniform(0.3, 1, k)
        bed = fire_bed[np.arange(n) % len(fire_bed)] * 0.25 + hiss[np.arange(n) % len(hiss)] * np.clip(smooth(pops, 2) * 60, 0, 1)
        place(sfx, bed * np.clip(np.minimum(np.arange(n), n - np.arange(n)) / (0.3 * SR), 0, 1), a, 0.3)
    elif kind == 'alarm':  # a digital alarm: four quick beeps, twice. Optional "gain".
        for burst in (0, 0.75):
            for b in range(4): place(sfx, beep, A(e['at']) + burst + b * 0.13, e.get('gain', 0.22))
    elif kind == 'tick':
        for at in np.arange(A(e['from']), A(e['to']), 0.5): place(sfx, click, at, 0.35)
breathers = [g for g in TL.get('gaps', []) if not any(abs(x['from'] / TL['fps'] - g['from']) < 0.05 for x in TL['items'])]
for g in breathers:
    if g['dur'] <= 1.0: place(sfx, whoosh, g['from'] - 0.6, 0.2)

score_path = os.path.join(SFX_DIR, f('score.wav'))
music = np.zeros(N, np.float32)
music_side = np.zeros(N, np.float32)
if os.path.exists(score_path):
    s = load(score_path, channels=2); n_ = min(N, len(s))
    music[:n_] = s[:n_].mean(axis=1); music_side[:n_] = (s[:n_, 0] - s[:n_, 1]) / 2
music *= P.get('music_level', 0.65)
music_side *= P.get('music_level', 0.65)

mix = vo + (wind + music) * duck * hit_duck + sfx
side = music_side * duck * hit_duck + sfx_side   # the voice stays centered
for name, sig in [('stem_music', music), ('stem_wind', wind), ('stem_sfx', sfx), ('mix_premaster', mix)]:
    raw = os.path.join(TMP, name + '.f32'); sig.astype(np.float32).tofile(raw)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', raw,
                    os.path.join(SFX_DIR, f(name + '.wav'))], check=True)
raw = os.path.join(TMP, 'mix_stereo.f32'); np.stack([mix + side, mix - side], axis=1).astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw,
                '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), '-ac', '2', os.path.join(REM, 'public', f('final_mix.wav'))], check=True)
print(f'mix: {T:.1f}s, {len(P.get("sfx", []))} effects, {len(breathers)} chapter whooshes, {sd_count} automatic sounds, stereo music')
