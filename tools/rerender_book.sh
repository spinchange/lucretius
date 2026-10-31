#!/bin/bash
# runs/rerender_book.sh N : refresh the changed chunks of Book N, synthesize them, QA, auto-accept, report.
N=$1; B=audiobook-build-book0$N
cd "H:/My Drive/agent-journal/lucretius" || exit 1
OUT=$(python tools/refresh_chunks.py $N --apply); echo "$OUT"
IDS=$(echo "$OUT" | sed 's/.*(applied): //; s/;.*//')
[ -z "$IDS" ] && { echo "no chunks to render"; exit 0; }
python tools/build_audiobook.py synthesize --build-dir $B --chunks $IDS --timeout 300 --retries 4 || exit 1
python tools/build_audiobook.py qa --build-dir $B --chunks $IDS --timeout 300 --retries 4 || exit 1
python tools/build_audiobook.py accept --build-dir $B --auto --chunks $IDS
python tools/build_audiobook.py report --build-dir $B
echo "RERENDER DONE book $N"
