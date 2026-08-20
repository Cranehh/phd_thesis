# -*- coding: utf-8 -*-
"""重建 HMM 总体框架图（中文版）→ PPTX + PDF。
版式对照英文原图 HMM_framework.pdf 忠实重建；文字为中文。
可在 PowerPoint/WPS 里直接改文字与框线。"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pptxlib as L
from _pptxlib import (box, textbox, bullets, line, MSO_SHAPE, RGBColor,
                      WHITE, BLACK, DARKLINE, BLUE_BG)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('CH6_OUT', os.path.join(BASE, '..', '..', '..'))
EDIT = os.path.join(BASE, '..', 'editable')
os.makedirs(OUT, exist_ok=True)
os.makedirs(EDIT, exist_ok=True)

W, H = 11.243, 6.797          # 对应原图 809.52 x 489.36 pt
prs, s = L.new_prez(W, H)

GRAY_SEC = RGBColor(0xF2, 0xF2, 0xF2)     # 上部分区淡灰底
GRAY_PANEL = RGBColor(0xEC, 0xEC, 0xEC)
BLUE_SEC = RGBColor(0xDD, 0xE7, 0xF3)     # 下部分区淡蓝底
BLUE_PANEL = RGBColor(0xD3, 0xE0, 0xF1)
GRP = RGBColor(0x8C, 0x8C, 0x8C)
PANEL_TITLE = 11.5
BULLET = 9.6

# ============================================================ 中部分区背景
top_x, top_w = 2.72, 5.80
box(s, top_x, 0.30, top_w, 3.02, '', fill=GRAY_SEC, line_color=GRP,
    line_w=1.0, shape=MSO_SHAPE.RECTANGLE)
textbox(s, top_x, 0.36, top_w, 0.34, '行为状态形成与转移', size=12.5,
        bold=True, align='c')
bot_y = 3.48
box(s, top_x, bot_y, top_w, 3.0, '', fill=BLUE_SEC, line_color=GRP,
    line_w=1.0, shape=MSO_SHAPE.RECTANGLE)
textbox(s, top_x, 6.14, top_w, 0.34, '单次出行选择与套餐订阅', size=12.5,
        bold=True, align='c')

# ============================================================ 四个侧栏
lx, lw = 0.12, 2.42
rx = 8.70
# 左上：初始状态识别变量
box(s, lx, 0.42, lw, 2.86, '', fill=GRAY_PANEL, line_color=GRP,
    shape=MSO_SHAPE.RECTANGLE, line_w=1.1)
textbox(s, lx, 0.50, lw, 0.5, '初始状态识别变量', size=PANEL_TITLE, bold=True)
bullets(s, lx + 0.06, 1.02, lw - 0.12, 2.2,
        ['性别', '年龄', '月收入', '受教育程度', '职业', '是否拥车',
         '每周各方式出行频率', '主要出行方式', '潜变量'],
        size=BULLET, fill=GRAY_PANEL, line_color=None, leading=1.06)
# 右上：行为状态转移变量
box(s, rx, 0.42, lw, 2.86, '', fill=GRAY_PANEL, line_color=GRP,
    shape=MSO_SHAPE.RECTANGLE, line_w=1.1)
textbox(s, rx, 0.50, lw, 0.5, '行为状态转移变量', size=PANEL_TITLE, bold=True)
bullets(s, rx + 0.06, 1.02, lw - 0.12, 2.2,
        ['体验到的费用节省', '体验到的时间节省', '所含方式与方式频率之差',
         '套餐价格与月度出行花费之差', '平均价格系数'],
        size=BULLET, fill=GRAY_PANEL, line_color=None, leading=1.25)
# 左下：单次出行选择变量
box(s, lx, 3.62, lw, 2.7, '', fill=BLUE_PANEL, line_color=GRP,
    shape=MSO_SHAPE.RECTANGLE, line_w=1.1)
textbox(s, lx, 3.70, lw, 0.5, '单次出行选择变量', size=PANEL_TITLE, bold=True)
bullets(s, lx + 0.06, 4.22, lw - 0.12, 2.0,
        ['无MaaS时的方式选择', '出发时间：非高峰', '出行距离：>40km',
         '平均轨道车内时间', '平均费用节省', '平均时间节省'],
        size=BULLET, fill=BLUE_PANEL, line_color=None, leading=1.2)
# 右下：套餐订阅变量
box(s, rx, 3.62, lw, 2.78, '', fill=BLUE_PANEL, line_color=GRP,
    shape=MSO_SHAPE.RECTANGLE, line_w=1.1)
textbox(s, rx, 3.70, lw, 0.5, '套餐订阅变量', size=PANEL_TITLE, bold=True)
bullets(s, rx + 0.06, 4.22, lw - 0.12, 2.1,
        ['套餐自身价格', '套餐含出租/网约车', '性别', '年龄', '月收入',
         '职业', '自行车/电单车拥有', '是否持驾照', '出行模式'],
        size=BULLET, fill=BLUE_PANEL, line_color=None, leading=1.04)

# ============================================================ 上部：状态形成与转移
# 两个子标题框
idbox = box(s, 3.02, 0.82, 2.02, 0.48, '初始状态识别', fill=WHITE,
            line_color=DARKLINE, line_w=1.25, size=11, bold=True)
trbox = box(s, 6.18, 0.82, 2.02, 0.48, '行为状态转移', fill=WHITE,
            line_color=DARKLINE, line_w=1.25, size=11, bold=True)
# T 标签
textbox(s, 3.30, 1.42, 1.2, 0.3, 'T =1', size=11, bold=True, align='l')
textbox(s, 6.46, 1.42, 1.2, 0.3, 'T =2', size=11, bold=True, align='l')
# 状态框
sw, sh = 1.62, 0.56
s1a = box(s, 3.22, 1.74, sw, sh, '状态1', fill=WHITE, line_color=DARKLINE,
          line_w=1.25, size=11, bold=True)
sSa = box(s, 3.22, 2.62, sw, sh, '状态S', fill=WHITE, line_color=DARKLINE,
          line_w=1.25, size=11, bold=True)
s1b = box(s, 6.36, 1.74, sw, sh, '状态1', fill=WHITE, line_color=DARKLINE,
          line_w=1.25, size=11, bold=True)
sSb = box(s, 6.36, 2.62, sw, sh, '状态S', fill=WHITE, line_color=DARKLINE,
          line_w=1.25, size=11, bold=True)
textbox(s, 3.22, 2.24, sw, 0.34, '……', size=13, bold=True)
textbox(s, 6.36, 2.24, sw, 0.34, '……', size=13, bold=True)
# 交叉转移箭头 T1 -> T2
for ya in (2.02, 2.90):
    for yb in (2.02, 2.90):
        line(s, 3.22 + sw, ya, 6.36, yb, color=BLACK, w=0.9)

# ============================================================ 下部：选择
stc = box(s, 3.12, 3.98, 1.92, 0.56, '单次出行选择', fill=WHITE,
          line_color=DARKLINE, line_w=1.4, size=11, bold=True)
bsc = box(s, 6.30, 3.98, 1.92, 0.56, '套餐订阅', fill=WHITE,
          line_color=DARKLINE, line_w=1.4, size=11, bold=True)
# 单次出行选择结果
box(s, 3.02, 5.34, 0.98, 0.66, '不转移', fill=WHITE, line_color=DARKLINE,
    line_w=1.2, size=10.5, bold=True)
box(s, 4.10, 5.34, 1.06, 0.66, '转移至\nMaaS', fill=WHITE, line_color=DARKLINE,
    line_w=1.2, size=10.5, bold=True)
# 套餐订阅结果（5个）
bnames = ['公交优先', '地铁畅行', '优惠出租', '全能畅行', 'PAYG']
bx0, bw, bgap = 5.22, 0.62, 0.045
for i, nm in enumerate(bnames):
    box(s, bx0 + i * (bw + bgap), 5.40, bw, 0.60, nm, fill=WHITE,
        line_color=DARKLINE, line_w=1.2, size=9.5, bold=True, wrap=False)

# ============================================================ 连接箭头
# 侧栏 -> 中部子标题
line(s, lx + lw, 1.55, idbox.left / 914400.0, 1.06, color=BLACK, w=1.0)
line(s, rx, 1.55, trbox.left / 914400.0 + 2.02, 1.06, color=BLACK, w=1.0)
# 初始状态识别 -> 状态1(T1)；行为状态转移 -> 状态间(T2)
line(s, 4.03, 1.30, 4.03, 1.74, color=BLACK, w=1.1)
line(s, 7.19, 1.30, 7.19, 1.74, color=BLACK, w=1.1)
# 状态列(T1) -> 单次出行选择；状态列(T2) -> 套餐订阅（向下）
line(s, 4.03, 3.18, 4.08, 3.98, color=BLACK, w=1.1)
line(s, 7.19, 3.18, 7.26, 3.98, color=BLACK, w=1.1)
# 单次出行体验（反馈，向上）
line(s, 4.55, 3.98, 4.55, 3.18, color=BLACK, w=1.1)
textbox(s, 4.6, 3.34, 2.2, 0.3, '单次出行体验', size=10.5, bold=True, align='l')
# 侧栏(下) -> 选择框
line(s, lx + lw, 4.4, stc.left / 914400.0, 4.26, color=BLACK, w=1.0)
line(s, rx, 4.4, bsc.left / 914400.0 + 1.92, 4.26, color=BLACK, w=1.0)
# 选择框 -> 结果
line(s, 3.55, 4.54, 3.51, 5.34, color=BLACK, w=1.0)
line(s, 4.55, 4.54, 4.63, 5.34, color=BLACK, w=1.0)
for i in range(5):
    cx = bx0 + i * (bw + bgap) + bw / 2
    line(s, 7.26, 4.54, cx, 5.40, color=BLACK, w=0.9)

# ============================================================ 保存
pptx_path = os.path.join(EDIT, 'HMM_framework_cn.pptx')
pdf = L.save_pdf(prs, pptx_path, OUT)
final_pdf = os.path.join(OUT, 'HMM_framework.pdf')
os.replace(pdf, final_pdf)
print('PPTX:', pptx_path)
print('PDF :', final_pdf)
