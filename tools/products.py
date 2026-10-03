"""One painter per catalogue piece, keyed by the slug index.html asks for.

PRODUCTS maps an asset slug to (painter, stone palette). The slugs must match
the img fields in assets/js/pieces.js; build_images.py checks that they do.
"""
from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter

from .palette import (
    GOLD_DK,
    GOLD_LT,
    PALETTES,
    ROSE_A,
    ROSE_B,
    SILVER_A,
    SILVER_B,
    backdrop,
    lerp,
)
from .primitives import (
    _coin_face,
    _coin_stack,
    chain_curve,
    chain_loop,
    claw,
    draw_chain,
    faceted_gem,
    flat_ring,
    metal_band,
    shaded_disc,
    sparkle,
    step_cut_gem,
)


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


def product_halo(size, pal="diamond"):
    """Ring with a thin circle of small stones set around the whole hoop."""
    W, H = size
    img = backdrop(size, seed=53)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.58)
    r = int(min(W, H) * 0.21)

    d.ellipse([cx - r * 1.75, cy + r * 0.42, cx + r * 1.75, cy + r * 1.08], fill=(40, 30, 18, 26))
    metal_band(d, cx, cy, r * 1.32, r * 1.06, color_a=ROSE_A, color_b=ROSE_B)
    halo = r * 1.19
    for i in range(24):
        a = i * math.tau / 24 - math.pi / 2
        faceted_gem(d, cx + halo * math.cos(a), cy + halo * math.sin(a),
                    r * 0.115, PALETTES[pal], facets=6, rotate=a)
    sparkle(d, cx + halo * 0.68, cy - halo * 0.70, r * 0.22)
    return img.filter(ImageFilter.SMOOTH)


def product_emerald(size, pal="emerald"):
    """Centre stone cut as a rectangle, flanked by two small brilliants."""
    W, H = size
    img = backdrop(size, seed=59)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.62)
    r = int(min(W, H) * 0.21)

    d.ellipse([cx - r * 1.7, cy + r * 0.4, cx + r * 1.7, cy + r * 1.05], fill=(40, 30, 18, 26))
    metal_band(d, cx, cy, r * 1.5, r * 1.2)
    stone_cy = cy - r * 1.68
    step_cut_gem(d, cx, stone_cy, r * 1.18, r * 0.86, PALETTES[pal])
    for ox in (-r * 0.82, r * 0.82):
        claw(d, cx + ox, stone_cy + r * 0.18, r * 0.19, r * 0.16)
        faceted_gem(d, cx + ox, stone_cy, r * 0.26, PALETTES["diamond"], facets=8)
    claw(d, cx, stone_cy + r * 0.40, r * 0.20, r * 0.18)
    sparkle(d, cx - r * 0.44, stone_cy - r * 0.30, r * 0.18)
    return img.filter(ImageFilter.SMOOTH)


