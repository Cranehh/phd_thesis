import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from raster_overlay import overlay
CH3=os.environ.get("CH3","/mnt/user-data/uploads/2026_06 博士毕业大论文撰写/0.4【】BJTU-Thesis-Latex-main(1)/0.4【】BJTU-Thesis-Latex-main/figures/ch3")
S=[(0.31,0.925,0.71,1.0,"Wasserstein距离",0.044,0.51,0.958,0,"mm"),
   (0.66,0.10,0.995,0.315,"VAE-BN正则化",0.033,0.665,0.147,0,"lm"),
   (0,0,0,0,"未加入正则化",0.033,0.665,0.202,0,"lm"),
   (0,0,0,0,"居民出行调查数据",0.033,0.665,0.257,0,"lm"),
   (0.008,0.30,0.07,0.66,"密度",0.044,0.028,0.48,90,"mm")]
overlay(f"{CH3}/samplingzero.pdf","/tmp/ch3work/中文版/samplingzero_cn.pdf",S)
