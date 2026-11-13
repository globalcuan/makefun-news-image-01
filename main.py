"""Draw a compact illustrated front page for the news of 13 November 2026.
The picture uses fixed vector strokes and flat colours, then writes one PNG.
"""

import os
import struct
import math
import zlib


WIDTH, HEIGHT = 1024, 768
BG = (18, 28, 48)
PANEL = (30, 44, 70)

# The strokes use a 3-by-5 coordinate grid; each glyph is a list of polylines.
GLYPHS = {
'A':[[(0,5),(1.5,0),(3,5)],[(.6,3.4),(2.4,3.4)]], 'B':[[(0,0),(0,5)],[(0,0),(2,0),(3,1),(2,2),(0,2)],[(0,2),(2.2,2),(3,3.2),(2,5),(0,5)]],
'C':[[(3,1),(1.5,0),(0,1),(0,4),(1.5,5),(3,4)]], 'D':[[(0,0),(0,5)],[(0,0),(2,0),(3,1.5),(3,3.5),(2,5),(0,5)]],
'E':[[(3,0),(0,0),(0,5),(3,5)],[(0,2.5),(2,2.5)]], 'F':[[(3,0),(0,0),(0,5)],[(0,2.5),(2,2.5)]],
'G':[[(3,1),(1.5,0),(0,1),(0,4),(1.5,5),(3,4),(3,2.8),(1.8,2.8)]], 'H':[[(0,0),(0,5)],[(3,0),(3,5)],[(0,2.5),(3,2.5)]],
'I':[[(1.5,0),(1.5,5)],[(.5,0),(2.5,0)],[(.5,5),(2.5,5)]], 'J':[[(3,0),(3,4),(2,5),(.8,5),(0,4)]],
'K':[[(0,0),(0,5)],[(3,0),(0,2.5),(3,5)]], 'L':[[(0,0),(0,5),(3,5)]], 'M':[[(0,5),(0,0),(1.5,2.2),(3,0),(3,5)]],
'N':[[(0,5),(0,0),(3,5),(3,0)]], 'O':[[(0,1),(1,0),(2,0),(3,1),(3,4),(2,5),(1,5),(0,4),(0,1)]],
'P':[[(0,5),(0,0),(2.4,0),(3,.8),(3,1.8),(2.4,2.5),(0,2.5)]], 'Q':[[(0,1),(1,0),(2,0),(3,1),(3,4),(2,5),(1,5),(0,4),(0,1)],[(2,3.6),(3.2,5)]],
'R':[[(0,5),(0,0),(2.4,0),(3,.8),(3,1.8),(2.4,2.5),(0,2.5)],[(1.6,2.5),(3,5)]], 'S':[[(3,.8),(1.8,0),(.6,.6),(0,1.6),(.8,2.4),(2.2,3),(3,3.8),(2.2,5),(.4,4.8),(0,4)]],
'T':[[(0,0),(3,0)],[(1.5,0),(1.5,5)]], 'U':[[(0,0),(0,4),(1,5),(2,5),(3,4),(3,0)]], 'V':[[(0,0),(1.5,5),(3,0)]],
'W':[[(0,0),(.7,5),(1.5,2.6),(2.3,5),(3,0)]], 'X':[[(0,0),(3,5)],[(3,0),(0,5)]], 'Y':[[(0,0),(1.5,2.2),(3,0)],[(1.5,2.2),(1.5,5)]], 'Z':[[(0,0),(3,0),(0,5),(3,5)]],
'0':[[(0,1),(1,0),(2,0),(3,1),(3,4),(2,5),(1,5),(0,4),(0,1)],[(.6,4),(2.4,1)]], '1':[[(.6,1),(1.5,0),(1.5,5)],[(.5,5),(2.5,5)]],
'2':[[(0,1),(1,0),(2.4,0),(3,1),(3,2),(0,5),(3,5)]], '3':[[(0,.6),(1.6,0),(3,.8),(2.2,2.2),(3,3.2),(2.4,5),(.6,5),(0,4.2)],[(.8,2.5),(2.2,2.5)]],
'4':[[(2.2,5),(2.2,0),(0,3.4),(3,3.4)]], '5':[[(3,0),(.4,0),(.2,2.2),(2,2),(3,3),(2.4,5),(.4,5),(0,4)]],
'6':[[(2.6,.6),(1.2,.2),(.4,1),(0,3),(.8,4.8),(2,5),(3,4.2),(2.8,2.8),(1.6,2.2),(.2,2.8)]], '7':[[(0,0),(3,0),(1.4,5)]],
'8':[[(.8,2.5),(.2,1.6),(.6,.4),(1.5,0),(2.4,.4),(2.8,1.6),(2.2,2.5),(.8,2.5)],[(.8,2.5),(.2,3.6),(.8,4.8),(2.2,4.8),(2.8,3.6),(2.2,2.5)]],
'9':[[(.4,4.4),(1.8,4.8),(2.6,4),(3,2),(2.2,.2),(1,0),(0,.8),(.2,2.2),(1.4,2.8),(2.8,2.2)]], '.':[[(1.4,4.7),(1.6,4.7)]], ',':[[(1.6,4.4),(1.2,5.2)]], '-':[[(.4,2.5),(2.6,2.5)]],
'$':[[(2.6,.6),(1.6,0),(.4,.4),(.2,1.4),(1,2.2),(2.2,2.8),(2.8,3.8),(2.2,5),(.6,4.9),(.2,4)],[(1.5,0),(1.5,5)]], ' ' : []}

