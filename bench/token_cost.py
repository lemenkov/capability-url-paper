#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Peter Lemenkov <lemenkov@gmail.com>
# SPDX-License-Identifier: Apache-2.0
"""
token_cost.py -- LLM-context cost of tool outputs: inline base64 vs by-reference
(capability-URL metadata). Demonstrates Bounded Output Context Cost: inline
scales with payload size; metadata is ~constant.

Random bytes stand in for compressed binary (PNG/JPEG/PDF) -- the worst case for
a BPE tokenizer. Use --dir to measure real files.

    pip install tiktoken
    python token_cost.py                 # synthetic size sweep
    python token_cost.py --dir outputs/  # real files
"""
import argparse, base64, hashlib, json, mimetypes, os, sys
import tiktoken

ENCODINGS = ("o200k_base", "cl100k_base")   # report both; ratio is stable across BPEs

def meta_json(name, data, mime):
    return json.dumps({
        "name": name, "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(), "mime": mime,
        "url": f"https://host.example/sandbox-out/{'A'*43}/{name}",
        "expires_in": 3600,
    })

def measure(enc, name, data, mime):
    inline = len(enc.encode(base64.b64encode(data).decode()))
    meta   = len(enc.encode(meta_json(name, data, mime)))
    return len(data), inline, meta

def report(enc, items):
    print(f"\n[{enc.name}]")
    print(f"{'payload':<22}{'bytes':>10}{'inline':>10}{'meta':>7}{'ratio':>8}{'tok/KB':>8}")
    print("-" * 65)
    for label, data, mime, name in items:
        raw, inline, meta = measure(enc, name, data, mime)
        print(f"{label:<22}{raw:>10}{inline:>10}{meta:>7}{inline/meta:>8.0f}{inline/(raw/1024):>8.1f}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", help="measure real files here instead of a synthetic sweep")
    a = ap.parse_args()

    items = []
    if a.dir:
        for fn in sorted(os.listdir(a.dir)):
            p = os.path.join(a.dir, fn)
            if os.path.isfile(p):
                data = open(p, "rb").read()
                mime = mimetypes.guess_type(fn)[0] or "application/octet-stream"
                items.append((fn[:22], data, mime, fn))
    else:
        for kb in (1, 4, 16, 64, 256, 1024):
            items.append((f"random {kb}KB", os.urandom(kb * 1024),
                          "application/octet-stream", f"blob_{kb}k.bin"))

    for name in ENCODINGS:
        try:
            report(tiktoken.get_encoding(name), items)
        except Exception as e:
            print(f"[{name}] unavailable: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
