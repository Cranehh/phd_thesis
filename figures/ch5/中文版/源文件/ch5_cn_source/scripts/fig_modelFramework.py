import graffle_render as G
D={
 'Alternative':'备选方案','Class 1: MaaS Skeptics':'类别1：MaaS存疑者','Class 2: MaaS Explorers':'类别2：MaaS乐观者',
 'Measurement relationship':'测量关系','Observed variable':'观测变量','Structural relationship':'结构关系',
 'Unobserved variable':'不可观测变量','Willingness to shift to MaaS':'MaaS转移意愿',
 'MaaS bundle subscription behavior':'MaaS套餐订阅行为','Shifting to MaaS behavior':'转移至MaaS行为',
 'Attitudinal statements':'态度陈述','Available taxi/ride-sourcing':'可用出租/网约车','Bargin hunter':'性价比追求者',
 'Bundle attributes':'套餐属性','Bus First':'公交优先','Context avariables in one-trip scenarios':'单次出行情境变量',
 'Departure time':'出发时间','Environmentalist':'环保主义者','In-metro time':'地铁内时间','Metro Access':'地铁畅行',
 'Non-shifting':'不转移','Overall satisfaction':'总体满意度','PAYG':'按次付费(PAYG)','PT-oriented nest':'公交导向巢',
 'Planner':'计划性','Preferred MaaS options':'偏好的MaaS选项','Price':'价格','Pro-technology':'技术偏好',
 'Shifting to M1':'转移至M1','Shifting to M2':'转移至M2','Shifting to M3':'转移至M3','Shifting to M4':'转移至M4',
 'Socio-demographic variables':'社会经济属性变量','Travel distance':'出行距离','Travel pattern variables':'出行模式变量',
 'Trip time':'出行时间','Ultra Access':'全能畅行','Value Taxi':'优惠出租',
}
G.render(1, D, 'modelFramework',(15,7), fs=8)
