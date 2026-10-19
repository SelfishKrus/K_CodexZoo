"""Rebuild both pet palettes on a 2px grid from archived original frames.

Requires Pillow. Run from any directory: python tools/normalize_pet.py
The source archive is immutable input; outlines are never added on top of a
previously outlined export. No AI regeneration is used for this cleanup.
"""
from collections import deque
from io import BytesIO
from pathlib import Path
import hashlib
import json
import zipfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BLACK = ROOT / 'output/pixel-dino'
WHITE = ROOT / 'output/pixel-dino-white'
GRID = 2
SIZE = (192, 208)
META = json.loads((BLACK / 'animations.json').read_text())


def remove_generated_outline(frame):
    """Keep black artwork and enclosed white eyes/screens, discard outer white."""
    width, height = frame.size
    pixels = list(frame.convert('RGBA').get_flattened_data())
    black = [p[3] > 127 and p[0] < 128 for p in pixels]
    outside = bytearray(width * height)
    queue = deque()
    for y in range(height):
        for x in (0, width - 1):
            i = y * width + x
            if not black[i] and not outside[i]:
                outside[i] = 1
                queue.append(i)
    for x in range(width):
        for y in (0, height - 1):
            i = y * width + x
            if not black[i] and not outside[i]:
                outside[i] = 1
                queue.append(i)
    while queue:
        i = queue.popleft()
        x, y = i % width, i // width
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                j = ny * width + nx
                if not black[j] and not outside[j]:
                    outside[j] = 1
                    queue.append(j)
    output = Image.new('RGBA', frame.size)
    output.putdata([
        (0, 0, 0, 255) if black[i] else
        (255, 255, 255, 255) if not outside[i] and p[3] > 127 else
        (0, 0, 0, 0)
        for i, p in enumerate(pixels)
    ])
    return output


