# -*- coding: utf-8 -*-
import re, shutil
src='odg/绘图1.fodg'
x=open(src,encoding='utf-8').read()
# English span-text -> Chinese  (exact span-content match). Longest first.
D={
 # ---- page 11: modelFramework_shift ----
 'Keep the choice without MaaS: private car':'无MaaS时维持选择：私家车',
 'Keep the choice without MaaS: taxi':'无MaaS时维持选择：出租/网约车',
 'Mode choice without MaaS: taxi':'无MaaS时方式选择：出租/网约车',
 'Mode choice without MaaS: PT':'无MaaS时方式选择：公共交通',
 'Structural equation model ':'结构方程模型',
 'Discrete choice model':'离散选择模型',
 'Structural Relationship':'结构关系','Measurement Relationship':'测量关系',
 'Observed Variables':'观测变量','Unobserved Variables':'不可观测变量',
 'Trip Frequency of Modes':'各方式出行频率','Vehicle Ownership':'车辆拥有',
 'Trip distance':'出行距离','Trip frequency':'出行频率',
 'In-metro time':'地铁内时间','Departure time':'出发时间','Trip time':'出行时间',
 'Travel habit':'出行习惯','Cross-scenario':'跨情境','Context':'情境属性',
 'Latent class':'潜在类别','Class 1':'类别1','Class 2':'类别2',
 'Non-shifting':'不转移','Utility':'效用',
 'Shifting to M1':'转移至M1','Shifting to M2':'转移至M2','Shifting to M3':'转移至M3','Shifting to M4':'转移至M4',
 'Education':'受教育程度','Occupation':'职业','Income':'收入','Age':'年龄','Gender':'性别',
 'Individual-':'个体','related':'相关','attributes':'属性',
 'Primary ':'主要','travel':'出行','mode':'方式',
 'Latent':'潜','variable':'变量','Quality ':'性价比','seeker':'偏好',
 'Attitudinal':'态度','statements':'陈述','LOS':'服务水平','variables':'变量',
 # ---- page 2: alternativeDecision ----
 'Choice result of the scenario without MaaS':'无MaaS情境的选择结果',
 'Choice result of the scenario with MaaS:':'含MaaS情境的选择结果：',
 'Choice result of the scenario with MaaS':'含MaaS情境的选择结果',
 'Shifting to MaaS':'转移至MaaS','behavior':'行为','Non-Shifting':'不转移',
 'Private car/ Taxi/ PT':'私家车/出租网约车/公交',
}
for en in sorted(D, key=len, reverse=True):
    x=x.replace(f'>{en}</text:span>', f'>{D[en]}</text:span>')
open('odg/绘图1_cn.fodg','w',encoding='utf-8').write(x)
print("wrote cn fodg; remaining sample checks:",
      x.count('Quality'), x.count('Cross-scenario'), x.count('转移至M1'), x.count('潜在类别'))

# --- robust substring pass for long distinctive phrases (handles colon/space variants) ---
x=open('odg/绘图1_cn.fodg',encoding='utf-8').read()
for en,cn in [
 ('Choice result of the scenario without MaaS','无MaaS情境的选择结果'),
 ('Choice result of the scenario with MaaS','含MaaS情境的选择结果'),
 ('Private car/ Taxi/ PT','私家车/出租网约车/公交'),
]:
    x=x.replace(en,cn)
open('odg/绘图1_cn.fodg','w',encoding='utf-8').write(x)
print("post-fix english remnants:", x.count('Choice result'), x.count('scenario with'))
