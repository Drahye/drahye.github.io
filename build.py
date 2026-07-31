#!/usr/bin/env python3
"""Inline the subset fonts into src/page.html and emit two builds.

    index.html     standalone document — deploy this anywhere
    artifact.html  body content only — for Claude Artifact publishing

Run:  python3 build.py
"""

import base64
import pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

FONTS = {
    # one variable face, wght 400-700: the system specifies a single
    # typeface, and weight 500 must be a real Medium, not a relabelled 400
    "__ISANS_VAR__": "isans-var.woff2",
}

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Abraham Ayoola — Product Designer</title>
<meta name="description" content="Product designer. Three interfaces shipped fast on instinct, and one portfolio built slowly with the research left in.">
<meta name="theme-color" content="#100904">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23100904'/><text x='16' y='23' font-family='sans-serif' font-size='19' font-weight='500' fill='%23ffedd7' text-anchor='middle'>A</text></svg>">
<meta property="og:title" content="Abraham Ayoola — Product Designer">
<meta property="og:description" content="Three interfaces shipped fast on instinct, and one portfolio built slowly with the research left in.">
<meta property="og:type" content="website">
<style>html,body{margin:0;padding:0;background:#100904;}</style>
</head>
<body>
"""

TAIL = """</body>
</html>
"""


def main() -> None:
    page = (SRC / "page.html").read_text(encoding="utf-8")

    assets = [(t, SRC / "fonts" / f, "font/woff2") for t, f in FONTS.items()]
    assets.append(("__PORTRAIT__", SRC / "img" / "portrait.webp", "image/webp"))

    for token, path, mime in assets:
        if token not in page:
            raise SystemExit(f"build: placeholder {token} not found in src/page.html")
        uri = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        page = page.replace(token, uri)

    (ROOT / "index.html").write_text(HEAD + page + TAIL, encoding="utf-8")
    (ROOT / "artifact.html").write_text(page, encoding="utf-8")

    size = len((ROOT / "index.html").read_bytes()) / 1024
    print(f"built index.html and artifact.html — {size:.0f} KB self-contained")


if __name__ == "__main__":
    main()
