# 剩余 3 张图的中文化说明（本地重跑）

guidance_district（16 个分区子图）、guidance_city（31 个属性）、population（北京市地图）
依赖模型运行时的中间数据，且地图需 `北京行政区划.shp`（在你桌面 `地图图片/北京行政区划/`）与联网底图，
无法在云端重画。请在你**本地** notebook 里，找到这三张图的绘图 cell，加上下面的字体设置并把英文标签改成中文，再重跑即可得到干净矢量中文图。

## 1) matplotlib 宋体设置（放在绘图 cell 顶部）
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimSun']      # 或 'Noto Serif CJK SC'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['pdf.fonttype'] = 42                 # 保证 PDF 里中文可嵌入
```

## 2) guidance_district / guidance_city 标签替换
- 纵轴 `Absolute Difference` → `绝对误差`
- 图例 `Guidance` → `加入引导`；`Non-Guidance` → `未加入引导`
- x 轴属性名映射（行政区尺度 5 项 / 城市尺度 31 项，按你的属性列表取用）：
```python
attr_cn = {
  'one_number':'1人户','two_number':'2人户','three_number':'3人户','four_number':'4人户','above_five_number':'5人及以上户',
  'worked_number':'户均就业人数','mean_family_size':'户均家庭规模','male_ratio':'男性占比',
  # 年龄结构（示例，按实际分组取用）
  'age_from_0_to_4':'0-4岁','age_from_5_to_9':'5-9岁','age_from_10_to_14':'10-14岁',
  'age_0_14':'0-14岁占比','age_15_64':'15-64岁占比','age_65_up':'65岁及以上占比',
  # 受教育程度
  'education_primary_or_below':'小学及以下','education_junior_high':'初中',
  'education_high_school':'高中','education_college':'大专','education_bachelor_and_above':'本科及以上',
}
# 用法：ax.set_xticklabels([attr_cn.get(x, x) for x in 原x标签])
```
> 上表按你截图里出现的英文列名整理，请对照实际列名补全后套用。

## 3) population（北京市人口分布）标签替换
- 图例 `Administrative Boundary` → `行政边界`
- 直方图子图：`Population Size` → `人口规模`；`Density` → `密度`；`Histogram` → `直方图`；`KDE` → `核密度估计`
- 色带（colorbar）标题若为英文：改为 `人口规模` / `人口数`
- 地图上"Langfang/Sanhe/…"等英文地名来自在线底图 `transbigdata.plot_map`。想要中文地名，把底图换成中文瓦片源，或改用你本地的 `北京行政区划.shp` 只画行政边界、不加英文底图。
