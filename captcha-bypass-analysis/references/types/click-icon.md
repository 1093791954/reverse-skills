# 点选图标（click-icon）

> 配套 SKILL.md Path 5 + 极验 v4 icon-crush。

## 1. 题型特征

- 提示文字：「请按顺序点击：齿轮、闪电、水滴」
- 图中显示乱序的 N 个抽象图标
- 用户按提示顺序点击

代表厂商：极验 v4 icon、数美、顶象。

## 2. CV 路径

- YOLO 训练抽象图标类（齿轮 / 闪电 / 水滴 / 心 / 星 / ...）
- CLIP 零样本（中文 prompt 用 multilingual CLIP）
- 多模态 LLM 兜底

详见 `scripts/click_yolo_demo.md`、`scripts/click_clip_demo.md`。

## 3. 已知研究 / 待研究

- [NEEDS_VERIFICATION] 多篇 CSDN 极验 v4 icon 还原文章
- 抽象图标的图像增强方式（颜色变化、形变）

## 来源

- [NEEDS_VERIFICATION] 多家厂商文档