def product_jhumka(size, pal="gold"):
    """Domed jhumka pair: pearl drop under a stud, then a fringe of chains."""
    W, H = size
    img = backdrop(size, seed=61, warm=True)
    d = ImageDraw.Draw(img, "RGBA")
    r = int(min(W, H) * 0.12)

    for ox in (-int(W * 0.19), int(W * 0.19)):
        cx = W // 2 + ox
        top = int(H * 0.22)
        d.ellipse([cx - r * 1.5, int(H * 0.62), cx + r * 1.5, int(H * 0.70)], fill=(40, 30, 18, 22))

        faceted_gem(d, cx, top, r * 0.34, PALETTES["diamond"], facets=8)
        for a in (0.4, 2.5, 4.6):
            d.line([(cx, top + r * 0.3),
                    (cx + r * 1.05 * math.cos(a), top + r * 0.3 + r * 1.05 * math.sin(a))],
                   fill=lerp(GOLD_DK, GOLD_LT, 0.6), width=3)

        dome_cy = top + r * 1.95
        for i in range(7, 0, -1):
            t = i / 7
            rr = r * 1.12 * t
            d.ellipse([cx - rr, dome_cy - rr, cx + rr, dome_cy + rr],
                      fill=lerp(GOLD_DK, GOLD_LT, (1 - t) ** 1.4 + 0.12))
        d.ellipse([cx - r * 1.16, dome_cy - r * 0.5, cx + r * 1.16, dome_cy + r * 1.16],
                  outline=lerp(GOLD_LT, (255, 255, 255), 0.4), width=2)
        for a in (-1.05, -0.35, 0.35, 1.05):
            ex = cx + r * 1.12 * math.cos(a)
            ey = dome_cy + r * 1.12 * math.sin(a)
            d.line([(cx, dome_cy + r * 0.2), (ex, ey + r * 0.5)],
                   fill=lerp(GOLD_DK, GOLD_LT, 0.45), width=2)

        for a in (-0.85, -0.3, 0.3, 0.85):
            d.line([(cx + r * 0.5 * math.cos(a), dome_cy + r * 1.5),
                    (cx + r * 0.62 * math.cos(a), dome_cy + r * 2.5)],
                   fill=lerp(GOLD_DK, GOLD_LT, 0.5), width=2)
        shaded_disc(d, cx, dome_cy + r * 2.72, r * 0.32, (238, 228, 210))
    return img.filter(ImageFilter.SMOOTH)


def product_studs(size, pal="sapphire"):
    """A pair of cabochon studs, close up and slightly apart."""
    W, H = size
    img = backdrop(size, seed=67, warm=False)
    d = ImageDraw.Draw(img, "RGBA")
    r = int(min(W, H) * 0.15)

    for k, ox in enumerate((-int(W * 0.17), int(W * 0.17))):
        cx = W // 2 + ox
        cy = int(H * 0.46)
        d.ellipse([cx - r * 1.25, cy + r * 0.62, cx + r * 1.25, cy + r * 1.14], fill=(40, 30, 18, 24))
        for i in range(14, 0, -1):
            t = i / 14
            rr = r * 0.98 * t
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                      fill=lerp(SILVER_B, SILVER_A, (1 - t) ** 1.5 + 0.1))
        shaded_disc(d, cx, cy, r * 0.66, PALETTES[pal][1], hi=lerp(PALETTES[pal][0], (255, 255, 255), 0.4))
        sparkle(d, cx - r * 0.24, cy - r * 0.28, r * 0.2)
    return img.filter(ImageFilter.SMOOTH)


def product_rani(size, pal="gold"):
    """Long haar: many small floral repeats along a deep U, one drop at the centre."""
    W, H = size
    img = backdrop(size, seed=73)
    d = ImageDraw.Draw(img, "RGBA")
    cx = W // 2
    curve = chain_curve(cx, int(H * 0.16), int(H * 0.78), 0.72, sag_pow=0.34)
    draw_chain(d, curve, thickness=5, samples=200)

    clusters = 15
    for i in range(clusters):
        t = 0.06 + (i / (clusters - 1)) * 0.88
        x, y = curve(t)
        scale = 1.0 if 0.4 < t < 0.6 else 0.74
        petal = max(int(min(W, H) * 0.022), 3) * scale
        for a in (0.0, 1.57, 3.14, 4.71):
            faceted_gem(d, x + petal * 1.7 * math.cos(a), y + petal * 1.7 * math.sin(a),
                        petal, PALETTES[pal], facets=6, rotate=a)
        faceted_gem(d, x, y, petal * 1.25, PALETTES["gold"], facets=8)

    x, y = curve(0.5)
    faceted_gem(d, x, y + int(min(W, H) * 0.055), int(min(W, H) * 0.045),
                PALETTES["diamond"], facets=10)
    sparkle(d, x, y + int(min(W, H) * 0.055), int(min(W, H) * 0.055))
    return img.filter(ImageFilter.SMOOTH)


