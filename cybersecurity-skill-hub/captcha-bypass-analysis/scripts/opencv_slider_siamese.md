# SiameseNet 滑块缺口识别原理（教学笔记）

配套 SKILL.md Path 3 + `opencv_slider_gap.py`。当 OpenCV 模板匹配在复杂底图（高噪声、低对比度、伪缺口）下失效时，用 Siamese 孪生网络做"patch 是否同源"判别。

## 1. 问题定义

输入：背景图 `bg`（H×W）+ 滑块块 `tile`（h×w）。
目标：在 `bg` 上找一个 h×w 的 ROI，使 ROI 与 tile 是"对应缺口位置 vs 凸出图块"。
传统方法（matchTemplate）输出最大相关位置；当底图噪声大时会误报。

## 2. SiameseNet 思路

- 训练两路同结构 CNN（共享权重），输入两个 patch，输出 128 维 embedding。
- 损失函数：contrastive loss / triplet loss。同源 pair → embedding 距离小；非同源 → 距离大。
- 推理：在 bg 上滑窗 → 每个候选 ROI 与 tile 共同 forward → 取距离最小的位置。

## 3. 训练数据

- 自有站点：可主动出题 + 标记真实答案，1 万 pair 起步。
- 公开数据集：网上有"slider-captcha-dataset"（GitHub 上有若干不同站点放出的数据）。
- 数据增强：对 tile 做随机缩放 ±5%、亮度抖动 ±10%、椒盐噪声。

## 4. 模型选型

- ResNet18 backbone + 全局平均池化 + 128-d 全连接。
- 训练 30 epoch，Adam lr=1e-3，batch 64。
- 推理在 GPU 上 ~10ms / 张；CPU ~100ms / 张。

## 5. 与传统方法的对比

| 方法 | 准确率 | 速度 | 训练成本 |
|------|-------|------|---------|
| pixel diff | ~70% | ms | 0 |
| Canny + matchTemplate | ~90% | ms | 0 |
| Sobel + ROI mask | ~95% | ms | 0 |
| SiameseNet | ~98% | 10ms (GPU) | 中（1万 pair） |
| YOLO 缺口检测 | ~99% | 5ms (GPU) | 高（标注 bbox） |
| ddddocr slide_match | ~85% | 50ms (CPU) | 0（开箱即用） |

## 6. 已知开源实现（待联网验证）

- [NEEDS_VERIFICATION] github.com/sml2h3/ddddocr （slide_match 内置 onnx 模型）
- [NEEDS_VERIFICATION] github.com/Bird-Translator/captcha-slider-cnn
- [NEEDS_VERIFICATION] keras 教程：siamese network for image similarity

## 7. 部署建议

- 把训练好的模型导出 ONNX → 用 onnxruntime CPU 推理（无需带 PyTorch 环境）。
- 移动端：onnxruntime-mobile / TFLite。
