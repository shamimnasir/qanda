# After publishing: turn the producer's YouTube Studio numbers into a plain diagnosis and update the channel ledger.
# The producer adds rows to 11_Performance/metrics.csv. Results go to 11_Performance/review.md and ../_Channel/video_ledger.csv.
# Compares only with the channel's own earlier films; "low" and "strong" (below 80%, above 120% of the median) are our own working lines.
# Usage: python3 performance_review.py
import csv, os, statistics
from common import P, ROOT

PERF = os.path.join(ROOT, '11_Performance')
SHEET = os.path.join(PERF, 'metrics.csv')
LEDGER = os.path.join(os.path.dirname(ROOT), '_Channel', 'video_ledger.csv')
FIELDS = ['video', 'language', 'checkpoint', 'impressions', 'click_rate_percent', 'views', 'shorts_stayed_to_watch_percent', 'percent_still_watching_at_30s',
          'average_percent_viewed', 'biggest_drop_time', 'next_step_clicks', 'leads', 'customers', 'revenue', 'notes']
MIN_FILMS = 3
SLUG = P['slug']

def num(row, key):
    """A number from a typed cell ("12,400", "5.2%"), or None when blank or not a number."""
    try: return float(str(row.get(key, '')).replace(',', '').replace('%', '').strip())
    except ValueError: return None

def read(path):
    if not os.path.exists(path): return []
    with open(path, encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

def save(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fields, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def key(row): return (row.get('video', '').strip(), row.get('language', '').strip(), row.get('checkpoint', '').strip())

if not read(SHEET):
    if not os.path.exists(SHEET): save(SHEET, FIELDS, [])
    print(f'No numbers yet. Add a row per video and language to {os.path.relpath(SHEET, ROOT)} at 48h, 7d and 28d, then run this again.')
    print('video = film or short. Leave anything you do not have blank.')
    raise SystemExit

rows = [r for r in read(SHEET) if any(key(r))]
earlier = [r for r in read(LEDGER) if r.get('film') != SLUG]
lines = [f'# Performance review: {P["title"]}', '',
         'Numbers are typed from YouTube Studio by the producer. High and low compare only with this channel\'s earlier films.', '']

def compare(row, field):
    """(ratio to the channel median, number of earlier films), or (None, count) when there are too few."""
    same = [num(r, field) for r in earlier if key(r) == key(row)]
    same = [v for v in same if v is not None]
    value = num(row, field)
    if value is None or len(same) < MIN_FILMS: return None, len(same)
    mid = statistics.median(same)
    return (value / mid if mid else None), len(same)

def diagnose(row):
    out = []
    flag = {}
    for field in ('impressions', 'click_rate_percent', 'shorts_stayed_to_watch_percent', 'percent_still_watching_at_30s', 'average_percent_viewed', 'next_step_clicks'):
        ratio, _ = compare(row, field)
        flag[field] = None if ratio is None else 'low' if ratio < 0.8 else 'strong' if ratio > 1.2 else 'normal'
    if flag['impressions'] == 'low': out.append('Few impressions: look first at topic demand and audience fit.')
    if flag['click_rate_percent'] == 'low': out.append('Low click rate: look first at the title and thumbnail. Test a clearer promise.')
    if flag['shorts_stayed_to_watch_percent'] == 'low': out.append('Many viewers swipe away: look first at the first frame and hook. Is it clear with the sound off?')
    if row.get('video', '').strip().lower() == 'short' and flag['average_percent_viewed'] == 'low':
        at = row.get('biggest_drop_time', '').strip()
        out.append(f'Low average viewed on this Short: cut wasted seconds{" around " + at if at else ""}, and check the final seconds.')
    if flag['percent_still_watching_at_30s'] == 'low': out.append('Viewers leave early: the opening may not match the packaging. Check Promise, Proof, Plan.')
    elif flag['average_percent_viewed'] == 'low' and row.get('video', '').strip().lower() != 'short':
        at = row.get('biggest_drop_time', '').strip()
        out.append(f'Good start, low average viewed: look at the story\'s middle{" around " + at if at else ""}.')
    if flag['next_step_clicks'] == 'low' and num(row, 'next_step_clicks'): out.append('Few next step clicks: check that the step fits the film and where it appears.')
    clicks, leads, customers = num(row, 'next_step_clicks'), num(row, 'leads'), num(row, 'customers')
    if num(row, 'views') and clicks == 0: out.append('Views but no next step clicks: the next step is missing, hidden or not wanted.')
    if clicks and leads == 0: out.append('Clicks but no leads: check the page and the resource.')
    if leads and customers == 0: out.append('Leads but no customers: review the offer or sales process, not the film.')
    return out

for row in rows:
    v, lang, cp = key(row)
    lines += [f'## {v or "video"}, {lang or "language not set"}, {cp or "checkpoint not set"}']
    funnel = [(n, row.get(f, '').strip()) for n, f in (('Impressions', 'impressions'), ('Click rate %', 'click_rate_percent'), ('Views', 'views'), ('Short: stayed to watch %', 'shorts_stayed_to_watch_percent'),
              ('Still watching at 30 s %', 'percent_still_watching_at_30s'), ('Average viewed %', 'average_percent_viewed'), ('Next step clicks', 'next_step_clicks'),
              ('Leads', 'leads'), ('Customers', 'customers'), ('Revenue', 'revenue'))]
    lines += [f'- {n}: {val}' + (lambda r: f' ({r:.2f}x the channel median)' if r is not None else '')(compare(row, f)[0])
              for (n, val), f in zip(funnel, ('impressions', 'click_rate_percent', 'views', 'shorts_stayed_to_watch_percent', 'percent_still_watching_at_30s', 'average_percent_viewed', 'next_step_clicks', 'leads', 'customers', 'revenue')) if val]
    count = compare(row, 'views')[1]
    if count < MIN_FILMS: lines.append(f'- Baseline: {count} earlier films at this checkpoint, {MIN_FILMS} needed, so high and low are not judged yet.')
    found = diagnose(row)
    lines += [f'- **{x}**' for x in found] or ['- No clear problem found from these numbers.']
    lines.append('')
lines += ['## Decision', '- One main change for the next film:', '- Signal or rule for `_Channel/learned_rules.md`:', '- Is a win repeatable? The next film to test it:', '']
report = os.path.join(PERF, 'review.md')
open(report, 'w', encoding='utf-8').write('\n'.join(lines))

ledger_fields = ['film'] + FIELDS
kept = {(r.get('film'),) + key(r): r for r in read(LEDGER)}
for r in rows: kept[(SLUG,) + key(r)] = {**r, 'film': SLUG}
save(LEDGER, ledger_fields, list(kept.values()))
print('\n'.join(lines))
print(f'Wrote {os.path.relpath(report, ROOT)} and updated the channel ledger ({len(kept)} rows).')
