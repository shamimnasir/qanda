# Render YouTube thumbnails (1280x720 JPG, under 2 MB) from data/thumbnails.json into 05_Motion_Graphics/thumbnails/,
# plus phone_size_check.jpg: every thumbnail at about the size YouTube shows on a phone (about 160 px wide in lists,
# 360 px in the home feed), to check it still reads.
# Usage: python3 make_thumbnails.py [name ...]
#
# thumbnails.json is a list. Each thumbnail:
#   {"name": "thumb1_okinawa",
#    "vertical": true,                   1080x1920 cover for the Short (default: 1280x720 for the film)
#    "shot": "S47", "t": 2.0,              background: a shot's licensed source (frame at t seconds for video)
#    "image": "03_Images/...jpg",          ...or any licensed image path (instead of "shot")
#    "focus": [0.5, 0.5], "zoom": 1.0,     which point of the image to keep centred, and extra zoom
#    "grade": "warm" | "cold" | "none",    colour grade (default: the film's look)
#    "darken": "left" | "right" | "top" | "bottom" | "all" | "none",   shade behind the text (default left)
#    "blur": 6,                            soften the background so a face stands out
#    "items": [
#      {"text": "43RD", "x": 70, "y": 300, "size": 230, "color": "#ff6f61", "align": "left", "weight": "Bold", "stroke": 10},
#      {"arrow": [[400, 200], [520, 420]], "color": "#ff6f61", "width": 34},
#      {"ring": [640, 360, 250], "percent": 80, "color": "#ff6f61", "width": 40},
#      {"box": [60, 80, 400, 200], "color": "#000000", "alpha": 0.5},
#      {"face": "serious", "cx": 960, "top": 90, "height": 1100, "flip": false, "rim": "#ff4f45", "fade": 150, "color": 0.5, "rim_alpha": 0.3}],
#        the producer's cutout (see 05_Motion_Graphics/producer/README.md), or a path to any transparent PNG or WebP, such as a made-up AI person related to the film (references/packaging.md).
#        color = 0.5 drains the colour for a heavy mood. cx = centre x, top = y of the top of the hair, height = full cutout height. List faces before text so text sits on top.
#    "credit": "Photo: Kugel, CC BY-SA 4.0"}   small credit, bottom left (real photos need one)
# Keep text to 0 to 3 words, away from the bottom-right corner (YouTube puts the video length there).
import json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from common import DATA, P, REM, ROOT

W, H = 1280, 720  # set per thumbnail in render()
CHROME = os.environ.get('DOC_CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
OUT = os.path.join(ROOT, '05_Motion_Graphics', 'thumbnails')
FONT = {'title': os.path.join(REM, 'public', 'Oswald.ttf'), 'body': os.path.join(REM, 'public', 'Inter.ttf')}
TMP = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'docstudio_thumbs')
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
ASSETS = os.path.join(DATA, 'assets.json')
assets = json.load(open(ASSETS, encoding='utf-8')) if os.path.exists(ASSETS) else {}

def font(size, weight='Bold', kind='title'):
    f = ImageFont.truetype(FONT[kind], size)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f

def background(t):
    if 'shot' in t:
        if t['shot'] not in assets: raise SystemExit(f"{t['name']}: shot {t['shot']} has no downloaded media yet (run ./studio.sh download first)")
        a = assets[t['shot']]; src = os.path.join(ROOT, a['path'])
        if a['type'] == 'pexels':
            frame = os.path.join(TMP, f"{t['name']}.png")
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t.get('t', 2.0)), '-i', src, '-frames:v', '1', frame], check=True)
            src = frame
    else:
        src = os.path.join(ROOT, t['image'])
    im = Image.open(src).convert('RGB')
    # Cover-crop to 16:9 around the focus point, with optional zoom.
    z = max(W / im.width, H / im.height) * t.get('zoom', 1.0)
    im = im.resize((round(im.width * z), round(im.height * z)), Image.LANCZOS)
    fx, fy = t.get('focus', [0.5, 0.5])
    x = min(max(round(fx * im.width - W / 2), 0), im.width - W)
    y = min(max(round(fy * im.height - H / 2), 0), im.height - H)
    im = im.crop((x, y, x + W, y + H))
    return im.filter(ImageFilter.GaussianBlur(t['blur'])) if t.get('blur') else im

def grade(im, look):
    if look == 'none': return im
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.15)).enhance(1.12)
    tint = (255, 170, 110) if look == 'warm' else (60, 120, 200)
    return Image.blend(im, Image.new('RGB', im.size, tint), 0.08)

def darken(im, side):
    """Shade behind the text plus a soft vignette that pulls the eye to the centre."""
    u, w = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
    ramp = {'left': 1 - u, 'right': u, 'top': 1 - w, 'bottom': w}
    s = np.clip((ramp[side] - 0.35) / 0.65, 0, 1) if side in ramp else np.full((H, W), 0.55 if side == 'all' else 0.0)
    vig = np.clip(np.hypot(u - 0.5, w - 0.5) * 1.3, 0, 1) ** 2.2 * 0.6
    m = Image.fromarray(np.uint8(255 * np.minimum(0.85, s * 0.8 + vig)))
    return Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, m)

