# Search licensed sources for every stock shot and build contact sheets to pick from.
#   kind "pexels":  "q": ["query 1", "query 2"]  -> Pexels videos (Pexels License, free, commercial use OK). An "mg" shot with "q" gets candidates too, for footage behind the graphic.
#   kind "commons": "q": "query"                  -> Wikimedia Commons photos with license metadata (check each!)
# Writes data/pexels_candidates.json, data/commons_candidates.json and 08_Timeline_and_Exports/review/*.jpg.
# Look at the sheets, then write data/picks.json: {"S01": "S01:3", "S04": "C7"} (shot -> candidate).
# The sheet labels show the Pexels page title: read them, because a thumbnail can hide what the clip really shows.
import io, json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from common import DATA, ROOT

REVIEW = os.path.join(ROOT, '08_Timeline_and_Exports', 'review')
os.makedirs(REVIEW, exist_ok=True)
KEY = dict(l.strip().split('=', 1) for l in open(os.path.join(ROOT, '.env')) if '=' in l)['PEXELS_API_KEY']
UA = {'User-Agent': 'DocumentaryStudio/1.0 (personal documentary research)'}
FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 15)
only = set(sys.argv[1:])  # optionally limit to some shot ids

def get(url, headers=None):
    for attempt in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=40).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4: raise
            time.sleep(int(e.headers.get('Retry-After') or 5 * (attempt + 1)))

def slug(url):
    return re.sub(r'-\d+/?$', '', url.rstrip('/').split('/')[-1])

shots = [s for s in json.load(open(os.path.join(DATA, 'shotlist.json'), encoding='utf-8')) if not only or s['id'] in only]

pex_path = os.path.join(DATA, 'pexels_candidates.json')
pex = json.load(open(pex_path)) if os.path.exists(pex_path) else {}
for s in [s for s in shots if s['kind'] == 'pexels' or (s['kind'] == 'mg' and s.get('q'))]:
    seen, lst = set(), []
    for q in s['q']:
        url = 'https://api.pexels.com/videos/search?' + urllib.parse.urlencode({'query': q, 'orientation': 'landscape', 'per_page': 8})
        for v in json.loads(get(url, {'Authorization': KEY}))['videos']:
            files = [x for x in v['video_files'] if x.get('width') and x['width'] >= 1280 and x['file_type'] == 'video/mp4']
            if v['id'] in seen or v['duration'] < 4 or not files: continue
            b = min(files, key=lambda x: abs(x['width'] - 1920))
            seen.add(v['id'])
            lst.append({'id': v['id'], 'page': v['url'], 'creator': v['user']['name'], 'creator_url': v['user']['url'], 'duration': v['duration'],
                        'w': b['width'], 'h': b['height'], 'file': b['link'], 'thumb': v['image'], 'q': q})
    pex[s['id']] = lst[:8]
json.dump(pex, open(pex_path, 'w'), indent=1)

com_path = os.path.join(DATA, 'commons_candidates.json')
com = json.load(open(com_path)) if os.path.exists(com_path) else []
for s in [s for s in shots if s['kind'] == 'commons']:
    p = {'action': 'query', 'generator': 'search', 'gsrsearch': s['q'], 'gsrnamespace': 6, 'gsrlimit': 20, 'prop': 'imageinfo',
         'iiprop': 'url|size|extmetadata|mime', 'iiurlwidth': 480, 'format': 'json'}
    for pg in json.loads(get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(p))).get('query', {}).get('pages', {}).values():
        ii = pg['imageinfo'][0]; m = ii['extmetadata']
        if ii['mime'] != 'image/jpeg' or ii['width'] < 1100 or any(c['title'] == pg['title'] for c in com): continue
        com.append({'title': pg['title'], 'w': ii['width'], 'h': ii['height'], 'license': m.get('LicenseShortName', {}).get('value', '?'),
                    'artist': re.sub('<[^>]+>', '', m.get('Artist', {}).get('value', '?')).strip(), 'thumb': ii['thumburl'],
                    'page': ii['descriptionurl'], 'desc': re.sub('<[^>]+>', '', m.get('ImageDescription', {}).get('value', ''))[:120],
                    'place': s.get('place', ''), 'query': s['q']})
    time.sleep(1)
json.dump(com, open(com_path, 'w'), indent=1)

def thumb(url):
    try:
        im = Image.open(io.BytesIO(get(url))).convert('RGB'); im.thumbnail((320, 180)); return im
    except Exception:
        return Image.new('RGB', (320, 180), 'gray')

ids = [s['id'] for s in shots if s['kind'] == 'pexels' or (s['kind'] == 'mg' and s.get('q'))]
with ThreadPoolExecutor(12) as ex:
    thumbs = {sid: list(ex.map(lambda c: thumb(c['thumb']), pex[sid])) for sid in ids}
for p in range(0, len(ids), 5):
    group = ids[p:p + 5]
    sheet = Image.new('RGB', (4 * 324 + 150, len(group) * 2 * 214), 'black'); d = ImageDraw.Draw(sheet)
    for r, sid in enumerate(group):
        desc = next(s.get('desc', '') for s in shots if s['id'] == sid)
        d.text((4, r * 428 + 8), sid, font=FONT, fill='yellow')
        d.multiline_text((4, r * 428 + 30), '\n'.join(desc[i:i + 16] for i in range(0, len(desc), 16)), font=FONT, fill='white')
        for c, im in enumerate(thumbs[sid]):
            x, y = 150 + (c % 4) * 324, r * 428 + (c // 4) * 214
            sheet.paste(im, (x, y))
            d.text((x + 3, y + 183), f"{c} {pex[sid][c]['duration']}s {slug(pex[sid][c]['page'])[:30]}", font=FONT, fill='cyan')
    sheet.save(os.path.join(REVIEW, f'pexels_{p // 5:02d}.jpg'), quality=80)
if com:
    cols = 5
    sheet = Image.new('RGB', (cols * 324, ((len(com) + cols - 1) // cols) * 236), 'black'); d = ImageDraw.Draw(sheet)
    for i, c in enumerate(com):
        x, y = (i % cols) * 324, (i // cols) * 236
        sheet.paste(thumb(c['thumb']), (x, y)); time.sleep(0.2)
        d.text((x + 3, y + 184), f"C{i} {c['license'][:20]}", font=FONT, fill='cyan')
        d.text((x + 3, y + 204), c['title'][5:40], font=FONT, fill='white')
    sheet.save(os.path.join(REVIEW, 'commons.jpg'), quality=80)
print(f"{len(ids)} Pexels shots searched, {len(com)} Commons photos listed. Sheets in 08_Timeline_and_Exports/review/")
