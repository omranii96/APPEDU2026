#!/usr/bin/env python3
"""Download media referenced by one recipe while preserving a provenance map."""
import argparse, hashlib, json, mimetypes, pathlib, re, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[4] / "vendor" / "claude-club-motion-library"  # fetched by tools/motion-skills/fetch.sh libraries
LIBRARY = ROOT / "library" / "library.json"


def safe_name(url, index, content_type=""):
    path = urllib.parse.urlparse(url).path
    suffix = pathlib.Path(path).suffix.lower()
    if not suffix or len(suffix) > 6:
        suffix = mimetypes.guess_extension(content_type.split(";")[0]) or ".bin"
    digest = hashlib.sha256(url.encode()).hexdigest()[:12]
    return f"{index:03d}-{digest}{suffix}"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("recipe_id")
    p.add_argument("--output", default="./reference-media")
    p.add_argument("--timeout", type=int, default=30)
    args = p.parse_args()
    entries = json.loads(LIBRARY.read_text())["entries"]
    entry = next((e for e in entries if e["id"] == args.recipe_id), None)
    if not entry:
        raise SystemExit(f"Unknown recipe id: {args.recipe_id}")
    urls = list(dict.fromkeys(u.rstrip("),.;]'\"") for u in re.findall(r"https?://[^\s`<>]+", entry.get("originalPrompt", ""))))
    out = pathlib.Path(args.output) / args.recipe_id
    out.mkdir(parents=True, exist_ok=True)
    records=[]
    for i,url in enumerate(urls,1):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 ClaudeClubLibrary/1.0"})
            with urllib.request.urlopen(req,timeout=args.timeout) as r:
                data=r.read(); ctype=r.headers.get("Content-Type","")
            name=safe_name(url,i,ctype); (out/name).write_bytes(data)
            records.append({"url":url,"file":name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"contentType":ctype,"status":"downloaded"})
            print(f"downloaded {name} ({len(data)} bytes)")
        except Exception as exc:
            records.append({"url":url,"status":"failed","error":str(exc)})
            print(f"failed {url}: {exc}")
    (out/"provenance.json").write_text(json.dumps({"recipe":args.recipe_id,"items":records},indent=2)+"\n")
    print(f"Wrote {out/'provenance.json'}")

if __name__ == "__main__":
    main()
