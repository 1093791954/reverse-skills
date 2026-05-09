# 9 格 / 16 格图片选择（Grid Image Select）

## 1. 题型描述
- 给一个大图（通常 3x3 或 4x4），按提示语「Select all images with X」点选所有包含目标的格子；或者一张大图被切片，需要选择所有包含 X 的子片。
- 代表：reCAPTCHA v2 grid、hCaptcha grid、yandex SmartCaptcha 部分场景。
- 题目类别多为：traffic lights, crosswalks, buses, bicycles, fire hydrants, motorcycles, taxis, stairs, mountains, palm trees, ...

## 2. 检测维度
- 选择正确率必须 100%（点对所有正例 + 不点错任何负例）。
- 题目可能动态刷新（点错后会换 1 张图继续）。
- 行为检测：选择间隔时长、鼠标 hover 路径。
- 后台对账号/IP/指纹累计判定。

## 3. 解题思路
- **CNN 分类**：每格独立丢进 ResNet50/EfficientNet 二分类（is_target/not）。
- **YOLO 检测**：在原大图上跑目标检测，bbox 与格子坐标交集判定。
- **CLIP / OpenCLIP**：text "a photo of a traffic light" + 每格 image embedding 余弦相似度 > 阈值。
- **多模态 LLM**：GPT-4o / Claude Vision / Gemini 直接给 prompt 返回选择。
- **数据集**：公开 captcha-dataset/recaptcha 和 hcaptcha-challenger 项目内置数据集；几十 ~ 数百类。

## 4. 已公开研究
- GitHub `Vinyzu/hCaptcha-Challenger`：图块识别 ONNX 模型仓库。
- GitHub `QIN2DIM/hcaptcha-challenger`：完整 challenger 训练集、模型、推理 demo。
- GitHub `dessant/buster`：reCAPTCHA audio bypass extension（已不再维护）。
- arxiv「reCAPTCHA Bypass with CLIP」论文系列。
- CSDN/medium 多篇 reCAPTCHA 9 格识别技术综述。

## 5. 防御性分析步骤
1. 收集挑战图（合法授权站点）按类聚合。
2. 训练分类 + CLIP 双路径，分类用于已知类、CLIP 用于开放词类。
3. 对动态刷新场景设最大尝试次数（避免被服务端识别为机器扫描）。
4. 行为：每格点击间隔 250~750ms 抖动。
5. 失败兜底：转 audio 模式（reCAPTCHA 还有，hCaptcha 已去）。

## 6. 缓解 / 趋势
- 类别从几十类扩展到上百类（开放词典）。
- 引入对抗性扰动让 CNN 失败。
- 越来越多动态题：选完后再加一张，疲劳战。
- hCaptcha 引入 motion 严校验。

## 7. 待研究
- 对抗性扰动样本的强度估计。
- 多模态 LLM 在低质量 reCAPTCHA 图（模糊/小目标）上的稳定性。
