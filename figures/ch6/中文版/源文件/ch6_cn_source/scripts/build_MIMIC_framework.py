# -*- coding: utf-8 -*-
"""重建 MIMIC 模型结构图（中文版）→ PPTX + PDF。
版式对照英文原图 MIMIC_framework.pdf 忠实重建；文字为中文。
可在 PowerPoint/WPS 里直接改文字与框线。"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pptxlib as L
from _pptxlib import (box, textbox, bullets, line, MSO_SHAPE,
                      RGBColor, GRAY_FILL, WHITE, BLACK, DARKLINE)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('CH6_OUT', os.path.join(BASE, '..', '..', '..'))
EDIT = os.path.join(BASE, '..', 'editable')
os.makedirs(OUT, exist_ok=True)
os.makedirs(EDIT, exist_ok=True)

W, H = 9.463, 8.765          # 对应原图 681.36 x 631.08 pt
prs, s = L.new_prez(W, H)

GRP = RGBColor(0x74, 0x74, 0x74)      # 灰描边

# ============================================================ 顶部图例
ly = 0.18
line(s, 0.30, ly + 0.13, 0.72, ly + 0.13, color=BLACK, w=1.0)
textbox(s, 0.78, ly, 1.4, 0.3, '结构关系', size=11, align='l')
line(s, 2.20, ly + 0.13, 2.62, ly + 0.13, color=BLACK, w=3.2)
textbox(s, 2.68, ly, 1.4, 0.3, '测量关系', size=11, align='l')
box(s, 4.55, ly, 0.30, 0.26, '', fill=GRAY_FILL, line_color=GRP,
    shape=MSO_SHAPE.RECTANGLE, line_w=1.0)
textbox(s, 4.92, ly, 1.4, 0.3, '观测变量', size=11, align='l')
box(s, 6.55, ly - 0.02, 0.42, 0.30, '', fill=WHITE, line_color=RGBColor(0x88, 0x88, 0x88),
    shape=MSO_SHAPE.OVAL, line_w=1.0)
textbox(s, 7.05, ly, 2.0, 0.3, '不可观测变量', size=11, align='l')

# ============================================================ 左列：两个信息容器
lx, lw = 0.16, 2.72
# --- 社会经济属性变量 ---
socio = ['年龄：≤24', '年龄：25–44', '年龄：45–60', '职业：学生',
         '收入：<6000元/月', '收入：6001–20000元/月']
sy, sh_title = 0.70, 0.50
sub_h, sub_gap = 0.36, 0.063
sc_h = sh_title + len(socio) * sub_h + (len(socio) - 1) * sub_gap + 0.18
box(s, lx, sy, lw, sc_h, '', fill=WHITE, line_color=GRP, line_w=1.25,
    shape=MSO_SHAPE.RECTANGLE)
textbox(s, lx, sy + 0.08, lw, 0.38, '社会经济属性变量', size=12.5, bold=True,
        italic=True, align='c')
yy = sy + sh_title
for t in socio:
    box(s, lx + 0.16, yy, lw - 0.32, sub_h, t, fill=GRAY_FILL, line_color=GRP,
        shape=MSO_SHAPE.RECTANGLE, line_w=1.0, size=11, italic=True)
    yy += sub_h + sub_gap
socio_bottom = sy + sc_h
socio_mid_y = sy + sc_h / 2

# --- 出行模式变量 ---
travel = ['每周出行频率：≥7', '每周出行距离：≥20km', '主要出行目的',
          '每周公交频率：≥10', '每周地铁频率：≥10', '每周出租/网约车频率：≥10',
          '每周电单车频率：≥10', '每周自行车频率：≥10']
ty = socio_bottom + 0.18
tsub_h, tsub_gap = 0.36, 0.063
tc_h = sh_title + len(travel) * tsub_h + (len(travel) - 1) * tsub_gap + 0.18
box(s, lx, ty, lw, tc_h, '', fill=WHITE, line_color=GRP, line_w=1.25,
    shape=MSO_SHAPE.RECTANGLE)
textbox(s, lx, ty + 0.08, lw, 0.38, '出行模式变量', size=12.5, bold=True,
        italic=True, align='c')
yy = ty + sh_title
for t in travel:
    box(s, lx + 0.16, yy, lw - 0.32, tsub_h, t, fill=GRAY_FILL, line_color=GRP,
        shape=MSO_SHAPE.RECTANGLE, line_w=1.0, size=10.5, italic=True)
    yy += tsub_h + tsub_gap
travel_mid_y = ty + tc_h / 2
left_right_edge = lx + lw

# ============================================================ 右列：指标分组
rx, rw = 6.52, 2.80
i_item_h, i_gap, g_pad, g_gap = 0.27, 0.035, 0.10, 0.10
groups = [('CP', ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7']),
          ('PT', ['I8', 'I9', 'I10', 'I11', 'I12']),
          ('PL', ['I13', 'I14']),
          ('EN', ['I15', 'I16']),
          ('SA', ['I19', 'I20', 'I21'])]
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
gy0 = 1.02
group_centers = {}
yy = gy0
for key, items in groups:
    gh = len(items) * i_item_h + (len(items) - 1) * i_gap + 2 * g_pad
    box(s, rx, yy, rw, gh, '', fill=WHITE, line_color=GRP, line_w=1.25,
        shape=MSO_SHAPE.RECTANGLE)
    iy = yy + g_pad
    for it in items:
        box(s, rx + 0.28, iy, rw - 0.56, i_item_h, ('I' + it[1:].translate(SUB)),
            fill=GRAY_FILL, line_color=GRP, shape=MSO_SHAPE.RECTANGLE,
            line_w=1.0, size=11, bold=True, italic=True)
        iy += i_item_h + i_gap
    group_centers[key] = yy + gh / 2
    yy += gh + g_gap
ind_bottom = yy - g_gap
textbox(s, rx, gy0 - 0.46, rw, 0.4, '指标', size=13, bold=True, italic=True)

# ============================================================ 中列：潜变量（虚线框）
mx, mw = 3.62, 2.12
lat_top = 0.86
lat_bottom = ind_bottom
box(s, mx, lat_top, mw, lat_bottom - lat_top, '', fill=None,
    line_color=BLACK, line_w=1.25, shape=MSO_SHAPE.RECTANGLE, dashed=True)
textbox(s, mx, lat_top + 0.06, mw, 0.5, '潜变量', size=13, bold=True,
        italic=True)
lat = [('CP', '性价比偏好'), ('PT', '技术接受度'), ('PL', '计划性偏好'),
       ('EN', '环保意识'), ('SA', '现状满意度')]
ell_w, ell_h = 1.74, 0.86
ell_cx = mx + mw / 2
ellipse_pts = {}
for key, name in lat:
    cy = group_centers[key]
    box(s, ell_cx - ell_w / 2, cy - ell_h / 2, ell_w, ell_h, name,
        fill=WHITE, line_color=RGBColor(0x80, 0x80, 0x80), line_w=1.25,
        shape=MSO_SHAPE.OVAL, size=11.5, bold=True, italic=True)
    ellipse_pts[key] = (ell_cx - ell_w / 2, ell_cx + ell_w / 2, cy)

# ============================================================ 结构关系箭头（细）
# 社会经济容器 → 汇聚到潜变量框左侧上部
conv_a = (mx, group_centers['PT'])
for i in range(6):
    y1 = socio_mid_y - 1.0 + i * 0.4
    line(s, left_right_edge, y1, conv_a[0], conv_a[1], color=BLACK, w=0.75)
# 出行模式容器 → 汇聚到潜变量框左侧下部
conv_b = (mx, group_centers['EN'])
for i in range(8):
    y1 = travel_mid_y - 1.5 + i * 0.42
    line(s, left_right_edge, y1, conv_b[0], conv_b[1], color=BLACK, w=0.75)

# ============================================================ 测量关系箭头（粗）
for key, _ in lat:
    xl, xr, cy = ellipse_pts[key]
    line(s, xr, cy, rx, group_centers[key], color=BLACK, w=3.2)

# ============================================================ 底部：结构模型 / 测量模型
by = ind_bottom + 0.22
box(s, 0.16, by, mx + mw - 0.16, 0.5, '结构模型', fill=L.BLUE_TAB,
    line_color=None, shape=MSO_SHAPE.RECTANGLE, size=14, bold=True,
    italic=True, color=RGBColor(0x1F, 0x38, 0x64))
box(s, rx - 0.9, by, rw + 0.9, 0.5, '测量模型', fill=L.ORANGE_TAB,
    line_color=None, shape=MSO_SHAPE.RECTANGLE, size=14, bold=True,
    italic=True, color=RGBColor(0x8A, 0x40, 0x1E))

# ============================================================ 保存
pptx_path = os.path.join(EDIT, 'MIMIC_framework_cn.pptx')
pdf = L.save_pdf(prs, pptx_path, OUT)
final_pdf = os.path.join(OUT, 'MIMIC_framework.pdf')
os.replace(pdf, final_pdf)
print('PPTX:', pptx_path)
print('PDF :', final_pdf)
