# 3D 选物（3d-object-select）

> 配套 SKILL.md Path 8 + Arkose FunCaptcha。

## 1. 题型特征

- 一个 3D 渲染的物体（roller / cube / animal）
- 用户旋转/选择正确的方向 / 类别
- FunCaptcha 主要题型之一

## 2. CV 路径

- 3D rollball：方向梯度直方图 / 渲染 360° 候选 frame + VGG 相似度
- 3D selector：YOLO + 类别匹配
- CLIP 零样本兜底

## 3. 已知研究

- [NEEDS_VERIFICATION] github.com 上若干 funcaptcha-3d-rotate repo
- [NEEDS_VERIFICATION] arxiv 论文：CNN-based 3D orientation estimation

## 来源

- [NEEDS_VERIFICATION] Arkose Labs docs