def product_choker(size, pal="diamond"):
    """Close-fitting collar laid flat, stones set all the way round."""
    W, H = size
    img = backdrop(size, seed=79)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.50)
    rx, ry = int(W * 0.30), int(H * 0.24)

    flat_ring(d, cx, cy, rx, ry, int(min(W, H) * 0.045))
    stones = 26
    for i in range(stones):
        a = i * math.tau / stones - math.pi / 2
        big = i % 2 == 0
        rad = int(min(W, H) * (0.030 if big else 0.019))
        faceted_gem(d, cx + (rx + int(min(W, H) * 0.022)) * math.cos(a),
                    cy + (ry + int(min(W, H) * 0.022)) * math.sin(a),
                    rad, PALETTES[pal], facets=6, rotate=a)
    sparkle(d, cx + rx * 0.72, cy - ry * 0.72, int(min(W, H) * 0.05))
    return img.filter(ImageFilter.SMOOTH)


def product_pendant(size, pal="diamond"):
    """Fine chain coiled into a loop with a single small pendant hanging off it."""
    W, H = size
    img = backdrop(size, seed=83)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.44)
    rx, ry = int(W * 0.27), int(H * 0.155)

    chain_loop(d, cx, cy, rx, ry, thickness=3)
    py = cy + ry
    d.ellipse([cx - rx * 0.09, py - rx * 0.06, cx + rx * 0.09, py + rx * 0.12],
              outline=GOLD_LT, width=3)
    gem_r = int(min(W, H) * 0.048)
    d.line([(cx, py + rx * 0.12), (cx, py + rx * 0.30)], fill=GOLD_LT, width=3)
    claw(d, cx - gem_r * 0.62, py + rx * 0.30, gem_r * 0.20, gem_r * 0.16)
    claw(d, cx + gem_r * 0.62, py + rx * 0.30, gem_r * 0.20, gem_r * 0.16)
    faceted_gem(d, cx, py + rx * 0.30 + gem_r * 0.5, gem_r, PALETTES[pal], facets=10)
    sparkle(d, cx + gem_r * 0.6, py + rx * 0.06, gem_r * 0.5)
    return img.filter(ImageFilter.SMOOTH)


def product_bangles(size, pal="gold"):
    """Four wide bangles stacked and slightly fanned on a flat surface."""
    W, H = size
    img = backdrop(size, seed=89)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, int(H * 0.52)
    rx, ry = int(W * 0.25), int(H * 0.15)
    thick = int(min(W, H) * 0.055)

    for k in range(4):
        ox = (k - 1.5) * int(W * 0.035)
        oy = -k * int(H * 0.012)
        shade = 0.30 + 0.7 * (1 - k / 4)
        flat_ring(d, cx + ox, cy + oy, rx, ry, thick,
                  color_a=lerp(GOLD_LT, (255, 255, 255), shade * 0.25),
                  color_b=lerp(GOLD_DK, (60, 44, 16), 1 - shade))
        for a in (-2.5, -1.9, -1.3, 1.3, 1.9, 2.5):
            d.line(
                [(cx + ox + rx * math.cos(a), cy + oy + ry * math.sin(a)),
                 (cx + ox + (rx + thick) * math.cos(a), cy + oy + (ry + thick) * math.sin(a))],
                fill=GOLD_DK, width=2,
            )
    return img.filter(ImageFilter.SMOOTH)


