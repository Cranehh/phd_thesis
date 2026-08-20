import cnstyle
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

p = pd.read_csv('people.csv', encoding='gbk')
N = 1260

# ---- Panel 1: main travel mode ----
modes = ['6a','6b','6c','6d','6e','6f','6g']
mode_cn = ['公共交通','出租/\n网约车','私家车','共享汽车','自行车/\n电动自行车','共享单车','步行']
vals1 = [p.groupby(m)['peopleID'].count().get(1,0)/N for m in modes]

# ---- Panel 2: weekly frequency lines ----
freq_cols = ['week_bus','week_metro','week_bike','week_ebike','week_taxi']
freq_cn   = ['公交','地铁','自行车','电动自行车','出租/网约车']
freq_colors = ['#E24A33','#348ABD','#988ED5','#777777','#FBC15E']
freq_x = ['≤3','4-7','8-11','12-15','≥15']
freq_vals = [p.groupby(c)['peopleID'].count().reindex([1,2,3,4,5]).fillna(0).values/N for c in freq_cols]

# ---- Panel 3: distance distribution weekday vs weekend ----
dw = p.groupby('travel_distance_work')['peopleID'].count().reindex(range(1,7)).fillna(0).values/N
de = p.groupby('travel_distance_weekend')['peopleID'].count().reindex(range(1,7)).fillna(0).values/N
dist_x = ['<5','5-10','10-20','20-40','40-60','>60']

print("Panel1 %:", [round(v*100,2) for v in vals1])
print("weekday %:", [round(v*100,2) for v in dw])
print("weekend %:", [round(v*100,2) for v in de])

# ================= FIGURE =================
fig = plt.figure(figsize=(13,9), dpi=200)
gs = GridSpec(2,2, height_ratios=[1,0.95], hspace=0.32, wspace=0.22)

# Panel 1
ax1 = fig.add_subplot(gs[0,0])
bars = ax1.bar(range(7), vals1, color='#009ca9', width=0.62)
ax1.set_title('主要出行方式', fontsize=20, fontweight='bold', pad=10)
ax1.set_xticks(range(7)); ax1.set_xticklabels(mode_cn, fontsize=13)
ax1.set_yticks([0,0.3,0.6,0.9]); ax1.tick_params(labelsize=13)
ax1.set_ylim(0,0.85)
for i,v in enumerate(vals1):
    ax1.text(i, v+0.012, f'{v*100:.2f}%', ha='center', fontsize=12.5)
for s in ['top','right']: ax1.spines[s].set_visible(False)

# Panel 2 (ggplot-like)
ax2 = fig.add_subplot(gs[0,1])
ax2.set_facecolor('#E5E5E5')
for v,c,lab in zip(freq_vals, freq_colors, freq_cn):
    ax2.plot(range(5), v, 'o-', lw=2, color=c, label=lab, markersize=5)
ax2.set_title('各方式每周出行频率（%，上周）', fontsize=20, fontweight='bold', pad=10)
ax2.set_xticks(range(5)); ax2.set_xticklabels(freq_x, fontsize=13)
ax2.set_xlabel('每周使用频率', fontsize=15); ax2.set_ylabel('比例', fontsize=15)
ax2.tick_params(labelsize=12)
ax2.grid(True, color='white', lw=1.1); ax2.set_axisbelow(True)
for s in ax2.spines.values(): s.set_visible(False)
ax2.legend(fontsize=12, loc='upper right', framealpha=0.9)

# Panel 3
ax3 = fig.add_subplot(gs[1,:])
x = np.arange(6); w=0.38
b1 = ax3.bar(x-w/2, dw, w, color='#4E9BD5', label='工作日出行距离分布')
b2 = ax3.bar(x+w/2, de, w, color='#F0A63A', label='周末出行距离分布')
ax3.set_title('出行距离分布', fontsize=20, fontweight='bold', pad=10)
ax3.set_xticks(x); ax3.set_xticklabels([f'{t}km' for t in dist_x], fontsize=14)
ax3.set_yticks([0,0.2,0.4]); ax3.tick_params(labelsize=13); ax3.set_ylim(0,0.42)
for i in range(6):
    ax3.text(i-w/2, dw[i]+0.008, f'{dw[i]*100:.2f}%', ha='center', fontsize=11.5)
    ax3.text(i+w/2, de[i]+0.008, f'{de[i]*100:.2f}%', ha='center', fontsize=11.5)
for s in ['top','right']: ax3.spines[s].set_visible(False)
ax3.legend(fontsize=14, loc='upper right', framealpha=0.9)

fig.savefig('out/travelPattern.pdf')
fig.savefig('out/travelPattern.png', dpi=150)
print('SAVED travelPattern')
