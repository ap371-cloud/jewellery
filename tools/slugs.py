"""Shared paths and the slug contract between the painters and index.html."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

#: Every product image, in the order the catalogue lists them.
PRODUCT_SLUGS = (
    "product-solitaire", "product-hoops", "product-necklace", "product-band",
    "product-bridal", "product-drops", "product-halo", "product-emerald",
    "product-jhumka", "product-studs", "product-rani", "product-choker",
    "product-pendant", "product-bangles", "product-bracelet", "product-lehenga",
    "product-coin", "product-silvercoin",
)

#: Non-product artwork: hero, social card, workbench, lookbook tiles.
SITE_SLUGS = ("hero", "og", "atelier")
