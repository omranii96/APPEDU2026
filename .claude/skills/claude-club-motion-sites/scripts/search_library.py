#!/usr/bin/env python3
"""Search the Claude Club Motion Sites catalog with no dependencies."""
import argparse, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[4] / "vendor" / "claude-club-motion-library"  # fetched by tools/motion-skills/fetch.sh libraries
LIBRARY = ROOT / "library" / "library.json"


def load_entries():
    return json.loads(LIBRARY.read_text(encoding="utf-8"))["entries"]


def media_urls(entry):
    text = entry.get("originalPrompt", "")
    return [u.rstrip("),.;]'\"") for u in re.findall(r"https?://[^\s`<>]+", text)]


def score(entry, terms):
    fields = {
        "title": entry.get("title", ""),
        "category": entry.get("category", ""),
        "tags": " ".join(entry.get("tags", [])),
        "surface": entry.get("surface", ""),
        "pattern": entry.get("pattern", ""),
        "prompt": entry.get("originalPrompt", ""),
    }
    values = {k: v.lower() for k, v in fields.items()}
    weights = {"title": 8, "category": 5, "tags": 5, "surface": 3, "pattern": 3, "prompt": 1}
    total = 0
    for term in terms:
        matched = False
        for field, value in values.items():
            count = value.count(term)
            if count:
                total += weights[field] * min(count, 3)
                matched = True
        if not matched:
            return -1
    return total


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--id")
    p.add_argument("--kind")
    p.add_argument("--surface")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--full", action="store_true")
    p.add_argument("--media", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--list-kinds", action="store_true")
    args = p.parse_args()
    entries = load_entries()

    if args.list_kinds:
        from collections import Counter
        print(json.dumps({"kinds": Counter(e["kind"] for e in entries), "surfaces": Counter(e.get("surface") for e in entries)}, indent=2))
        return

    if args.id:
        matches = [e for e in entries if e["id"] == args.id]
        if not matches:
            sys.exit(f"Unknown recipe id: {args.id}")
        e = matches[0]
        if args.media:
            print("\n".join(media_urls(e)) or "No media URLs found.")
        elif args.json:
            print(json.dumps(e, indent=2, ensure_ascii=False))
        elif args.full:
            print(f"{e['id']} — {e['title']}\nkind={e['kind']} category={e.get('category')} surface={e.get('surface')}\n")
            print(e.get("originalPrompt", "No original prompt for this companion recipe."))
        else:
            print(json.dumps({k:e.get(k) for k in ("id","title","kind","category","surface","pattern","tags")}, indent=2))
        return

    filtered = [e for e in entries if (not args.kind or e["kind"] == args.kind) and (not args.surface or e.get("surface") == args.surface)]
    terms = re.findall(r"[\w-]+", args.query.lower())
    ranked = sorted(((score(e, terms), e) for e in filtered), key=lambda x: (-x[0], x[1]["id"]))
    ranked = [(s,e) for s,e in ranked if s >= 0][:max(args.limit, 1)]
    if args.json:
        print(json.dumps([{**e, "score":s} for s,e in ranked], indent=2, ensure_ascii=False))
        return
    for s,e in ranked:
        print(f"{e['id']:<18} score={s:<3} {e['title']} [{e['kind']} / {e.get('category')} / {e.get('surface')}]")

if __name__ == "__main__":
    main()
