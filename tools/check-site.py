#!/usr/bin/env python3
"""Fetch every page and verify each referenced asset and internal link resolves."""
import re, urllib.request, urllib.error, os, sys
from html.parser import HTMLParser

BASE = "http://localhost:8000/"
PAGES = ["index.html","about.html","leadership.html","metals.html","news.html",
         "contact.html","legal.html","news/company-formation-announcement.html",
         "cestos-project.html","why-liberia.html","critical-minerals.html","company.html"]

def get(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, str(e).encode()

seen, bad, checked = {}, [], 0

def resolve(page, ref):
    if ref.startswith(("http://","https://","mailto:","#","data:")): return None
    ref = ref.split("#")[0]
    if not ref: return None
    d = os.path.dirname(page)
    return os.path.normpath(os.path.join(d, ref)).replace("\\","/")

for page in PAGES:
    st, body = get(BASE + page)
    print(f"{st}  {page}")
    if st != 200:
        bad.append((page, page, st)); continue
    h = body.decode("utf-8", "replace")

    refs = set()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', h):
        refs.add(m.group(1))
    for m in re.finditer(r'srcset="([^"]+)"', h):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u: refs.add(u)

    for ref in sorted(refs):
        tgt = resolve(page, ref)
        if not tgt: continue
        if tgt in seen:
            code = seen[tgt]
        else:
            code, _ = get(BASE + tgt); seen[tgt] = code; checked += 1
        if code != 200:
            bad.append((page, ref, code))

print(f"\nchecked {checked} unique assets/links")
if bad:
    print(f"\n!! {len(bad)} BROKEN:")
    for p, r, c in bad: print(f"   [{c}] {r}   (on {p})")
    sys.exit(1)
print("all resolve 200")