def product_bracelet(size, pal="diamond"):
    """Line-eternity bracelet laid in a loose S so the row of stones catches light."""
    W, H = size
    img = backdrop(size, seed=97, warm=False)
    d = ImageDraw.Draw(img, "RGBA")

    def spine(t):
        x = int(W * 0.16) + t * int(W * 0.68)
        y = int(H * 0.50) + math.sin(t * math.pi * 1.6) * int(H * 0.17)
        return x, y

    pts = [spine(i / 120) for i in range(121)]
    for i in range(len(pts) - 1):
        shade = (math.sin(i * 0.11 - 0.6) + 1) / 2
        d.line([pts[i], pts[i + 1]], fill=lerp(SILVER_B, SILVER_A, shade ** 1.4), width=6)

    stones = 22
    for i in range(stones):
        x, y = spine(0.03 + (i / (stones - 1)) * 0.94)
        faceted_gem(d, x, y, int(min(W, H) * 0.028), PALETTES[pal], facets=6, rotate=i * 0.3)
    sparkle(d, spine(0.42)[0], spine(0.42)[1] - int(min(W, H) * 0.03), int(min(W, H) * 0.03))
    return img.filter(ImageFilter.SMOOTH)


def product_lehenga(size, pal="gold"):
    """Full bridal set: choker, haar, earrings, tikka, bangles and a ring."""
    W, H = size
    img = backdrop(size, seed=101)
    d = ImageDraw.Draw(img, "RGBA")
    cx = W // 2
    gem = int(min(W, H) * 0.026)

    faceted_gem(d, cx, int(H * 0.09), gem * 1.7, PALETTES["gold"], facets=8)
    claw(d, cx, int(H * 0.09) + gem * 1.35, gem * 0.7, gem * 0.4)
    for a in (0.5, 1.6, 3.7, 4.8):
        d.line([(cx, int(H * 0.09) + gem * 1.6),
                (cx + gem * 2.2 * math.cos(a), int(H * 0.09) + gem * 1.6 + gem * 2.2 * math.sin(a))],
               fill=GOLD_LT, width=2)

    choker = chain_curve(cx, int(H * 0.21), int(H * 0.34), 0.54, sag_pow=0.26)
    draw_chain(d, choker, thickness=7, samples=180)
    for t in (0.14, 0.28, 0.42, 0.58, 0.72, 0.86):
        x, y = choker(t)
        faceted_gem(d, x, y, gem * 1.05, PALETTES["diamond"], facets=8)

    haar = chain_curve(cx, int(H * 0.36), int(H * 0.70), 0.66, sag_pow=0.30)
    draw_chain(d, haar, thickness=5, samples=180)
    for i in range(13):
        t = 0.05 + i / 12 * 0.90
        x, y = haar(t)
        faceted_gem(d, x, y, gem * (1.25 if 0.42 < t < 0.58 else 0.85), PALETTES["gold"], facets=8)
    x, y = haar(0.5)
    faceted_gem(d, x, y + gem * 2.1, gem * 1.5, PALETTES["diamond"], facets=10)

    for ox in (-int(W * 0.31), int(W * 0.31)):
        ex = cx + ox
        ey = int(H * 0.30)
        for i in range(6, 0, -1):
            t = i / 6
            rr = gem * 2.4 * t
            d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr],
                      fill=lerp(GOLD_DK, GOLD_LT, (1 - t) ** 1.4 + 0.12))
        shaded_disc(d, ex, ey + gem * 3.3, gem * 0.85, (238, 228, 210))
        faceted_gem(d, ex, ey, gem * 0.7, PALETTES["diamond"], facets=8)

    for ox in (-int(W * 0.24), int(W * 0.24)):
        bx, by = cx + ox, int(H * 0.80)
        flat_ring(d, bx, by, int(W * 0.075), int(H * 0.045), int(min(W, H) * 0.022))

    rx, ry = cx + int(W * 0.10), int(H * 0.855)
    flat_ring(d, rx, ry, int(W * 0.052), int(H * 0.031), int(min(W, H) * 0.016))
    faceted_gem(d, rx, ry - int(min(W, H) * 0.030), gem * 1.3, PALETTES["diamond"], facets=8)

    sparkle(d, cx, int(H * 0.26), int(min(W, H) * 0.05))
    return img.filter(ImageFilter.SMOOTH)


