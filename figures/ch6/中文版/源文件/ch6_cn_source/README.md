# ch6_cn_source — 第六章中文图源文件

第六章 5 张图的中文版源文件。目录：

- `scripts/` — Python 生成脚本
  - `cnstyle.py` — 中文字体样式（Noto Serif CJK SC ≈宋体 + Times New Roman）
  - `_pptxlib.py` — python-pptx 构图小工具（框架图用）
  - `fig_elasticity_by_state.py` — 图6-3 状态条件弹性（→ `elasticity_by_state.pdf`）
  - `fig_elasticity_aggregate.py` — 图6-4 / 图6-5 聚合弹性
    （→ `elasticity_aggregate_overall.pdf` + `elasticity_by_bundle.pdf`）
  - `build_MIMIC_framework.py` — 图6-1 MIMIC 结构（→ pptx + `MIMIC_framework.pdf`）
  - `build_HMM_framework.py` — 图6-2 HMM 框架（→ pptx + `HMM_framework.pdf`）
  - `fonts/` — 精简版 Noto Serif CJK SC（Regular/Bold，仅含所用汉字）
- `editable/` — 两张框架图的可编辑 PPTX（PowerPoint/WPS 打开改文字）
  - `MIMIC_framework_cn.pptx`、`HMM_framework_cn.pptx`
- `data/` — 弹性结果 CSV（弹性图输入，来自 `弹性分析结果/`）
  - `HMM_弹性_state_conditional.csv`
  - `HMM_弹性_aggregate_subscription.csv`
  - `HMM_弹性_aggregate_bundle.csv`

## 依赖

```
pip install matplotlib pandas python-pptx fonttools
# 框架图 pptx→pdf 需要 LibreOffice（soffice）；或在 PowerPoint 里手动导出 PDF
```

## 重跑（在 scripts/ 目录）

```
python fig_elasticity_by_state.py
python fig_elasticity_aggregate.py
python build_MIMIC_framework.py
python build_HMM_framework.py
```

- 输出默认写到本包外层的 `中文版/`（同名 PDF 覆盖）。
  可用 `CH6_OUT=/some/dir` 改输出目录、`CH6_DATA=/some/dir` 改数据目录。
- 字体：默认走 `fonts/` 内精简字体；Windows 换系统字体改 `cnstyle.py` 的
  `plt.rcParams['font.family']`（如 `['Times New Roman','SimSun']`）。
  框架图的中文字体在 PPTX 内设为 “Noto Serif CJK SC”，Windows PowerPoint 里
  如无此字体，可全选文字改成“宋体”。

## 说明

- 弹性图**不重跑模型**，只读 CSV 重绘，数值与英文原图一致。
- 框架图**无原始代码/矢量源**（原为 Visio 二进制），此处按英文原图 PDF 逐块
  重建为中文 PPTX；页面尺寸与英文原图一致（MIMIC 681×631pt、HMM 809×489pt），
  不影响论文 `\includegraphics[width=\textwidth]` 排版。
- 收入档 “6001–20000 元/月”：英文原图 MIMIC 图中写作 “6001-200000”，疑为笔误，
  已按正文表格更正为 20000。
