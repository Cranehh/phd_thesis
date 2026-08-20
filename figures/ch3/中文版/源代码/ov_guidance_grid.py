import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from raster_overlay import overlay
CH3=os.environ.get("CH3","/mnt/user-data/uploads/2026_06 博士毕业大论文撰写/0.4【】BJTU-Thesis-Latex-main(1)/0.4【】BJTU-Thesis-Latex-main/figures/ch3")
S=[(0.02,0.02,0.47,0.135,"未加入能量引导（均值=0.2952）",0.046,0.245,0.082,0,"mm"),
   (0.52,0.02,0.965,0.135,"加入能量引导（均值=0.2145）",0.046,0.735,0.082,0,"mm")]
overlay(f"{CH3}/guidance_grid.pdf","/tmp/ch3work/中文版/guidance_grid_cn.pdf",S)
