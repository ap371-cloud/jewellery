"""The drawing primitives every product is assembled from.

A gem, a band, a claw, a pearl, a chain, a coin. Nothing here knows what a
"ring" is — that lives in products.py.
"""
from __future__ import annotations

import math

from .palette import GOLD_DK, GOLD_LT, add_light, lerp, radial_glow

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


def shaded_disc(draw, cx, cy, r, color, hi=(255, 255, 255)):
    """Sphere shaded from an off-centre highlight — pearls and cabochons."""
    steps = 24
    for i in range(steps, 0, -1):
        t = i / steps
        rr = r * t
        ox = oy = -r * 0.32 * (1 - t)
        draw.ellipse(
            [cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
            fill=lerp(color, hi, (1 - t) ** 2.1),
        )


def step_cut_gem(draw, cx, cy, w, h, palette, bevel=3):
    """Rectangular step cut (emerald cut): nested rectangles, flat table."""
    for i in range(bevel, 1, -1):
        t = i / (bevel + 1)
        ww, hh = w * (1 - t * 0.3), h * (1 - t * 0.3)
        draw.rectangle(
            [cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2],
            fill=lerp(palette[1], palette[2], t),
        )
    draw.rectangle(
        [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
        fill=lerp(palette[0], palette[1], 0.45),
    )
    draw.rectangle(
        [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=palette[2], width=2
    )
    draw.line(
        [(cx - w * 0.30, cy - h * 0.32), (cx + w * 0.26, cy - h * 0.32)],
        fill=lerp(palette[0], (255, 255, 255), 0.7),
        width=2,
    )


def flat_ring(draw, cx, cy, rx, ry, thick, color_a=GOLD_LT, color_b=GOLD_DK, steps=180):
    """Annulus squashed into an ellipse — a bangle lying flat on a surface."""
    for i in range(steps):
        a0 = i / steps * math.tau
        a1 = (i + 1) / steps * math.tau
        shade = (math.sin(a0 - 0.8) + 1) / 2
        draw.polygon(
            [
                (cx + rx * math.cos(a0), cy + ry * math.sin(a0)),
                (cx + (rx + thick) * math.cos(a0), cy + (ry + thick) * math.sin(a0)),
                (cx + (rx + thick) * math.cos(a1), cy + (ry + thick) * math.sin(a1)),
                (cx + rx * math.cos(a1), cy + ry * math.sin(a1)),
            ],
            fill=lerp(color_b, color_a, shade ** 1.5),
        )


def chain_loop(draw, cx, cy, rx, ry, thickness=3, color_a=GOLD_LT, color_b=GOLD_DK, steps=220):
    """A chain coiled into a flat loop, the way it is photographed off the neck."""
    for i in range(steps):
        a0 = i / steps * math.tau
        a1 = (i + 1) / steps * math.tau
        shade = (math.sin(a0 * 2 - 1.0) + 1) / 2
        draw.line(
            [
                (cx + rx * math.cos(a0), cy + ry * math.sin(a0)),
                (cx + rx * math.cos(a1), cy + ry * math.sin(a1)),
            ],
            fill=lerp(color_b, color_a, shade ** 1.3),
            width=thickness,
        )


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


def _coin_stack(draw, cx, base_y, radii, thickness, color_a, color_b):
    """Coins lying flat and stacked, each an ellipse with a milled edge."""
    for k, r in enumerate(radii):
        cy = base_y - k * thickness
        ry = r * 0.34
        draw.ellipse([cx - r, cy - ry, cx + r, cy + ry], fill=lerp(color_b, color_a, 0.45))
        draw.ellipse([cx - r, cy - ry - thickness, cx + r, cy + ry - thickness],
                     fill=lerp(color_b, color_a, 0.8))
        draw.ellipse([cx - r * 0.86, cy - ry - thickness * 0.5,
                      cx + r * 0.86, cy + ry - thickness * 0.5],
                     fill=lerp(color_a, (255, 255, 255), 0.25))
        for i in range(26):
            a = i * math.tau / 26
            draw.line([(cx + r * math.cos(a), cy + ry * math.sin(a)),
                       (cx + r * math.cos(a), cy + ry * math.sin(a) - thickness)],
                      fill=color_b, width=1)


def _coin_face(draw, cx, cy, r, color_a, color_b):
    """A coin stood upright on its edge, showing its milled face."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=lerp(color_b, color_a, 0.5))
    draw.ellipse([cx - r * 0.88, cy - r * 0.88, cx + r * 0.88, cy + r * 0.88],
                 fill=lerp(color_a, (255, 255, 255), 0.2))
    for i in range(16):
        a = i * math.tau / 16
        draw.line([(cx + r * 0.34 * math.cos(a), cy + r * 0.34 * math.sin(a)),
                   (cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a))],
                  fill=lerp(color_a, color_b, 0.35), width=2)
    draw.ellipse([cx - r * 0.26, cy - r * 0.26, cx + r * 0.26, cy + r * 0.26],
                 fill=lerp(color_b, color_a, 0.7))
    sparkle(draw, cx - r * 0.4, cy - r * 0.44, r * 0.22)

