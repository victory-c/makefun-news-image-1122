# SPDX-License-Identifier: MIT
"""Original geometric editorial illustrations, not documentary photographs."""
import math
from raster import INK, PAPER

RED = '#bd4c32'
TEAL = '#467e79'
GOLD = '#c99740'
MUTED = '#cbd7ce'


def miniature(c, draw, x, y, scale=.72):
    """Scale code-drawn icons to stay clear of adjacent text."""
    class Local:
        def rect(self,a,b,w,h,color):
            c.rect(x+a*scale,y+b*scale,w*scale,h*scale,color)
        def polygon(self,points,color):
            c.polygon([(x+a*scale,y+b*scale) for a,b in points],color)
        def line(self,points,color,width=1):
            c.line([(x+a*scale,y+b*scale) for a,b in points],color,width*scale)
        def ellipse(self,a,b,rx,ry,color,width=0):
            c.ellipse(x+a*scale,y+b*scale,rx*scale,ry*scale,color,width*scale)
    draw(Local(),0,0)


def globe(c, x, y, r):
    c.ellipse(x,y,r,r,TEAL)
    for f in [.35,.7]:
        c.ellipse(x,y,r*f,r,'#8eb2a1',1)
    for f in [-.5,0,.5]:
        ry = r*math.sqrt(1-f*f)
        c.line([(x-ry,y+r*f),(x+ry,y+r*f)],'#8eb2a1',1)
    # Deliberately abstract landforms: illustration, not a geographic map.
    for points in [[(-.7,-.5),(-.3,-.65),(-.1,-.3),(-.4,-.05),(-.6,-.2)], [(-.35,.05),(-.05,.1),(.1,.35),(-.15,.8),(-.3,.45)],[(.15,-.6),(.65,-.45),(.8,-.15),(.5,.05),(.25,-.1),(.05,-.3)],[(.45,.4),(.7,.5),(.65,.7),(.4,.65)]]:
        c.polygon([(x+a*r,y+b*r) for a,b in points],MUTED)


def treaty(c,x,y):
    c.polygon([(x,y),(x+90,y),(x+104,y+14),(x+104,y+124),(x,y+124)],PAPER)
    c.line([(x,y),(x+90,y),(x+104,y+14),(x+104,y+124),(x,y+124),(x,y)],INK,2)
    for dy in [35,47,59,90,102]:
        c.rect(x+15,y+dy,73,2,'#aebbb2')
    c.polygon([(x+55,y-3),(x+43,y+34),(x+63,y+55),(x+42,y+86),(x+52,y+127),(x+65,y+127),(x+57,y+88),(x+78,y+57),(x+57,y+32),(x+68,y-3)],RED)


def ship(c,x,y,s: float=1):
    def poly(pts,col):c.polygon([(x+a*s,y+b*s) for a,b in pts],col)
    poly([(0,36),(88,36),(72,58),(14,58)],INK)
    poly([(23,20),(60,20),(65,36),(18,36)],TEAL)
    c.line([(x+46*s,y+20*s),(x+46*s,y-3*s)],INK,2)
    c.line([(x+46*s,y+3*s),(x+69*s,y+3*s)],INK,2)
    poly([(61,23),(67,4),(72,18),(83,-5),(85,29)],RED)
    for dy in [65,74]:
        c.line([(x,y+dy*s),(x+19*s,y+(dy-3)*s),(x+38*s,y+dy*s),(x+57*s,y+(dy-3)*s),(x+87*s,y+dy*s)],TEAL,2)


def chip(c,x,y):
    c.rect(x+12,y+12,57,57,INK)
    c.rect(x+18,y+18,45,45,PAPER)
    for a in [24,40,56]:
        for b in [0,70]:
            c.rect(x+a,y+b,2,12,INK)
            c.rect(x+b,y+a,12,2,INK)
    c.text(x+40,y+24,'AI',21,'bold',TEAL,'center')
    c.line([(x+65,y+64),(x+89,y+88)],RED,7)


def storm(c,x,y):
    for xx,yy,r in [(22,20,17),(43,12,23),(65,24,19)]:
        c.ellipse(x+xx,y+yy,r,r,TEAL)
    c.rect(x+12,y+23,63,18,TEAL)
    c.polygon([(x+44,y+37),(x+29,y+61),(x+43,y+61),(x+36,y+80),(x+64,y+48),(x+48,y+48),(x+57,y+37)],GOLD)
    for xx in [12,72]:c.line([(x+xx,y+49),(x+xx-6,y+62)],TEAL,2)


def factory(c,x,y):
    c.polygon([(x,y+55),(x,y+24),(x+21,y+13),(x+21,y+24),(x+44,y+13),(x+44,y+24),(x+66,y+13),(x+66,y+55)],TEAL)
    for xx in [9,30,51]:c.rect(x+xx,y+35,8,9,PAPER)
    c.rect(x+70,y+2,5,60,INK)
    c.rect(x+58,y-4,32,23,RED)
    c.line([(x+63,y+4),(x+84,y+4)],PAPER,2)
    c.line([(x+63,y+11),(x+79,y+11)],PAPER,2)


def homes(c,x,y):
    for xx in [0,45]:
        c.polygon([(x+xx,y+31),(x+xx+17,y+14),(x+xx+34,y+31)],INK)
        c.rect(x+xx+4,y+31,26,27,TEAL)
        c.rect(x+xx+14,y+44,7,14,PAPER)
    c.polygon([(x+23,y+33),(x+28,y+11),(x+38,y+22),(x+43,y),(x+53,y+34)],RED)


def court(c,x,y):
    c.rect(x,y,94,55,TEAL)
    c.line([(x+7,y+5),(x+87,y+5),(x+87,y+50),(x+7,y+50),(x+7,y+5)],PAPER,1)
    c.line([(x+24,y+5),(x+24,y+50)],PAPER,1)
    c.line([(x+70,y+5),(x+70,y+50)],PAPER,1)
    c.line([(x+24,y+27),(x+70,y+27)],PAPER,1)
    c.line([(x+47,y),(x+47,y+55)],PAPER,2)
    c.ellipse(x+72,y+14,5,5,GOLD)
