# 消融实验分布对比图 ablation1(家庭级9属性,3x3) / ablation2(个人级6属性,3x2)
# 数据来自 数据/ 下的 raw_/results_ CSV；四组：居民出行调查数据 / HiDiT完整 / 无图结构 / 无画像条件；对数纵轴
import os, sys; sys.path.insert(0,os.path.dirname(__file__)); import figstyle; figstyle.apply()
import numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib.font_manager as fm
from figstyle import FP_R
DATA=os.environ.get("DATA","/mnt/user-data/uploads/2025_05博士论文第一章-合成人口/数据")
OUT=os.environ.get("OUTDIR","/tmp/ch3work/中文版")
SERIES=[("居民出行调查数据","raw",'coral'),("HiDiT（完整模型）","full",'steelblue'),
        ("HiDiT（无图处理模块）","nongr",'mediumseagreen'),("HiDiT（无画像条件）","noncl",'mediumpurple')]
def load(level):
    p={"raw":f"raw_{level}_df.csv","full":f"results_{level}_df_tunning.csv",
       "nongr":f"results_{level}_nongragh_df.csv","noncl":f"results_{level}_noncluster_df.csv"}
    return {k:pd.read_csv(f"{DATA}/{v}") for k,v in p.items()}
def make(level, attrs, nrow, ncol, figsize, out):
    dfs=load(level)
    fig,axes=plt.subplots(nrow,ncol,figsize=figsize); width=0.2
    for ax,(col,zh) in zip(axes.flat,attrs):
        cats=sorted(set().union(*[set(dfs[k][col].dropna().unique()) for _,k,_ in SERIES]))
        x=np.arange(len(cats))
        for j,(lab,k,color) in enumerate(SERIES):
            vc=dfs[k][col].value_counts()
            ax.bar(x+(j-1.5)*width,[vc.get(c,0) for c in cats],width,alpha=0.8,color=color,label=lab)
        ax.set_yscale('log')
        ax.set_xticks(x); ax.set_xticklabels([str(int(c)) if float(c).is_integer() else str(c) for c in cats],fontsize=11)
        ax.set_xlabel(zh,fontsize=13,fontproperties=fm.FontProperties(fname=FP_R,size=13))
        ax.set_ylabel("频数（对数刻度）",fontsize=11,fontproperties=fm.FontProperties(fname=FP_R,size=11))
        ax.tick_params(axis='y',labelsize=10); ax.grid(axis='y',alpha=0.3,which='both')
    for k in range(len(attrs),nrow*ncol): axes.flat[k].axis('off')
    h,l=axes.flat[0].get_legend_handles_labels()
    fig.legend(h,l,loc='upper center',ncol=4,prop=fm.FontProperties(fname=FP_R,size=13),frameon=False,bbox_to_anchor=(0.5,1.0))
    fig.tight_layout(rect=[0,0,1,0.955]); fig.savefig(out); plt.close(fig); print("saved",os.path.basename(out))

make("family",[("family_家庭成员数量","家庭成员数量"),("family_家庭工作人口数","家庭工作人口数"),("family_机动车数量","家庭机动车数量"),
 ("family_脚踏自行车数量","家庭自行车数量"),("family_电动自行车数量","家庭电动自行车数量"),("family_摩托车数量","家庭摩托车数量"),
 ("family_老年代步车数量","家庭老年代步车数量"),("family_家庭年收入","家庭年收入"),("have_student","是否有学生")],
 3,3,(15,8.6),f"{OUT}/ablation1_cn.pdf")
make("person",[("age","年龄"),("gender","性别"),("license","驾照"),("relation","与户主关系"),("education","受教育程度"),("occupation","职业")],
 3,2,(11,9),f"{OUT}/ablation2_cn.pdf")
