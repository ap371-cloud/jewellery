"""Draw every image the site needs, from code, with no external assets.

Each PNG is composed from primitives in primitives.py: faceted gem renders,
metal bands, chain links, studio backdrops and gold bokeh. Nothing is sourced
from the web.

    python -m tools.build_images
    python -m tools.build_images --only product-coin
    python -m tools.build_images --only product-rani --only product-bangles

Without --only this rewrites assets/ completely, including hero.jpg, og.jpg and
atelier.jpg. Pass --only to keep photographic versions of those.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from .editorial import LOOK_SLUGS, LOOK_TONES, atelier, editorial, hero_bg, og_image
from .palette import PALETTES
from .products import PRODUCTS
from .slugs import ASSETS, PRODUCT_SLUGS, SITE_SLUGS

PRODUCT_SIZE = (800, 1000)
LOOK_SIZE = (800, 1067)
DIMS = {
    "hero.jpg": ((1920, 1080), 88),
    "og.jpg": ((1200, 630), 90),
    "atelier.jpg": ((900, 1125), 90),
}


def check_slugs() -> None:
    """The painters, the slug contract and pieces.js have to agree."""
    painted = set(PRODUCTS)
    promised = set(PRODUCT_SLUGS)
    if painted != promised:
        raise SystemExit(
            "product slugs disagree\n"
            f"  only painted: {sorted(painted - promised)}\n"
            f"  only promised: {sorted(promised - painted)}"
        )

    page = ASSETS.parent / "assets" / "js" / "pieces.js"
    if not page.exists():
        return
    asked = set(re.findall(r'img:\s*"(assets/(?:product-[a-z]+)\.jpg)"', page.read_text(encoding="utf-8")))
    wanted = {f"assets/{slug}.jpg" for slug in promised}
    if asked != wanted:
        raise SystemExit(
            "pieces.js and the painters disagree\n"
            f"  only in pieces.js: {sorted(asked - wanted)}\n"
            f"  only painted:     {sorted(wanted - asked)}"
        )


class Writer:
    def __init__(self, only: set[str]) -> None:
        self.only = only
        self.written: list[tuple[str, tuple[int, int], int]] = []

    def wants(self, name: str) -> bool:
        return not self.only or name.rsplit(".", 1)[0] in self.only

    def save(self, image, name: str, quality: int = 90) -> None:
        if not self.wants(name):
            return
        ASSETS.mkdir(parents=True, exist_ok=True)
        path = ASSETS / name
        image.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
        self.written.append((name, image.size, path.stat().st_size))


def build(only: set[str]) -> list[tuple[str, tuple[int, int], int]]:
    check_slugs()
    out = Writer(only)

    if not only:
        out.save(hero_bg((1920, 1080)), "hero.jpg", 88)
        out.save(og_image(), "og.jpg", 90)
        out.save(atelier(DIMS["atelier.jpg"][0]), "atelier.jpg", 90)

    for slug in PRODUCT_SLUGS:
        painter, palette = PRODUCTS[slug]
        if palette not in PALETTES:
            raise SystemExit(f"{slug}: unknown palette {palette!r}")
        out.save(painter(PRODUCT_SIZE, palette), f"{slug}.jpg", 90)

    for index, (slug, tone) in enumerate(zip(LOOK_SLUGS, LOOK_TONES)):
        out.save(editorial(LOOK_SIZE, seed=100 + index * 13, tone=tone), f"{slug}.jpg", 88)

    return out.written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", action="append", default=[], metavar="SLUG",
                        help="regenerate a single asset; repeat for several")
    args = parser.parse_args(argv)

    known = set(PRODUCT_SLUGS) | set(LOOK_SLUGS) | set(SITE_SLUGS)
    unknown = [s for s in args.only if s not in known]
    if unknown:
        parser.error("unknown slug(s): " + ", ".join(unknown))

    written = build(set(args.only))
    for name, size, nbytes in written:
        print(f"{name:24s} {size[0]}x{size[1]}  {nbytes / 1024:.0f} KB")
    print(f"\n{len(written)} images -> {ASSETS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
