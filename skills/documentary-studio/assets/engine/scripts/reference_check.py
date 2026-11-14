# Measure a reference video and compare it with this film, to learn technique. Nothing from it may go into a film.
# Use only a video the producer has the right to analyze: their own, or one with permission. Never download other creators' videos for this.
# Usage: ./studio.sh reference /path/to/video.mp4  -> 08_Timeline_and_Exports/review/reference_report.md and reference_frames.jpg
# It measures sound and picture. It cannot hear, so how the music feels stays with the producer's ear.
import glob, json, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw
from common import ROOT

REVIEW = os.path.join(ROOT, '08_Timeline_and_Exports', 'review'); os.makedirs(REVIEW, exist_ok=True)
MODEL = os.path.expanduser('~/.cache/whisper/ggml-base.en.bin')
SR = 22050
BANDS = [(20, 80, 'sub'), (80, 250, 'bass'), (250, 800, 'low mid'), (800, 2500, 'mid'), (2500, 6000, 'presence'), (6000, 11000, 'air')]
if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]): sys.exit('Usage: ./studio.sh reference /path/to/video.mp4')
renders = sorted(glob.glob(os.path.join(ROOT, '08_Timeline_and_Exports', 'renders', '*_film.mp4')))
FILES = [('Reference', sys.argv[1])] + ([('This film', renders[0])] if renders else [])

