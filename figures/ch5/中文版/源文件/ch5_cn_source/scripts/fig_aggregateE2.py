# -*- coding: utf-8 -*-
"""第五章 aggregateE2 中文版：套餐订阅对非价格变量的集计直接点弹性。
数据来源：分弹性和总弹性_非价格因素_LCLV.csv（聚合逻辑同notebook cell53-62）。"""
import cnstyle
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
e=pd.read_csv(r"/mnt/user-data/uploads/2023_04 MaaS单次出行对套餐购买的影响/弹性分析结果/分弹性和总弹性_非价格因素_LCLV.csv", encoding='gbk')
m1={'m1':'direct_elas_m11','m2':'direct_elas_m21','m3':'direct_elas_m31','m4':'direct_elas_m41',
    'l1':'direct_elas_l11','l2':'direct_elas_l21','l3':'direct_elas_l31','l4':'direct_elas_l41','l6':'direct_elas_l61'}
m2={'taxi':'direct_elas_taxi_source2','m1':'direct_elas_m12','m2':'direct_elas_m22','m3':'direct_elas_m32','m4':'direct_elas_m42',
    'l1':'direct_elas_l12','l2':'direct_elas_l22','l3':'direct_elas_l32','l4':'direct_elas_l42','l6':'direct_elas_l62'}
agg1=e.groupby('type')[list(m1.values())].sum(); agg1.columns=list(m1)
agg2=e.groupby('type')[list(m2.values())].sum(); agg2.columns=list(m2)
types=sorted(agg1.index); t0=types[0]
cats=['出租/\n网约车','M1','M2','M3','M4','LV1','LV2','LV3','LV4','LV5']
print('types:',[round(t,2) for t in types])
print('check @%.2f  M1_skep=%.2f M1_exp=%.2f taxi_exp=%.2f LV2_skep=%.2f LV5_skep=%.2f'%(
   t0, agg1.loc[t0,'m1'], agg2.loc[t0,'m1'], agg2.loc[t0,'taxi'], agg1.loc[t0,'l2'], agg1.loc[t0,'l6']))

def bars(ax,c1vals,c2vals,fs,col1,col2,lab):
    # c1 has 9 (no taxi) -> positions 1..9 ; c2 has 10 -> 0..9
    idx=np.arange(10); w=0.38
    b1=ax.bar(idx[1:]+ - w/2, c1vals, w, color=col1, label='MaaS存疑者')
    b2=ax.bar(idx + w/2, c2vals, w, color=col2, label='MaaS乐观者')
    ax.axhline(0,color='k',lw=0.8)
    for b in list(b1)+list(b2):
        y=b.get_height(); ax.text(b.get_x()+b.get_width()/2, y, ('%.2f'%y) if abs(y)>=0.01 else '0',
                                  ha='center', va='bottom' if y>=0 else 'top', fontsize=fs)
    ax.set_xticks(idx); ax.set_xticklabels(cats,fontsize=fs+2)
    ax.legend(fontsize=fs+2,loc='upper right')

fig=plt.figure(figsize=(17,11),dpi=150)
gs=GridSpec(2,3,height_ratios=[1.05,1],hspace=0.32,wspace=0.2,top=0.93)
# top: absolute at t0
axt=fig.add_subplot(gs[0,:])
bars(axt, agg1.loc[t0].values, agg2.loc[t0].values, 11,'blue','green','')
axt.set_ylabel('订阅MaaS套餐的\n集计直接点弹性',fontsize=15)
axt.set_title('订阅MaaS套餐对非价格变量的集计直接点弹性（价格系数为0.50）',fontsize=18,fontweight='bold',pad=8)
# bottom 3 diffs
for k,ti in enumerate([1,2,3]):
    t=types[ti]; ax=fig.add_subplot(gs[1,k])
    d1=agg1.loc[t].values-agg1.loc[t0].values
    d2=agg2.loc[t].values-agg2.loc[t0].values
    bars(ax,d1,d2,7,'lightcoral','lightblue','')
    ax.set_title('价格系数为 %.2f'%t,fontsize=14,fontweight='bold')
    if k==0: ax.set_ylabel('集计直接点弹性差异',fontsize=12)
fig.suptitle('')
fig.text(0.5,0.485,'以价格系数0.50为参照的集计直接点弹性差异',fontsize=16,fontweight='bold',ha='center')
fig.savefig('out/aggregateE2.pdf',bbox_inches='tight')
fig.savefig('out/aggregateE2.png',dpi=110,bbox_inches='tight')
print('saved aggregateE2')
