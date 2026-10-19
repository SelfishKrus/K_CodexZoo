"""Export README GIFs from each pet's runtime atlas and animation timings.

Requires Pillow. Run: python tools/render_readme_previews.py
"""
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BACKGROUND = (23, 25, 31, 255)


def main():
    for manifest in sorted((ROOT / 'output').glob('*/pet.json')):
        folder = manifest.parent
        pet = json.loads(manifest.read_text(encoding='utf-8'))
        meta = json.loads((folder / 'animations.json').read_text(encoding='utf-8'))
        atlas = Image.open(folder / pet['spritesheetPath']).convert('RGBA')
        width, height = meta['cellWidth'], meta['cellHeight']
        destination = folder / 'states'
        destination.mkdir(exist_ok=True)
        for state in meta['states']:
            frames = []
            for column in range(state['frames']):
                x, y = column * width, state['row'] * height
                sprite = atlas.crop((x, y, x + width, y + height))
                frame = Image.new('RGBA', (width, height), BACKGROUND)
                frame.alpha_composite(sprite)
                frames.append(frame.convert('RGB'))
            output = destination / f"{state['name']}.gif"
            frames[0].save(output, save_all=True, append_images=frames[1:],
                           duration=state['durationsMs'], loop=0,
                           disposal=2, optimize=False)
            # Verify every decoded frame and its timing against the runtime atlas.
            with Image.open(output) as saved:
                assert saved.n_frames == len(frames), output
                assert saved.info['loop'] == 0, output
                for index, expected in enumerate(frames):
                    saved.seek(index)
                    assert saved.convert('RGB').tobytes() == expected.tobytes(), output
                    assert saved.info['duration'] == state['durationsMs'][index], output
            print(f"Verified {output.relative_to(ROOT)}: {len(frames)} frames")


if __name__ == '__main__':
    main()
