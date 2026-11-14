# Search a pool of exciting licensed clips by theme, because a 5-minute film at 3 s a shot needs far more footage than one search per shot.
# project.json: "media_pool": {"X01": "lightning storm night", "X02": "molten metal foundry sparks", ...}
# Writes candidates to data/pexels_candidates.json under each X id, and contact sheets to review/pool_N.jpg.
# Look at the sheets, read the titles, then pick in data/picks.json: {"S07c1": "X21:0"} (shot -> theme:candidate).
import io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from common import DATA, P, ROOT

REVIEW = os.path.join(ROOT, '08_Timeline_and_Exports', 'review')
os.makedirs(REVIEW, exist_ok=True)
KEY = dict(l.strip().split('=', 1) for l in open(os.path.join(ROOT, '.env')) if '=' in l)['PEXELS_API_KEY']
UA = {'User-Agent': 'DocumentaryStudio/1.0 (personal documentary research)'}
FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 12)
POOL = P.get('media_pool') or sys.exit('Add "media_pool": {"X01": "search words", ...} to project.json first.')

def get(url, headers=None):
    for attempt in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=40).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4: raise
            time.sleep(int(e.headers.get('Retry-After') or 5 * (attempt + 1)))

def thumb(url):
    try:
        im = Image.open(io.BytesIO(get(url))).convert('RGB'); im.thumbnail((240, 135)); return im
    except Exception:
        return Image.new('RGB', (240, 135), 'gray')

path = os.path.join(DATA, 'pexels_candidates.json')
pex = json.load(open(path)) if os.path.exists(path) else {}
for k, q in POOL.items():
    url = 'https://api.pexels.com/videos/search?' + urllib.parse.urlencode({'query': q, 'orientation': 'landscape', 'per_page': 10})
    lst = []
    for v in json.loads(get(url, {'Authorization': KEY}))['videos']:
        files = [x for x in v['video_files'] if x.get('width') and x['width'] >= 1280 and x['file_type'] == 'video/mp4']
        if v['duration'] < 4 or not files: continue
        b = min(files, key=lambda x: abs(x['width'] - 1920))
        lst.append({'id': v['id'], 'page': v['url'], 'creator': v['user']['name'], 'creator_url': v['user']['url'], 'duration': v['duration'],
                    'w': b['width'], 'h': b['height'], 'file': b['link'], 'thumb': v['image'], 'q': q})
    pex[k] = lst[:8]
json.dump(pex, open(path, 'w'), indent=1)

keys = list(POOL)
for part in range((len(keys) + 9) // 10):
    sel = keys[part * 10:(part + 1) * 10]
    sheet = Image.new('RGB', (240 * 8, 165 * len(sel)), 'black'); d = ImageDraw.Draw(sheet)
    for r, k in enumerate(sel):
        with ThreadPoolExecutor(8) as ex:
            ims = list(ex.map(thumb, [v['thumb'] for v in pex[k]]))
        for c, (v, im) in enumerate(zip(pex[k], ims)):
            sheet.paste(im, (240 * c, 165 * r + 28))
            title = re.sub(r'-\d+/?$', '', v['page'].rstrip('/').split('/')[-1])
            d.text((240 * c + 2, 165 * r + 1), f"{k}:{c} {v['duration']}s", font=FONT, fill='yellow')
            d.text((240 * c + 2, 165 * r + 14), title[:36], font=FONT, fill='white')
    sheet.save(os.path.join(REVIEW, f'pool_{part}.jpg'), quality=82)
print(f'{len(keys)} themes searched, sheets in 08_Timeline_and_Exports/review/pool_N.jpg')
