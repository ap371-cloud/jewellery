"""Fetch photorealistic jewellery imagery from the free Pollinations API.

No API key and no account are required. Prompts are written for
product-photography style output, then each response is written into ../assets
using the exact filenames index.html already references, so nothing else in the
site needs to change.

    python -m tools.fetch_ai_images
    python -m tools.fetch_ai_images --only product-solitaire

This is the optional counterpart to build_images.py: run it when you want real
photography rather than drawn artwork.
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .slugs import ASSETS as OUT

BASE = "https://image.pollinations.ai/prompt/"

STYLE = (
    "professional jewellery product photography, soft studio lighting, "
    "neutral cream backdrop, shallow depth of field, ultra detailed, "
    "macro shot, 8k, editorial magazine quality"
)

FLATLAY = (
    "top-down flat lay photograph of jewellery objects arranged on a fabric "
    "surface, product only, nothing worn by anyone, empty frame, "
)

TARGETS = {
    "product-solitaire": (
        FLATLAY + "a single solitaire diamond ring in yellow gold, round "
        "brilliant cut centre stone in six prongs, plain polished band, "
        "standing upright on a cream stone slab, " + STYLE
    ),
    "product-hoops": (
        FLATLAY + "two thick polished gold hoop earrings lying flat side by "
        "side, high gloss, hinged clasps visible, " + STYLE
    ),
    "product-necklace": (
        FLATLAY + "an elegant rose gold necklace with a single diamond "
        "pendant, chain coiled in a loose circle on cream silk, " + STYLE
    ),
    "product-band": (
        FLATLAY + "a silver coloured eternity band ring fully set with small "
        "round clear stones all the way around, standing on edge on its edge, " + STYLE
    ),
    "product-bridal": (
        FLATLAY + "a complete antique gold jewellery set: a wide collar "
        "necklace, a long necklace, a pair of round dangling earrings and a "
        "small forehead ornament, laid out together on dark red velvet with "
        "gold fabric, " + STYLE
    ),
    "product-drops": (
        FLATLAY + "a pair of rose gold teardrop earrings with small diamond "
        "tops, lying side by side on pale silk, " + STYLE
    ),
    "product-halo": (
        FLATLAY + "a slim rose gold ring with a thin open circle of small "
        "diamonds surrounding the finger, standing upright on cream stone, " + STYLE
    ),
    "product-emerald": (
        FLATLAY + "a yellow gold ring set with one large rectangular step cut "
        "emerald and two small diamonds either side of it, " + STYLE
    ),
    "product-jhumka": (
        FLATLAY + "a pair of ornate antique gold jhumka earrings with domed "
        "tops, pearl drops and fine fringe chains, laid flat on deep red silk, " + STYLE
    ),
    "product-studs": (
        FLATLAY + "a pair of platinum stud earrings each holding a single "
        "round sapphire, resting on a pale grey stone slab, " + STYLE
    ),
    "product-rani": (
        FLATLAY + "a long antique gold rani haar necklace made of small "
        "repeating floral links, arranged in a wide U on ivory silk, " + STYLE
    ),
    "product-choker": (
        FLATLAY + "a close fitting yellow gold choker necklace set all round "
        "with alternating round diamonds, laid flat in a neat oval, " + STYLE
    ),
    "product-pendant": (
        FLATLAY + "a fine yellow gold chain with a single small round "
        "laboratory grown diamond pendant, chain coiled loosely, " + STYLE
    ),
    "product-bangles": (
        FLATLAY + "a stack of four wide textured gold bangles lying flat "
        "together, one pair open with small hooks, " + STYLE
    ),
    "product-bracelet": (
        FLATLAY + "a platinum tennis bracelet set in a single line of round "
        "diamonds with a hidden clasp, laid in a soft curve, " + STYLE
    ),
    "product-lehenga": (
        FLATLAY + "a complete bridal jewellery set arranged on deep maroon "
        "velvet: a heavy choker, a long haar, a jhumka pair, a maang tikka, "
        "two bangles and a ring, " + STYLE
    ),
    "product-coin": (
        FLATLAY + "a single gold Lakshmi coin standing on its edge next to a "
        "small stack of three more coins on cream silk, milled edges visible, "
        + STYLE
    ),
    "product-silvercoin": (
        FLATLAY + "a heavy silver bullion coin lying flat beside three smaller "
        "silver coins on a dark slate surface, high shine, " + STYLE
    ),
    "look-sitara": (
        FLATLAY + "a rose gold pendant necklace with a diamond pendant resting "
        "on cream silk, chain coiled beside it, " + STYLE
    ),
    "look-sehra": (
        FLATLAY + "a set of antique gold ornaments placed on dark maroon "
        "velvet: a wide collar necklace, a long necklace, a pair of round "
        "dangling earrings and a small forehead ornament, " + STYLE
    ),
    "look-ziya": (
        FLATLAY + "two polished gold hoop earrings standing upright on a pale "
        "stone slab, soft reflection, " + STYLE
    ),
    "look-noor": (
        FLATLAY + "a pair of rose gold teardrop earrings lying side by side "
        "on pale silk, small diamond tops catching light, " + STYLE
    ),
    "look-jewellery": (
        FLATLAY + "a single diamond solitaire ring resting on a small velvet "
        "ring cushion, one dramatic highlight, " + STYLE
    ),
    "look-eternity": (
        FLATLAY + "two stacked wedding bands, one silver coloured set with "
        "small clear stones and one plain yellow gold band, leaning together, " + STYLE
    ),
    "atelier": (
        "still life of a jeweller's workbench with nobody in frame, "
        "goldsmith files and a burnisher lying on worn leather, a loupe, a "
        "ring in a jewelling clamp, tiny loose diamonds in a dish, "
        "warm low workshop light, documentary photograph, "
        "shallow depth of field, empty bench"
    ),
    "hero": (
        "elegant gold jewellery arranged on a cream silk surface, "
        "soft directional light, gold and diamond highlights, "
        "luxury brand hero image, cinematic, dark warm background, "
        "lots of negative space in the centre"
    ),
}

DIMS = {
    "hero": (1920, 1080),
    "atelier": (900, 1125),
}


def strip_watermark(path: Path) -> None:
    """Crop off the bottom strip carrying the Pollinations watermark.

    The mark sits in roughly the last 3% of the frame, so trimming there clears
    it without touching the subject.
    """
    try:
        from PIL import Image
    except ImportError:
        return

    try:
        with Image.open(path) as im:
            w, h = im.size
            im.convert("RGB").crop((0, 0, w, int(h * 0.965))).save(
                path, "JPEG", quality=92, optimize=True, progressive=True
            )
    except OSError as exc:
        print(f"       watermark crop skipped: {exc}")


def fetch(slug: str, prompt: str, seed: int = 0) -> tuple[int, int, int]:
    w, h = DIMS.get(slug, (800, 1000))
    if slug.startswith("look-"):
        w, h = 800, 1067
    q = urllib.parse.quote(prompt, safe="")
    url = f"{BASE}{q}?width={w}&height={h}&nologo=true&model=flux&seed={seed}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    ext = ".png" if data[:8] == b"\x89PNG\r\n\x1a\n" else ".jpg"
    path = OUT / (slug + ext)
    path.write_bytes(data)
    if ext == ".jpg":
        strip_watermark(path)
    return w, h, path.stat().st_size


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", help="regenerate a single slug")
    ap.add_argument("--sleep", type=float, default=3.0, help="delay between calls")
    args = ap.parse_args(argv)

    OUT.mkdir(parents=True, exist_ok=True)
    slugs = [args.only] if args.only else list(TARGETS)
    ok = 0
    for i, slug in enumerate(slugs):
        prompt = TARGETS.get(slug)
        if not prompt:
            print(f"skip unknown slug {slug}")
            continue
        for attempt in range(1, 4):
            try:
                w, h, nbytes = fetch(slug, prompt, seed=1000 + i)
                print(f"[ok]   {slug:20s} {w}x{h}  {nbytes / 1024:.0f} KB")
                ok += 1
                break
            except Exception as exc:
                # 402 means the anonymous quota ran out, 500 is a flaky upstream.
                # Both clear up on their own, so just back off and retry.
                print(f"[try{attempt}] {slug}: {exc}")
                time.sleep(8 * attempt)
        else:
            print(f"[FAIL] {slug} kept previous image")
        if not args.only:
            time.sleep(args.sleep)

    print(f"\n{ok}/{len(slugs)} generated into {OUT}")
    return 0 if ok == len(slugs) else 1


if __name__ == "__main__":
    sys.exit(main())
