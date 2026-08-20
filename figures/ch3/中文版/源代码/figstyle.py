# 中文（宋体）绘图字体配置 —— 供第三章各图脚本 import
# 云端用 Noto Serif CJK SC 近似宋体；如需真·宋体，把 simsun.ttc 放同目录并改 FP_R/FP_B 即可
import matplotlib, matplotlib.font_manager as fm, os
matplotlib.rcParams['pdf.fonttype']=3   # 关键：Type3 嵌入，各PDF阅读器都能正常显示中文
FP_R=os.environ.get("SC_R","/tmp/fonts/NotoSerifSC-Regular.ttf")
FP_B=os.environ.get("SC_B","/tmp/fonts/NotoSerifSC-Bold.ttf")
fm.fontManager.addfont(FP_R); fm.fontManager.addfont(FP_B)
propR=fm.FontProperties(fname=FP_R); propB=fm.FontProperties(fname=FP_B)
def apply():
    matplotlib.rcParams['font.family']=propR.get_name()
    matplotlib.rcParams['axes.unicode_minus']=False
    matplotlib.rcParams['mathtext.fontset']='cm'
