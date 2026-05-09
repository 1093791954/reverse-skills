# OCR / 模板匹配 / 缺口检测（CV 基线）

## 1. 工具与库
| 工具 | 用途 | 备注 |
|------|------|------|
| ddddocr (sml2h3) | 文本/滑块/点选 | 一站式，准确率 80~95% |
| Pillow + OpenCV | 模板匹配/Canny/Sobel | 基础 |
| YOLOv5/v8 (ultralytics) | 目标检测 | 点选/滑块缺口 95%+ |
| DBNet / DBNet++ + CRNN | 通用 OCR 检测+识别 | 中文好 |
| PaddleOCR | 中文 OCR | 工业级 |
| EasyOCR | 80+ 语言 | 一键 |
| Tesseract | 经典 | 中文略弱 |
| MMOCR | 多模型 | 灵活 |
| Chandra OCR | 中日韩多语 | 视觉语言模型 + vLLM |
| CLIP / OpenCLIP | 图文匹配 | 语义点选 |
| MobileCLIP | 端侧轻量 CLIP | 速度优先 |
| Whisper | 音频 ASR | reCAPTCHA audio |
| SiameseNet / ArcFace | 文字配对 | 点选第二阶段 |

## 2. 滑块缺口检测
- ddddocr `slide_match(target, background)`：返回 `{target_y, target, target_w, target_h}`，距离取 `target[0]`。
- ddddocr `slide_comparison(target_byte, background_byte)`：基于像素差对比，对纯色背景效果好。
- OpenCV：`bg = cv2.imread(...,0); tpl = cv2.imread(...,0); cv2.matchTemplate(bg, tpl, cv2.TM_CCOEFF_NORMED)` 取 `argmax`。
- Canny + Sobel：背景图先过滤再找最暗块。
- 自训练 YOLO：500~2000 张样本即可达 95%+。

## 3. 文字点选
两阶段：
1. **检测**：YOLOv5/v8 输出每个候选 bbox（汉字/字母/图标）。
2. **匹配**：把提示语与候选 bbox 截图通过 ArcFace/Siamese 嵌入向量做距离匹配。
- 数据集 1k~10k 张，YOLO 单类 mAP 95%+；ArcFace 三元组损失 + InsightFace 训练。
- ddddocr 1.3 起内置点选检测能力。

## 4. 9 格图片识别
- 类别公开（数十类）：直接 ResNet50 二分类。
- 类别开放：CLIP text-image 余弦相似度 > 0.25。
- LLM 多模态（GPT-4o / Gemini 2.5 / Claude 3.5 Vision）零样本，准确率 90%+。

## 5. 已公开研究
- CSDN「Python 实战：用 ddddocr 轻松破解滑动验证码」(153949909)。
- CSDN「保姆级教程：用 Python+ddddocr 搞定超星学习通滑块验证码」(159631946)。
- CSDN「DdddOcr 不止能识别验证码？实测它的滑块检测与目标定位能力」(159880166)：slide_match / slide_comparison / det 三种能力。
- CSDN「文字点选验证码识别 (上)-YOLO 位置识别」：抖音点选案例。
- CSDN「YOLOv5 文字点选验证码识别」：YOLOv5 + InsightFace + Triplet + ONNX + OpenVINO 量化。
- CSDN「告别手动点选！用 ddddocr 1.3 搞定汉字验证码自动识别」：CNN+改进 YOLO。
- CSDN「从零构建文字点选验证码识别模型：YOLO 检测与特征匹配实战」：YOLO + ArcFace 64 维向量 + 余弦。
- CSDN「2026 点选验证码终极实战：OCR+语义匹配双路径」：DBNet++ / 改进 CRNN / YOLOv8s / MobileCLIP / 真人行为模拟 / 轻量化 ONNX，55% → 95%+。
- CSDN「【实战指南】高效中文点选验证码识别方案解析」：YOLOv5/v8/SSD 对比 + Focal Loss + NMS。
- CSDN「Chandra OCR 多语言 OCR 展示」：中日韩 + 视觉语言模型 + vLLM。
- CSDN「OpenCV 与图像处理学习四：图像几何变换」：基础 warpAffine、resize 用法。
- ddddocr GitHub README 与文档。

## 6. 防御性分析步骤
1. baseline：先用 ddddocr 测一遍，记录 ↑/↓ 的题型。
2. 不达标 → 训自家 YOLO 或细分模型。
3. 准备 LLM 兜底（成本高），混合策略 90% 靠 YOLO + 10% 兜底。
4. 注意提交参数加密（ddddocr 只解决 CV，不解决参数还原）。

## 7. 待研究
- 抗对抗扰动训练（使用真实失败样本扩增）。
- 端到端 ViT 替代 YOLO+ArcFace 两阶段方案。
- LLM 视觉模型在小目标点选的鲁棒性。
