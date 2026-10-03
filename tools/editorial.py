"""Non-product artwork: the hero, the social card, the workbench and the
lookbook tiles behind the collection."""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .palette import (
    GOLD_DK,
    GOLD_LT,
    PALETTES,
    add_light,
    backdrop,
    bokeh,
    radial_glow,
    vertical_gradient,
)
from .primitives import faceted_gem, sparkle

LOOK_TONES = ("rose", "warm", "warm", "rose", "cool", "cool")

LOOK_SLUGS = (
    "look-sitara", "look-sehra", "look-ziya",
    "look-noor", "look-jewellery", "look-eternity",
)


def editorial(size, seed, tone="warm"):
    """Abstract bokeh editorial shot, used for the lookbook tiles."""
    rng = np.random.default_rng(seed)
    W, H = size
    img = backdrop(size, seed=seed, warm=(tone == "warm"))
    light = np.zeros((H, W, 3), np.float32)
    picks = {
        "warm": [(236, 210, 140), (255, 246, 224), (206, 168, 74)],
        "cool": [(196, 214, 236), (240, 246, 252), (120, 152, 190)],
        "rose": [(244, 208, 196), (255, 240, 236), (198, 132, 118)],
    }[tone]
    for _ in range(38):
        cx = rng.uniform(0, 1) * W
        cy = rng.uniform(0, 1) * H
        r = rng.uniform(W * 0.03, W * 0.19)
        light += radial_glow(size, (cx, cy), r, rng.choice(picks), rng.uniform(0.16, 0.5))
    img = add_light(img, light)

    d = ImageDraw.Draw(img, "RGBA")
    # bokeh discs
    for _ in range(16):
        cx = rng.uniform(0, W)
        cy = rng.uniform(0, H)
        r = rng.uniform(W * 0.03, W * 0.11)
        a = int(rng.uniform(16, 46))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 252, 244, a))
    for _ in range(9):
        sparkle(d, rng.uniform(0, W), rng.uniform(0, H), rng.uniform(6, 22))
    return img.filter(ImageFilter.GaussianBlur(0.6))


def atelier(size, seed=5):
    """Bigger scene for the story block: workbench, tools, stone."""
    W, H = size
    img = vertical_gradient(size, (247, 241, 230), (223, 212, 193), angle=100)
    img = add_light(img, bokeh(size, n=26, seed=seed) * 0.5)
    d = ImageDraw.Draw(img, "RGBA")

    bench_y = int(H * 0.72)
    d.rectangle([0, bench_y, W, H], fill=(206, 190, 163, 255))
    d.rectangle([0, bench_y, W, bench_y + 10], fill=(176, 158, 128, 255))
    for i in range(26):
        x = (i * 97) % W
        d.line([(x, bench_y + 12), (x + 40, H)], fill=(190, 172, 143, 120), width=2)

    # bench pin
    d.rectangle([int(W * 0.14), int(H * 0.52), int(W * 0.18), bench_y], fill=(150, 134, 108, 255))
    # burnisher
    d.polygon([(int(W * 0.62), bench_y - 8), (int(W * 0.80), bench_y - 8),
               (int(W * 0.78), int(H * 0.52)), (int(W * 0.66), int(H * 0.52))],
              fill=(150, 134, 108, 255))
    d.line([(int(W * 0.80), bench_y - 8), (int(W * 0.92), int(H * 0.50))], fill=(126, 112, 90, 255), width=7)
    # stone on pin
    faceted_gem(d, int(W * 0.16), int(H * 0.46), int(min(W, H) * 0.10), PALETTES["diamond"], facets=8)
    sparkle(d, int(W * 0.16), int(H * 0.38), int(min(W, H) * 0.05))

    # warm lamp pool
    img = add_light(img, radial_glow(size, (int(W * 0.30), int(H * 0.22)), int(W * 0.55),
                                     (255, 232, 176), 0.42))
    return img.filter(ImageFilter.SMOOTH)


def hero_bg(size):
    W, H = size
    img = vertical_gradient(size, (252, 249, 243), (231, 221, 203), angle=100)
    img = add_light(img, bokeh(size, n=110, seed=99) * 0.85)
    img = add_light(img, radial_glow(size, (int(W * 0.5), int(H * 0.46)), int(W * 0.42),
                                     (238, 214, 150), 0.55))
    return img.filter(ImageFilter.GaussianBlur(1.2))


def og_image(size=(1200, 630)):
    W, H = size
    img = vertical_gradient(size, (24, 18, 15), (60, 46, 24), angle=110)
    img = add_light(img, bokeh(size, n=70, seed=17) * 0.7)
    d = ImageDraw.Draw(img, "RGBA")
    faceted_gem(d, W // 2, int(H * 0.44), int(H * 0.26), PALETTES["gold"], facets=10)
    sparkle(d, int(W * 0.5) + int(H * 0.20), int(H * 0.30), 26)
    sparkle(d, int(W * 0.5) - int(H * 0.22), int(H * 0.56), 18)
    return img

