# SPDX-License-Identifier: MIT
"""Small deterministic, antialiased RGB compositor, using only Python's stdlib."""
import base64
import json
import math
import pathlib
import struct
import zlib

S = 2
W = H = 1024
INK = '#172f35'
PAPER = '#f4efe4'


def rgb(color):
    return tuple(bytes.fromhex(color.lstrip('#')))


class Canvas:
    def __init__(self, color=PAPER):
        self.width = W * S
        self.height = H * S
        self.pixels = bytearray(bytes(rgb(color)) * (self.width * self.height))
        packed = pathlib.Path(__file__).with_name('assets').joinpath('type.pack')
        self.fonts = json.loads(zlib.decompress(packed.read_bytes()))
        self.boxes = []

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, round(x*S)), max(0, round(y*S))
        x1, y1 = min(self.width, round((x+w)*S)), min(self.height, round((y+h)*S))
        row = bytes(rgb(color)) * max(0, x1-x0)
        for yy in range(y0, y1):
            start = (yy*self.width+x0)*3
            self.pixels[start:start+len(row)] = row

    def polygon(self, points, color):
        points = [(x*S, y*S) for x, y in points]
        for y in range(max(0, math.floor(min(p[1] for p in points))), min(self.height, math.ceil(max(p[1] for p in points)))):
            cuts = []
            for (x1,y1), (x2,y2) in zip(points, points[1:]+points[:1]):
                if min(y1,y2) <= y+.5 < max(y1,y2):
                    cuts.append(x1+(y+.5-y1)*(x2-x1)/(y2-y1))
            cuts.sort()
            for a,b in zip(cuts[::2],cuts[1::2]):
                self.rect(math.ceil(a-.5)/S, y/S, (math.ceil(b-.5)-math.ceil(a-.5))/S, 1/S, color)

    def line(self, points, color, width=1):
        for (x,y),(xx,yy) in zip(points,points[1:]):
            length = math.hypot(xx-x,yy-y)
            if not length:
                continue
            dx,dy = -(yy-y)*width/length/2,(xx-x)*width/length/2
            self.polygon([(x+dx,y+dy),(xx+dx,yy+dy),(xx-dx,yy-dy),(x-dx,y-dy)],color)

    def ellipse(self, x, y, rx, ry, color, width=0):
        n = max(48, round(max(rx,ry)*3))
        points = [(x+rx*math.cos(i*math.tau/n),y+ry*math.sin(i*math.tau/n)) for i in range(n)]
        if width:
            self.line(points+[points[0]],color,width)
        else:
            self.polygon(points,color)

    def measure(self, text, size, family='sans'):
        glyphs = self.fonts[f'{family}:{size}']
        return sum(glyphs[c][0] for c in text)/S

    def text(self, x, y, text, size=16, family='sans', color=INK, align='left'):
        glyphs = self.fonts[f'{family}:{size}']
        width = self.measure(text,size,family)
        if align == 'right':
            x -= width
        elif align == 'center':
            x -= width/2
        self.boxes.append([round(x,2),y,round(width,2),size*1.25,text])
        cr,cg,cb = rgb(color)
        for char in text:
            advance, (ox,oy), (w,h), encoded = glyphs[char]
            mask = base64.b64decode(encoded)
            left, top = round(x*S)+ox, round(y*S)+oy
            for yy in range(h):
                if not 0 <= top+yy < self.height:
                    continue
                for xx in range(w):
                    alpha = mask[yy*w+xx]
                    if alpha and 0 <= left+xx < self.width:
                        at = ((top+yy)*self.width+left+xx)*3
                        inv = 255-alpha
                        self.pixels[at] = (cr*alpha+self.pixels[at]*inv+127)//255
                        self.pixels[at+1] = (cg*alpha+self.pixels[at+1]*inv+127)//255
                        self.pixels[at+2] = (cb*alpha+self.pixels[at+2]*inv+127)//255
            x += advance/S
        return width

    def paragraph(self, x, y, text, width, size=16, leading=23, family='sans', color=INK):
        lines = []
        for word in text.split():
            if not lines or self.measure(lines[-1]+' '+word,size,family) > width:
                lines.append(word)
            else:
                lines[-1] += ' '+word
        for i,line in enumerate(lines):
            self.text(x,y+i*leading,line,size,family,color)
        return y+len(lines)*leading

    def png(self):
        raw = bytearray()
        p, stride = self.pixels, self.width*3
        for y in range(H):
            raw.append(0)
            for x in range(W):
                at = ((y*S)*self.width+x*S)*3
                for c in range(3):
                    raw.append((p[at+c]+p[at+3+c]+p[at+stride+c]+p[at+stride+3+c]+2)//4)
        def chunk(name,data):
            return struct.pack('>I',len(data))+name+data+struct.pack('>I',zlib.crc32(name+data)&0xffffffff)
        return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
