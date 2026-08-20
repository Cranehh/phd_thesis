# 第五章图 · 中文版 — 说明

本文件夹为大论文第五章14张图的**中文版PDF**及其**可编辑源文件**，未改动 ch5 下的任何原图。
日后替换：将本文件夹内同名PDF覆盖到 `figures/ch5/` 即可（建议先备份）。

## 一、14张中文PDF与生成方式

| PDF | 图题 | 生成方式 / 源 |
|---|---|---|
| staged_framework.pdf | 分阶段建模总体框架 | 原图已是中文，直接沿用 |
| travelPattern.pdf | 样本出行模式特征 | `绘图脚本/fig_travelPattern.py`（读 数据/聚类csv 重绘） |
| IndexDistribution_density.pdf | 转移意愿指数核密度 | `replot_vector.py`（从原矢量PDF提取曲线+中文重绘） |
| classIndexDistribution_density.pdf | 两类别指数核密度 | 同上 |
| sentiveanalysis.pdf | 出行时间灵敏度 | 同上 |
| scenarioSensitiveAnalysis.pdf | 分距离灵敏度 | `fig_scenarioSensitiveAnalysis.py`（原图为位图，按颜色提取三线重绘） |
| priceSensitivity.pdf | 价格灵敏度 | `fig_priceSensitivity.py`（读 数据/价格灵敏度_LCLV.csv） |
| aggregateE.pdf | 价格集计点弹性 | `fig_aggregateE.py`（读 数据/aggE_results_forCN.csv） |
| aggregateE2.pdf | 非价格集计点弹性 | `fig_aggregateE2.py`（读 数据/非价格因素csv） |
| modelFramework_shift.pdf | 转移建模框架 | 在Visio源(绘图1)中译中文→见 可编辑源文件/绘图1_中文版.fodg 第11页 |
| alternativeDecision.pdf | 备选方案示意图 | 同上，绘图1_中文版.fodg 第2页 |
| modelFramework.pdf | 套餐订阅模型框架 | `fig_modelFramework.py`（按OmniGraffle坐标重建为中文矢量图） |
| overallSurvey.pdf | 问卷总体设计框架 | `fig_overallSurvey.py`（重建结构+嵌入中文SP情境+中文套餐框） |
| spExample.pdf | SP实验界面示例 | 在PPT中译中文→见 可编辑源文件/spExample_中文版.pptx |

## 二、可编辑源文件（方便日后修改）
- `可编辑源文件/绘图1_中文版.fodg`：Visio原图转成的可编辑矢量图（用 LibreOffice Draw 打开），含 modelFramework_shift(第11页)、alternativeDecision(第2页)。改完“文件→导出为PDF”即可。
- `可编辑源文件/spExample_中文版.pptx`：SP情境幻灯片（用 PowerPoint 打开直接改文字），导出PDF即为 spExample。
- `绘图脚本/*.py`：各数据图/框架图的Python生成脚本，改标签/配色/数据后重跑即可。

## 三、重跑脚本须知
1. 字体：脚本用 **Noto Serif CJK SC（宋体风格）+ Liberation Serif（Times风格）**。Windows可改用系统 **SimSun(宋体)+Times New Roman**：编辑 `cnstyle.py` 的 `font.family`。
2. 依赖：`pip install matplotlib pandas pdfminer.six pillow striprtf python-pptx`。
3. 数据路径：脚本内数据路径需按本机实际位置调整（数据文件见 `数据/`）。
4. aggregateE 的数据 `aggE_results_forCN.csv` 由原始 `分弹性和总弹性_LCLV.csv`(454MB) 聚合而来（聚合逻辑同notebook cell30-33）。

## 四、两处可继续微调（非必须）
- overallSurvey 第一部分三个小框文字略有靠近，可在脚本里微调坐标。
- spExample 目前为“含MaaS情境”单幅；如需原图的“无MaaS+含MaaS”两步式两幅拼图，可告知我补做。

## 五、本压缩包目录（全英文命名，避免Windows乱码）
- `scripts/`：全部Python生成脚本
- `editable/Visio_cn_...fodg`：Visio源转中文可编辑图（LibreOffice Draw打开）→ 第11页=modelFramework_shift，第2页=alternativeDecision
- `editable/spExample_cn.pptx`：SP情境幻灯片（PowerPoint打开改文字）
- `data/`：脚本所需数据（原中文名→英文名对照）
  - price_sensitivity_LCLV.csv ← 价格灵敏度_LCLV.csv
  - elasticity_nonprice_LCLV.csv ← 分弹性和总弹性_非价格因素_LCLV.csv
  - people_cluster_attr.csv ← MaaS被调查者聚类加个人属性加态度.csv
  - aggE_results_forCN.csv（由454MB的 分弹性和总弹性_LCLV.csv 聚合得到）
