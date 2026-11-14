# Time every English narration word in the English voiceover (whisper.cpp + text alignment).
# Writes data/vo_words_en.json and prints each sentence with its first word index (use these in shotlist.json).
# Needs: brew install whisper-cpp, and ~/.cache/whisper/ggml-base.en.bin.
import difflib, json, os, re, subprocess, sys, tempfile
from common import DATA, ROOT, vo_path

MODEL = os.path.expanduser('~/.cache/whisper/ggml-base.en.bin')
if not os.path.exists(MODEL):
    sys.exit(f'Speech model missing: {MODEL}. Disk cleanups can remove it. Run setup.sh --install, or download ggml-base.en.bin to that path.')
sentences = json.load(open(os.path.join(DATA, 'sentences.json'), encoding='utf-8'))
words = ' '.join(s['en'] for s in sentences).split()

tmp = tempfile.mkdtemp()
wav = os.path.join(tmp, 'vo16k.wav')
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', vo_path('en'), '-ar', '16000', '-ac', '1', wav], check=True)
subprocess.run(['whisper-cli', '-m', MODEL, '-f', wav, '-ml', '1', '-sow', '-mc', '0', '-ojf', '-of', os.path.join(tmp, 'w'), '-np'],
               check=True, capture_output=True)
segs = json.loads(open(os.path.join(tmp, 'w.json'), 'rb').read().decode('utf-8', errors='replace'))['transcription']
heard = [(s['text'].strip(), s['offsets']['from'] / 1000, s['offsets']['to'] / 1000) for s in segs if s['text'].strip()]

# Numbers are often heard as digits but written as words (or the reverse): fold a few common forms.
NUM = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
       'fifteen': '15', 'twenty': '20', 'thirty': '30', 'hundred': '100'}
norm = lambda x: NUM.get(re.sub(r"[^a-z0-9.]", '', x.lower()).strip('.'), re.sub(r"[^a-z0-9.]", '', x.lower()).strip('.'))
A, B = [norm(w) for w in words], [norm(h[0]) for h in heard]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
T = [None] * len(words)
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        T[a + k] = (heard[b + k][1], heard[b + k][2])
matched = sum(t is not None for t in T)
i = 0
while i < len(T):
    if T[i] is None:
        j = i
        while j < len(T) and T[j] is None: j += 1
        s = T[i - 1][1] if i > 0 else 0.0
        e = T[j][0] if j < len(T) else heard[-1][2]
        for k in range(j - i): T[i + k] = (s + (e - s) * k / (j - i), s + (e - s) * (k + 1) / (j - i))
        i = j
    else:
        i += 1
out = [{'w': w, 's': round(t[0], 3), 'e': round(t[1], 3)} for w, t in zip(words, T)]
json.dump(out, open(os.path.join(DATA, 'vo_words_en.json'), 'w'), indent=0)
print(f'{matched}/{len(words)} words matched by speech recognition, rest interpolated. Duration {out[-1]["e"]:.1f}s')
if matched / len(words) < 0.8:
    print('WARNING: low match rate. Check that the voiceover reads the same text as script_master.tsv.')
for s in sentences:
    print(f"{s['en_word']:4d}  {out[s['en_word']]['s']:7.2f}s  {s['en'][:90]}")
