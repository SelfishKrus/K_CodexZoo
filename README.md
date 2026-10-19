# K_CodexZoo

Black and white pixel dinosaurs for Codex, with crisp 2px outlines and a desktop computer that shows task activity.

## Every animation state

Each preview loops through the complete sequence at its original speed. Both pets appear at their native 192 × 208 size on a dark background. The installable sprites have transparent backgrounds.

| Status | Black dinosaur · Pixel Dino | White dinosaur · Pixel Dino White |
| --- | --- | --- |
| **Idle** — breathing and blinking | ![Black dinosaur: idle](output/pixel-dino/states/idle.gif) | ![White dinosaur: idle](output/pixel-dino-white/states/idle.gif) |
| **Running right** — rightward gait | ![Black dinosaur: running right](output/pixel-dino/states/running-right.gif) | ![White dinosaur: running right](output/pixel-dino-white/states/running-right.gif) |
| **Running left** — leftward gait | ![Black dinosaur: running left](output/pixel-dino/states/running-left.gif) | ![White dinosaur: running left](output/pixel-dino-white/states/running-left.gif) |
| **Waving** — greeting | ![Black dinosaur: waving](output/pixel-dino/states/waving.gif) | ![White dinosaur: waving](output/pixel-dino-white/states/waving.gif) |
| **Jumping** — takeoff and landing | ![Black dinosaur: jumping](output/pixel-dino/states/jumping.gif) | ![White dinosaur: jumping](output/pixel-dino-white/states/jumping.gif) |
| **Failed** — error cross on the monitor | ![Black dinosaur: failed](output/pixel-dino/states/failed.gif) | ![White dinosaur: failed](output/pixel-dino-white/states/failed.gif) |
| **Waiting** — hourglass on the monitor | ![Black dinosaur: waiting](output/pixel-dino/states/waiting.gif) | ![White dinosaur: waiting](output/pixel-dino-white/states/waiting.gif) |
| **Working** (`running`) — typing and activity bars | ![Black dinosaur: working](output/pixel-dino/states/running.gif) | ![White dinosaur: working](output/pixel-dino-white/states/running.gif) |
| **Review** — inspecting the screen and a completion check | ![Black dinosaur: review](output/pixel-dino/states/review.gif) | ![White dinosaur: review](output/pixel-dino-white/states/review.gif) |

## Download and install

- **Black dinosaur:** [Download resource ZIP](output/pixel-dino.zip) · [Installation and file guide](output/pixel-dino/README.txt)
- **White dinosaur:** [Download resource ZIP](output/pixel-dino-white.zip) · [Installation and file guide](output/pixel-dino-white/README.txt)

Extract the chosen ZIP and copy its `pet.json` and `spritesheet.webp` together into the matching folder:

```text
%USERPROFILE%\.codex\pets\pixel-dino\
%USERPROFILE%\.codex\pets\pixel-dino-white\
```

If `CODEX_HOME` is customized, use its `pets` directory instead. Reopen Codex's pet selector and choose **Pixel Dino** or **Pixel Dino White**. Restart Codex if the list does not refresh.

## More previews

- [Both palettes on light and dark backgrounds](output/variants-preview.png)
- All frames: [Black dinosaur](output/pixel-dino/contact-sheet-dark.png) · [White dinosaur](output/pixel-dino-white/contact-sheet-dark.png)
- Interactive players, to download and open locally alongside their sprite sheets: [Black dinosaur](output/pixel-dino/preview.html) · [White dinosaur](output/pixel-dino-white/preview.html)

## Resource format

Each pet uses the Codex v1 sprite format: a 1536 × 1872 atlas, 192 × 208 cells, nine states and 57 animation frames. The optional v2 gaze-direction rows are not included. The `running` state represents active work; `running-right` and `running-left` represent movement.

The artwork is based on the reference in `img/`. Precise pixel processing removes the background grid and rebuilds uniform outlines with binary transparency. The white dinosaur uses the inverse opaque palette. Each pet includes validation and quality reports.

To regenerate the README animations with Python and Pillow installed:

```sh
python tools/render_readme_previews.py
```

The exporter reads each pet's runtime sprite sheet and `animations.json`, preserves frame timing and checks every decoded GIF frame against the source artwork.
