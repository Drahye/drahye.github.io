#!/usr/bin/env python3
"""Normalise raw site screenshots into the page's hover previews.

    python3 tools/capture-shots.mjs   # writes tools/shots/*.png  (see header there)
    python3 tools/grade-shots.py      # writes src/img/shot-*.webp

The four linked sites are not tonally comparable — two are light themed and two
are near-black — so a single CSS filter cannot serve them. Everything below
exists to land all four in one tonal range before they reach the browser.
"""

import math
import pathlib

from PIL import Image, ImageEnhance, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = ROOT / "tools" / "shots"
OUT = ROOT / "src" / "img"

SITES = ["scholr", "learningforest", "agencymart", "tourstack"]

TARGET_MEAN = 70          # where every preview ends up, whatever it started at
CROP_FRACTION = 1.0       # the preview backs the whole section, so keep the whole page
WIDTH = 1280
WARM = (1.05, 0.965, 0.84)  # nudge toward the walnut / ember family
DESATURATE = 0.55

# The row's cream copy (relative luminance 0.836) sits over the preview, which
# renders at 0.7 opacity. Solve that for a 4.5:1 contrast ratio rather than
# picking a ceiling by eye.
PREVIEW_OPACITY = 0.7
CREAM_LUMINANCE = 0.836
_needed_bg = (CREAM_LUMINANCE + 0.05) / 4.5 - 0.05
CEILING = int(255 * (_needed_bg / PREVIEW_OPACITY) ** (1 / 2.2))


def mean_of(im: Image.Image) -> float:
    return sum(ImageStat.Stat(im).mean) / 3


def to_target(im: Image.Image, target: float) -> Image.Image:
    """Move an image's mean brightness onto `target`.

    Darkening uses a linear scale, which is exact: mean(k*x) == k*mean(x), and
    nothing clips on the way down. Lifting uses gamma, because linear scaling a
    near-black image would clip its highlights.

    The two are not interchangeable. Gamma cannot darken a white pixel at all
    (255 ** n == 255), so using it to darken a light-themed screenshot leaves
    every white region intact and the mean lands far above target.
    """
    current = mean_of(im)
    if current > target:
        k = target / current
        return im.point([max(0, min(255, int(i * k))) for i in range(256)] * 3)

    lo, hi = 0.05, 1.0
    for _ in range(24):                                # binary search the exponent
        g = (lo + hi) / 2
        lut = [max(0, min(255, int(255 * ((i / 255) ** g)))) for i in range(256)]
        if mean_of(im.point(lut * 3)) < target:
            hi = g
        else:
            lo = g
    g = (lo + hi) / 2
    return im.point([max(0, min(255, int(255 * ((i / 255) ** g)))) for i in range(256)] * 3)


def main() -> None:
    if not SHOTS.exists():
        raise SystemExit(f"no captures in {SHOTS} — run tools/capture-shots.mjs first")
    OUT.mkdir(parents=True, exist_ok=True)

    tint: list[int] = []
    for mult in WARM:
        tint += [max(0, min(255, int(i * mult))) for i in range(256)]
    # applied last: capping before the tint lets the tint push the ceiling
    # back up (a 150 cap became 157, and contrast fell to 3.0:1)
    cap = [min(i, CEILING) for i in range(256)] * 3

    print(f"highlight ceiling for 4.5:1 against cream: {CEILING}\n")
    print(f"{'site':16} {'before':>7} {'after':>6} {'peak':>5}  {'contrast':>9}")

    means = []
    for name in SITES:
        src = SHOTS / f"{name}.png"
        if not src.exists():
            print(f"{name:16} MISSING {src}")
            continue

        im = Image.open(src).convert("RGB")
        w, h = im.size
        band = int(h * CROP_FRACTION)
        im = im.crop((0, 0, w, band)).resize((WIDTH, int(WIDTH * band / w)), Image.LANCZOS)
        im = ImageEnhance.Color(im).enhance(DESATURATE)

        before = mean_of(im)
        im = to_target(im, TARGET_MEAN).point(tint).point(cap)
        im.save(OUT / f"shot-{name}.webp", "WEBP", quality=68, method=6)

        stat = ImageStat.Stat(im)
        after = sum(stat.mean) / 3
        peak = max(stat.extrema[c][1] for c in range(3))
        ratio = (CREAM_LUMINANCE + 0.05) / ((peak / 255) ** 2.2 * PREVIEW_OPACITY + 0.05)
        means.append(after)
        flag = "ok" if ratio >= 4.5 else "FAILS AA"
        print(f"{name:16} {before:7.1f} {after:6.1f} {peak:5d}  {ratio:6.1f}:1 {flag}")

    if means:
        kb = sum(q.stat().st_size for q in OUT.glob("shot-*.webp")) / 1024
        print(f"\nspread across the set: {max(means) - min(means):.1f}   total: {kb:.0f} KB")


if __name__ == "__main__":
    main()