def product_coin(size, pal="gold"):
    """Gold bullion: one coin on its edge beside a short stack lying flat."""
    W, H = size
    img = backdrop(size, seed=103)
    d = ImageDraw.Draw(img, "RGBA")
    r = int(min(W, H) * 0.115)

    _coin_stack(d, int(W * 0.68), int(H * 0.70),
                [r * 1.5, r * 1.5, r * 1.5], int(H * 0.026), GOLD_LT, GOLD_DK)
    _coin_face(d, int(W * 0.33), int(H * 0.55), r, GOLD_LT, GOLD_DK)
    d.ellipse([int(W * 0.33) - r * 1.2, int(H * 0.70), int(W * 0.33) + r * 1.2, int(H * 0.78)],
              fill=(40, 30, 18, 26))
    sparkle(d, int(W * 0.68), int(H * 0.53), int(min(W, H) * 0.045))
    return img.filter(ImageFilter.SMOOTH)


def product_silvercoin(size, pal="silver"):
    """Silver bullion on a darker slate so the shine separates from the backdrop."""
    W, H = size
    img = backdrop(size, seed=107, warm=False)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, int(H * 0.52), W, H], fill=(96, 100, 106, 255))
    d.rectangle([0, int(H * 0.52), W, int(H * 0.52) + 6], fill=(120, 124, 130, 255))
    r = int(min(W, H) * 0.125)

    _coin_stack(d, int(W * 0.36), int(H * 0.76),
                [r * 1.55, r * 1.55], int(H * 0.030), SILVER_A, SILVER_B)
    _coin_stack(d, int(W * 0.72), int(H * 0.80),
                [r * 1.2, r * 1.2, r * 1.2], int(H * 0.026), SILVER_A, SILVER_B)
    _coin_face(d, int(W * 0.55), int(H * 0.60), r * 0.95, SILVER_A, SILVER_B)
    sparkle(d, int(W * 0.36), int(H * 0.56), int(min(W, H) * 0.05))
    return img.filter(ImageFilter.SMOOTH)


PRODUCTS = {
    "product-solitaire": (product_solitaire, "diamond"),
    "product-hoops": (product_hoops, "gold"),
    "product-necklace": (product_necklace, "rose"),
    "product-band": (product_band, "diamond"),
    "product-bridal": (product_bridal, "gold"),
    "product-drops": (product_drops, "rose"),
    "product-halo": (product_halo, "diamond"),
    "product-emerald": (product_emerald, "emerald"),
    "product-jhumka": (product_jhumka, "gold"),
    "product-studs": (product_studs, "sapphire"),
    "product-rani": (product_rani, "gold"),
    "product-choker": (product_choker, "diamond"),
    "product-pendant": (product_pendant, "diamond"),
    "product-bangles": (product_bangles, "gold"),
    "product-bracelet": (product_bracelet, "diamond"),
    "product-lehenga": (product_lehenga, "gold"),
    "product-coin": (product_coin, "gold"),
    "product-silvercoin": (product_silvercoin, "silver"),
}


PRODUCTS = {
    "product-solitaire": (product_solitaire, "diamond"),
    "product-hoops": (product_hoops, "gold"),
    "product-necklace": (product_necklace, "rose"),
    "product-band": (product_band, "diamond"),
    "product-bridal": (product_bridal, "gold"),
    "product-drops": (product_drops, "rose"),
    "product-halo": (product_halo, "diamond"),
    "product-emerald": (product_emerald, "emerald"),
    "product-jhumka": (product_jhumka, "gold"),
    "product-studs": (product_studs, "sapphire"),
    "product-rani": (product_rani, "gold"),
    "product-choker": (product_choker, "diamond"),
    "product-pendant": (product_pendant, "diamond"),
    "product-bangles": (product_bangles, "gold"),
    "product-bracelet": (product_bracelet, "diamond"),
    "product-lehenga": (product_lehenga, "gold"),
    "product-coin": (product_coin, "gold"),
    "product-silvercoin": (product_silvercoin, "silver"),
}
