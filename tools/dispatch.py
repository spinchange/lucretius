"""Dispatch segment work to headless Claude models (claude -p) and record it.

Stages and defaults:
  translate  opus    Latin segment -> line-for-line English (segments/bNN/sKK.translate.txt)
  fidelity   sonnet  Latin + English -> findings table      (sKK.fidelity.txt)
  annotate   sonnet  English + Latin -> draft notes           (sKK.annotate.txt)
A segment is ready for fidelity/annotate once translate is done. Output and
stage records go to segments/manifest.json, so a run can be stopped and
resumed at any time; nothing lives in a conversation.

Billing: by default ANTHROPIC_API_KEY is removed from the child environment
so claude -p uses the claude.ai login (your subscription). Pass
--billing api to leave the key in place and bill the API instead.

Usage:
  python tools/dispatch.py --stage translate --book 1 --max 3
  python tools/dispatch.py --stage fidelity --ids b01s01,b01s02
  python tools/dispatch.py --stage translate --all --dry-run
"""
import argparse, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from common import ROOT, PROMPTS, load_manifest, update_stage, read_book, fmt_line, seg_path, strip_fences
import check_segment

DEFAULT_MODEL = {"translate": "opus", "fidelity": "sonnet", "annotate": "sonnet"}
CONTEXT = 8
RUNS = ROOT / "runs"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def context(entry, before=True):
    rows = read_book(entry["book"])
    if before:
        lo = max(0, entry["start_idx"] - CONTEXT); sl = rows[lo:entry["start_idx"]]
    else:
        sl = rows[entry["end_idx"] + 1:entry["end_idx"] + 1 + CONTEXT]
    return "\n".join(fmt_line(k, t) for k, t in sl) or "(none: book boundary)"


def build_prompt(stage, entry):
    tpl = (PROMPTS / f"{stage}.md").read_text(encoding="utf-8")
    fields = {
        "book": entry["book"], "first": entry["first"], "last": entry["last"], "n": entry["n"],
        "conventions": (ROOT / "translation" / "CONVENTIONS.md").read_text(encoding="utf-8"),
        "sample": (ROOT / "translation" / "proem_sample.txt").read_text(encoding="utf-8"),
        "before": context(entry, True), "after": context(entry, False),
        "segment": seg_path(entry, "latin").read_text(encoding="utf-8"),
    }
    if stage in ("fidelity", "annotate"):
        fields["english"] = seg_path(entry, "translate").read_text(encoding="utf-8")
    return tpl.format(**fields)


def ready(entry, stage):
    st = entry["stages"]
    if st.get(stage, {}).get("status") == "done":
        return False
    if stage in ("fidelity", "annotate"):
        return st.get("translate", {}).get("status") == "done"
    return True


def run_one(entry, stage, model, billing, timeout):
    prompt = build_prompt(stage, entry)
    env = dict(os.environ)
    if billing == "subscription":
        env.pop("ANTHROPIC_API_KEY", None)
    exe = shutil.which("claude")
    cmd = [exe, "-p", "--model", model, "--output-format", "text", "--max-turns", "1"]
    RUNS.mkdir(exist_ok=True)
    t0 = time.time()
    r = subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, cwd=str(RUNS), env=env, timeout=timeout)
    out = strip_fences(r.stdout.decode("utf-8", "replace").replace("\r\n", "\n"))
    err = r.stderr.decode("utf-8", "replace")
    (RUNS / f"{entry['id']}.{stage}.log").write_text(err, encoding="utf-8")
    ok = r.returncode == 0 and len(out.strip()) > 0
    if ok:
        seg_path(entry, stage).write_text(out, encoding="utf-8")
    return ok, out, err, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=list(DEFAULT_MODEL))
    ap.add_argument("--model"); ap.add_argument("--book", type=int)
    ap.add_argument("--ids"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--max", type=int, default=3, help="concurrent runs")
    ap.add_argument("--limit", type=int, default=0, help="stop after this many segments (0 = no limit)")
    ap.add_argument("--billing", choices=["subscription", "api"], default="subscription")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    model = a.model or DEFAULT_MODEL[a.stage]
    m = load_manifest()
    want = set(a.ids.split(",")) if a.ids else None
    if not (want or a.book or a.all):
        print("say which segments: --book N, --ids a,b or --all"); sys.exit(2)
    todo = [e for e in m["segments"] if ready(e, a.stage)
            and (want is None or e["id"] in want) and (a.book is None or e["book"] == a.book)]
    if a.limit: todo = todo[:a.limit]
    print(f"{a.stage} with {model} ({a.billing}): {len(todo)} segments: {', '.join(e['id'] for e in todo)}", flush=True)
    if a.dry_run:
        if todo: print(build_prompt(a.stage, todo[0])[:3000])
        return
    by_id = {e["id"]: e for e in m["segments"]}
    for e in todo:
        e["stages"][a.stage] = {"status": "running", "model": model, "started": now()}
        update_stage(e["id"], a.stage, e["stages"][a.stage])
    with ThreadPoolExecutor(max_workers=a.max) as ex:
        futs = {ex.submit(run_one, e, a.stage, model, a.billing, a.timeout): e for e in todo}
        for f in as_completed(futs):
            e = futs[f]; rec = by_id[e["id"]]["stages"][a.stage]
            try:
                ok, out, err, secs = f.result()
            except Exception as ex_:
                ok, out, err, secs = False, "", repr(ex_), 0
            rec.update({"status": "done" if ok else "error", "finished": now(), "seconds": round(secs)})
            if not ok:
                rec["error"] = err.strip().splitlines()[-1][:200] if err.strip() else "empty output"
            if ok and a.stage == "translate":
                probs = check_segment.check(by_id[e["id"]], quiet=True)
                rec["check"] = "clean" if not probs else probs
            update_stage(e["id"], a.stage, rec)
            msg = f"{e['id']}: {'ok' if ok else 'ERROR'} in {secs:.0f}s"
            if not ok: msg += f" :: {rec['error']}"
            elif a.stage == "translate": msg += " :: " + ("check clean" if rec["check"] == "clean" else "; ".join(rec["check"]))
            print(msg, flush=True)


if __name__ == "__main__":
    main()
