#!/usr/bin/env python3
"""Serve one standalone recipe on localhost."""
import argparse, functools, http.server, json, pathlib, shutil, socketserver, tempfile

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[4] / "vendor" / "claude-club-motion-library"  # fetched by tools/motion-skills/fetch.sh libraries
LIBRARY = ROOT / "library"

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("recipe_id")
    p.add_argument("--port",type=int,default=4173)
    args=p.parse_args()
    manifest=json.loads((LIBRARY/"manifest.json").read_text())
    rec=next((r for r in manifest["recipes"] if r["id"]==args.recipe_id),None)
    if not rec: raise SystemExit(f"Unknown recipe id: {args.recipe_id}")
    source=LIBRARY/"recipes"/pathlib.Path(rec["path"]).name
    if not source.exists(): raise SystemExit(f"Missing recipe file: {source}")
    with tempfile.TemporaryDirectory(prefix="claude-club-preview-") as td:
        shutil.copy2(source,pathlib.Path(td)/"index.html")
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=td)
        with socketserver.TCPServer(("127.0.0.1",args.port),handler) as server:
            print(f"Serving {args.recipe_id} at http://127.0.0.1:{args.port}/")
            try: server.serve_forever()
            except KeyboardInterrupt: pass

if __name__=="__main__": main()