def stderr(cmd): return subprocess.run(cmd, capture_output=True, text=True).stderr
def rms(x): return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-7)
def share(sig):
    n, hop = 4096, 2048; fr = np.fft.rfftfreq(n, 1 / SR); idx = list(range(0, max(1, len(sig) - n), hop))
    step = max(1, len(idx) // 3000)
    P = np.mean([np.abs(np.fft.rfft(sig[i:i + n] * np.hanning(n))) ** 2 for i in idx[::step]], axis=0)
    return {b[2]: round(float(10 * np.log10(P[(fr >= b[0]) & (fr < b[1])].sum() / P.sum() + 1e-12)), 1) for b in BANDS}

def measure(path, tmp):
    r = {}
    info = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', path], capture_output=True, text=True).stdout)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    dur = float(info['format']['duration'])
    r['Resolution'] = f"{v['width']}x{v['height']}"; r['Length'] = f'{int(dur // 60)}:{int(dur % 60):02d}'
    e = stderr(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-map', '0:a:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'])
    e = re.sub(r'\s+', ' ', e[e.rfind('Summary:'):])
    r['Loudness (LUFS)'] = (re.search(r'I: (-?[\d.]+) LUFS', e) or [0, '?'])[1]; r['Loudness range (LU)'] = (re.search(r'LRA: ([\d.]+) LU', e) or [0, '?'])[1]
    r['True peak (dBFS)'] = (re.search(r'Peak: (-?[\d.]+) dBFS', e) or [0, '?'])[1]
    raw = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', path, '-map', '0:a:0', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2); m = a.mean(axis=1)
    r['Stereo'] = 'mono (left equals right)' if np.allclose(a[:, 0], a[:, 1], atol=1e-4) else f'stereo, correlation {np.corrcoef(a[::50, 0], a[::50, 1])[0, 1]:.2f}'
    wav = os.path.join(tmp, 'a.wav'); subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', path, '-map', '0:a:0', '-ar', '16000', '-ac', '1', wav], check=True)
    subprocess.run(['whisper-cli', '-m', MODEL, '-f', wav, '-ojf', '-of', os.path.join(tmp, 'w'), '-np'], capture_output=True)
    segs = json.load(open(os.path.join(tmp, 'w.json'), errors='replace'))['transcription']
    sp = [(s['offsets']['from'] / 1000, s['offsets']['to'] / 1000) for s in segs if s['text'].strip()]
    mask = np.zeros(len(m), bool)
    for x, y in sp: mask[int(x * SR):int(y * SR)] = True
    gaps, t = [], 0.0
    for x, y in sp + [(len(m) / SR, 0)]:
        if x - t >= 0.8: gaps.append((t + 0.15, x - 0.15))
        t = max(t, y)
    r['Narration share'] = f'{mask.mean() * 100:.0f}%'; r['Pauses of 0.8 s or more'] = f'{len(gaps)}, one every {dur / max(1, len(gaps)):.0f} s'
    gs = np.concatenate([m[int(x * SR):int(y * SR)] for x, y in gaps]) if gaps else np.zeros(4096)
    hop = SR // 20; env = np.array([np.sqrt((gs[i:i + hop] ** 2).mean()) for i in range(0, max(1, len(gs) - hop), hop)])
    r['Sharp sound hits per pause minute'] = f'{(np.diff(20 * np.log10(env + 1e-6)) > 6).sum() / max(1, len(gs) / SR) * 60:.0f}'
    r['Pause level against narration (dB)'] = f'{rms(gs) - rms(m[mask]):.1f}'
    v_share, g_share = share(m[mask]), share(gs)
    for b in ('bass', 'mid', 'presence', 'air'):
        r[f'Voice {b} (dB)'] = v_share[b]; r[f'Pause {b} (dB)'] = g_share[b]
    e = stderr(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-vf', "scale=480:-1,select='gt(scene,0.3)',showinfo", '-an', '-f', 'null', '-'])
    ts = [float(x) for x in re.findall(r'pts_time:([0-9.]+)', e)]
    g = np.diff([0] + ts + [dur])
    r['Clear hard cuts per minute'] = f'{len(ts) / dur * 60:.1f} (soft fades are not counted)'
    r['Median shot (s)'] = f'{np.median(g):.1f}'; r['Shots over 3 s'] = f'{(g > 3).mean() * 100:.0f}%'; r['Cuts in the first 6 s'] = sum(x <= 6 for x in ts)
    r['_sp'] = [(x, y, s['text'].strip()) for (x, y), s in zip(sp, [s for s in segs if s['text'].strip()])][:12]; r['_dur'] = dur
    return r

results = []
for name, path in FILES:
    with tempfile.TemporaryDirectory() as tmp:
        results.append((name, measure(path, tmp)))
keys = [k for k in results[0][1] if not k.startswith('_')]
out = ['# Reference comparison', '', 'Measured only. Nothing here says how the music feels, so listen as well. Learn the technique and never copy the footage, music or words.', '',
       '| Measure | ' + ' | '.join(n for n, _ in results) + ' |', '|---' * (len(results) + 1) + '|']
out += ['| ' + k + ' | ' + ' | '.join(str(r.get(k, '')) for _, r in results) + ' |' for k in keys]
out += ['', '## How the reference opens', ''] + [f'- {x:.0f} s: {t}' for x, y, t in results[0][1]['_sp']]
out = '\n'.join(out) + '\n'
open(os.path.join(REVIEW, 'reference_report.md'), 'w', encoding='utf-8').write(out)
dur = results[0][1]['_dur']; sheet = Image.new('RGB', (8 * 300, 4 * 169)); d = ImageDraw.Draw(sheet)
with tempfile.TemporaryDirectory() as tmp:
    for i, t in enumerate(np.linspace(0.5, dur - 2, 32)):
        p = os.path.join(tmp, f'{i}.jpg')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', sys.argv[1], '-frames:v', '1', '-vf', 'scale=300:-1', p])
        if os.path.exists(p):
            sheet.paste(Image.open(p).resize((300, 169)), (300 * (i % 8), 169 * (i // 8))); d.text((300 * (i % 8) + 3, 169 * (i // 8) + 2), f'{int(t // 60)}:{int(t % 60):02d}', fill='yellow')
sheet.save(os.path.join(REVIEW, 'reference_frames.jpg'), quality=85)
print(out)
print('Report and frames saved in 08_Timeline_and_Exports/review/.')
