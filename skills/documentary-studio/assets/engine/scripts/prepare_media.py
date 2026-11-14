# Trim each picked video to the length its shot needs (1080p, 30 fps, no audio) and copy stills into Remotion's public folder.
# Clips are made long enough for every language's timeline that exists, so all versions render from the same files.
import glob, json, os, shutil, subprocess
from common import DATA, REM, ROOT, duration

PUB = os.path.join(REM, 'public')
tls = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(REM, 'src', 'timeline*.json')))]
assets = json.load(open(os.path.join(DATA, 'assets.json')))
need = {}
for t in tls:
    for it in t['items']:
        if it.get('srcType') == 'video':
            key = it['src'][5:-4]
            need[key] = max(need.get(key, 0), it['dur'] / t['fps'] + 0.6)
        elif it.get('srcType') == 'image':
            a = next(x for x in assets.values() if os.path.basename(x['path']) == it['src'])
            shutil.copy(os.path.join(ROOT, a['path']), os.path.join(PUB, it['src']))
for sid, secs in need.items():
    a = assets[sid]
    src = os.path.join(ROOT, a['path'])
    dur = duration(src)
    slow = 1.0 if dur - 0.5 >= secs else secs / (dur - 0.5)
    start = 0.3 if slow > 1 else max(0.3, (dur - secs) / 3)
    vf = (f'setpts={slow:.4f}*PTS,' if slow > 1 else '') + 'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{start:.2f}', '-i', src, '-t', f'{secs / slow:.2f}',
                    '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', os.path.join(PUB, f'clip_{sid}.mp4')], check=True)
    a['used_start'], a['used_seconds'], a['slowdown'] = round(start, 2), round(secs / slow, 2), round(slow, 2)
    if slow > 1:
        print(f'clip_{sid}: source too short, slowed x{slow:.2f}')
json.dump(assets, open(os.path.join(DATA, 'assets.json'), 'w'), indent=1)
print(f'{len(need)} clips trimmed, stills copied')
