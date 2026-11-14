# Write tracker.csv, an SRT per language, and the credits block for the video description.
# Extra tracker rows (voiceovers, score, fonts, your own files) come from project.json "tracker_extra": [[14 columns], ...].
import csv, glob, json, os, re
from common import DATA, FPS, P, REM, ROOT

assets = json.load(open(os.path.join(DATA, 'assets.json')))
clean = lambda s: (s or '').replace(chr(0x2014), '-').replace(chr(0x2013), '-')

def ts(frames, srt=False):
    s = frames / FPS
    if srt:
        return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    return f"{int(s // 60)}:{s % 60:04.1f}"

TL = json.load(open(os.path.join(REM, 'src', 'timeline.json'), encoding='utf-8'))
cols = ['shot_id', 'script_timestamp', 'chapter', 'description', 'source_type', 'source_site', 'asset_url_or_file_name', 'creator',
        'license_type', 'commercial_use_allowed', 'attribution_text_required', 'cost', 'status', 'notes']
rows = []
for it in TL['items']:
    a = assets.get(it['id']) or (assets.get(it.get('of', '')) if it['kind'] == 'reuse' else None)
    base = {'shot_id': it['id'], 'script_timestamp': f"{ts(it['from'])} to {ts(it['from'] + it['dur'])}", 'chapter': it['ch'], 'description': clean(it['desc'])}
    if a and a['type'] == 'pexels':
        rows.append({**base, 'source_type': 'stock', 'source_site': 'Pexels', 'asset_url_or_file_name': a['page'], 'creator': clean(a['creator']),
                     'license_type': 'Pexels License', 'commercial_use_allowed': 'yes', 'attribution_text_required': 'no (credited anyway)', 'cost': '0',
                     'status': 'downloaded', 'notes': f"Illustrative, not filmed at the story location. Used {a.get('used_seconds', '?')}s from {a.get('used_start', '?')}s."})
    elif a and a['type'] == 'commons':
        pd = a['license'].lower().startswith('public domain')
        rows.append({**base, 'source_type': 'public domain' if pd else 'Creative Commons', 'source_site': 'Wikimedia Commons', 'asset_url_or_file_name': a['page'],
                     'creator': clean(a['creator']), 'license_type': a['license'], 'commercial_use_allowed': 'yes',
                     'attribution_text_required': ('no (credited anyway): ' if pd else 'yes: ') + clean(it.get('credit')), 'cost': '0', 'status': 'downloaded',
                     'notes': f"Real photo ({a.get('place') or 'see page'}), credited on screen." + ('' if pd or 'SA' not in a['license'] else ' ShareAlike: decide before publishing.')})
    elif a and a.get('license'):   # a local crop of a licensed photo: project.json local_assets gives its license
        pd = 'public domain' in a['license'].lower()
        rows.append({**base, 'source_type': 'public domain' if pd else 'Creative Commons', 'source_site': 'Wikimedia Commons, cropped', 'asset_url_or_file_name': a.get('page') or a['path'],
                     'creator': clean(a.get('creator', '')), 'license_type': a['license'], 'commercial_use_allowed': 'yes',
                     'attribution_text_required': ('no (credited anyway): ' if pd else 'yes: ') + clean(it.get('credit')), 'cost': '0', 'status': 'downloaded',
                     'notes': f"Real photo ({a.get('place') or 'see page'}), cropped, credited on screen."})
    elif a:
        rows.append({**base, 'source_type': 'your own file', 'source_site': 'local', 'asset_url_or_file_name': a['path'], 'creator': 'see notes',
                     'license_type': 'fill in', 'commercial_use_allowed': 'unclear', 'attribution_text_required': 'fill in', 'cost': '', 'status': 'needs license info', 'notes': 'Add the license before publishing.'})
    else:
        rows.append({**base, 'source_type': 'motion graphic', 'source_site': 'original (Remotion)', 'asset_url_or_file_name': f"graphics: {it.get('mg') or it['kind']}",
                     'creator': 'this production', 'license_type': 'original', 'commercial_use_allowed': 'yes', 'attribution_text_required': 'no', 'cost': '0',
                     'status': 'downloaded', 'notes': 'Quote card: wording from the source material, unverified.' if it['kind'] == 'quote' else ''})
