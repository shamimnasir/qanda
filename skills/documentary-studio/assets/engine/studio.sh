#!/bin/bash
# Documentary Studio pipeline. Run from anywhere: ./studio.sh <step> [args]
#   scripts            script_master.tsv -> ElevenLabs paste files + narration (shows credit cost)
#   align              time the English VO (Whisper) and every other language VO (pause fitting)
#   media [ids...]     search Pexels + Commons, write contact sheets to 08_Timeline_and_Exports/review/
#   pool               search project.json media_pool for themed clips, write review/pool_N.jpg
#   download           download picks (data/picks.json), log licenses
#   build              timelines for every language, map, trimmed clips
#   sound              score, mix and Short audio for every language
#   docs               tracker.csv, SRT per language, credits for the description
#   stills <lang> <frame> [frame...]   quick picture check, writes renders/stills/
#   render [lang]      film + Short for one language (or all), with a watchdog that stops a hung render
#   render-film [lang] the film only, for a re-cut that keeps the live Short
#   qa                 long dashes, licenses, picks, render length and loudness
#   thumbs [names...]  thumbnails and Short covers from data/thumbnails.json, plus a phone-size check
#   cutout in.jpg out.png  cut a person out of a photo on this Mac (Apple Vision, nothing is uploaded)
#   restyle in.webp out.webp [--mood sad|stern] [--style cinema|noir|halftone|ink]  new look or mood for a cutout, on this Mac
#   upload             gather videos, SRT, thumbnails and paste-ready text into 10_Ready_to_Upload/ (after the publish kit)
#   reference file.mp4 measure a video you may analyze against this film, write review/reference_report.md
#   review             after publishing: diagnose 11_Performance/metrics.csv, update the channel ledger
#   all                scripts, align, build, sound, docs, render, qa (after picks exist)
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
S="$ROOT/08_Timeline_and_Exports/scripts"
R="$ROOT/08_Timeline_and_Exports/remotion"
OUT="$ROOT/08_Timeline_and_Exports/renders"
TMP="${TMPDIR:-/tmp}/docstudio"; mkdir -p "$TMP" "$OUT/stills"
PY="${DOC_PY:-/usr/bin/python3}"; [ -x "$PY" ] || PY=python3
LANGS=$($PY -c "import json;print(' '.join(json.load(open('$ROOT/project.json'))['languages']))")
SLUG=$($PY -c "import json;print(json.load(open('$ROOT/project.json'))['slug'])")
GC="${DOC_CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ -x "$GC" ]; then CHROME=(--browser-executable="$GC" --chrome-mode=chrome-for-testing); else CHROME=(); fi
up() { echo "$1" | tr '[:lower:]' '[:upper:]'; }

step() {
  case "$1" in
    scripts) $PY "$S/build_scripts.py" ;;
    align) $PY "$S/align_en.py"; for l in $LANGS; do [ "$l" != en ] && DOC_LANG=$l $PY "$S/align_lang.py"; done; true ;;
    media) shift; $PY "$S/find_media.py" "$@" ;;
    pool) $PY "$S/find_pool.py" ;;
    reference) $PY "$S/reference_check.py" "$2" ;;
    download) $PY "$S/download_assets.py" ;;
    build)
      for l in $LANGS; do DOC_LANG=$l $PY "$S/build_timeline.py"; done
      if $PY -c "import json,sys;sys.exit(0 if 'map' in json.load(open('$ROOT/project.json')) else 1)"; then $PY "$S/build_map.py"; fi
      $PY "$S/prepare_media.py" ;;
    sound) for l in $LANGS; do DOC_LANG=$l $PY "$S/build_score.py" "$TMP"; DOC_LANG=$l $PY "$S/build_audio.py" "$TMP"; DOC_LANG=$l $PY "$S/build_short.py"; done ;;
    docs) $PY "$S/write_docs.py" ;;
    stills)
      l=$2; shift 2; cd "$R"
      for fr in "$@"; do npx remotion still src/index.ts "Film$(up $l)" "$OUT/stills/${l}_$fr.jpg" --frame=$fr --image-format=jpeg --scale=0.5 --timeout=60000 "${CHROME[@]}" --log=error; done ;;
    render)
      cd "$R"
      for l in ${2:-$LANGS}; do
        bash "$S/render_watch.sh" "Film$(up $l)" "$OUT/${SLUG}_${l}_film.mp4" "${CHROME[@]}" || exit 1
        bash "$S/render_watch.sh" "Short$(up $l)" "$OUT/${SLUG}_${l}_short.mp4" "${CHROME[@]}" || exit 1
        echo "rendered $l"
      done ;;
    render-film)
      cd "$R"
      for l in ${2:-$LANGS}; do
        bash "$S/render_watch.sh" "Film$(up $l)" "$OUT/${SLUG}_${l}_film.mp4" "${CHROME[@]}" || exit 1
      done ;;
    qa) $PY "$S/qa_check.py" "$OUT"/*.mp4 ;;
    thumbs) shift; $PY "$S/make_thumbnails.py" "$@" ;;
    cutout) shift; swift "$S/cutout_face.swift" "$1" "$2" ;;
    restyle) shift; $PY "$S/restyle_face.py" "$@" ;;
    upload) $PY "$S/build_upload.py" ;;
    review) $PY "$S/performance_review.py" ;;
    all) for s in scripts align build sound docs render qa; do echo "== $s"; step $s; done ;;
    *) sed -n '2,18p' "$0"; exit 1 ;;
  esac
}
step "$@"