pixels = bytearray(BG * (WIDTH * HEIGHT))

def put(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        i = (y * WIDTH + x) * 3
        pixels[i:i+3] = bytes(color)

def disc(cx, cy, radius, color):
    r = int(radius + 1)
    for y in range(max(0, int(cy)-r), min(HEIGHT, int(cy)+r+1)):
        for x in range(max(0, int(cx)-r), min(WIDTH, int(cx)+r+1)):
            if (x-cx)**2 + (y-cy)**2 <= radius**2: put(x,y,color)

def line(x1,y1,x2,y2,color,width=1):
    steps = max(1, int(max(abs(x2-x1),abs(y2-y1))*1.5))
    for k in range(steps+1):
        t=k/steps; disc(x1+(x2-x1)*t,y1+(y2-y1)*t,width/2,color)

def poly(points,color):
    # Scanline fill, with boundaries included.
    ymin=max(0,int(min(y for _,y in points))); ymax=min(HEIGHT-1,int(max(y for _,y in points)))
    for y in range(ymin,ymax+1):
        xs=[]
        for (x1,y1),(x2,y2) in zip(points,points[1:]+points[:1]):
            if (y1 <= y < y2) or (y2 <= y < y1): xs.append(x1+(y-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for a,b in zip(xs[::2],xs[1::2]):
            for x in range(max(0,int(a)),min(WIDTH,int(b)+1)): put(x,y,color)

def rect(x,y,w,h,color):
    for yy in range(max(0,y),min(HEIGHT,y+h)):
        start=(yy*WIDTH+max(0,x))*3; end=(yy*WIDTH+min(WIDTH,x+w))*3
        if end>start: pixels[start:end]=bytes(color)*((end-start)//3)

def rounded_rect(x,y,w,h,r,color):
    rect(x+r,y,w-2*r,h,color); rect(x,y+r,w,h-2*r,color)
    for cx,cy in ((x+r,y+r),(x+w-r-1,y+r),(x+r,y+h-r-1),(x+w-r-1,y+h-r-1)): disc(cx,cy,r,color)

def text_width(s,scale,spacing): return max(0, len(s)*(3*scale+spacing)-spacing)
def draw_text(s,x,y,scale,color,spacing=None,stroke=None):
    spacing=scale if spacing is None else spacing; stroke= max(1,scale*.2) if stroke is None else stroke
    for ch in s:
        for points in GLYPHS.get(ch,[]):
            coords=[(x+a*scale,y+b*scale) for a,b in points]
            for p,q in zip(coords,coords[1:]): line(*p,*q,color,stroke)
        x += 3*scale+spacing

def centered(s,cx,y,scale,color,spacing=None):
    sp=scale if spacing is None else spacing; draw_text(s,cx-text_width(s,scale,sp)/2,y,scale,color,sp)

# Step 1: compose the newspaper masthead, four illustrated stories, and ticker.
rect(0,0,WIDTH,150,(177,42,50))
centered('THE WORLD IN ONE DAY',512,20,14,(255,255,255),7)
centered('FRIDAY 13 NOVEMBER 2026',512,105,6,(236,226,218),4)
boxes=[(36,172),(524,172),(36,438),(524,438)]
for x,y in boxes: rounded_rect(x,y,464,246,22,PANEL)

# Chip icon and pins.
cx,cy=268,243; rounded_rect(cx-50,cy-44,100,88,13,(50,160,111))
for k in range(6):
    d=-38+k*15
    line(cx+d,cy-56,cx+d,cy-43,(115,220,163),5); line(cx+d,cy+43,cx+d,cy+56,(115,220,163),5)
    line(cx-62,cy+d*1.0,cx-49,cy+d*1.0,(115,220,163),5) if abs(d)<40 else None
    line(cx+49,cy+d,cx+62,cy+d,(115,220,163),5) if abs(d)<40 else None
rounded_rect(cx-27,cy-24,54,48,5,(219,166,61));
for d in (-12,0,12): line(cx+d,cy-17,cx+d,cy+17,(247,207,101),2)

# Tanker, waves, and red impact burst.
sx,sy=756,241
poly([(sx-110,sy-19),(sx+52,sy-19),(sx+91,sy+1),(sx+66,sy+25),(sx-84,sy+25),(sx-105,sy+9)],(156,168,181))
rect(sx-43,sy-43,72,24,(189,198,205)); rect(sx-24,sy-58,38,15,(210,215,218)); rect(sx-20,sy-68,7,10,(207,82,66))
for xx in range(sx-110,sx+111,37): line(xx,sy+38,xx+27,sy+38,(56,136,191),4)
for i in range(12):
    a=i*math.pi/6; line(sx+104,sy-26,sx+104+math.cos(a)*25,sy-26+math.sin(a)*25,(224,67,57),5)

# Dove with branch and two flags.
fx,fy=122,474
rect(fx,fy,46,54,(230,205,55)); rect(fx,fy,23,54,(47,102,194));
rect(fx+46,fy,74,54,(191,219,237))
# Bird silhouette with wing/tail/head and olive twig.
poly([(fx+64,fy+81),(fx+88,fy+63),(fx+111,fy+68),(fx+137,fy+52),(fx+130,fy+75),(fx+154,fy+73),(fx+135,fy+87),(fx+110,fy+91),(fx+87,fy+84)],(246,246,239))
poly([(fx+92,fy+67),(fx+111,fy+35),(fx+118,fy+67),(fx+108,fy+79)],(246,246,239))
disc(fx+133,fy+58,10,(246,246,239)); poly([(fx+141,fy+55),(fx+154,fy+59),(fx+141,fy+63)],(220,174,72))
line(fx+94,fy+89,fx+119,fy+106,(111,160,93),3)
for xx,yy in ((100,95),(108,99),(115,104)): poly([(fx+xx,fy+yy),(fx+xx-7,fy+yy-5),(fx+xx-3,fy+yy+1)],(119,174,94))

# Lima church, cross, and a compact crowd.
qx,qy=756,515
poly([(qx-64,qy+1),(qx,qy-43),(qx+64,qy+1)],(230,227,216)); rect(qx-64,qy,128,58,(230,227,216))
rect(qx-6,qy-60,12,30,(230,227,216)); rect(qx-17,qy-49,34,7,(230,227,216)); rect(qx-3,qy-68,6,22,(230,227,216))
rect(qx-13,qy+25,26,33,(117,133,150));
for xx in (-43,-25,25,43): rect(qx+xx-5,qy+14,10,19,(93,113,135))
for row in range(2):
    for col in range(15):
        px=qx-78+col*11+(row%2)*5; py=qy+65+row*14
        disc(px,py,3,(229,181,131)); rect(px-2,py+3,5,7,(82,132,174))

captions=[('NVIDIA CEO HUANG RESIGNS','KRESS NAMED INTERIM CEO'),('TANKER STRIKES MINE IN','STRAIT OF HORMUZ'),('EUROPE JOINS UKRAINE','PEACE TALKS'),('POPE LEO IN LIMA MEETS','ABUSE SURVIVORS')]
for (x,y),(a,b) in zip(boxes,captions):
    # Caption band begins at y+168; icons stay above it. At scale 4.6,
    # 36-pixel pitch is greater than 1.5 times the 23-pixel glyph height.
    for row,s in enumerate((a,b)):
        scale=4.6; spacing=2.0
        while text_width(s,scale,spacing)>424: scale-=.1
        centered(s,x+232,y+171+row*36,scale,(246,246,242),spacing)

rect(0,706,WIDTH,62,(116,31,40))
ticker='DOJ TO SEIZE $1.2B CRYPTO - SENATE LEADERSHIP CHALLENGE - BROOKLYN TOLL 8'
sp=3.0; scale=4.0
while text_width(ticker,scale,sp)>960: scale-=.1
# The old fitted size was 4px, so its default stroke was 0.8px;
# 1.2px keeps the ticker stroke about 1.5 times as thick.
draw_text(ticker,512-text_width(ticker,scale,sp)/2,706+(62-5*scale)/2,scale,(255,248,243),sp,1.2)

def png_chunk(kind,data):
    body=kind+data
    return struct.pack('>I',len(data))+body+struct.pack('>I',zlib.crc32(body)&0xffffffff)

def save_png(path):
    raw=b''.join(b'\0'+pixels[y*WIDTH*3:(y+1)*WIDTH*3] for y in range(HEIGHT))
    png=b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',struct.pack('>2I5B',WIDTH,HEIGHT,8,2,0,0,0))+png_chunk(b'IDAT',zlib.compress(raw,9))+png_chunk(b'IEND',b'')
    with open(path,'wb') as f: f.write(png)

def main():
    outdir=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
    os.makedirs(outdir,exist_ok=True)
    save_png(os.path.join(outdir,'entry.png'))

if __name__=='__main__': main()
