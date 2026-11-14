# Build the route map data for the "map" graphic from project.json "map".
# "map": {"points": {"Moscow": [37.62, 55.75], "Yakutsk": [129.73, 62.03]},          name: [lon, lat]
#         "legs": [{"from": "Moscow", "to": "Yakutsk", "mode": "air", "label": "7 HOURS BY AIR"},
#                  {"from": "Yakutsk", "to": "Oymyakon", "mode": "road", "via": [[135.6, 62.66]], "label": "900 KM", "sub": "18 HOURS BY ROAD"}]}
# In the shot list, use {"mg": "map", "props": {"leg": 0}} for the first leg. Country outlines: Natural Earth (public domain).
import json, math, os, urllib.request
from common import DATA, P, REM

SRC = os.path.join(DATA, 'ne_50m_admin_0_countries.geojson')
if not os.path.exists(SRC):
    urllib.request.urlretrieve('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson', SRC)
cfg = P['map']
pts = cfg['points']
lons = [p[0] for p in pts.values()] + [v[0] for l in cfg['legs'] for v in l.get('via', [])]
lats = [p[1] for p in pts.values()] + [v[1] for l in cfg['legs'] for v in l.get('via', [])]
lon0, lon1, lat0, lat1 = min(lons) - 20, max(lons) + 20, min(lats) - 12, max(lats) + 12
kx = math.cos(math.radians((lat0 + lat1) / 2))   # simple equirectangular projection, corrected for latitude
S = 20

def proj(lon, lat):
    if lon < lon0 - 180: lon += 360
    return [round((lon - lon0) * kx * S, 1), round((lat1 - lat) * S, 1)]

paths = []
for feat in json.load(open(SRC))['features']:
    g = feat['geometry']
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    d = []
    for poly in polys:
        ring = [proj(*c) for c in poly[0]]
        W, H = (lon1 - lon0) * kx * S, (lat1 - lat0) * S
        if not any(-W * 0.2 < x < W * 1.2 and -H * 0.2 < y < H * 1.2 for x, y in ring): continue
        out = []
        for q in ring:
            if not out or q != out[-1]: out.append(q)
        if len(out) > 3: d.append('M' + ' L'.join(f'{x},{y}' for x, y in out) + ' Z')
    if d:
        paths.append({'name': feat['properties'].get('ADMIN'), 'd': ' '.join(d)})
legs = []
for l in cfg['legs']:
    route = [proj(*pts[l['from']])] + [proj(*v) for v in l.get('via', [])] + [proj(*pts[l['to']])]
    xs, ys = [p[0] for p in route], [p[1] for p in route]
    w = max(max(xs) - min(xs), 1) * 1.6 + 120
    h = w * 9 / 16
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    legs.append({**l, 'route': route, 'viewEnd': [cx - w / 2, cy - h / 2, w, h], 'viewStart': [cx - w * 0.65, cy - h * 0.65, w * 1.3, h * 1.3],
                 'fromXY': route[0], 'toXY': route[-1]})
json.dump({'paths': paths, 'legs': legs, 'highlight': cfg.get('highlight', '')}, open(os.path.join(REM, 'src', 'mapdata.json'), 'w'))
print(f'map: {len(paths)} countries, {len(legs)} legs')
