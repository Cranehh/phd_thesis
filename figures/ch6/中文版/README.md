# 第六章图 · 中文版 — 说明

本文件夹为大论文**第六章 5 张图**的**中文版 PDF** 及其**可编辑源文件**，
**未改动 `figures/ch6/` 下的任何英文原图**。

日后替换：将本文件夹内**同名 PDF** 覆盖到 `figures/ch6/` 即可（建议先备份原图）。
其中 `MIMIC_framework.pdf`、`elasticity_by_state.pdf`、`elasticity_by_bundle.pdf`
三张原来只在期刊论文文件夹里、尚未放进 `figures/ch6/`，一并补齐即可编译。

## 一、5 张中文 PDF 与生成方式

| PDF | 对应图题（第六章） | 生成方式 / 源 |
|---|---|---|
| `MIMIC_framework.pdf` | 图6-1 MIMIC模型结构 | 原图**无代码/矢量源**，按英文原图重建为中文 PPT → `源文件/…/editable/MIMIC_framework_cn.pptx`，导出 PDF |
| `HMM_framework.pdf` | 图6-2 一体化建模总体框架 | 同上 → `HMM_framework_cn.pptx` |
| `elasticity_by_state.pdf` | 图6-3 状态条件弹性 | `scripts/fig_elasticity_by_state.py`（读 `data/HMM_弹性_state_conditional.csv` 重绘） |
| `elasticity_aggregate_overall.pdf` | 图6-4 套餐整体订阅弹性 | `scripts/fig_elasticity_aggregate.py`（读 `data/HMM_弹性_aggregate_subscription.csv`） |
| `elasticity_by_bundle.pdf` | 图6-5 分套餐订阅弹性 | `scripts/fig_elasticity_aggregate.py`（读 `data/HMM_弹性_aggregate_bundle.csv`） |

> 弹性图的**数值**全部来自原始弹性结果 CSV，未重跑模型，与英文原图逐一核对一致。

## 二、缺哪些图的代码/源（检查结论）

- **3 张弹性图**：Python 代码 + 数据 CSV 齐全 → 已直接改中文重绘。
- **2 张框架图（MIMIC、HMM）**：只有导出的 PDF 和一个二进制 Visio 文件
  （`…一体化建模/绘图1.vsdx`），**无代码、无可编辑矢量源** → 已按英文原图
  在 PowerPoint 中忠实重建为中文，源文件即 `editable/*.pptx`，方便日后修改。

## 三、可编辑源文件（方便日后修改）

- `源文件/ch6_cn_source/editable/MIMIC_framework_cn.pptx`、`HMM_framework_cn.pptx`
  ：用 **PowerPoint / WPS** 打开直接改文字、框线、配色，改完“文件→导出为 PDF”。
- `源文件/ch6_cn_source/scripts/*.py`：3 张弹性图的 Python 生成脚本，
  改标签/配色/数据后重跑即可。

## 四、重跑脚本须知

1. **字体**：脚本用 **Noto Serif CJK SC（≈宋体）+ Times New Roman**。Windows 上
   可改用系统 **SimSun(宋体)+Times New Roman**：编辑 `scripts/cnstyle.py` 的
   `font.family`。`scripts/fonts/` 内已附精简版 Noto Serif CJK SC（仅含所用汉字，
   供 Linux/无字体环境直接复现）。
2. **依赖**：`pip install matplotlib pandas python-pptx fonttools`。
3. **一键重跑**（在 `scripts/` 目录下）：
   ```
   python fig_elasticity_by_state.py
   python fig_elasticity_aggregate.py
   python build_MIMIC_framework.py     # 需要 LibreOffice（pptx→pdf）
   python build_HMM_framework.py
   ```
   PDF 默认输出到本 `中文版/` 目录（同名覆盖）。也可用环境变量
   `CH6_OUT` 指定输出目录、`CH6_DATA` 指定数据目录。
4. PPTX→PDF：脚本用 LibreOffice 无头转换；也可在 PowerPoint 里“导出为 PDF”，
   两者页面尺寸均与英文原图一致（不影响论文排版）。

## 五、目录结构

```
中文版/
├── MIMIC_framework.pdf                 5 张中文PDF（同名，便于替换）
├── HMM_framework.pdf
├── elasticity_by_state.pdf
├── elasticity_aggregate_overall.pdf
├── elasticity_by_bundle.pdf
├── README.md                           （本文件）
└── 源文件/ch6_cn_source/
    ├── README.md                       源码说明
    ├── scripts/                        Python 脚本 + cnstyle.py + fonts/
    ├── editable/                       两张框架图的可编辑 PPTX
    └── data/                           弹性结果 CSV（脚本输入）
```
