# -*- coding: utf-8 -*-
"""第五章 priceSensitivity 中文版：MaaS存疑者与乐观者的价格灵敏度。
数据来源：弹性分析结果/价格灵敏度_LCLV.csv （即 choice_people，按价格系数聚合的各方案选择概率之和）。"""
import cnstyle
import pandas as pd, numpy as np, matplotlib.pyplot as plt
cp = pd.read_csv(r"/mnt/user-data/uploads/2023_04 MaaS单次出行对套餐购买的影响/弹性分析结果/价格灵敏度_LCLV.csv", encoding='gbk')
N=1242.0
cp['buy1']=cp[['Prob. PT1','Prob. metro1','Prob. taxi1','Prob. more1']].sum(1)
cp['buy2']=cp[['Prob. PT2','Prob. metro2','Prob. taxi2','Prob. more2']].sum(1)
bundle_cn=['公交优先','地铁畅行','优惠出租','全能畅行','按次付费(PAYG)']
probcols=['Prob. PT','Prob. metro','Prob. taxi','Prob. more','Prob. no']
colors5=['b','g','r','c','m']

def maxscale(df, buycol, nocol):
    j=df[buycol]>df[nocol]
    if j.any(): 
        t=df[j].iloc[-1]; return t['type'], t[buycol]/N
    return None

fig,axes=plt.subplots(2,2,figsize=(13,9),dpi=200)
plt.subplots_adjust(hspace=0.28,wspace=0.22,left=0.14,top=0.90)
for r,(cls,who) in enumerate([('1','存疑者'),('2','乐观者')]):
    # left: bundles vs PAYG
    ax=axes[r,0]
    ax.plot(cp['type'],cp[f'buy{cls}']/N,'b',label='MaaS套餐')
    ax.plot(cp['type'],cp[f'Prob. no{cls}']/N,'g',label='按次付费(PAYG)')
    ms=maxscale(cp,f'buy{cls}',f'Prob. no{cls}')
    if ms: ax.plot(ms[0],ms[1],'ks',ms=5); ax.text(ms[0]-0.2,ms[1],'最大价格系数：%.2f'%ms[0],fontsize=13,ha='right')
    ax.set_ylabel('订阅MaaS套餐的比例',fontsize=13); ax.set_xlabel('价格系数',fontsize=13)
    ax.set_xlim(0.5,10); ax.set_xticks([0.5,2,4,6,8,10]); ax.legend(fontsize=11,loc='upper right'); ax.tick_params(labelsize=11)
    # right: each bundle
    ax=axes[r,1]
    for pc,col,lab in zip(probcols,colors5,bundle_cn):
        ax.plot(cp['type'],cp[f'{pc}{cls}']/N,col,label=lab)
    ax.set_ylabel('订阅比例',fontsize=13); ax.set_xlabel('价格系数',fontsize=13)
    ax.set_xlim(0.5,10); ax.set_xticks([0.5,2,4,6,8,10]); ax.legend(fontsize=10,loc='upper right'); ax.tick_params(labelsize=11)
# column titles + row labels
axes[0,0].set_title('订阅MaaS套餐的比例',fontsize=16,fontweight='bold',pad=12)
axes[0,1].set_title('订阅各MaaS套餐的比例',fontsize=16,fontweight='bold',pad=12)
fig.text(0.025,0.71,'MaaS存疑者的\n价格灵敏度',fontsize=15,fontweight='bold',ha='center',va='center',rotation=90)
fig.text(0.025,0.29,'MaaS乐观者的\n价格灵敏度',fontsize=15,fontweight='bold',ha='center',va='center',rotation=90)
fig.savefig('out/priceSensitivity.pdf',bbox_inches='tight')
fig.savefig('out/priceSensitivity.png',dpi=130,bbox_inches='tight')
print('saved priceSensitivity; crossings:',
      maxscale(cp,'buy1','Prob. no1')[0], maxscale(cp,'buy2','Prob. no2')[0])
