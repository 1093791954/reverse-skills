# 语义点选（semantic-text）

> 配套 SKILL.md Path 5 + Path 9。

## 1. 题型特征

- 提示："点击图中所有红色的物品" / "点击温度最高的物品"
- 强语义依赖，单纯目标检测不够，需"语义理解"
- 多用于极验 v4、数美高难版本

## 2. CV 路径

- 多模态 LLM（GPT-4V / Gemini / Claude Vision）直接喂题目截图 + 提示，让它返回坐标
- CLIP 零样本兜底
- 自训练专用模型（成本高）

## 3. 已知研究

- [NEEDS_VERIFICATION] 极验 / 数美 语义点选分析文章
- [NEEDS_VERIFICATION] OpenAI GPT-4V 验证码识别评测

## 4. 防御性分析思路

- 自有站点：评估多模态 LLM 攻击下的准确率；适度增加题型多样性。
- 监控"短时间内多次失败后忽然全对"模式（疑似攻击者拿到 LLM 后接入）。

## 来源

- [NEEDS_VERIFICATION] 多家厂商文档
