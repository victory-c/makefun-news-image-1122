# SPDX-License-Identifier: MIT
"""Offline acceptance tests. Run with python3 -S tests.py (no third-party packages)."""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time
import unittest
import zlib
from main import render

ROOT = Path(__file__).resolve().parent


def inspect_png(data):
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    offset, payload, names = 8, bytearray(), []
    while offset < len(data):
        size = struct.unpack('>I',data[offset:offset+4])[0]
        name = data[offset+4:offset+8]
        content = data[offset+8:offset+8+size]
        crc = struct.unpack('>I',data[offset+8+size:offset+12+size])[0]
        assert crc == zlib.crc32(name+content)&0xffffffff
        names.append(name)
        if name == b'IHDR':
            assert struct.unpack('>IIBBBBB',content) == (1024,1024,8,2,0,0,0)
        if name == b'IDAT':
            payload.extend(content)
        if name == b'IEND':
            assert size == 0
        offset += size+12
    assert offset == len(data)
    assert names[0] == b'IHDR' and names[-1] == b'IEND'
    raw = zlib.decompress(payload)
    assert len(raw) == 1024*(1+1024*3)
    assert all(raw[y*(1+1024*3)] == 0 for y in range(1024))
    return raw


class Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start = time.perf_counter()
        cls.canvas = render()
        cls.png = cls.canvas.png()
        cls.seconds = time.perf_counter()-start

    def test_whole_image_and_limits(self):
        inspect_png(self.png)
        self.assertLessEqual(len(self.png),1048576)
        self.assertLess(self.seconds,60)

    def test_text_inside_page(self):
        for x,y,w,h,text in self.canvas.boxes:
            with self.subTest(text=text):
                self.assertGreaterEqual(x,0)
                self.assertGreaterEqual(y,0)
                self.assertLessEqual(x+w,1024)
                self.assertLessEqual(y+h,1024)

    def test_no_text_collisions(self):
        boxes = self.canvas.boxes
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                dx = min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])
                dy = min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1])
                self.assertFalse(dx > 1 and dy > 1, f'{a[4]} overlaps {b[4]}')

    def test_date_breadth_and_content(self):
        text = ' '.join(b[4] for b in self.canvas.boxes)
        for token in ['22','NOVEMBER 2026','COP31','Merkury','Choi Kyo-jin','Tupanciretã','Gazipur','Eisenkot','Alcaraz']:
            self.assertIn(token,text)
        for number in range(1,7):
            self.assertTrue(any(b[4] == f'{number:02}' for b in self.canvas.boxes))
        self.assertIn('07 / TURIN',text)
        self.assertIn('Friday’s storm',text)
        self.assertIn('no claim of responsibility',text)
        self.assertIn('Other decisions pass',text)

    def test_deterministic_clean_processes(self):
        with tempfile.TemporaryDirectory(prefix='atlas-') as tmp:
            paths = [Path(tmp)/'one',Path(tmp)/'two']
            for i,path in enumerate(paths):
                env = dict(os.environ,MAKEFUN_OUTPUT_DIR=str(path),PYTHONHASHSEED=str(i*123+7),TZ=['UTC','Pacific/Honolulu'][i])
                env.pop('ATLAS_DEBUG',None)
                subprocess.run([sys.executable,'-S',str(ROOT/'main.py')],env=env,cwd=tmp,check=True,timeout=60,capture_output=True)
                self.assertEqual([p.name for p in path.iterdir()],['entry.png'])
            self.assertEqual(paths[0].joinpath('entry.png').read_bytes(),self.png)
            self.assertEqual(paths[1].joinpath('entry.png').read_bytes(),self.png)

    def test_reference_image(self):
        reference = ROOT/'entry.png'
        if reference.exists():
            self.assertEqual(reference.read_bytes(),self.png)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Acceptance)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(json.dumps({'bytes':len(Acceptance.png),'sha256':hashlib.sha256(Acceptance.png).hexdigest(),'render_seconds':round(Acceptance.seconds,3),'text_runs':len(Acceptance.canvas.boxes)},sort_keys=True))
    sys.exit(not result.wasSuccessful())
