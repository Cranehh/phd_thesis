import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTCurve, LTLine, LTChar
import numpy as np

def extract(pdf):
    chars=[]; curves=[]
    for page in extract_pages(pdf):
        stack=list(page)
        while stack:
            el=stack.pop()
            if isinstance(el,LTChar):
                t=el.get_text()
                if t.strip(): chars.append([el.x0,el.y0,el.x1,el.y1,t])
            elif isinstance(el,(LTCurve,LTLine)):
                pts=getattr(el,'pts',None)
                if pts and len(pts)>=20:
                    col=getattr(el,'stroking_color',None)
                    curves.append((list(pts),col))
            if hasattr(el,'_objs'): stack.extend(el._objs)
    return chars,curves

def words(chars):
    # group chars into words by row (y baseline) then contiguous x
    chars=sorted(chars,key=lambda c:(-round(c[1],0),c[0]))
    ws=[]; cur=[]
    for c in chars:
        if not cur: cur=[c]; continue
        prev=cur[-1]
        if abs(c[1]-prev[1])<3 and (c[0]-prev[2])<3.5:
            cur.append(c)
        else:
            ws.append(cur); cur=[c]
    if cur: ws.append(cur)
    out=[]
    for w in ws:
        txt=''.join(ch[4] for ch in w)
        x0=min(ch[0] for ch in w); x1=max(ch[2] for ch in w)
        y0=min(ch[1] for ch in w); y1=max(ch[3] for ch in w)
        out.append({'t':txt,'cx':(x0+x1)/2,'cy':(y0+y1)/2,'x0':x0,'y0':y0,'x1':x1,'y1':y1})
    return out

def num(s):
    s=s.replace('%','').replace('−','-')
    try: return float(s)
    except: return None

def calib(words_, plot_xmin, plot_ymin, pct_x=False):
    # y ticks: numeric words left of plot area
    yt=[(w['cy'],num(w['t'])) for w in words_ if w['x1']<plot_xmin-2 and num(w['t']) is not None]
    # x ticks: numeric words below plot area
    xt=[(w['cx'],num(w['t'])) for w in words_ if w['cy']<plot_ymin-2 and num(w['t']) is not None]
    def fit(pairs):
        pairs=sorted(set(pairs))
        P=np.array([p[0] for p in pairs]); D=np.array([p[1] for p in pairs])
        A=np.polyfit(P,D,1)
        return A,pairs
    ax,xp=fit(xt); ay,yp=fit(yt)
    return ax,ay,xp,yp
