K_CodexZoo

Pixel Dino: black and white pixel-art Codex pets based on the reference in img/.
The background grid is removed. Uniform 2px outlines support both backgrounds.
A desktop computer makes working, waiting, review and error states distinct.

Black variant: output/pixel-dino.zip
White variant: output/pixel-dino-white.zip
Both palettes on light/dark backgrounds: output/variants-preview.png
Interactive preview: output/pixel-dino/preview.html (open locally in a browser)
Animated overview: output/pixel-dino/preview.gif
Installation and file guide: output/pixel-dino/README.txt

Codex v1 sprite format: 1536 x 1872 pixels, 192 x 208 cells, 9 states, 57 frames.
Each variant has its own pet.json and spritesheet.webp runtime files.
The optional v2 gaze-direction rows are not included.

Validation reports and selected source artwork are included with the resource
set. Artwork was generated with built-in Image Generation and assembled using
connected-component extraction and nearest-neighbor resizing. Precise cleanup
in tools/normalize_pet.py rebuilds exact 2px outlines on a fixed 2px grid with
binary transparency. The white version uses the inverse opaque palette.
