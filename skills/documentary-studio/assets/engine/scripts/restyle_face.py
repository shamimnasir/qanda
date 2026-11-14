# Make a new look from a producer cutout, on this Mac, with no upload and no credits.
# Usage: python3 restyle_face.py in.webp out.webp [--mood sad|stern] [--strength 1.0] [--style cinema|noir|halftone|ink|none] [--color '#ff4f45']
# --mood gently moves the mouth corners and brows (it cannot make a new pose). --style changes the picture.
# The results are edited illustrations: log them in the tracker and say so.
import argparse, json, os, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
a = argparse.ArgumentParser()
a.add_argument('src'); a.add_argument('out'); a.add_argument('--mood'); a.add_argument('--strength', type=float, default=1.0)
a.add_argument('--style', default='none'); a.add_argument('--color', default='#ff4f45'); a.add_argument('--light', default='left')
A = a.parse_args()
im = Image.open(A.src).convert('RGBA')
arr = np.asarray(im).astype(np.float32); H, W = arr.shape[:2]

def rgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)

def landmarks():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'flat.png'); bg = Image.new('RGBA', im.size, (200, 200, 200, 255)); bg.alpha_composite(im); bg.convert('RGB').save(p)
        return json.loads(subprocess.run(['swift', os.path.join(HERE, 'face_landmarks.swift'), p], check=True, capture_output=True, text=True).stdout)

def warp(px, moves):
    """Move each (x, y, dx, dy, radius) smoothly. Small moves only, so the face stays the producer's."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); sx, sy = xx.copy(), yy.copy()
    for x, y, dx, dy, r in moves:
        w = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * r * r)); sx -= w * dx; sy -= w * dy
    x0 = np.clip(sx, 0, W - 2); y0 = np.clip(sy, 0, H - 2); xi = x0.astype(int); yi = y0.astype(int); fx = (x0 - xi)[..., None]; fy = (y0 - yi)[..., None]
    return px[yi, xi] * (1 - fx) * (1 - fy) + px[yi, xi + 1] * fx * (1 - fy) + px[yi + 1, xi] * (1 - fx) * fy + px[yi + 1, xi + 1] * fx * fy

def mood(px, kind, k):
    L = landmarks(); (bx0, by0), (bx1, by1) = L['box']; fh = by1 - by0; lips = np.array(L['lips']); cx = (bx0 + bx1) / 2
    lc, rc = lips[lips[:, 0].argmin()], lips[lips[:, 0].argmax()]
    r = fh * 0.10; moves = [(lc[0], lc[1], fh * .006 * k, fh * .032 * k, r), (rc[0], rc[1], -fh * .006 * k, fh * .032 * k, r)]
    for name in ('left_brow', 'right_brow'):
        b = np.array(L[name]); inner = b[np.abs(b[:, 0] - cx).argmin()]; outer = b[np.abs(b[:, 0] - cx).argmax()]; toward = np.sign(cx - inner[0])
        if kind == 'sad': moves += [(inner[0], inner[1], toward * fh * .006 * k, -fh * .022 * k, fh * .07), (outer[0], outer[1], 0, fh * .016 * k, fh * .07)]
        else: moves += [(inner[0], inner[1], toward * fh * .012 * k, fh * .026 * k, fh * .07), (outer[0], outer[1], 0, -fh * .006 * k, fh * .07)]
    return warp(px, moves), L

def gray(px): return (px[..., :3] * [0.299, 0.587, 0.114]).sum(-1) / 255

def curve(g, lo=.12, hi=.86, gamma=1.0): return np.clip((g - lo) / (hi - lo), 0, 1) ** gamma

def cinema(px):
    """Natural colour with a soft key light from one side, and the shadows tinted to match the scene (--color)."""
    xs = np.where((px[..., 3] > 10).any(0))[0]; u = (np.arange(W) - xs[0]) / max(1, xs[-1] - xs[0])
    if A.light == 'right': u = 1 - u
    light = np.clip(1.12 - np.clip(u - .35, 0, 1) * 1.05, .42, 1.12)[None, :, None]
    c = px[..., :3] / 255; g = (c * [0.299, 0.587, 0.114]).sum(-1, keepdims=True)
    c = g + (c - g) * .86
    c = np.clip(c * light, 0, 1); c = c * c * (3 - 2 * c) * .55 + c * .45
    g = (c * [0.299, 0.587, 0.114]).sum(-1, keepdims=True); shade = np.clip(1 - g * 1.6, 0, 1) * .4
    c = c * (1 - shade) + rgb(A.color) / 255 * g * 1.2 * shade
    return np.dstack([c * 255, px[..., 3]])

def noir(px):
    """Black and white with a hard cold window light from one side, the other half of the face in shadow."""
    g = curve(gray(px), .1, .82); u = np.linspace(0, 1, W)[None, :]
    alive = px[..., 3] > 10; xs = np.where(alive.any(0))[0]; c = (xs[0] + xs[-1]) / 2 / W
    light = np.clip(1.15 - (u - (c - .12)) * 3.4, .1, 1.15)
    v = np.clip(g * light, 0, 1) ** 1.15
    tint = v[..., None] * np.array([190, 215, 255.]) + (1 - v[..., None]) * np.array([4, 7, 14.])
    return np.dstack([tint, px[..., 3]])

def halftone(px):
    """Two-colour print: ink dots on the accent colour, like a protest poster."""
    g = curve(gray(px), .12, .8); cell = max(6, W // 130); yy, xx = np.mgrid[0:H, 0:W]; t = np.radians(45)
    u = (xx * np.cos(t) + yy * np.sin(t)) / cell; v = (-xx * np.sin(t) + yy * np.cos(t)) / cell
    d = np.hypot(u - np.round(u), v - np.round(v)) * 1.41
    ink = np.clip((np.sqrt(np.clip(1 - g, 0, 1)) * 1.05 - d) * 5, 0, 1)
    solid = np.clip((.2 - g) * 8, 0, 1); ink = np.maximum(ink, solid)
    paper = rgb(A.color); col = paper * (1 - ink[..., None]) + np.array([12, 8, 10.]) * ink[..., None]
    return np.dstack([col, px[..., 3]])

def ink_style(px):
    """Graphic novel: flat tones with dark ink lines."""
    g = curve(gray(px), .1, .85); levels = np.array([.06, .3, .6, .95]); idx = np.digitize(g, [.2, .45, .72]); flat = levels[idx]
    b = np.asarray(Image.fromarray(np.uint8(g * 255)).filter(ImageFilter.GaussianBlur(max(2, W / 300)))).astype(np.float32) / 255
    edge = np.clip((b - g - .05) * 7, 0, 1); v = (flat * (1 - edge))[..., None]
    c = rgb(A.color); col = v * (c * .35 + 255 * .65) + (1 - v) * np.array([10, 10, 16.])
    return np.dstack([col, px[..., 3]])

if A.mood: arr, _ = mood(arr, A.mood, A.strength)
arr = {'cinema': cinema, 'noir': noir, 'halftone': halftone, 'ink': ink_style, 'none': lambda p: p}[A.style](arr)
Image.fromarray(np.uint8(np.clip(arr, 0, 255))).save(A.out, quality=92, method=6)
print('saved', A.out)
