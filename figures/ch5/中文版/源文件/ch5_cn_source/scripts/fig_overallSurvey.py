# -*- coding: utf-8 -*-
"""overallSurvey 中文版：graffle画布7的文字结构(中文) + 第三部分嵌入中文SP情境 + 第四部分中文套餐框。"""
import graffle_render as G
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
D={
 'Part 1: Survey introduction & Socio-demographic information collection':'第一部分：调查简介与社会经济属性采集',
 'Part 2: Travel pattern survey':'第二部分：出行模式调查',
 'Part 3: Five SP scenarios for shifting to MaaS':'第三部分：单次出行场景下MaaS转移的5个SP情境',
 'Part 4: Five SP scenarios of MaaS bundle subscription':'第四部分：MaaS套餐订阅的5个SP情境',
 'Part 5: Attitude survey':'第五部分：态度调查',
 '• The goal of the survey':'• 调查目的','• How the response will be used':'• 回答数据的用途',
 '• The name of the organization • A series of multiple choice quizzes (e.g. gender, age, education, occupation, and income )':
   '• 调查机构名称\n• 一系列选择题（性别、年龄、\n  受教育程度、职业、收入等）',
 '• Main travel mode • Main multimodal travel mode':'• 主要出行方式\n• 主要多模式出行方式',
 '• Average travel distance on weekdays • Average travel distance on weekends':'• 工作日平均出行距离\n• 周末平均出行距离',
 '• Main trip purpose • Trip frequency per week':'• 主要出行目的\n• 每周出行频率',
 '• Introduce MaaS':'• 介绍MaaS','• Two scenarios with and without MaaS are required to respond':'• 需回答含MaaS与不含MaaS两个情境',
 'Connection: Travel demand survey to help respondents review travel needs':'衔接：出行需求调查，帮助受访者回顾出行需求',
 '• Weekly trip frequency for five travel modes':'• 五种方式的每周出行频率','• Monthly travel cost estimation':'• 月度出行花费估计',
 '• Respondents are required to make a choice between PAYG and one out of four MaaS bundles.':'• 受访者需在按次付费与四种MaaS套餐间做出选择',
 '• Five-point Likert scale is applied':'• 采用5级李克特量表','• 25 attitudinal statements are required to respond':'• 需回答25条态度陈述',
}
bundles=[('公交优先','64 元/月',['不限次公交','地铁 10 次/月','不限次共享单车','共享电动车 0 次','出租/网约车 0 km']),
 ('地铁畅行','184 元/月',['不限次公交','地铁 60 次/月','不限次共享单车','共享电动车 0 次','出租/网约车 0 km']),
 ('优惠出租','768 元/月',['不限次公交','地铁 30 次/月','不限次共享单车','共享电动车 12 次','出租/网约车 350 km']),
 ('全能畅行','1245 元/月',['不限次公交','地铁 90 次/月','不限次共享单车','共享电动车 24 次','出租/网约车 520 km']),
 ('按次付费','用后付费',['出行后按次付费'])]
def extra(ax):
    # Part 3 scenario image (graffle bounds ~ x613-1133,y431-680)
    try:
        img=mpimg.imread('ppt/spex_thumb-1.png')
        ax.imshow(img, extent=[615,1131,678,433], aspect='auto', zorder=5)
    except Exception as e: print('img err',e)
    # Part 4 bundle boxes (x629-1117,y791-978)
    x0,x1,y0,y1=629,1117,793,976; n=5; gap=6
    bw=(x1-x0-gap*(n-1))/n
    cols=['#DCE6F1','#DCE6F1','#DCE6F1','#DCE6F1','#EAEAEA']
    for i,(nm,pr,items) in enumerate(bundles):
        bx=x0+i*(bw+gap)
        ax.add_patch(Rectangle((bx,y0),bw,y1-y0,facecolor=cols[i],edgecolor='#4472A4',lw=0.8,zorder=6))
        ax.text(bx+bw/2,y0+9,nm,ha='center',va='top',fontsize=8,fontweight='bold',color='#1F3864',zorder=7)
        ax.text(bx+bw/2,y0+26,pr,ha='center',va='top',fontsize=7.5,color='#C00000',zorder=7)
        for j,it in enumerate(items):
            ax.text(bx+bw/2,y0+42+j*22,it,ha='center',va='top',fontsize=5.6,zorder=7)
G.render(7, D, 'overallSurvey',(9.5,13), fs=9, extra=extra, skip_images=True)
