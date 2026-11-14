# Turn 01_Script/script_master.tsv into paste-ready ElevenLabs files and plain narration for every language.
#
# script_master.tsv: one sentence per row, tab separated, with a header row:
#   break   tags              en                        en_tts (optional)                bn
#   para    [quietly]         This wolf did not die.    This wolf did not die.           এই নেকড়েটা মারা যায়নি।
#   line                      It stopped moving...      ...                              ...
# break: "para" = blank line before the row, "line" = new line, empty = same line as the previous sentence.
# A row with tags but no text (for example "[long pause]") is a standalone pause.
# en is what the captions show (digits are fine); en_tts is what the voice reads (numbers spelled out). bn is both.
import csv, json, os
from common import DATA, ROOT

SRC = os.path.join(ROOT, '01_Script', 'script_master.tsv')
rows = list(csv.DictReader(open(SRC, encoding='utf-8'), delimiter='\t'))
langs = [c for c in rows[0].keys() if c not in ('break', 'tags', 'en_tts') and not c.endswith('_tts')]

def paste_text(lang):
    out = []
    for r in rows:
        text = (r.get(f'{lang}_tts') or r.get(lang) or '').strip()
        tags = (r.get('tags') or '').strip()
        piece = ' '.join(x for x in (tags, text) if x)
        if not piece:
            continue
        sep = {'para': '\n\n', 'line': '\n'}.get((r.get('break') or '').strip(), ' ')
        out.append((sep if out else '') + piece)
    return ''.join(out).strip() + '\n'

sentences, word_at = [], 0
for r in rows:
    en = (r.get('en') or '').strip()
    if not en:
        continue
    item = {'en': en, 'en_word': word_at}
    for lang in langs:
        if lang != 'en':
            item[lang] = (r.get(lang) or '').strip()
    sentences.append(item)
    word_at += len(en.split())
os.makedirs(DATA, exist_ok=True)
json.dump(sentences, open(os.path.join(DATA, 'sentences.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

for lang in langs:
    paste = paste_text(lang)
    open(os.path.join(ROOT, '01_Script', f'elevenlabs_{lang}.txt'), 'w', encoding='utf-8').write(paste)
    plain = ' '.join(s['en'] if lang == 'en' else s.get(lang, '') for s in sentences)
    open(os.path.join(ROOT, '01_Script', f'narration_{lang}.txt'), 'w', encoding='utf-8').write(plain + '\n')
    dashes = [c for c in paste if c in chr(0x2014) + chr(0x2013)]
    print(f"{lang}: {len(paste)} characters to paste (about {len(paste)} ElevenLabs credits on v3/v4), "
          f"{len(plain.split())} words{', LONG DASHES FOUND' if dashes else ''}")
print(f'{len(sentences)} sentences -> data/sentences.json')
