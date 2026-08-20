import pdfcurve as pc, numpy as np, matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
BASE=Path("/Users/haohe/Library/CloudStorage/OneDrive-个人/研究生阶段/2026/2026_06 博士毕业大论文撰写/0.4【】BJTU-Thesis-Latex-main(1)/0.4【】BJTU-Thesis-Latex-main/figures/ch5")
OUT=Path(__file__).resolve().parents[2] / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
PDF_METADATA={'CreationDate':None,'ModDate':None}

def load(name):
    chars,curves=pc.extract(str(BASE / f"{name}.pdf"))
    ws=pc.words(chars)
    longc=[c for c in curves if len(c[0])>=40]
    allx=[p[0] for c in longc for p in c[0]]; ally=[p[1] for c in longc for p in c[0]]
    ax,ay,xp,yp=pc.calib(ws,min(allx),min(ally))
    out=[]
    for pts,col in longc:
        X=np.polyval(ax,np.array([p[0] for p in pts]))
        Y=np.polyval(ay,np.array([p[1] for p in pts]))
        out.append((X,Y,col))
    return out

def apply_style():
    plt.style.use('fivethirtyeight')
    import cnstyle  # re-registers fonts & sets family AFTER style
    plt.rcParams['font.family']=['Times New Roman','Songti SC']
    plt.rcParams['pdf.fonttype']=42; plt.rcParams['axes.unicode_minus']=False
    plt.rcParams['figure.facecolor']='white'; plt.rcParams['savefig.facecolor']='white'

def ckey(col):
    if col is None: return 'k'
    r,g,b=col
    if b>0.6 and r<0.2: return 'blue'
    if r>0.9 and g<0.45: return 'red'
    if r>0.8 and g>0.6: return 'gold'
    return 'other'

# ---------- 1. IndexDistribution_density ----------
apply_style()
c=load("IndexDistribution_density")
X,Y,col=c[0]
fig=plt.figure(figsize=(9,6),dpi=200); ax=plt.subplot(111)
ax.plot(X,Y,lw=2.2,color='#008fd5')
ax.set_xlabel('MaaS转移意愿指数',fontsize=17)
ax.set_ylabel('密度',fontsize=17)
ax.tick_params(labelsize=13)
fig.savefig(OUT / 'IndexDistribution_density.pdf',bbox_inches='tight')
fig.savefig(OUT / 'IndexDistribution_density.png',dpi=140,bbox_inches='tight'); plt.close()

# ---------- 2. classIndexDistribution_density ----------
apply_style()
c=load("classIndexDistribution_density")
fig=plt.figure(figsize=(9,6),dpi=200); ax=plt.subplot(111)
lab={'blue':'类别1','red':'类别2'}
for X,Y,col in c:
    k=ckey(col); color='#008fd5' if k=='blue' else '#fc4f30'
    ax.plot(X,Y,lw=2.2,color=color,label=lab.get(k,k))
ax.legend(fontsize=14,loc='center right')
ax.set_xlabel('MaaS转移意愿指数',fontsize=17); ax.set_ylabel('密度',fontsize=17)
ax.tick_params(labelsize=13)
fig.savefig(OUT / 'classIndexDistribution_density.pdf',bbox_inches='tight')
fig.savefig(OUT / 'classIndexDistribution_density.png',dpi=140,bbox_inches='tight'); plt.close()

# ---------- 3. sentiveanalysis ----------
apply_style()
c=load("sentiveanalysis")
fig=plt.figure(figsize=(12,8),dpi=200); ax=plt.subplot(111)
style={'blue':('#008fd5','s','情况1',4),'red':('#fc4f30','o','情况2',4),'gold':('#e5ae38','1','情况3',7)}
series={ckey(col):(X,Y) for X,Y,col in c}
missing={'blue','red','gold'}-set(series)
if missing:
    raise RuntimeError(f"sentiveanalysis缺少曲线：{sorted(missing)}")
for k in ('blue','red','gold'):
    X,Y=series[k]; color,mk,lab,ms=style[k]
    idx=np.argsort(X)
    ax.plot(X[idx],Y[idx],lw=1.8,marker=mk,markersize=ms,color=color,label=lab,markevery=8)
ax.set_xticks([0,20,40,60,80,100]); ax.set_xticklabels(['0%','20%','40%','60%','80%','100%'])
ax.set_xlabel('MaaS方案出行时间水平',fontsize=17); ax.set_ylabel('转移至MaaS的人数',fontsize=17)
ax.tick_params(labelsize=14); ax.legend(fontsize=15)
fig.savefig(OUT / 'sentiveanalysis.pdf',bbox_inches='tight',metadata=PDF_METADATA)
fig.savefig(OUT / 'sentiveanalysis.png',dpi=130,bbox_inches='tight'); plt.close()
print("done 3 vector figs")
