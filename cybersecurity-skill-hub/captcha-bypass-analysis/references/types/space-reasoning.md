# 空间推理（space-reasoning）

> 配套 SKILL.md Path 9 + 极验 v4 winlinze。

## 1. 题型特征

- 提示："找出与示例图同方向的图标"
- 或："按从远到近 / 从大到小 / 从左到右 排列"
- 极验 v4 winlinze 是这类题的主力

## 2. CV 路径

1. 先 YOLO / CLIP detect 出每个候选物体
2. 再用语义模型解析"提示文字" → 推断排序规则
3. 多模态 LLM 直接给坐标列表（最稳）

## 3. 已知研究

- [NEEDS_VERIFICATION] CSDN 极验 v4 winlinze 分析
- [NEEDS_VERIFICATION] 学术：Visual Reasoning with Multimodal LLM

## 4. 防御性分析思路

- 自有站点：空间推理对真实人类难度也偏高（用户体验差），慎用。
- 配合行为评分一起部署。

## 来源

- [NEEDS_VERIFICATION] 极验官方文档
