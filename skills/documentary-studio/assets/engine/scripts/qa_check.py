# Pre-publish QA: long dashes, licenses, unpicked shots, AI labels, render length and loudness.
# Usage: python3 qa_check.py [renders/file.mp4 ...]
import csv, json, os, re, subprocess, sys
from common import DATA, ROOT

problems = []
ext = ('.txt', '.md', '.csv', '.srt', '.json', '.tsx', '.ts', '.py', '.tsv')
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'review')]
    for name in files:
        if name.endswith(ext):
            p = os.path.join(dirpath, name)
            text = open(p, encoding='utf-8', errors='ignore').read()
            if chr(0x2014) in text or chr(0x2013) in text:
                problems.append(f'long dash in {os.path.relpath(p, ROOT)}')
rows = list(csv.DictReader(open(os.path.join(ROOT, 'tracker.csv'), encoding='utf-8')))
for r in rows:
    if r['commercial_use_allowed'] != 'yes':
        problems.append(f"tracker {r['shot_id']}: commercial use is '{r['commercial_use_allowed']}'")
    if r['source_type'] == 'AI' and 'AI' not in r['notes'] + r['description'] + r['source_site']:
        problems.append(f"tracker {r['shot_id']}: AI asset not labelled as AI")
shots = json.load(open(os.path.join(DATA, 'shotlist.json')))
picks = json.load(open(os.path.join(DATA, 'picks.json')))
for s in shots:
    if s['kind'] in ('pexels', 'commons') and s['id'] not in picks:
        problems.append(f"shot {s['id']} has no pick")
for path in sys.argv[1:]:
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    lufs = re.findall(r'I:\s+(-?[0-9.]+) LUFS', log)
    blacks = re.findall(r'black_start', subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-vf', 'blackdetect=d=1.0:pix_th=0.05', '-an', '-f', 'null', '-'],
                                                       capture_output=True, text=True).stderr)
    lra = re.findall(r'LRA:\s+([0-9.]+) LU', log)
    print(f'{os.path.basename(path)}: {int(d // 60)}:{d % 60:04.1f}, {lufs[-1] if lufs else "?"} LUFS, loudness range {lra[-1] if lra else "?"} LU, {len(blacks)} black stretches over 1 s')

# Style check (references/viral_style_guide.md). These are prompts for judgment, not errors.
tl_path = os.path.join(ROOT, '08_Timeline_and_Exports', 'remotion', 'src', 'timeline.json')
if os.path.exists(tl_path):
    tl = json.load(open(tl_path, encoding='utf-8'))
    fps, items = tl.get('fps', 30), sorted(tl['items'], key=lambda x: x['from'])
    over = [(x['id'], round(x['dur'] / fps, 2)) for x in items if x['dur'] / fps > 3.01 and not x.get('hold')]
    if over: print('Style: visuals over 3 s, the producer\'s limit:', over)
    no_media = [x['id'] for x in items if not x.get('src') and (x['kind'] in ('pexels', 'commons', 'image', 'reuse') and not x.get('mg') or x.get('mg') in ('title', 'endcard'))]
    if no_media:
        print('QA PROBLEM: shots with no picture, they render as black "missing media":', no_media); sys.exit(1)
    wall, run, longest, at, begin = {'pexels', 'reuse'}, 0.0, 0.0, 0.0, 0.0
    for x in items:
        d = x['dur'] / fps
        if x['kind'] in wall and not x.get('overlay'):
            if run == 0: begin = x['from'] / fps
            run += d
            if run > longest: longest, at = run, begin
        else:
            run = 0.0
    picture = [x['dur'] / fps for x in items]
    variety = (sum((p - sum(picture) / len(picture)) ** 2 for p in picture) / len(picture)) ** 0.5 / (sum(picture) / len(picture))
    made = sum(1 for x in items if x['kind'] not in wall)
    print(f"Style: {made} of {len(items)} shots are graphics, photos or cards. Longest run of plain stock {longest:.0f} s, from {int(at // 60)}:{int(at % 60):02d}. Shot length variety {variety:.2f}.")
    if longest > 25: print('Style: long stock run. Could a graphic, map or real example change the picture when the idea changes?')
    if variety < 0.3: print('Style: shots are all about the same length. Within the 3 s limit, let some sections cut faster.')
brief = os.path.join(ROOT, '01_Script', 'demand_brief.md')
if not os.path.exists(brief):
    print('Reminder: no 01_Script/demand_brief.md, so demand, promise and next step are not recorded')
print('\n'.join(problems) if problems else 'QA: no problems found')
