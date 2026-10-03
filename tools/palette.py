"""Colour, light and backdrop helpers.

Everything in the generated artwork starts here: the metal tones, the stone
palettes, the gradients and the out-of-focus highlights that sit behind a piece.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image

GOLD = (201, 162, 39)

GOLD_LT = (235, 208, 138)

GOLD_DK = (124, 96, 22)

PALETTES = {
    "diamond": ((250, 252, 255), (196, 216, 236), (120, 150, 182)),
    "gold": ((250, 236, 190), (222, 184, 84), (150, 112, 30)),
    "rose": ((255, 232, 224), (232, 168, 148), (162, 96, 82)),
    "emerald": ((214, 248, 232), (74, 176, 132), (26, 96, 74)),
    "sapphire": ((214, 232, 252), (58, 116, 208), (22, 52, 122)),
    "silver": ((250, 251, 253), (188, 197, 209), (108, 119, 134)),
}

ROSE_A, ROSE_B = (238, 168, 146), (152, 84, 66)

SILVER_A, SILVER_B = (206, 212, 220), (96, 104, 118)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vertical_gradient(size, top, bottom, angle=90):
    """Linear gradient across an arbitrary angle."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rad = math.radians(angle)
    t = (xx * math.cos(rad) + yy * math.sin(rad))
    t = (t - t.min()) / max(t.max() - t.min(), 1e-6)
    top = np.array(top, np.float32)
    bottom = np.array(bottom, np.float32)
    arr = top[None, None, :] + (bottom - top)[None, None, :] * t[:, :, None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGB")


def radial_glow(size, center, radius, color, strength=1.0):
    """Additive radial light blob as an RGB array."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2)
    fall = np.clip(1 - d / max(radius, 1e-6), 0, 1) ** 2
    return fall[:, :, None] * np.array(color, np.float32) * strength


def add_light(img, light):
    arr = np.clip(np.asarray(img, np.float32) + light, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def bokeh(size, n=90, seed=11):
    rng = np.random.default_rng(seed)
    light = np.zeros((size[1], size[0], 3), np.float32)
    for _ in range(n):
        cx = rng.uniform(-0.05, 1.05) * size[0]
        cy = rng.uniform(-0.05, 1.05) * size[1]
        r = rng.uniform(size[0] * 0.02, size[0] * 0.12)
        tint = rng.choice([
            np.array(GOLD_LT, np.float32),
            np.array(GOLD, np.float32),
            np.array((255, 246, 222), np.float32),
        ], p=[0.4, 0.4, 0.2])
        strength = rng.uniform(0.10, 0.42)
        light += radial_glow(size, (cx, cy), r, tint, strength)
    return light


def backdrop(size, seed=3, warm=True):
    """Studio sweep: a graded backdrop with a little gold bokeh in it.

    The gradient is deliberately kept well short of white at the bottom edge so
    gold and silver still have something to sit against.
    """
    base = vertical_gradient(
        size,
        (251, 248, 241) if warm else (243, 242, 240),
        (223, 210, 187) if warm else (216, 216, 214),
        angle=105,
    )
    return add_light(base, bokeh(size, n=26, seed=seed) * 0.30)


PALETTES = {
    "diamond": ((250, 252, 255), (196, 216, 236), (120, 150, 182)),
    "gold": ((250, 236, 190), (222, 184, 84), (150, 112, 30)),
    "rose": ((255, 232, 224), (232, 168, 148), (162, 96, 82)),
    "emerald": ((214, 248, 232), (74, 176, 132), (26, 96, 74)),
    "sapphire": ((214, 232, 252), (58, 116, 208), (22, 52, 122)),
    "silver": ((250, 251, 253), (188, 197, 209), (108, 119, 134)),
}

ROSE_A, ROSE_B = (238, 168, 146), (152, 84, 66)
SILVER_A, SILVER_B = (206, 212, 220), (96, 104, 118)

