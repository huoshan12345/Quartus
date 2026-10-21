"""Render the saved BDF drawing objects for layout inspection (not Quartus screenshots)."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from build_schematics import parse, TOPS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews'


def child(n,key):
    return next(c for c in n if isinstance(c,list) and c[0]==key)


def render(name):
    nodes=parse((ROOT/(name+'.bdf')).read_text())
    points=[]
    for n in nodes:
        if n[0] in ['symbol','pin']:
            r=list(map(int,child(n,'rect')[1:]));points.append((r[2],r[3]))
        elif n[0]=='connector':
            points += [tuple(map(int,p[1:])) for p in n if isinstance(p,list) and p[0]=='pt']
        elif n[0]=='text':
            r=list(map(int,child(n,'rect')[1:]));points.append((r[2],r[3]))
    w=max(x for x,y in points)+48;h=max(y for x,y in points)+64
    im=Image.new('RGB',(w,h),'white');draw=ImageDraw.Draw(im)

    def shape(n,ox=0,oy=0):
        tag=n[0]
        if tag=='text':
            if any(c==['invisible'] for c in n):
                return
            x,y,*_=map(int,child(n,'rect')[1:])
            font=child(n,'font');size=8
            for c in font:
                if isinstance(c,list) and c[0]=='font_size':
                    size=int(c[1])
            path='C:/Windows/Fonts/arial.ttf' if size<12 else 'C:/Windows/Fonts/arialbd.ttf'
            f=ImageFont.truetype(path,max(8,round(size*1.3)))
            draw.text((ox+x,oy+y),json.loads(n[1]),fill='#222222',font=f)
        elif tag=='line':
            pts=[(ox+int(c[1]),oy+int(c[2])) for c in n if isinstance(c,list) and c[0]=='pt']
            draw.line(pts,fill='#111111',width=1)
        elif tag in ['circle','rectangle','arc']:
            x0,y0,x1,y1=map(int,child(n,'rect')[1:]);rect=(ox+x0,oy+y0,ox+x1,oy+y1)
            if tag=='circle':draw.ellipse(rect,outline='#111111')
            elif tag=='rectangle':draw.rectangle(rect,outline='#111111')
            else:
                pts=[c for c in n if isinstance(c,list) and c[0]=='pt']
                cx,cy=(x0+x1)/2,(y0+y1)/2;rx,ry=(x1-x0)/2,(y1-y0)/2
                angles=[math.degrees(math.atan2((int(p[2])-cy)/ry,(int(p[1])-cx)/rx)) for p in pts]
                draw.arc(rect,start=angles[1],end=angles[0],fill='#111111')
        elif tag in ['drawing','port']:
            for c in n[1:]:
                if isinstance(c,list):shape(c,ox,oy)

    # Wires are drawn first so symbols and labels remain legible at crossings.
    for n in nodes:
        if n[0]=='connector':
            pts=[tuple(map(int,p[1:])) for p in n if isinstance(p,list) and p[0]=='pt']
            bus=any(p==['bus'] for p in n)
            draw.line(pts,fill='#1b4a88',width=3 if bus else 1)
            for c in n:
                if isinstance(c,list) and c[0]=='text':shape(c)
    for n in nodes:
        if n[0] in ['symbol','pin']:
            r=list(map(int,child(n,'rect')[1:]))
            for c in n:
                if isinstance(c,list):shape(c,r[0],r[1])
        elif n[0]=='text':shape(n)
        elif n[0]=='junction':
            p=child(n,'pt');x,y=map(int,p[1:]);draw.ellipse((x-3,y-3,x+3,y+3),fill='#1b4a88')
    OUT.mkdir(exist_ok=True)
    im.save(OUT/(name+'.png'))
    if name!='priority_control':
        cutoff=1408 if name=='bus16_mux8' else 1520 if name.startswith('counter') else 1056
        im.crop((0,0,w,min(cutoff,h))).save(OUT/(name+'_detail.png'))
    print(name,w,h)


if __name__=='__main__':
    for top in [*TOPS,'priority_control']:
        render(top)
