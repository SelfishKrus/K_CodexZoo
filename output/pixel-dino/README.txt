PIXEL DINO — CODEX PET RESOURCE SET

Based on the supplied black pixel dinosaur reference. The background grid has
been removed. A uniform two-pixel white outline keeps the dinosaur and computer visible on
dark backgrounds. Every 2 x 2 pixel block has one exact color, with no blended
edge colors or partial transparency. The sprite backgrounds are transparent.

INSTALLATION
Copy pet.json and spritesheet.webp together into:
  %USERPROFILE%\.codex\pets\pixel-dino\
If CODEX_HOME is customized, use its pets\pixel-dino folder instead.
Reopen the pet selector and choose Pixel Dino. Restart Codex if it does not
refresh the list. This resource set does not install or activate itself.

FORMAT
The installed Codex app (26.1013.4894.0) supports this v1 format:
  Canvas: 1536 x 1872 pixels; RGBA PNG and lossless WebP.
  Grid: 8 columns x 9 rows, 192 x 208 pixels per frame.
  57 occupied cells; 15 unused cells remain fully transparent.
  Manifest: spriteVersionNumber = 1; spritesheetPath = spritesheet.webp.

Rows, from the top (zero-based):
  0  idle           6 frames  Quiet breathing and blinking.
  1  running-right  8 frames  Alternating rightward gait.
  2  running-left   8 frames  Mirrored leftward gait, same temporal order.
  3  waving         4 frames  A small attached-arm greeting.
  4  jumping        5 frames  Anticipation, rise, peak, descent, landing.
  5  failed         8 frames  Error cross on monitor, disappointed reaction.
  6  waiting        6 frames  Hourglass on monitor, expectant waiting.
  7  running        6 frames  Typing at computer, changing activity bars.
  8  review         6 frames  Inspecting the screen and a completion check.

The state named "running" means an active task; directional movement has its
own running-right and running-left rows. This v1 set does not include the
optional sixteen gaze-direction frames used by v2.

CONTENTS
pet.json                Codex import manifest.
spritesheet.webp        Lossless runtime atlas referenced by the manifest.
spritesheet.png         Matching transparent PNG atlas.
dinosaur.png            Transparent 192 x 208 idle pose for standalone use.
animations.json         Row mapping, cell geometry and playback durations.
preview.html            Offline interactive player; state, frame, size and
                        background controls. Open in a browser.
preview.gif             Animated nine-state overview on a dark background.
preview-dark.png        Actual-size browser preview on a pure black background.
contact-sheet.png       Every frame on a light background.
contact-sheet-dark.png  Every frame on a dark background.
validation.json         Bundled atlas validator's report for the WebP file.
frame-review.json       Bundled extracted-frame inspection report.
quality-checks.json    Palette, transparency, margins and jump checks.
source-assets.zip       Selected generated strips, source references, prompts
                        and registration information for future revision.

ARTWORK AND VERIFICATION
Original artwork uses built-in Image Generation. After approval for precise
pixel processing, tools/normalize_pet.py removes the generated outer outline,
preserves enclosed eyes/screens, snaps artwork onto a 2px grid, and rebuilds
an exact one-grid-cell (2px) outline using square/Chebyshev dilation. The white
variant in output/pixel-dino-white uses the inverse opaque palette.

Rebuild both palettes from the repository root with Pillow installed:
  python tools/normalize_pet.py
The source-assets.zip archive contains the original generated strips and
pre-cleanup frame inputs, prompts and registration information. It is kept as
immutable input, so repeated cleanup never stacks outlines. The script builds
atlases, manifests, contact sheets, GIFs and quality checks; rerun the bundled
atlas/frame validators and refresh browser captures and ZIPs after rebuilding.

Format and timing were checked against the locally installed app. Both variants
pass atlas and frame checks. The quality report checks the exact 2px grid and
outline construction, opaque black/white palette and binary transparency.
No in-app installation or activation is claimed.

The original reference in img/ remains unchanged.
