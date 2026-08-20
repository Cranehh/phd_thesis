# -*- coding: utf-8 -*-
"""第六章 图：考虑全体用户的MaaS服务水平聚合弹性（中文版）。

由 plot_aggregate_elasticities.py 改写，绘图逻辑完全一致，仅将标签/图例
译为中文并改用中文字体（见 cnstyle.py）。数值读取原始弹性结果CSV，不重跑。

图1 elasticity_aggregate_overall：MaaS套餐整体订阅弹性（横向龙卷风图）
图2 elasticity_by_bundle：分套餐订阅弹性（2x2，每套餐一栏，11变量共享次序）
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cnstyle  # noqa: F401  中文字体样式

# ---------------------------------------------------------------- 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('CH6_DATA', os.path.join(BASE_DIR, '..', 'data'))
OUT_DIR = os.environ.get('CH6_OUT',
                         os.path.join(BASE_DIR, '..', '..', '..'))  # -> 中文版/
SUB_CSV = os.path.join(DATA_DIR, 'HMM_弹性_aggregate_subscription.csv')
BND_CSV = os.path.join(DATA_DIR, 'HMM_弹性_aggregate_bundle.csv')
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- 样式
plt.rcParams.update({'font.size': 9, 'axes.linewidth': 0.8})
C_POS = '#2C6FB0'   # 弹性 >= 0
C_NEG = '#D1603D'   # 弹性 <  0
C_AGG = '#5C6B73'   # 图1 中性色（正负由柱方向表示）

# 图1（整体订阅）单行标签
PRETTY1 = {
    'price1': '价格（公交优先）',
    'price2': '价格（地铁畅行）',
    'price3': '价格（优惠出租）',
    'price4': '价格（全能畅行）',
    'taxi_12': '出租/网约车里程',
    'avg_rail_time': '平均轨道车内时间',
    'avg_cost_savings': '平均费用节省',
    'avg_time_savings': '平均时间节省',
    'cost_savings': '体验到的费用节省',
    'time_savings': '体验到的时间节省',
    'price_ratio': '价格比例系数',
}

# 图2 x轴紧凑单行标签
PRETTY2 = {
    'price1': '价格(公交优先)',
    'price2': '价格(地铁畅行)',
    'price3': '价格(优惠出租)',
    'price4': '价格(全能畅行)',
    'taxi_12': '出租/网约车里程',
    'price_ratio': '价格比例系数',
    'avg_rail_time': '平均轨道车内时间',
    'avg_cost_savings': '平均费用节省',
    'avg_time_savings': '平均时间节省',
    'cost_savings': '体验费用节省',
    'time_savings': '体验时间节省',
}

# 图2 固定变量次序（4栏共享）
VAR_ORDER = ['price1', 'price2', 'price3', 'price4', 'taxi_12',
             'price_ratio', 'avg_rail_time', 'avg_cost_savings',
             'avg_time_savings', 'cost_savings', 'time_savings']

# ---------------------------------------------------------------- 数据
df_sub = pd.read_csv(SUB_CSV)
assert df_sub['target'].nunique() == 1, df_sub['target'].unique()
df_sub = df_sub.copy()
df_sub['absx'] = df_sub['elasticity'].abs()
df_sub = df_sub.sort_values('absx', ascending=True)        # 最大在上
a_lab = [PRETTY1.get(v, v) for v in df_sub['variable']]
a_val = df_sub['elasticity'].tolist()

df_bnd = pd.read_csv(BND_CSV)
B_KEYS = ['Bus', 'Metro', 'VT', 'Ultra']
B_LAB = ['公交优先', '地铁畅行', '优惠出租', '全能畅行']


def bvec(bundle):
    out = []
    for v in VAR_ORDER:
        m = df_bnd[(df_bnd['bundle'] == bundle) & (df_bnd['variable'] == v)]
        assert len(m) == 1, f'{bundle}/{v}: {len(m)} rows'
        out.append(float(m['elasticity'].iloc[0]))
    return out


bundle_vals = {b: bvec(b) for b in B_KEYS}

print('目标:', df_sub['target'].iloc[0])
for lab, v in sorted(zip(a_lab, a_val), key=lambda kv: -abs(kv[1])):
    print(f'  {lab:<18} {v:+.4f}')

# ================================================================ 图1
fig1, ax1 = plt.subplots(figsize=(7.0, 4.0))
y = np.arange(len(a_val))
ax1.barh(y, a_val, color=C_AGG, edgecolor='black', linewidth=0.5)
ax1.axvline(0, color='black', lw=0.6)
amax = max(abs(min(a_val)), abs(max(a_val)))
ax1.set_xlim(-amax * 1.30, amax * 0.45)
for yi, v in zip(y, a_val):
    off = amax * 0.015
    txt = f'{v:.3f}' if abs(v) > 1e-4 else '~0'
    ax1.text(v - off if v < 0 else v + off, yi, txt,
             va='center', ha='right' if v < 0 else 'left', fontsize=7.5)
ax1.set_yticks(y)
ax1.set_yticklabels(a_lab, fontsize=8.5)
ax1.set_xlabel('聚合弹性', fontsize=9)
ax1.grid(axis='x', ls='--', alpha=0.3)
ax1.spines[['top', 'right']].set_visible(False)
fig1.tight_layout()
p1_pdf = os.path.join(OUT_DIR, 'elasticity_aggregate_overall.pdf')
fig1.savefig(p1_pdf)
plt.close(fig1)
print('已保存 图1:', p1_pdf)

# ================================================================ 图2
x = np.arange(len(VAR_ORDER))
x_lab = [PRETTY2.get(v, v) for v in VAR_ORDER]
allv = [v for b in B_KEYS for v in bundle_vals[b]]
gmin, gmax = min(allv), max(allv)
grng = gmax - gmin
ylo, yhi = gmin - 0.16 * grng, gmax + 0.16 * grng
pad = 0.020 * grng

fig2, axes = plt.subplots(2, 2, figsize=(9.6, 7.4), sharey=True)
for ax, b, cap in zip(axes.flat, B_KEYS,
                       ['(a) 公交优先', '(b) 地铁畅行',
                        '(c) 优惠出租', '(d) 全能畅行']):
    vals = bundle_vals[b]
    colors = [C_POS if v >= 0 else C_NEG for v in vals]
    ax.bar(x, vals, 0.62, color=colors, edgecolor='black', linewidth=0.5)
    ax.axhline(0, color='black', lw=0.6)
    ax.set_ylim(ylo, yhi)
    for xi, v in zip(x, vals):
        ax.text(xi, v + pad if v >= 0 else v - pad,
                f'{v:.3f}' if abs(v) > 5e-4 else '~0',
                ha='center', va='bottom' if v >= 0 else 'top',
                fontsize=5.6)
    ax.set_xticks(x)
    ax.set_xticklabels(x_lab, rotation=40, ha='right', fontsize=6.6)
    ax.tick_params(axis='x', pad=1)
    ax.grid(axis='y', ls='--', alpha=0.3)
    ax.spines[['top', 'right']].set_visible(False)
    ax.text(0.5, -0.68, cap, transform=ax.transAxes, ha='center',
            va='top', fontsize=9)

for ax in axes[:, 0]:
    ax.set_ylabel('分套餐弹性', fontsize=8.5)

handles = [
    mpatches.Patch(facecolor=C_POS, edgecolor='black', label='弹性 ≥ 0'),
    mpatches.Patch(facecolor=C_NEG, edgecolor='black', label='弹性 < 0'),
]
fig2.legend(handles=handles, loc='upper center', ncol=2, frameon=False,
            fontsize=8.5, bbox_to_anchor=(0.5, 0.995))
fig2.subplots_adjust(left=0.085, right=0.985, top=0.93, bottom=0.16,
                     hspace=1.08, wspace=0.10)
p2_pdf = os.path.join(OUT_DIR, 'elasticity_by_bundle.pdf')
fig2.savefig(p2_pdf)
plt.close(fig2)
print('已保存 图2:', p2_pdf)
