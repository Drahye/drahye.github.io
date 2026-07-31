# drahye.github.io

Landing page for Abraham Ayoola — product designer. One page, two kinds of work:
four interfaces shipped fast on instinct, and one portfolio built slowly with the
research left in.

Live at **https://drahye.github.io/**

## Structure

```
src/page.html      the source: styles, markup and script
src/fonts/         subset Instrument Sans (variable, wght 400-700)
src/img/           the hero portrait, cropped and encoded as webp
build.py           inlines the fonts and image, emits the deployable file
index.html         build output — self-contained, no external requests
```

`index.html` is generated. Edit `src/page.html`, then:

```bash
python3 build.py
```

Everything is inlined as data URIs, so the page is a single file with zero network
dependencies beyond itself. That also means it renders identically offline, from a
file:// URL, or behind a strict CSP.

## Design system

Built to the ORYZO AI visual system — a darkroom product editorial: warm near-black
canvas, cream typography, one vivid orange reserved for editorial credit lines.
Tokens come from `variables.css` / `tokens.json` and are used verbatim.

Values that are deliberate and easy to "helpfully" break:

- **Fixed type scale.** 8 / 10 / 12 / 14 / 18 / 24 / 29 / 41 / 51px. No `clamp()`
  anywhere. The wordmark steps between fixed sizes at breakpoints rather than
  interpolating, so every viewport lands on a chosen value.
- **Weight 500 everywhere**, and it is a real Medium — the face is variable
  (wght 400–700), not a Regular relabelled. Weight 400 appears exactly once, on
  the 29px mixed-case paragraph, and that case-and-weight shift is the signal that
  you are reading description rather than a label.
- **`#dc5000` is never a button.** It marks credit lines only. There is exactly one
  filled button on the page; its rarity is the point.
- **Line-height 0.9** at display sizes. The caps overlap their line box and stack
  as solid form. This is intentional, not a bug.
- **Radii are a closed set**: 12px cards, 22.5px ghost buttons, 36px pill, 0 for
  inline links.

Two deliberate departures from the extracted tokens, both documented in the CSS:

- `driftwood` `#6c5f51` measures 2.8:1 on the canvas and fails as body text, so
  secondary copy uses a derived `#a49687` (cream at 62% over walnut, 6.5:1).
  Driftwood keeps to dividers, which is what its own token description asks of it.
- Halyard Display is Typekit-licensed and cannot be embedded. Instrument Sans
  stands in — the closest structural match with a real variable weight axis.

Note: `--surface-cork-border` in the upstream token files is `#40372`, a five-digit
hex. The correct value is `#40372e`, as `--color-cork-border` has it.

## The object

The portfolio section renders a shallow dish with a raised rim as a point cloud on
canvas. Two rotations run at once and neither can degenerate: it spins on its own
axis, where radial symmetry keeps the silhouette fixed so the moving spiral pattern
carries the motion, while the tilt sweeps top-down to three-quarter.

The cursor turns it. Tilt is clamped to `[-1.05, -0.22]` and yaw to `±0.42`, giving
a worst case foreshortening of 0.45 — measured across nine cursor positions, the
silhouette aspect stays between 0.89 and 1.02, so no pointer position can drive it
edge-on. Disabled under `prefers-reduced-motion` and on coarse pointers.

Points are stamped from pre-rendered sprites. Batching thousands of arcs into a
single path is pathologically slow to rasterise and will stall the main thread.

## Hover previews

Hovering a workbench row fills the whole section behind it with a screenshot of
that site. It backs the section rather than the row, so the captured page has room
to read — clipped inside a row it was a letterbox band showing little more than a
nav bar. It is not laid over the canvas but emerges from it: `mix-blend-mode:
screen` means the screenshot's dark pixels stay walnut and only its lit areas
surface, and a two-axis gradient mask dissolves all four edges.

A row drives a layer that is not its descendant, via `:has()` on the section.
Where `:has()` is unsupported the preview simply never appears and nothing else
is affected.

While a capture is showing, the row bands settle back toward walnut. Raw contrast
already passes, but the captures carry their own body copy, and text sitting on
text is hard to read regardless of ratio. The preview stays vivid in the gaps
between rows and around the heading.

The captures are normalised at build time, not in CSS, because the four sites are
not tonally comparable — Scholr and Learning Forest are light themed (mean
brightness 215 and 239), Agency Mart and TourStack are dark (26 and 19). A single
CSS filter cannot serve both; screen-blending the light pair would have produced
white slabs. `tools/grade-shots.py` brings all four into one range: means of 57-66,
a spread of 9.2 where they started 223.3 apart. (Normalisation alone gets the
spread to 0.6; the highlight cap below then pulls the darker captures down a
little further, which is the right trade.)

Two constraints that look arbitrary and are not:

- **Darkening uses a linear scale, lifting uses gamma.** Gamma cannot darken a
  white pixel — `255 ** n == 255` — so a single gamma left Scholr's white regions
  intact and the mean stuck at 133. Linear scaling is exact when reducing.
- **Highlights are capped at 125.** The row's cream copy sits over this. Solving
  cream (L = 0.836) at the preview's 0.7 opacity for 4.5:1 gives a ceiling of 125,
  and the cap is applied *after* the warm tint, since tinting a 150 cap pushed it
  back to 157 and contrast to 3.0:1.

Regenerating: `node tools/capture-shots.mjs` then `python3 tools/grade-shots.py`.
The raw captures land in `tools/shots/` and are gitignored — they are ~1MB and the
capture script rebuilds them. Note that headless Brave/Chrome does not work on
macOS 13 (`--headless=new` hangs, `--headless=old` exits 0 without writing a file,
failing on CVDisplayLink), and current Playwright dropped mac13 — pin 1.49.1.

## Licences

Instrument Sans is under the SIL Open Font License — see
`src/fonts/OFL-InstrumentSans.txt`. The portrait and written content are not
covered by that licence.
