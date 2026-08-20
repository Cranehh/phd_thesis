# 通用示意图翻译引擎：抽取原PDF英文文字→按词典替换为中文→matplotlib(Type3)叠加到矢量底图
# 用法见文件底部 build_one()。保留原图所有框/箭头/配色，只把文字换成中文（宋体）。
import fitz, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import figstyle
import matplotlib.pyplot as plt

def norm(t): return re.sub(r"\s+"," ",t).strip()

def group_spans(page):
    S=[]
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines",[]):
            for s in l["spans"]:
                if s["text"].strip():
                    S.append(dict(t=s["text"],x0=s["bbox"][0],y0=s["bbox"][1],x1=s["bbox"][2],y1=s["bbox"][3],
                                  sz=s["size"],bold=("Bold" in s["font"])))
    n=len(S); par=list(range(n))
    def f(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    def u(a,b): par[f(a)]=f(b)
    for i in range(n):
        for j in range(i+1,n):
            a,b=S[i],S[j]
            if abs(a["sz"]-b["sz"])>2.2: continue
            ox=min(a["x1"],b["x1"])-max(a["x0"],b["x0"])
            minw=min(a["x1"]-a["x0"],b["x1"]-b["x0"])
            # vertical stack
            top,bot=(a,b) if a["y0"]<=b["y0"] else (b,a)
            vgap=bot["y0"]-top["y1"]
            if ox>minw*0.30 and -2<=vgap<=6: u(i,j); continue
            # same line
            if abs(a["y0"]-b["y0"])<=2.5:
                l,r=(a,b) if a["x0"]<=b["x0"] else (b,a)
                if 0<=(r["x0"]-l["x1"])<=13: u(i,j)
    groups={}
    for i in range(n): groups.setdefault(f(i),[]).append(S[i])
    out=[]
    for g in groups.values():
        g.sort(key=lambda s:(round(s["y0"]/3),s["x0"]))
        txt=norm(" ".join(s["t"] for s in g))
        out.append(dict(text=txt,x0=min(s["x0"] for s in g),y0=min(s["y0"] for s in g),
                        x1=max(s["x1"] for s in g),y1=max(s["y1"] for s in g),
                        sz=max(s["sz"] for s in g),bold=any(s["bold"] for s in g)))
    return out

def estw(t,s): return sum(s*(0.55 if ord(c)<128 else 1.0) for c in t)

def build_one(src,out,DICT,pad=1.0):
    d=fitz.open(src); p=d[0]; W,H=p.rect.width,p.rect.height
    groups=group_spans(p)
    place=[]; leftover=[]
    for g in groups:
        key=norm(g["text"])
        if key in DICT:
            zh=DICT[key]
            if zh is None: continue
            p.add_redact_annot(fitz.Rect(g["x0"]-pad,g["y0"]-pad,g["x1"]+pad,g["y1"]+pad),fill=None,cross_out=False)
            place.append((g["x0"],g["y0"],g["x1"],g["y1"],zh,g["sz"],g["bold"]))
        elif re.search(r"[A-Za-z]",key):
            leftover.append(key)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    bg=out+".bg.pdf"; d.save(bg,garbage=4,deflate=True,clean=True)
    fig=plt.figure(figsize=(W/72,H/72)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis('off')
    for (x0,y0,x1,y1,zh,sz,bold) in place:
        s=sz; boxw=(x1-x0)
        while s>4.5 and estw(zh,s)>boxw*1.02: s-=0.3
        ax.text((x0+x1)/2,(y0+y1)/2,zh,ha='center',va='center',
                fontproperties=(figstyle.propB if bold else figstyle.propR),fontsize=s,color='black')
    txt=out+".txt.pdf"; fig.savefig(txt,transparent=True); plt.close(fig)
    b=fitz.open(bg); t=fitz.open(txt); b[0].show_pdf_page(b[0].rect,t,0); b.save(out,garbage=4,deflate=True,clean=True)
    os.remove(bg); os.remove(txt)
    return leftover
