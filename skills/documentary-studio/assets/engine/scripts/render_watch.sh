#!/bin/bash
# Render one Remotion composition with a watchdog. A dead Chrome can leave a render hanging forever with no error,
# so this stops the job if Chrome closes or the log goes quiet for 10 minutes.
# Usage: render_watch.sh <composition> <output.mp4> [extra remotion flags]. Run from the remotion folder.
COMP="$1"; OUT="$2"; shift 2
LOG="${TMPDIR:-/tmp}/docstudio/render_${COMP}.log"; mkdir -p "$(dirname "$LOG")"; : > "$LOG"
FREE_GB=$(df -g . | tail -1 | awk '{print $4}')
if [ "${FREE_GB:-99}" -lt 10 ]; then
  echo "WARNING: only ${FREE_GB} GB free on this disk. Renders have failed below about 4 GB. Free space first."
fi
npx remotion render src/index.ts "$COMP" "$OUT" --codec=h264 --crf=18 --audio-codec=aac --audio-bitrate=256k \
  --concurrency=3 --timeout=300000 "$@" >> "$LOG" 2>&1 &
PID=$!
stop_job() { pkill -P "$PID" 2>/dev/null; kill "$PID" 2>/dev/null; }
report() { tr '\r' '\n' < "$LOG" | grep -E 'Rendered|Encoded|rror' | tail -2 | cut -c1-200; }
LAST_SIZE=-1; LAST_CHANGE=$(date +%s)
while kill -0 "$PID" 2>/dev/null; do
  sleep 20
  if grep -qE 'Target closed|Session closed' "$LOG"; then
    stop_job; echo "WATCHDOG: Chrome closed during the render of $COMP. Check free disk space and other Remotion jobs, then retry."; report; exit 3
  fi
  SIZE=$(wc -c < "$LOG"); NOW=$(date +%s)
  if [ "$SIZE" != "$LAST_SIZE" ]; then LAST_SIZE=$SIZE; LAST_CHANGE=$NOW; fi
  if [ $((NOW - LAST_CHANGE)) -ge 600 ]; then
    stop_job; echo "WATCHDOG: no progress for 10 minutes on $COMP."; report; exit 4
  fi
done
wait "$PID"; CODE=$?
report
if [ "$CODE" = 0 ]; then echo "RENDER_DONE $COMP"; else echo "RENDER_FAILED $COMP code $CODE. Full log: $LOG"; fi
exit "$CODE"