for extra in P.get('tracker_extra', []):
    rows.append(dict(zip(cols, extra)))
with open(os.path.join(ROOT, 'tracker.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

for path in sorted(glob.glob(os.path.join(REM, 'src', 'timeline*.json'))):
    tl = json.load(open(path, encoding='utf-8'))
    lang = os.path.basename(path)[len('timeline'):-5].lstrip('_') or 'en'
    if lang not in P['languages']: continue  # placeholder timeline for an unused language
    entries = [(c['from'], c['dur'], c['text']) for c in tl['captions']]
    entries += [(x['from'], x['dur'], '\n'.join(f'{who}: {what}' for who, what in x['lines'])) for x in tl['items'] if x['kind'] == 'quote']
    with open(os.path.join(ROOT, '08_Timeline_and_Exports', f"{P['slug']}_captions_{lang}.srt"), 'w', encoding='utf-8') as fh:
        for n, (a, d, text) in enumerate(sorted(entries), 1):
            fh.write(f"{n}\n{ts(a, True)} --> {ts(a + d, True)}\n{clean(text)}\n\n")

seen, pex, real, other = set(), [], [], []
for it in TL['items']:
    a = assets.get(it['id'])
    if not a or a['path'] in seen: continue
    seen.add(a['path'])
    if a['type'] == 'pexels':
        pex.append(f"- Video by {clean(a['creator'])} on Pexels: {a['page']}")
    elif a['type'] == 'commons':
        line = f"- \"{a['title'][5:]}\" by {clean(a['creator'])}, {a['license']}, via Wikimedia Commons: {a['page']}"
        (real if a.get('place') else other).append(line)  # a shot's "place" marks a real photo of a named place
credits = ['CREDITS', '', *P.get('credits_description', []), '',
           "Real photos of the places named (via Wikimedia Commons):", *real, '',
           'Other photos (illustrative):', *other, '',
           'Stock footage (illustrative, not filmed at the story location), Pexels License:', *pex]
open(os.path.join(ROOT, '09_Permissions_and_Licenses', 'credits_for_description.txt'), 'w', encoding='utf-8').write('\n'.join(credits) + '\n')
# Short credits for the YouTube description (5,000-character limit): photo credits in full, Pexels filmmakers by name.
# Credits go in the description only, never in a pinned comment as well. The full list stays here as the project's own record.
def short_title(t):
    t = re.sub(r'\.(jpe?g|png|tiff?|webp)$', '', t, flags=re.I).replace('_', ' ')
    if len(t) > 70: t = ' '.join(w for w in t.split() if w.isascii())  # long titles: keep the Latin-script words
    return t if len(t) <= 70 else t[:67].rstrip() + '...'
def short_line(line):
    m = re.match(r'- "(.+?)" by (.+?), (.+?), via Wikimedia Commons: (\S+)$', line)
    if m and P.get('credits_compact'): return f'- {m[2].replace("~commonswiki", "")}, {m[3]}: {m[4]}'   # for films with many photos: the link names the file
    return f'- "{short_title(m[1])}" by {m[2].replace("~commonswiki", "")}, {m[3]}: {m[4]}' if m else line
names = []
for line in pex:
    n = re.sub(r'\s+', ' ', re.match(r'- Video by (.+?) on Pexels', line)[1]).strip()
    if n not in names: names.append(n)
short = ['CREDITS', *P.get('credits_description', [])]
pd_note = P.get('credits_public_domain_summary')   # optional: name public domain sources in one line when the description runs long
real_short = [l for l in real if ', Public domain,' not in l] if pd_note else real
if real_short: short += ['', 'Real photos of the places named (Wikimedia Commons):', *map(short_line, real_short)]
if pd_note: short += ['', pd_note]
if other: short += ['', 'Other photos (illustrative, Wikimedia Commons):', *map(short_line, other)]
if names: short += ['', 'Stock footage from Pexels (Pexels License, illustrative, not filmed at the places named). Filmmakers: ' + ', '.join(names) + '.']
open(os.path.join(ROOT, '09_Permissions_and_Licenses', 'credits_short_for_description.txt'), 'w', encoding='utf-8').write('\n'.join(short) + '\n')
print(f'{len(rows)} tracker rows, SRT files written, {len(pex)} Pexels and {len(real) + len(other)} Commons credits')
