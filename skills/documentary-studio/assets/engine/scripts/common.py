# Shared helpers for every pipeline script: project config, per-language file names, and anchors on the timeline.
#
# Run any script with DOC_LANG=en (default) or DOC_LANG=bn (or any language listed in project.json).
# An "anchor" names a moment in the film. Forms:
#   {"start": true}  {"end": true}
#   {"item": "S14"}  {"item_end": "S14"}        a shot's first or last frame
#   {"word": 120}    {"word_end": 120}          start or end of English word 120 (works in every language)
#   {"gap": 272}                                 start of the gap opened after word 272
# Any anchor may add "offset": seconds.
import json, os, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA = os.path.join(ROOT, '08_Timeline_and_Exports', 'data')
REM = os.path.join(ROOT, '08_Timeline_and_Exports', 'remotion')
SFX_DIR = os.path.join(ROOT, '07_Music_SFX')
P = json.load(open(os.path.join(ROOT, 'project.json'), encoding='utf-8'))
LANG = os.environ.get('DOC_LANG', 'en')
FPS = P.get('fps', 30)
SR = 48000

def f(name):
    """'timeline.json' -> 'timeline_bn.json' outside English."""
    if LANG == 'en':
        return name
    base, ext = os.path.splitext(name)
    return f'{base}_{LANG}{ext}'

def vo_path(lang=None):
    return os.path.join(ROOT, '06_Audio_Voiceover', P['languages'][lang or LANG]['vo'])

def words_path(lang=None):
    lang = lang or LANG
    return os.path.join(DATA, 'vo_words_en.json' if lang == 'en' else f'vo_words_virtual_{lang}.json')

def load_words(lang=None):
    return json.load(open(words_path(lang), encoding='utf-8'))

def timeline_path():
    return os.path.join(REM, 'src', f('timeline.json'))

def load_timeline():
    return json.load(open(timeline_path(), encoding='utf-8'))

def duration(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))

class Anchors:
    """Resolve anchors to film seconds on a built timeline."""

    def __init__(self, tl, words):
        self.tl, self.W = tl, words
        self.T = tl['durationInFrames'] / tl['fps']
        self.items = {x['id']: x for x in tl['items']}
        self.gaps = {g['after_word']: g for g in tl.get('gaps', [])}

    def film_t(self, vo_t):
        for p in self.tl['vo']:
            if p['voStart'] - 1e-6 <= vo_t <= p['voEnd'] + 1e-6:
                return p['from'] + vo_t - p['voStart']
        raise ValueError(f'voiceover time {vo_t} is outside every piece')

    def __call__(self, a):
        off = a.get('offset', 0.0)
        if a.get('start'): t = 0.0
        elif a.get('end'): t = self.T
        elif 'item' in a: t = self.items[a['item']]['from'] / FPS
        elif 'item_end' in a:
            x = self.items[a['item_end']]; t = (x['from'] + x['dur']) / FPS
        elif 'word' in a: t = self.film_t(self.W[a['word']]['s'])
        elif 'word_end' in a: t = self.film_t(self.W[a['word_end']]['e'])
        elif 'gap' in a: t = self.gaps[a['gap']]['from']
        else: raise ValueError(f'unknown anchor {a}')
        return t + off
