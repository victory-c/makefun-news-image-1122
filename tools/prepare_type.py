# SPDX-License-Identifier: MIT
"""Development only: bake licensed DejaVu glyph coverage; runtime needs no Pillow."""
import base64
import json
import pathlib
import zlib
from PIL import ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = {
    'serif': 'DejaVuSerif.ttf',
    'display': 'DejaVuSerif-Bold.ttf',
    'sans': 'DejaVuSans.ttf',
    'bold': 'DejaVuSans-Bold.ttf',
}
SIZES = [11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 26, 28, 30, 32, 36, 40, 42, 44, 48, 56, 64, 72]
CHARS = ''.join(chr(c) for c in range(32, 127)) + '’‘“”–—°éã·−'
result = {}
for family, filename in FONTS.items():
    for size in SIZES:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/' + filename, size * 2)
        glyphs = {}
        for char in CHARS:
            mask, offset = font.getmask2(char, mode='L')
            glyphs[char] = [round(font.getlength(char), 4), list(offset), list(mask.size), base64.b64encode(bytes(mask)).decode()]
        result[f'{family}:{size}'] = glyphs
path = ROOT / 'assets' / 'type.pack'
path.parent.mkdir(exist_ok=True)
path.write_bytes(zlib.compress(json.dumps(result, separators=(',', ':')).encode(), 9))
print(f'Baked {len(result)} font instances: {path.stat().st_size} bytes')
