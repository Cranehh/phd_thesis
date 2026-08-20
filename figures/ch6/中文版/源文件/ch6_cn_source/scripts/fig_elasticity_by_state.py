# -*- coding: utf-8 -*-
"""第六章 图：服务水平相关属性对MaaS多阶段采纳意愿的状态条件弹性（中文版）。

由 plot_state_elasticities.py 改写而来，绘图逻辑完全一致，仅将标签/图例
译为中文并改用中文字体（见 cnstyle.py）。数值直接读取原始弹性结果CSV，
不重跑模型。

一图两栏：
  (a) 单次出行MaaS采纳
        平均费用节省 | 平均时间节省 | 平均轨道车内时间
  (b) 套餐订阅
        自身价格块(4个套餐) | 出租/网约车里程块(合并为2组)

时间敏感型的自身价格系数不显著(beta_Price_S2=0.015, t=0.84)，对应柱子
加斜纹并标注"不显著"。

输出：中文矢量PDF elasticity_by_state.pdf
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
CSV_PATH = os.path.join(DATA_DIR, 'HMM_弹性_state_conditional.csv')
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- 样式
plt.rcParams.update({'font.size': 9, 'axes.linewidth': 0.8})

C_COST = '#2C6FB0'   # 费用敏感型 (S1)  -- 钢蓝
C_TIME = '#D1603D'   # 时间敏感型 (S2)  -- 朱红
W = 0.38

# ---------------------------------------------------------------- 数据
df = pd.read_csv(CSV_PATH)


def elas(stage, choice, state, variable):
    m = df[(df['stage'] == stage) & (df['choice'] == choice) &
           (df['state'] == state) & (df['variable'] == variable)]
    if len(m) != 1:
        raise ValueError(f'expected 1 row, got {len(m)} for '
                         f'{stage}/{choice}/{state}/{variable}')
    return float(m['elasticity'].iloc[0])


# 单次出行 (Stage 1)
s1_cats = ['平均\n费用节省', '平均\n时间节省', '平均轨道\n车内时间']
s1_vars = ['avg_cost_savings', 'avg_time_savings', 'avg_rail_time']
s1_cost = [elas('Stage1', 'MaaS', 'S1', v) for v in s1_vars]
s1_time = [elas('Stage1', 'MaaS', 'S2', v) for v in s1_vars]

# 套餐订阅 (Stage 2) 自身价格(4套餐) + taxi_12(5套餐)
op_keys = ['Bus', 'Metro', 'VT', 'Ultra']
op_lab = ['公交优先', '地铁畅行', '优惠出租', '全能畅行']
op_price = {'Bus': 'price1', 'Metro': 'price2', 'VT': 'price3',
            'Ultra': 'price4'}
op_cost = [elas('Stage2', b, 'S1', op_price[b]) for b in op_keys]
op_time = [elas('Stage2', b, 'S2', op_price[b]) for b in op_keys]

tx_keys = ['Bus', 'Metro', 'VT', 'Ultra', 'PAYG']
tx_cost_raw = [elas('Stage2', b, 'S1', 'taxi_12') for b in tx_keys]
tx_time_raw = [elas('Stage2', b, 'S2', 'taxi_12') for b in tx_keys]

# 合并 taxi_12 弹性相同的套餐（数据驱动）
_groups = {}
for k, c, t in zip(tx_keys, tx_cost_raw, tx_time_raw):
    _groups.setdefault((round(c, 6), round(t, 6)), []).append(k)
assert len(_groups) == 2, f'expected 2 taxi groups, got {_groups}'
_g_sorted = sorted(_groups.items(), key=lambda kv: kv[0][0])  # cost asc
assert [set(v) for _, v in _g_sorted] == \
    [{'Bus', 'Metro'}, {'VT', 'Ultra', 'PAYG'}], _g_sorted
tx_cost = [k[0] for k, _ in _g_sorted]
tx_time = [k[1] for k, _ in _g_sorted]
tx_lab = ['公交优先/\n地铁畅行', '优惠出租/全能\n畅行/PAYG']

print('S1 费用敏感型:', [round(v, 4) for v in s1_cost])
print('S1 时间敏感型:', [round(v, 4) for v in s1_time])
print('自身价格 费用:', [round(v, 4) for v in op_cost])
print('自身价格 时间:', [round(v, 4) for v in op_time])
print('taxi 费用:', [round(v, 4) for v in tx_cost])
print('taxi 时间:', [round(v, 4) for v in tx_time])


# ---------------------------------------------------------------- 辅助
def grouped(ax, x, cost, time, hatch_time=False):
    ax.bar(x - W / 2, cost, W, color=C_COST, edgecolor='black',
           linewidth=0.5)
    ax.bar(x + W / 2, time, W, color=C_TIME, edgecolor='black',
           linewidth=0.5, hatch='///' if hatch_time else None)


def vlabels(ax, x, vals, rng, fmt, ns=False, lift_small=False,
            lift_level=1.7):
    pad = 0.022 * rng
    small = 0.06 * rng
    for xi, v in zip(x, vals):
        if lift_small and abs(v) < small:
            ax.text(xi, lift_level * pad, fmt.format(v), ha='center',
                    va='bottom', fontsize=6.5)
            continue
        if v >= 0:
            ax.text(xi, v + pad, fmt.format(v), ha='center', va='bottom',
                    fontsize=6.8)
            if ns:
                ax.text(xi, v + pad + 0.085 * rng, '不显著', ha='center',
                        va='bottom', fontsize=6.0, style='italic',
                        color='#555555')
        else:
            ax.text(xi, v - pad, fmt.format(v), ha='center', va='top',
                    fontsize=6.8)


# ---------------------------------------------------------------- 绘图
fig, (axa, axb) = plt.subplots(1, 2, figsize=(8.2, 4.4),
                               gridspec_kw={'width_ratios': [1.15, 1.7]})

# ---- (a) 单次出行 ----------------------------------------------------
xa = np.arange(len(s1_cats))
grouped(axa, xa, s1_cost, s1_time)
axa.axhline(0, color='black', lw=0.6)
lo_a, hi_a = min(s1_cost + s1_time), max(s1_cost + s1_time + [0.0])
rng_a = hi_a - lo_a
axa.set_ylim(lo_a - 0.12 * rng_a, hi_a + 0.30 * rng_a)
vlabels(axa, xa - W / 2, s1_cost, rng_a, '{:.4f}', lift_small=True,
        lift_level=1.4)
vlabels(axa, xa + W / 2, s1_time, rng_a, '{:.4f}', lift_small=True,
        lift_level=4.2)
axa.set_xticks(xa)
axa.set_xticklabels(s1_cats)
axa.set_ylabel('状态条件弹性（样本均值处）', fontsize=8.5)
axa.grid(axis='y', ls='--', alpha=0.3)
axa.spines[['top', 'right']].set_visible(False)

# ---- (b) 套餐订阅：自身价格块 | 出租/网约车里程块 ------------------
x_op = np.arange(4)                       # 0..3  (4个自身价格套餐)
x_tx = np.array([4.4, 5.4])               # 2个合并的里程组
grouped(axb, x_op, op_cost, op_time, hatch_time=True)
grouped(axb, x_tx, tx_cost, tx_time)
axb.axhline(0, color='black', lw=0.6)
allv = op_cost + op_time + tx_cost + tx_time
lo_b, hi_b = min(allv), max(allv)
rng_b = hi_b - lo_b
axb.set_ylim(lo_b - 0.12 * rng_b, hi_b + 0.34 * rng_b)
vlabels(axb, x_op - W / 2, op_cost, rng_b, '{:.3f}')
vlabels(axb, x_op + W / 2, op_time, rng_b, '{:.3f}', ns=True)
vlabels(axb, x_tx - W / 2, tx_cost, rng_b, '{:.3f}')
vlabels(axb, x_tx + W / 2, tx_time, rng_b, '{:.3f}')
axb.axvline(3.7, color='0.75', lw=0.8, ls='--')        # 块分隔线
axb.set_xticks(list(x_op) + list(x_tx))
axb.set_xticklabels(op_lab + tx_lab, rotation=30, ha='right',
                    fontsize=7.5)
# 块标题（贴近上边框）
axb.text(1.5, hi_b + 0.27 * rng_b, '自身价格', ha='center',
         va='center', fontsize=8.5, color='#333333')
axb.text(4.9, hi_b + 0.27 * rng_b, '出租/网约车里程', ha='center',
         va='center', fontsize=8.5, color='#333333')
axb.set_xlim(-0.8, 6.2)
axb.grid(axis='y', ls='--', alpha=0.3)
axb.spines[['top', 'right']].set_visible(False)

# ---- 共享图例(顶部) + 分栏标题(底部) --------------------------------
handles = [
    mpatches.Patch(facecolor=C_COST, edgecolor='black', label='费用敏感型'),
    mpatches.Patch(facecolor=C_TIME, edgecolor='black', label='时间敏感型'),
    mpatches.Patch(facecolor='white', edgecolor='black', hatch='///',
                   label='不显著'),
]
fig.legend(handles=handles, loc='upper center', ncol=3, frameon=False,
           fontsize=8, bbox_to_anchor=(0.5, 1.01))
fig.text(0.245, 0.012, '(a) 单次出行MaaS采纳', ha='center',
         va='bottom', fontsize=9)
fig.text(0.70, 0.012, '(b) 套餐订阅', ha='center',
         va='bottom', fontsize=9)

fig.subplots_adjust(left=0.095, right=0.975, top=0.90, bottom=0.17,
                    wspace=0.16)

# ---------------------------------------------------------------- 保存
pdf_path = os.path.join(OUT_DIR, 'elasticity_by_state.pdf')
fig.savefig(pdf_path)
plt.close(fig)
print('已保存:', pdf_path)
