# -*- coding: utf-8 -*-
"""中文图字体样式（与第五章 cnstyle.py 保持一致）。
Latin 用 Liberation Serif（≈Times New Roman），中文回退到 Noto Serif CJK SC（≈宋体）。
Windows 上重跑：把 font.family 改成 ['Times New Roman','SimSun'] 即可。"""
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

_here = os.path.dirname(os.path.abspath(__file__))
_fonts = [
    os.path.join(_here, "fonts/NotoSerifCJKsc-Regular.otf"),
    os.path.join(_here, "fonts/NotoSerifCJKsc-Bold.otf"),
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
]
for f in _fonts:
    if os.path.exists(f):
        fm.fontManager.addfont(f)

plt.rcParams['font.family'] = ['Liberation Serif', 'Noto Serif CJK SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['pdf.fonttype'] = 42   # 嵌入TrueType，PDF内文字可编辑/可选中
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['savefig.bbox'] = 'tight'
