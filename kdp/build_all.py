"""
One command rebuilds the whole TOP 3 line (6 interiors, 6 covers, Kindle files, listings) and preflights it.

    cd kdp && python3 build_all.py            # everything
    python3 build_all.py 03_nova               # one book

To use your own imprint / pen name everywhere first:
    sed -i 's/Dino Quest Kids Press/Your Imprint/g' books/*/*.py listings.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS = ["01_dino_quest", "02_dino_abc", "03_nova"]


def run(args, cwd):
    print("$", " ".join(args), f"(in {os.path.relpath(cwd, ROOT)})")
    r = subprocess.run([sys.executable] + args, cwd=cwd)
    if r.returncode:
        sys.exit(r.returncode)


def main():
    todo = [b for b in BOOKS if b in sys.argv[1:]] or BOOKS
    for b in todo:
        d = os.path.join(ROOT, "books", b)
        run(["build.py"], d)
        run(["cover.py"], d)
    run(["listings.py"], ROOT)
    run(["-m", "lib.qa"], ROOT)


if __name__ == "__main__":
    main()
