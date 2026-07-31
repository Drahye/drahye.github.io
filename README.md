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

## Licences

Instrument Sans is under the SIL Open Font License — see
`src/fonts/OFL-InstrumentSans.txt`. The portrait and written content are not
covered by that licence.
