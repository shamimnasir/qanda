#!/bin/bash
# One-time setup for the documentary-studio skill on a Mac.
#   bash setup.sh            check everything, change nothing
#   bash setup.sh --install  install what is missing (Homebrew packages, Whisper model, Remotion packages)
#   bash setup.sh --key      store the Pexels API key (typed by the producer, hidden, never printed)
# The Remotion packages are cached once in ~/.cache/documentary-studio/remotion and cloned into each project.
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
CACHE="$HOME/.cache/documentary-studio"
CONF="$HOME/.config/documentary-studio"
MODEL="$HOME/.cache/whisper/ggml-base.en.bin"
MODE="$1"
ok() { echo "  OK      $1"; }
bad() { echo "  MISSING $1"; MISSING=1; }

if [ "$MODE" = "--key" ]; then
  mkdir -p "$CONF"; chmod 700 "$CONF"
  printf "Paste your Pexels API key (hidden), then press Return: "; read -rs KEY; echo
  [ -z "$KEY" ] && { echo "No key entered."; exit 1; }
  (umask 077; echo "PEXELS_API_KEY=$KEY" > "$CONF/.env")
  echo "Saved to $CONF/.env (only your user can read it)."
  exit 0
fi

echo "documentary-studio setup check"
command -v brew >/dev/null && ok "Homebrew" || bad "Homebrew (install from https://brew.sh)"
for t in ffmpeg whisper-cli node npx; do
  if command -v $t >/dev/null; then ok "$t"
  else
    bad "$t"
    if [ "$MODE" = "--install" ] && command -v brew >/dev/null; then
      case $t in ffmpeg) brew install ffmpeg ;; whisper-cli) brew install whisper-cpp ;; node|npx) brew install node ;; esac
    fi
  fi
done
if [ -f "$MODEL" ]; then ok "Whisper English model"
else
  bad "Whisper English model ($MODEL)"
  if [ "$MODE" = "--install" ]; then
    mkdir -p "$(dirname "$MODEL")"
    curl -L --fail -o "$MODEL" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin && ok "downloaded Whisper model"
  fi
fi
[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] && ok "Google Chrome" || bad "Google Chrome (install from google.com/chrome; renders use it)"
PY="${DOC_PY:-/usr/bin/python3}"; [ -x "$PY" ] || PY=python3
if $PY -c "import numpy, PIL" 2>/dev/null; then ok "Python with numpy and Pillow ($PY)"
else
  bad "numpy or Pillow for $PY"
  [ "$MODE" = "--install" ] && $PY -m pip install --user numpy Pillow
fi

# Remotion packages, cached once
mkdir -p "$CACHE/remotion"
if [ -d "$CACHE/remotion/node_modules" ] && cmp -s "$SKILL/assets/engine/remotion/package-lock.json" "$CACHE/remotion/package-lock.json"; then
  ok "Remotion packages ($CACHE/remotion)"
else
  bad "Remotion packages (about 260 MB, one time)"
  if [ "$MODE" = "--install" ] && command -v npm >/dev/null; then
    cp "$SKILL/assets/engine/remotion/package.json" "$SKILL/assets/engine/remotion/package-lock.json" "$CACHE/remotion/"
    (cd "$CACHE/remotion" && npm ci --no-audit --no-fund) && ok "installed Remotion packages"
  fi
fi

[ -f "$CONF/.env" ] && grep -q "^PEXELS_API_KEY=." "$CONF/.env" && ok "Pexels key ($CONF/.env)" || bad "Pexels key: run  bash \"$SKILL/scripts/setup.sh\" --key  in Terminal (free key at pexels.com/api)"

if [ -n "$MISSING" ] && [ "$MODE" != "--install" ]; then echo "Some items are missing. Run with --install to fix the installable ones."; fi
[ -z "$MISSING" ] && echo "All set."
true
