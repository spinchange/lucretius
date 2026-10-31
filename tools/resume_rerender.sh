#!/bin/bash
# runs/resume_rerender.sh N : finish an interrupted re-render of Book N.
# Synthesizes only chunks that still lack a fresh candidate, QAs candidates
# without QA, auto-accepts, reports. Safe to re-run.
N=$1; B=audiobook-build-book0$N
cd "H:/My Drive/agent-journal/lucretius" || exit 1
# Optional local credentials: runs/ is gitignored. One line: OPENAI_API_KEY=sk-...
[ -f runs/openai.env ] && set -a && . runs/openai.env && set +a
# Otherwise take the current user-level Windows variable, which a running
# Claude Code session does not see if it was changed after the session began.
if [ ! -f runs/openai.env ]; then
  K=$(powershell -NoProfile -Command '[Environment]::GetEnvironmentVariable("OPENAI_API_KEY","User")' | tr -d '\r\n ')
  [ -n "$K" ] && export OPENAI_API_KEY="$K"
fi
python tools/refresh_chunks.py $N --apply
read -r SYN QA <<< "$(python - $N <<'PY'
import json, sys
n = int(sys.argv[1]); m = json.load(open(f"audiobook-build-book0{n}/manifest.json", encoding="utf-8"))
fresh = lambda c: [x for x in c["candidates"] if x.get("status") != "superseded"]
syn = [c["id"] for c in m["chunks"] if c["accepted_candidate"] is None and not fresh(c)]
qa = [c["id"] for c in m["chunks"] if any(not x.get("qa") for x in fresh(c))]
print(",".join(syn) or "-", ",".join(qa) or "-")
PY
)"
if [ "$SYN" != "-" ]; then python tools/build_audiobook.py synthesize --build-dir $B --chunks ${SYN//,/ } --timeout 300 --retries 4 || exit 1; fi
ALL=$(python - $N <<'PY'
import json, sys
n = int(sys.argv[1]); m = json.load(open(f"audiobook-build-book0{n}/manifest.json", encoding="utf-8"))
print(" ".join(c["id"] for c in m["chunks"] if c["accepted_candidate"] is None))
PY
)
[ -z "$ALL" ] && { echo "book $N: nothing pending"; exit 0; }
python tools/build_audiobook.py qa --build-dir $B --chunks $ALL --timeout 300 --retries 4 || exit 1
python tools/build_audiobook.py accept --build-dir $B --auto --chunks $ALL
python tools/build_audiobook.py report --build-dir $B
echo "RESUME DONE book $N"
