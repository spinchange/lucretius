"""Refresh the text of audiobook chunks whose narration-source lines changed,
without re-chunking the book (prepare would discard every accepted candidate).

Usage: python tools/refresh_chunks.py N [--apply]
Reads audiobook-build-book0N/manifest.json and audiobook-source/book_0N.txt,
recomputes each chunk's text from its stored line range (as rebalance-boundary
does), and for every chunk whose canonical text differs: archives the old
chunk record under superseded_chunk_versions, marks its candidates
"superseded" (so `accept --auto` sees only new passes), clears the accepted
candidate, rewrites the chunk text file and updates source_sha256. Without
--apply it only reports. Prints the chunk ids to pass to `synthesize --chunks`.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_audiobook as b

def main():
    n = int(sys.argv[1]); apply = "--apply" in sys.argv
    build_dir = b.ROOT / f"audiobook-build-book{n:02d}"
    manifest = b.load_manifest(build_dir)
    source = b.resolve_stored_path(manifest["source_path"])
    units = b.parse_translation(source)
    pron = {}
    for headword, instruction in manifest.get("pronunciation_notes", {}).items():
        pron[headword] = {"instruction": instruction, "status": "confirmed"}
    changed, over = [], []
    for chunk in manifest["chunks"]:
        selected = b.select_ranges(units, [[chunk["line_start"], chunk["line_end"]]])
        text = b.chunk_text(selected)
        if text == chunk["canonical_text"]:
            continue
        changed.append(chunk["id"])
        if len(text) > int(manifest["max_chars"]): over.append(chunk["id"])
        if not apply: continue
        tts_text = b.apply_tts_replacements(text, manifest.get("tts_replacements", {}))
        manifest.setdefault("superseded_chunk_versions", []).append({
            "superseded_at": b.utc_now(),
            "reason": "second-round verse changes (review2); text refreshed, audio re-rendered",
            "chunks": json.loads(json.dumps([chunk], ensure_ascii=False))})
        for cand in chunk["candidates"]:
            cand["status"] = "superseded"
            cand["superseded_at"] = b.utc_now()
        b.resolve_stored_path(chunk["text_path"]).write_text(text + "\n", encoding="utf-8", newline="\n")
        chunk.update({
            "canonical_text": text, "tts_text": tts_text,
            "canonical_sha256": b.sha256_text(text), "tts_sha256": b.sha256_text(tts_text),
            "characters": len(text), "words": len(b.normalize_words(text)),
            "ends_on_sentence_boundary": b.ends_sentence(selected[-1].verses[-1].text),
            "pronunciations": b.pronunciations_for_text(text, pron),
            "accepted_candidate": None})
    if apply:
        manifest["source_sha256"] = b.sha256_bytes(source.read_bytes())
        if manifest.get("human_review"):
            manifest["human_review"]["status"] = "reopened"
            manifest["human_review"]["reopened_at"] = b.utc_now()
        b.save_manifest(build_dir, manifest)
    print(f"book {n}: {len(changed)} chunk(s) changed {'(applied)' if apply else '(dry run)'}: {' '.join(changed)}"
          + (f"; OVER max_chars: {' '.join(over)}" if over else ""))

if __name__ == "__main__":
    main()
