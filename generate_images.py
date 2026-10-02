"""Procedurally generate all artwork for the Jewellery jewellery site.

No external assets and no image-generation API are used. Every PNG here is
drawn from scratch with Pillow + numpy: faceted gem renders, metal bands, chain
links, studio backdrops and gold bokeh.

Run:
    python generate_images.py

Output goes to ./assets.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

GOLD = (201, 162, 39)
GOLD_LT = (235, 208, 138)
GOLD_DK = (124, 96, 22)


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


def sparkle(draw, cx, cy, r, color=(255, 255, 255), alpha=255):
    """Four-point star sparkle."""
    draw.polygon(
        [(cx, cy - r), (cx + r * 0.16, cy - r * 0.16), (cx + r, cy),
         (cx + r * 0.16, cy + r * 0.16), (cx, cy + r), (cx - r * 0.16, cy + r * 0.16),
         (cx - r, cy), (cx - r * 0.16, cy - r * 0.16)],
        fill=color + (alpha,),
    )


def metal_band(draw, cx, cy, r_out, r_in, color_a=GOLD_LT, color_b=GOLD_DK, steps=360):
    """Ring / band drawn as a solid shaded annulus of quad segments."""
    for i in range(steps):
        a0 = i / steps * math.tau
        a1 = (i + 1) / steps * math.tau
        shade = (math.sin(a0 - 0.9) + 1) / 2
        col = lerp(color_b, color_a, shade ** 1.7)
        pts = [
            (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)),
            (cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)),
            (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)),
            (cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)),
        ]
        draw.polygon(pts, fill=col)
    for r, c in ((r_out, lerp(color_a, (255, 255, 255), 0.35)),
                 (r_in, color_b)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)


def claw(draw, x, y, w, h, color_a=GOLD_LT, color_b=GOLD_DK):
    """Short tapered prong that grips a stone at its girdle."""
    draw.polygon(
        [(x - w * 0.5, y + h), (x + w * 0.5, y + h), (x + w * 0.16, y - h), (x - w * 0.16, y - h)],
        fill=color_b,
    )
    draw.polygon(
        [(x - w * 0.5, y + h), (x - w * 0.12, y + h), (x - w * 0.03, y - h), (x - w * 0.16, y - h)],
        fill=color_a,
    )
    draw.ellipse([x - w * 0.17, y - h - w * 0.16, x + w * 0.17, y - h + w * 0.16],
                 fill=lerp(color_a, (255, 255, 255), 0.45))


def faceted_gem(draw, cx, cy, r, palette, facets=8, rotate=0.0):
    """Brilliant-cut style gem: crown triangles + pavilion facets."""
    top = (cx, cy - r)
    girdle_y = cy - r * 0.34
    bottom = (cx, cy + r)
    girdle = []
    for i in range(facets):
        a = rotate + i * math.tau / facets - math.pi / 2
        girdle.append((cx + r * 0.92 * math.cos(a), girdle_y + r * 0.16 * math.sin(a)))

    for i in range(facets):
        col = lerp(palette[0], palette[1], (i % 3) / 2.0)
        draw.polygon([top, girdle[i], girdle[(i + 1) % facets]], fill=col)

    for i in range(facets):
        col = lerp(palette[1], palette[2], (i % 4) / 3.0)
        draw.polygon([bottom, girdle[i], girdle[(i + 1) % facets]], fill=col)

    for i in range(facets):
        draw.line([top, girdle[i]], fill=(255, 255, 255), width=1)
    draw.line(
        [(x, y) for (x, y) in girdle] + [girdle[0]],
        fill=lerp(palette[0], (255, 255, 255), 0.4),
        width=2,
    )


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
    base = vertical_gradient(
        size,
        (253, 251, 246) if warm else (246, 243, 236),
        (236, 228, 212) if warm else (232, 226, 214),
        angle=105,
    )
    return add_light(base, bokeh(size, n=34, seed=seed) * 0.55)


PALETTES = {
    "diamond": ((250, 252, 255), (196, 216, 236), (120, 150, 182)),
    "gold": ((250, 236, 190), (222, 184, 84), (150, 112, 30)),
    "rose": ((255, 232, 224), (232, 168, 148), (162, 96, 82)),
    "emerald": ((214, 248, 232), (74, 176, 132), (26, 96, 74)),
    "sapphire": ((214, 232, 252), (58, 116, 208), (22, 52, 122)),
}


def product_solitaire(size, pal="diamond"):
    W, H = size
    img = backdrop(size, seed=3)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.63)
    r = int(min(W, H) * 0.20)

    d.ellipse([cx - r * 2.0, cy + r * 0.35, cx + r * 2.0, cy + r * 1.05], fill=(40, 30, 18, 26))
    metal_band(d, cx, cy, r * 1.58, r * 1.26)
    gem_cy = cy - r * 1.62
    claw(d, cx - r * 0.80, gem_cy + r * 0.20, r * 0.20, r * 0.17)
    claw(d, cx + r * 0.80, gem_cy + r * 0.20, r * 0.20, r * 0.17)
    faceted_gem(d, cx, gem_cy, r, PALETTES[pal], facets=10, rotate=0.18)
    sparkle(d, cx + r * 0.40, gem_cy - r * 0.52, r * 0.30)
    sparkle(d, cx - r * 0.66, gem_cy + r * 0.10, r * 0.16)
    return img.filter(ImageFilter.SMOOTH)


def product_hoops(size, pal="gold"):
    W, H = size
    img = backdrop(size, seed=7)
    d = ImageDraw.Draw(img, "RGBA")
    r = int(min(W, H) * 0.17)
    cy = int(H * 0.46)
    for k, ox in enumerate((-int(W * 0.19), int(W * 0.19))):
        cx = W // 2 + ox
        d.ellipse([cx - r * 1.45, cy + r * 0.5, cx + r * 1.45, cy + r * 1.15], fill=(40, 30, 18, 26))
        metal_band(d, cx, cy, r, r * 0.76)
        claw(d, cx, cy + r * 0.94, r * 0.18, r * 0.13)
        faceted_gem(d, cx, cy + r * 1.32, r * 0.44, PALETTES["diamond" if k else "gold"], facets=8)
        sparkle(d, cx + r * 0.55, cy - r * 0.7, r * 0.15)
    return img.filter(ImageFilter.SMOOTH)


def product_necklace(size, pal="rose"):
    W, H = size
    img = backdrop(size, seed=12)
    d = ImageDraw.Draw(img, "RGBA")
    cx = W // 2
    curve = chain_curve(cx, int(H * 0.18), int(H * 0.74), 0.66, sag_pow=0.30)
    draw_chain(d, curve, thickness=4)
    for t in (0.18, 0.5, 0.82):
        x, y = curve(t)
        faceted_gem(d, x, y, int(min(W, H) * (0.085 if t == 0.5 else 0.05)), PALETTES[pal], facets=8)
    x, y = curve(0.5)
    sparkle(d, x, y, int(min(W, H) * 0.06))
    return img.filter(ImageFilter.SMOOTH)


def product_band(size, pal="diamond"):
    W, H = size
    img = backdrop(size, seed=21)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.55)
    r = int(min(W, H) * 0.24)
    metal_band(d, cx, cy, r, r * 0.74, color_b=(96, 104, 116))
    steps = 16
    for i in range(steps):
        a = i * math.tau / steps - math.pi / 2
        fx = cx + r * 0.87 * math.cos(a)
        fy = cy + r * 0.87 * math.sin(a)
        faceted_gem(d, fx, fy, r * 0.13, PALETTES[pal], facets=6, rotate=a)
    for a in (-2.3, -0.85, 0.6):
        sparkle(d, cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a), r * 0.16)
    return img.filter(ImageFilter.SMOOTH)


def chain_curve(cx, top, bot, span, sag_pow=0.72):
    """Shared geometry for a draped chain.

    Returns f(t) -> (x, y) for t in [0, 1]. Both the chain line and the stones
    are sampled from this one function so they always sit on the same curve.
    """
    span_px = cx * 2 * span
    sag = (bot - top) * sag_pow

    def f(t):
        x = cx + (t - 0.5) * span_px
        bell = math.sin(math.pi * t)
        y = top + (bot - top - sag) * bell + sag * bell
        return x, y

    return f


def draw_chain(d, curve, thickness=4, color_a=GOLD_LT, color_b=GOLD_DK, samples=140):
    pts = [curve(i / samples) for i in range(samples + 1)]
    for i in range(len(pts) - 1):
        shade = (math.sin(i * 0.085 - 1.0) + 1) / 2
        d.line([pts[i], pts[i + 1]], fill=lerp(color_b, color_a, shade ** 1.4), width=thickness)
    return pts


def product_bridal(size, pal="gold"):
    W, H = size
    img = backdrop(size, seed=33)
    d = ImageDraw.Draw(img, "RGBA")
    cx = W // 2
    gem = int(min(W, H) * 0.036)

    # maang tikka at the crown
    faceted_gem(d, cx, int(H * 0.12), gem * 1.9, PALETTES["gold"], facets=8)
    claw(d, cx, int(H * 0.12) + gem * 1.5, gem * 0.7, gem * 0.4)

    # choker
    choker = chain_curve(cx, int(H * 0.26), int(H * 0.46), 0.58, sag_pow=0.30)
    draw_chain(d, choker, thickness=8)
    for t in (0.16, 0.32, 0.5, 0.68, 0.84):
        x, y = choker(t)
        faceted_gem(d, x, y, gem * 1.15, PALETTES["diamond"], facets=8)

    # long rani haar
    rani = chain_curve(cx, int(H * 0.44), int(H * 0.80), 0.66, sag_pow=0.26)
    draw_chain(d, rani, thickness=6)
    for t in (0.12, 0.30, 0.5, 0.70, 0.88):
        x, y = rani(t)
        faceted_gem(d, x, y, gem * 1.35, PALETTES["gold"], facets=8)
    for t in (0.42, 0.58):
        x, y = rani(t)
        faceted_gem(d, x, y + gem * 1.9, gem * 0.8, PALETTES["diamond"], facets=6)

    sparkle(d, cx, int(H * 0.30), int(min(W, H) * 0.07))
    return img.filter(ImageFilter.SMOOTH)


def product_drops(size, pal="rose"):
    W, H = size
    img = backdrop(size, seed=41)
    d = ImageDraw.Draw(img, "RGBA")
    r = int(min(W, H) * 0.13)
    for ox in (-int(W * 0.18), int(W * 0.18)):
        cx = W // 2 + ox
        cy = int(H * 0.32)
        d.ellipse([cx - r * 1.3, cy + r * 0.55, cx + r * 1.3, cy + r * 1.1], fill=(40, 30, 18, 26))
        metal_band(d, cx, cy, r * 0.96, r * 0.7)
        claw(d, cx, cy + r * 0.94, r * 0.16, r * 0.12)
        faceted_gem(d, cx, cy + r * 1.5, r * 0.56, PALETTES["rose" if ox > 0 else "diamond"], facets=8)
        sparkle(d, cx + r * 0.34, cy + r * 1.22, r * 0.22)
    return img.filter(ImageFilter.SMOOTH)


PRODUCTS = {
    "product-solitaire": (product_solitaire, "diamond"),
    "product-hoops": (product_hoops, "gold"),
    "product-necklace": (product_necklace, "rose"),
    "product-band": (product_band, "diamond"),
    "product-bridal": (product_bridal, "gold"),
    "product-drops": (product_drops, "rose"),
}


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


def main() -> None:
    written = []

    def save(img, name, q=92):
        p = OUT / name
        if name.endswith(".jpg"):
            img.convert("RGB").save(p, "JPEG", quality=q, optimize=True, progressive=True)
        else:
            img.save(p, "PNG", optimize=True)
        written.append((name, img.size, p.stat().st_size))

    save(hero_bg((1920, 1080)), "hero.jpg", 88)
    save(og_image(), "og.jpg", 90)
    save(atelier((900, 1125)), "atelier.jpg", 90)

    for slug, (paint, pal) in PRODUCTS.items():
        save(paint((800, 1000), pal), slug + ".jpg", 90)

    tones = ["rose", "warm", "warm", "rose", "cool", "cool"]
    for i, tone in enumerate(tones):
        slug = ("sitara", "sehra", "ziya", "noor", "jewellery", "eternity")[i]
        save(editorial((800, 1067), seed=100 + i * 13, tone=tone), f"look-{slug}.jpg", 88)

    for name, size, nbytes in written:
        print(f"{name:24s} {size[0]}x{size[1]}  {nbytes / 1024:.0f} KB")
    print(f"\n{len(written)} images -> {OUT}")


if __name__ == "__main__":
    main()