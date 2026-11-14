import re
# Download every picked asset into the licensed folders and record its source and license in data/assets.json.
# Picks (data/picks.json): "S01": "S01:3" (Pexels candidate 3 of shot S01, any shot's list may be used),
# "S04": "C7" (Commons candidate 7), or "S20": "file:03_Images/my_photo.jpg" (your own file; add its license to the tracker).
# Removes downloads that are no longer picked.
import json, os, time, urllib.error, urllib.parse, urllib.request
def once(name):
    """Commons sometimes doubles a name: 'Unknown authorUnknown author'."""
    m = re.fullmatch(r'(.+?)\s*\1', name.strip())
    return m.group(1) if m else name
from concurrent.futures import ThreadPoolExecutor
from common import DATA, ROOT

UA = {'User-Agent': 'DocumentaryStudio/1.0 (personal documentary research)'}
picks = json.load(open(os.path.join(DATA, 'picks.json')))
pex = json.load(open(os.path.join(DATA, 'pexels_candidates.json'))) if os.path.exists(os.path.join(DATA, 'pexels_candidates.json')) else {}
com = json.load(open(os.path.join(DATA, 'commons_candidates.json'))) if os.path.exists(os.path.join(DATA, 'commons_candidates.json')) else []
for d in ('02_Footage_Licensed/originals', '03_Images/commons'):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

def open_retry(url, timeout=60):
    for attempt in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5: raise
            time.sleep(int(e.headers.get('Retry-After') or 5 * (attempt + 1)))

titles = sorted({com[int(p[1:])]['title'] for p in picks.values() if p.startswith('C')})
thumbs = {}
for k in range(0, len(titles), 40):
    api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(
        {'action': 'query', 'titles': '|'.join(titles[k:k + 40]), 'prop': 'imageinfo', 'iiprop': 'url', 'iiurlwidth': 2400, 'format': 'json'})
    thumbs.update({pg['title']: pg['imageinfo'][0]['thumburl'] for pg in json.loads(open_retry(api).read())['query']['pages'].values()})

assets = {}
for sid, p in picks.items():
    if p.startswith('file:'):
        path = p[5:]
        assets[sid] = {'type': 'image' if path.lower().endswith(('.jpg', '.jpeg', '.png')) else 'local_video', 'path': path,
                       'page': '', 'creator': 'see tracker', 'license': 'see tracker'}
    elif p.startswith('C'):
        c = com[int(p[1:])]
        assets[sid] = {'type': 'commons', 'url': thumbs[c['title']], 'path': f"03_Images/commons/{p}_{c['title'][5:].replace(' ', '_')}",
                       'page': c['page'], 'creator': once(c['artist']), 'license': c['license'], 'title': c['title'], 'place': c.get('place', '')}
    else:
        src, i = p.split(':')
        v = pex[src][int(i)]
        assets[sid] = {'type': 'pexels', 'url': v['file'], 'path': f"02_Footage_Licensed/originals/pexels_{v['id']}.mp4", 'page': v['page'],
                       'creator': v['creator'], 'creator_url': v['creator_url'], 'license': 'Pexels License', 'duration': v['duration']}

def fetch(a):
    dst = os.path.join(ROOT, a['path'])
    if not os.path.exists(dst):
        with open_retry(a['url'], 300) as r, open(dst + '.part', 'wb') as out:
            while chunk := r.read(1 << 20): out.write(chunk)
        os.rename(dst + '.part', dst)
    return os.path.getsize(dst)

for a in assets.values():
    if a['type'] == 'image': a.update(json.load(open(os.path.join(ROOT, 'project.json'))).get('local_assets', {}).get(a['path'], {}))
remote = {a['path']: a for a in assets.values() if 'url' in a}.values()
sizes = [fetch(a) for a in remote if a['type'] == 'commons']
with ThreadPoolExecutor(6) as ex:
    sizes += list(ex.map(fetch, [a for a in remote if a['type'] == 'pexels']))
json.dump(assets, open(os.path.join(DATA, 'assets.json'), 'w'), indent=1)
used = {os.path.basename(a['path']) for a in assets.values()}
for d in ('02_Footage_Licensed/originals', '03_Images/commons'):
    for name in os.listdir(os.path.join(ROOT, d)):
        if name not in used:
            os.remove(os.path.join(ROOT, d, name)); print('removed unpicked download:', name)
print(len(sizes), 'files,', round(sum(sizes) / 1e6), 'MB')
