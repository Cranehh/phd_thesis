# -*- coding: utf-8 -*-
"""第五章 aggregateE 中文版：订阅意愿对套餐价格的集计直接点弹性。
数据来源：aggE_results_forCN.csv（由 分弹性和总弹性_LCLV.csv 在本机聚合得到，逻辑同notebook cell30-33）。"""
import cnstyle
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
a=pd.read_csv(r"/mnt/user-data/uploads/2026_06 博士毕业大论文撰写/aggE_results_forCN.csv")
# max price scale: last type where bundleaggE2 > bundleaggE1
j=a['bundleaggE2']>a['bundleaggE1']
mp=a[j].iloc[-1] if j.any() else None
fig=plt.figure(figsize=(16,9),dpi=200)
gs=GridSpec(2,4,height_ratios=[1.25,1],hspace=0.33,wspace=0.34,top=0.90)
# top wide
axt=fig.add_subplot(gs[0,:])
axt.plot(a['type'],a['bundleaggE1'],'b',label='MaaS存疑者')
axt.plot(a['type'],a['bundleaggE2'],'g',label='MaaS乐观者')
if mp is not None:
    axt.plot(mp['type'],mp['bundleaggE2'],'ks',ms=6)
    axt.text(mp['type']-5.2,mp['bundleaggE2'],'最大价格系数：%.2f'%mp['type'],fontsize=16)
axt.set_xlim(0.5,10); axt.set_xticks([0.5,2,4,6,8,10])
axt.set_xlabel('价格系数',fontsize=15); axt.set_ylabel('订阅MaaS套餐的\n集计直接点弹性',fontsize=15)
axt.legend(fontsize=13,loc='upper right'); axt.tick_params(labelsize=13)
axt.set_title('订阅MaaS套餐对价格系数的集计直接点弹性',fontsize=19,fontweight='bold',pad=10)
# bottom 4
subs=[('PTaggE','公交优先'),('metroaggE','地铁畅行'),('taxiaggE','优惠出租'),('moreaggE','全能畅行')]
for k,(col,name) in enumerate(subs):
    ax=fig.add_subplot(gs[1,k])
    ax.plot(a['type'],a[col+'1'],'b',label='MaaS存疑者')
    ax.plot(a['type'],a[col+'2'],'g',label='MaaS乐观者')
    ax.set_title(name,fontsize=15,fontweight='bold')
    ax.set_xlim(0.5,10); ax.set_xticks([0.5,4,8]); ax.tick_params(labelsize=11)
    ax.set_xlabel('价格系数',fontsize=12)
    if k==0: ax.set_ylabel('集计直接点弹性',fontsize=12)
    ax.legend(fontsize=9,loc='best')
fig.savefig('out/aggregateE.pdf',bbox_inches='tight')
fig.savefig('out/aggregateE.png',dpi=120,bbox_inches='tight')
print('saved aggregateE; max price scale =', None if mp is None else round(mp['type'],2))
