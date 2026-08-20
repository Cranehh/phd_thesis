import matplotlib, matplotlib.pyplot as plt, os
from matplotlib import font_manager as fm
_here = os.path.dirname(os.path.abspath(__file__))
_fonts = [
 os.path.join(_here,"fonts/NotoSerifCJKsc-Regular.otf"),
 os.path.join(_here,"fonts/NotoSerifCJKsc-Bold.otf"),
 "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
 "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
 "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
]
for f in _fonts:
    if os.path.exists(f): fm.fontManager.addfont(f)
# Latin from Liberation Serif (≈Times New Roman); CJK fallback to Noto Serif CJK SC (≈宋体)
plt.rcParams['font.family'] = ['Liberation Serif', 'Noto Serif CJK SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['savefig.bbox'] = 'tight'
