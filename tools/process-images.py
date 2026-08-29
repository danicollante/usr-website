#!/usr/bin/env python3
"""Derive responsive WebP + JPEG sets from the supplied photography."""
from PIL import Image
import os, json

SRC = "/Users/danielcollante/Library/CloudStorage/GoogleDrive-dani.collante@gmail.com/My Drive/HP_2018_06/Trabajos_Escri/US Strategic Resources/Website/resources/feedback 0828/photos by Robin aug28"
OUT = os.path.join(os.path.dirname(__file__), "..", "site", "assets", "img")
WIDTHS = [1920, 1280, 800, 480]

# source file -> output slug. Only photographs actually placed on a page are
# derived; the Drive folder holds more (a second NASA frame, the aerial ore
# terrain, two further patriotic shots, the open-pit mines). Add a line here to
# bring one in — the open-pit shots are deliberately excluded, since leading
# with an operating mine implies production this company cannot claim.
JOBS = {
    "svntx-0nLU_L0Uz94-unsplash.jpg":       "terrain-sandstone",
    "drill rig.avif":                       "drill-rig",
    "core samples.jpg":                     "core-samples",
    "rail 1.avif":                          "rail-corridor",
    "brandon-day-YkanZqsbkQ0-unsplash.jpg": "us-flag",
    "nasa-1lfI7wkGWZ4-unsplash.jpg":        "earth-at-night",
}

os.makedirs(OUT, exist_ok=True)
manifest = {}

for fname, slug in JOBS.items():
    path = os.path.join(SRC, fname)
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    made = []
    for w in WIDTHS:
        tw = min(w, sw)          # never upscale
        if tw in made:           # source narrower than this step
            continue
        th = round(tw * sh / sw)
        r = im.resize((tw, th), Image.LANCZOS)
        r.save(os.path.join(OUT, f"{slug}-{tw}.webp"), "WEBP", quality=82, method=6)
        r.save(os.path.join(OUT, f"{slug}-{tw}.jpg"), "JPEG", quality=82,
               optimize=True, progressive=True)
        made.append(tw)
    manifest[slug] = {"widths": made, "native": [sw, sh],
                      "ratio": round(sw / sh, 4), "source": fname}
    print(f"{slug:18s} {sw}x{sh}  ->  {made}")

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print("\nDone.")
