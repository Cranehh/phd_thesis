# 第三章插图中文化 — 源文件说明

本目录是把第三章 12 张图从英文改为中文（宋体）的**可编辑源文件**。生成的中文 PDF 在上一级 `中文版/` 文件夹。原始英文图（`figures/ch3/*.pdf`）一律未改动。

## 三种方法
1. **示意图**（framework/backbone/energy）——`diagram_build.py`
   在原 PDF 矢量图上"去英文、叠中文"，中文用 matplotlib 的 **Type3** 方式嵌入（各阅读器都能正常显示，不会乱码）。输出仍是矢量图。每个标签用显式坐标定位；技术缩写（MLP、adaLN、Q/K/V、HGT、VAE 等）按惯例保留英文。
2. **消融图**（ablation1 家庭级 / ablation2 个人级）——`ablation.py`
   直接用 `数据/` 里的 CSV **重画**，纯矢量中文。四组：居民出行调查数据 / HiDiT（完整模型）/（无图结构模块）/（无画像条件），对数纵轴。
3. **位图贴中文**（samplingzero/group/group2/guidance_grid）——`ov_*.py` + `raster_overlay.py`
   这些图的图身是位图（由模型运行结果生成、云端无法干净重画），故在原图上遮住英文、叠加清晰中文。真实数据不变。

## 文件
- `figstyle.py`     中文字体配置（默认 Noto Serif CJK SC 近似宋体）
- `diagram_build.py` 示意图：framework/backbone/energy
- `ablation.py`      消融图：ablation1/ablation2
- `translate_diagram.py` 示意图自动分组翻译引擎（备用）
- `raster_overlay.py` 位图贴中文引擎
- `ov_samplingzero.py / ov_group.py / ov_group2.py / ov_guidance_grid.py` 四张位图贴字脚本
- `待本地重跑_guidance_population.md` 剩余 3 张（见下）的中文化说明

## 想用"真·宋体"
云端用的是 Noto Serif CJK SC（宋体风格）。若要 Windows 宋体：把 `simsun.ttc` 放到本目录，并把 `figstyle.py` 里的 `FP_R`/`FP_B` 指向它即可（示意图脚本会自动生效）。

## 依赖与运行
```
pip install pymupdf matplotlib pandas pillow fonttools
export CH3="…/figures/ch3"          # 原英文图目录
export OUTDIR="…/figures/ch3/中文版"  # 输出目录
export DATA="…/数据"                 # 消融图数据（含 raw_*/results_* CSV）
python diagram_build.py    # 3 张示意图
python ablation.py         # 2 张消融图
python ov_samplingzero.py  # 依次跑各 ov_*.py
```

## 还差 3 张（guidance_district / guidance_city / population）
它们依赖"跑模型时算出来的中间数据"（生成栅格人口、分尺度边际误差等），且地图还需桌面上的 `北京行政区划.shp` 和联网底图，云端无法重画。请按 `待本地重跑_guidance_population.md` 在你本地 notebook 里给这三张的绘图 cell 加中文字体并替换标签后重跑。
