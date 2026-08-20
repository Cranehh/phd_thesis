# 把 framework/backbone/energy 导出为“可编辑 SVG”：去掉原图英文后转 SVG(矢量框/箭头/配色)，
# 再把中文作为可编辑 <text> 写入。可在 Illustrator / Inkscape / 浏览器 / PPT 里直接改文字和位置。
import fitz, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from diagram_build import FW_R, FW_L, FW_EX, BB_R, EN_R, CH3
OUT=os.environ.get("OUTDIR","/tmp/ch3work/中文版")
FONT="SimSun, 'Noto Serif CJK SC', serif"
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def allspans(p):
    return [s["bbox"] for b in p.get_text("dict")["blocks"] for l in b.get("lines",[]) for s in l["spans"] if s["text"].strip()]
def make(src,out,R,L=[],EX=[]):
    d=fitz.open(src); p=d[0]; sp=allspans(p)
    def snap(r):
        x0,y0,x1,y1=r; c=[b for b in sp if x0<=(b[0]+b[2])/2<=x1 and b[1]<y1 and b[3]>y0]
        return (min(b[0] for b in c),min(b[1] for b in c),max(b[2] for b in c),max(b[3] for b in c)) if c else r
    for r in R: p.add_redact_annot(fitz.Rect(*[v+dv for v,dv in zip(snap(r[:4]),(-1,-1,1,1))]),fill=None,cross_out=False)
    for r in L: p.add_redact_annot(fitz.Rect(*[v+dv for v,dv in zip(snap(r[:4]),(-1,-1,1,1))]),fill=None,cross_out=False)
    for r in EX: p.add_redact_annot(fitz.Rect(*r),fill=None,cross_out=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    svg=p.get_svg_image(text_as_path=False)
    T=[]
    for (x0,y0,x1,y1,zh,size,bold) in R:
        cx=(x0+x1)/2; cy=(y0+y1)/2; fw=' font-weight="bold"' if bold else ''
        T.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="{FONT}" font-size="{size}" text-anchor="middle" dominant-baseline="central" fill="#000"{fw}>{esc(zh)}</text>')
    for (x0,y0,x1,y1,items,size) in L:
        step=(y1-y0)/len(items)
        for i,it in enumerate(items):
            cy=y0+step*(i+0.5)
            T.append(f'<text x="{x0:.1f}" y="{cy:.1f}" font-family="{FONT}" font-size="{size}" text-anchor="start" dominant-baseline="central" fill="#000">{esc(it)}</text>')
    svg=svg.replace("</svg>", "\n"+"\n".join(T)+"\n</svg>")
    open(out,"w",encoding="utf-8").write(svg); print("saved",os.path.basename(out),round(len(svg)/1024,1),"KB")
if __name__=="__main__":
    make(f"{CH3}/framework.pdf",f"{OUT}/framework_cn.svg",FW_R,FW_L,FW_EX)
    make(f"{CH3}/backbone.pdf", f"{OUT}/backbone_cn.svg", BB_R)
    make(f"{CH3}/energy.pdf",   f"{OUT}/energy_cn.svg",   EN_R)
