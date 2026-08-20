import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from raster_overlay import overlay
CH3=os.environ.get("CH3","/mnt/user-data/uploads/2026_06 博士毕业大论文撰写/0.4【】BJTU-Thesis-Latex-main(1)/0.4【】BJTU-Thesis-Latex-main/figures/ch3")
S=[(0.14,0.82,0.40,0.912,"准确率",0.042,0.27,0.862,0,"mm"),(0.63,0.82,0.875,0.912,"准确率",0.042,0.752,0.862,0,"mm"),
   (0.09,0.915,0.49,0.975,"(a) 边类型准确率",0.05,0.29,0.94,0,"mm"),(0.59,0.915,0.99,0.975,"(b) 节点类型准确率",0.05,0.775,0.94,0,"mm"),
   (0.09,0.02,0.30,0.082,"均值=0.889",0.036,0.198,0.05,0,"mm"),(0.575,0.02,0.775,0.082,"均值=0.839",0.036,0.685,0.05,0,"mm")]
overlay(f"{CH3}/group2.pdf","/tmp/ch3work/中文版/group2_cn.pdf",S)
