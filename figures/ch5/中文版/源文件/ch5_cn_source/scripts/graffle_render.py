# -*- coding: utf-8 -*-
"""通用 OmniGraffle(.graffle) 画布 -> matplotlib 渲染器：按原图形坐标重建，文字替换为中文。"""
import plistlib, re, matplotlib.pyplot as plt, cnstyle
from matplotlib.patches import Rectangle, Ellipse, FancyArrowPatch

from striprtf.striprtf import rtf_to_text
def rtf2txt(t):
    raw=(t or {}).get('Text','') or ''
    if not raw: return ''
    try: return rtf_to_text(raw).strip()
    except Exception: return ''


def bounds(b):
    m=re.findall(r'-?\d+\.?\d*', b); return [float(x) for x in m[:4]]
def pts(g):
    return [tuple(map(float, re.findall(r'-?\d+\.?\d*', p)[:2])) for p in g.get('Points',[])]
def col(c):
    if not c: return None
    return (c['r'],c['g'],c['b'])

def flatten(gl):
    out=[]
    for g in gl:
        if g.get('Class')=='Group': out+=flatten(g.get('GraphicsList',[]))
        else: out.append(g)
    return out

def render(canvas_idx, D, outname, figsize, fs=9, extra=None, skip_images=False):
    d=plistlib.load(open('graffle/data.plist','rb'))
    gl=flatten(d['Sheets'][canvas_idx]['GraphicsList'])
    xs=[];ys=[]
    for g in gl:
        if g.get('Bounds'):
            x,y,w,h=bounds(g['Bounds']); xs+=[x,x+w]; ys+=[y,y+h]
        for p in pts(g): xs.append(p[0]); ys.append(p[1])
    minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
    fig,ax=plt.subplots(figsize=figsize,dpi=200)
    # draw lines first
    for g in gl:
        if g.get('Class')=='LineGraphic':
            p=pts(g)
            if len(p)>=2:
                st=g.get('Style',{}).get('stroke',{})
                arrow='-|>' if st.get('HeadArrow','0')!='0' and st.get('HeadArrow') else '-'
                for i in range(len(p)-1):
                    a=FancyArrowPatch(p[i],p[i+1],arrowstyle=arrow if i==len(p)-2 else '-',
                                      mutation_scale=8,lw=max(st.get('Width',0.5),0.6),color='#333')
                    ax.add_patch(a)
    # draw shapes
    for g in gl:
        if g.get('Class')!='ShapedGraphic' or not g.get('Bounds'): continue
        if skip_images and g.get('ImageID'): continue
        x,y,w,h=bounds(g['Bounds']); style=g.get('Style',{})
        fc=col((style.get('fill') or {}).get('Color'))
        has_fill=(style.get('fill') or {}).get('Draws','YES')!='NO' and fc is not None
        stroke=style.get('stroke') or {}
        has_stroke=stroke.get('Draws','YES')!='NO'
        ec='#222' if has_stroke else 'none'
        shp=g.get('Shape')
        if shp=='Circle':
            ax.add_patch(Ellipse((x+w/2,y+h/2),w,h,facecolor=(fc if has_fill else 'white'),edgecolor=ec,lw=0.8))
        else:
            dash=(0,(4,3)) if str(stroke.get('Pattern',''))=='1' else 'solid'
            ax.add_patch(Rectangle((x,y),w,h,facecolor=(fc if has_fill else 'none'),
                         edgecolor=ec,lw=0.9,linestyle=dash))
        txt=rtf2txt(g.get('Text',{}))
        key=re.sub(r'\s+',' ',txt).strip()
        cn=D.get(key, txt)
        if cn:
            tc='white' if (has_fill and fc and sum(fc)<1.2) else 'black'
            ax.text(x+w/2,y+h/2,cn.replace('\\n','\n'),ha='center',va='center',
                    fontsize=fs,color=tc,wrap=True)
    if extra: extra(ax)
    ax.set_xlim(minx-10,maxx+10); ax.set_ylim(maxy+10,miny-10)  # invert y
    ax.axis('off'); ax.set_aspect('equal')
    fig.savefig(f'out/{outname}.pdf',bbox_inches='tight')
    fig.savefig(f'out/{outname}.png',dpi=140,bbox_inches='tight')
    print('saved',outname)