def text_item(d, it):
    f = font(it.get('size', 120), it.get('weight', 'Bold'), it.get('font', 'title'))
    s = it['text']; sw = it.get('stroke', max(4, it.get('size', 120) // 22))
    l, t_, r, b = d.textbbox((0, 0), s, font=f, stroke_width=sw)
    x = it['x'] - {'left': 0, 'center': (r - l) / 2, 'right': r - l}[it.get('align', 'left')]
    # Drop shadow, then text with a dark outline: readable on any background at phone size.
    d.text((x + 6, it['y'] + 8), s, font=f, fill=(0, 0, 0, 150), stroke_width=sw, stroke_fill=(0, 0, 0, 150))
    d.text((x, it['y']), s, font=f, fill=it.get('color', '#ffffff'), stroke_width=sw, stroke_fill=it.get('stroke_color', '#140c0e'))

def bangla_item(layer, it):
    """Bangla needs real text shaping, which Pillow lacks here: draw it with Chrome on a transparent page, then paste."""
    size, sw = it.get('size', 120), it.get('stroke', max(4, it.get('size', 120) // 22))
    tx = {'left': '0', 'center': '-50%', 'right': '-100%'}[it.get('align', 'left')]
    html = os.path.join(TMP, 'bn_text.html'); png = os.path.join(TMP, 'bn_text.png')
    open(html, 'w', encoding='utf-8').write(f"""<!doctype html><meta charset="utf-8"><style>
      @font-face {{font-family: N; src: url('file://{os.path.join(REM, 'public', 'NotoSansBengali.ttf')}'); font-weight: 100 900;}}
      html, body {{margin: 0; background: transparent;}}
      div {{position: absolute; left: {it['x']}px; top: {it['y']}px; transform: translateX({tx}); white-space: nowrap; font: 700 {size}px/1.25 N;
           color: {it.get('color', '#ffffff')}; -webkit-text-stroke: {sw * 2}px {it.get('stroke_color', '#140c0e')}; paint-order: stroke fill;
           text-shadow: 6px 8px 0 rgba(0,0,0,0.55);}}</style><div>{it['text']}</div>""")
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--default-background-color=00000000',
                    f'--window-size={W},{H}', '--force-device-scale-factor=1', f'--screenshot={png}', f'file://{html}'], check=True, capture_output=True)
    layer.alpha_composite(Image.open(png).convert('RGBA').crop((0, 0, W, H)))

def face_item(layer, it, name):
    """A person cutout (the producer or a made-up person), lifted off the background with a coloured rim light and a dark shadow."""
    dirs = [os.path.join(ROOT, '05_Motion_Graphics', 'producer'), os.path.expanduser('~/.claude/skills/documentary-studio/assets/producer')]
    paths = [it['face']] + [os.path.join(d, it['face'] + '.webp') for d in dirs]
    path = next((p for p in paths if os.path.isfile(p)), None)
    if not path: raise SystemExit(f"{name}: face '{it['face']}' not found in 05_Motion_Graphics/producer")
    im = Image.open(path).convert('RGBA'); im = im.crop(im.getchannel('A').getbbox())
    if it.get('flip'): im = im.transpose(Image.FLIP_LEFT_RIGHT)
    z = it['height'] / im.height
    im = im.resize((round(im.width * z), it['height']), Image.LANCZOS)
    a = im.getchannel('A')
    rgb = ImageEnhance.Color(ImageEnhance.Contrast(im.convert('RGB')).enhance(1.08)).enhance(it.get('color', 1.1))
    im = Image.merge('RGBA', (*rgb.split(), a))
    x, y = round(it['cx'] - im.width / 2), it.get('top', 0)
    if y + im.height < H: print(f"WARNING {name}: face '{it['face']}' stops {H - y - im.height} px above the bottom edge")
    full = Image.new('RGBA', (W, H), (0, 0, 0, 0)); full.paste(im, (x, y))
    mask = full.getchannel('A')
    solid = np.asarray(mask) / 255
    if it.get('fade'):  # melt the lowest pixels into the background, for a photo whose shoulders stop at a straight edge
        ramp = np.clip((H - np.arange(H)) / it['fade'], 0, 1)[:, None]
        mask = Image.fromarray(np.uint8(np.asarray(mask) * ramp)); full.putalpha(mask)
    if it.get('side_fade'):  # melt a sleeve that stops at a straight vertical edge: positive fades the left side, negative the right
        n = it['side_fade']
        ramp = np.clip((np.arange(W) - x) / n, 0, 1) if n > 0 else np.clip((x + im.width - np.arange(W)) / -n, 0, 1)
        mask = Image.fromarray(np.uint8(np.asarray(mask) * ramp[None, :])); full.putalpha(mask)
    shadow = mask.filter(ImageFilter.GaussianBlur(26)).point(lambda v: round(v * 0.75))
    layer.alpha_composite(Image.merge('RGBA', (*Image.new('RGB', (W, H), (0, 0, 0)).split(), shadow)))
    if it.get('rim'):
        c = it['rim'].lstrip('#'); c = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
        rim = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(9)).point(lambda v: min(255, round(v * 1.2 * it.get('rim_alpha', 1.0))))
        rim = Image.fromarray(np.uint8(np.asarray(rim) * (1 - solid)))  # only outside the person, so a fade never shows the rim colour
        layer.alpha_composite(Image.merge('RGBA', (*Image.new('RGB', (W, H), c).split(), rim)))
    layer.alpha_composite(full)

def arrow_item(d, it):
    (x0, y0), (x1, y1) = it['arrow']; w = it.get('width', 30); c = it.get('color', '#ff6f61')
    ang = math.atan2(y1 - y0, x1 - x0); hl = w * 2.4
    bx, by = x1 - hl * math.cos(ang) * 0.8, y1 - hl * math.sin(ang) * 0.8
    for col, extra in (('#140c0e', 10), (c, 0)):
        d.line([(x0, y0), (bx, by)], fill=col, width=w + extra)
        pts = [(x1 + extra * math.cos(ang), y1 + extra * math.sin(ang)),
               (bx + (hl * 0.75 + extra) * math.cos(ang + math.pi / 2), by + (hl * 0.75 + extra) * math.sin(ang + math.pi / 2)),
               (bx + (hl * 0.75 + extra) * math.cos(ang - math.pi / 2), by + (hl * 0.75 + extra) * math.sin(ang - math.pi / 2))]
        d.polygon(pts, fill=col)

def ring_item(d, it):
    cx, cy, r = it['ring']; w = it.get('width', 36); c = it.get('color', '#ff6f61')
    box = [cx - r, cy - r, cx + r, cy + r]
    d.ellipse([cx - r - w / 2 - 5, cy - r - w / 2 - 5, cx + r + w / 2 + 5, cy + r + w / 2 + 5], outline='#140c0e', width=w + 10)
    d.arc(box, -90, -90 + 360 * it['percent'] / 100, fill=c, width=w)
    d.arc(box, -90 + 360 * it['percent'] / 100, 270, fill=it.get('rest', '#ffffff55'), width=w)

def render(t):
    global W, H
    W, H = (1080, 1920) if t.get('vertical') else (1280, 720)
    im = grade(background(t), t.get('grade', P.get('look', 'cold')))
    im = darken(im, t.get('darken', 'left'))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for it in t.get('items', []):
        if 'face' in it: face_item(layer, it, t['name']); d = ImageDraw.Draw(layer)
        elif 'text' in it and re.search('[\u0980-\u09FF]', it['text']): bangla_item(layer, it); d = ImageDraw.Draw(layer)
        elif 'text' in it: text_item(d, it)
        elif 'arrow' in it: arrow_item(d, it)
        elif 'ring' in it: ring_item(d, it)
        elif 'box' in it:
            x, y, w, h = it['box']; c = it.get('color', '#000000').lstrip('#')
            d.rounded_rectangle([x, y, x + w, y + h], radius=it.get('radius', 18), fill=tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (round(255 * it.get('alpha', 0.5)),))
    if t.get('credit'):
        f = font(20, 'Medium', 'body'); d.text((18, H - 34), t['credit'], font=f, fill=(255, 255, 255, 210), stroke_width=2, stroke_fill=(0, 0, 0, 200))
    im = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')
    path = os.path.join(OUT, t['name'] + '.jpg')
    for q in (92, 85, 78):
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < 2_000_000: break
    return path, im

specs = json.load(open(os.path.join(DATA, 'thumbnails.json'), encoding='utf-8'))
want = set(sys.argv[1:])
done = [render(t) for t in specs if not want or t['name'] in want]
# Phone-size check: each thumbnail at 360 px (home feed) and 160 px (lists), side by side.
row = 210
sheet = Image.new('RGB', (360 + 160 + 60, row * len(done) + 20), (24, 24, 24))
for n, (path, im) in enumerate(done):
    for box, x in (((360, 203), 20), ((160, 90), 400)):
        small = im.copy(); small.thumbnail(box, Image.LANCZOS)
        sheet.paste(small, (x, 10 + n * row + (0 if box[1] > 100 else 56)))
sheet.save(os.path.join(OUT, 'phone_size_check.jpg'), quality=85)
# TV check: YouTube on a TV often shows only the top of a recommended video, so show each thumbnail with its lower half covered.
wide = [im for _, im in done if im.height < im.width]   # vertical Short covers do not appear in TV rows
tv = Image.new('RGB', (640, max(1, len(wide)) * 370), '#101010')
for n, im in enumerate(wide):
    small = im.convert('RGB').resize((640, 360), Image.LANCZOS)
    small.paste((16, 16, 16), (0, 180, 640, 360)); tv.paste(small, (0, n * 370))
tv.save(os.path.join(OUT, 'tv_half_check.jpg'), quality=85)
for path, _ in done: print(f'{os.path.relpath(path, ROOT)}  {os.path.getsize(path) // 1024} KB')
print('phone-size check: 05_Motion_Graphics/thumbnails/phone_size_check.jpg')
print('TV check, lower half covered: 05_Motion_Graphics/thumbnails/tv_half_check.jpg')