def snap_to_grid(frame):
    """Area-majority sampling, without interpolation or partial-alpha pixels."""
    small = Image.new('RGBA', (SIZE[0] // GRID, SIZE[1] // GRID))
    src, dst = frame.load(), small.load()
    for y in range(small.height):
        for x in range(small.width):
            block = [src[x * GRID + dx, y * GRID + dy]
                     for dy in range(GRID) for dx in range(GRID)]
            occupied = [p for p in block if p[3]]
            if len(occupied) < 2:
                continue
            white = sum(p[0] == 255 for p in occupied)
            color = 255 if white > len(occupied) / 2 else 0
            dst[x, y] = (color, color, color, 255)
    return small


def normalize(frame):
    core = snap_to_grid(remove_generated_outline(frame))
    alpha = core.getchannel('A')
    expanded = alpha.filter(ImageFilter.MaxFilter(3))
    ring = ImageChops.subtract(expanded, alpha)
    normalized = Image.new('RGBA', core.size)
    normalized.paste((255, 255, 255, 255), (0, 0), ring)
    normalized.alpha_composite(core)
    assert normalized.getchannel('A').tobytes() == expanded.tobytes()
    assert all(p[:3] == (255, 255, 255) for p, v in
               zip(normalized.get_flattened_data(), ring.get_flattened_data()) if v)
    return normalized.resize(SIZE, Image.Resampling.NEAREST), core, ring


def inverse_palette(frame):
    output = Image.new('RGBA', frame.size)
    output.putdata([(255-r, 255-g, 255-b, a) if a else (0, 0, 0, 0)
                    for r, g, b, a in frame.get_flattened_data()])
    return output


def get_font(size):
    for candidate in ('C:/Windows/Fonts/segoeui.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def render_previews(folder, atlas, title):
    font = get_font(16)
    for suffix, bg, fg in (('', '#eeeeee', '#222222'), ('-dark', '#17191f', '#eeeeee')):
        sheet = Image.new('RGB', (896, 1160), bg)
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 10), title + ' | uniform 2px outline', fill=fg, font=font)
        for state in META['states']:
            row = state['row']; y = 44 + row * 124
            draw.text((12, y + 42), state['name'], fill=fg, font=font)
            for col in range(state['frames']):
                cell = atlas.crop((col*192, row*208, (col+1)*192, (row+1)*208))
                cell = cell.resize((96,104), Image.Resampling.NEAREST)
                sheet.paste(cell, (128 + col*96, y), cell)
        sheet.save(folder / f'contact-sheet{suffix}.png')
    movie = []
    for tick in range(152):
        page = Image.new('RGB', (624,758), '#17191f')
        draw = ImageDraw.Draw(page)
        for state in META['states']:
            row = state['row']; timings = state['durationsMs']
            phase = tick*50 % sum(timings); col = 0
            while phase >= timings[col]:
                phase -= timings[col]; col += 1
            x = 8 + row%3*208; y = 14 + row//3*250
            draw.text((x+8,y),state['name'],fill='#eeeeee',font=font)
            cell = atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
            page.paste(cell,(x,y+28),cell)
        movie.append(page)
    movie[0].save(folder/'preview.gif',save_all=True,append_images=movie[1:],
                  duration=50,loop=0,optimize=True)


def main():
    frames = {}; rules = []
    with zipfile.ZipFile(BLACK/'source-assets.zip') as archive:
        for state in META['states']:
            name = state['name']; row = state['row']; frames[name] = []
            for col in range(state['frames']):
                raw = Image.open(BytesIO(archive.read(f'frames/{name}/{col:02}.png'))).convert('RGBA')
                frame, core, ring = normalize(raw)
                frames[name].append(frame)
                rules.append({'state':name,'frame':col,'outlinePixels':sum(ring.histogram()[1:])*4,
                              'exactOneLogicalPixelRing':True})
    # Derive left from right after normalization to preserve exact reflection.
    frames['running-left'] = [ImageOps.mirror(f) for f in frames['running-right']]
    base_html = (BLACK/'preview.html').read_text(encoding='utf-8')
    for folder, invert, title in ((BLACK,False,'Pixel Dino'),(WHITE,True,'Pixel Dino White')):
        folder.mkdir(parents=True,exist_ok=True)
        atlas = Image.new('RGBA',(1536,1872))
        report_rows = []
        for state in META['states']:
            name = state['name']; row = state['row']; bottoms = []; hashes = []
            frame_dir = ROOT/'.work/frames'/folder.name/name
            frame_dir.mkdir(parents=True,exist_ok=True)
            for col, f in enumerate(frames[name]):
                if invert: f = inverse_palette(f)
                f.save(frame_dir/f'{col:02}.png')
                atlas.alpha_composite(f,(col*192,row*208))
                bounds = f.getbbox(); assert bounds and min(bounds[0],bounds[1],192-bounds[2],208-bounds[3]) >= 6
                assert f.resize((96,104),Image.Resampling.NEAREST).resize(SIZE,Image.Resampling.NEAREST).tobytes() == f.tobytes()
                bottoms.append(bounds[3]); hashes.append(hashlib.sha256(f.tobytes()).hexdigest())
            assert len(set(hashes)) > 1
            report_rows.append({'state':name,'frames':state['frames'],'distinctFrames':len(set(hashes)),'bottoms':bottoms})
        palette = set(atlas.get_flattened_data())
        assert palette == {(0,0,0,0),(0,0,0,255),(255,255,255,255)}
        atlas.save(folder/'spritesheet.png')
        atlas.save(folder/'spritesheet.webp',lossless=True,exact=True)
        assert Image.open(folder/'spritesheet.webp').convert('RGBA').tobytes() == atlas.tobytes()
        atlas.crop((0,0,192,208)).save(folder/'dinosaur.png')
        (folder/'animations.json').write_text(json.dumps(META,indent=2)+'\n')
        description = f'A {"white" if invert else "black"} pixel dinosaur with a uniform two-pixel {"black" if invert else "white"} outline and a desktop computer for task states.'
        pet = {'id':folder.name,'displayName':title,'description':description,'spriteVersionNumber':1,'spritesheetPath':'spritesheet.webp'}
        (folder/'pet.json').write_text(json.dumps(pet,indent=2)+'\n')
        if invert:
            html = base_html.replace('Pixel Dino','Pixel Dino White').replace('white outline','black outline')
            (folder/'preview.html').write_text(html,encoding='utf-8')
        render_previews(folder,atlas,title)
        jump = next(r for r in report_rows if r['state']=='jumping')
        lift = max(jump['bottoms'])-min(jump['bottoms'])
        assert lift >= 20 and abs(jump['bottoms'][0]-jump['bottoms'][-1]) <= 4
        report = {'ok':True,'atlasSha256':hashlib.sha256((folder/'spritesheet.webp').read_bytes()).hexdigest(),
                  'pixelGrid':2,'outlineWidthPixels':2,'outlineMetric':'one logical pixel, square/Chebyshev dilation',
                  'allTwoByTwoPixelBlocksUniform':True,'alphaValues':[0,255],
                  'palette':'transparent, opaque black, opaque white','pngWebpPixelsIdentical':True,
                  'jumpLiftPixels':lift,'rows':report_rows,'outlineChecks':rules}
        (folder/'quality-checks.json').write_text(json.dumps(report,indent=2)+'\n')
        print(folder.name, '57 frames; exact 2px grid and outline; jump lift:',lift)


if __name__ == '__main__':
    main()
