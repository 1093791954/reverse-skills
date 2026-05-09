# 深度学习模型选型（deeplearning-models）

> 配套 SKILL.md Path 3 / Path 5 / Path 8 / Path 9。

## 1. 模型类型 vs 任务

| 任务 | 推荐模型 | 备注 |
|------|---------|------|
| 滑块缺口距离 | YOLOv8 / SiameseNet | 自训成本中 |
| 点选目标检测 | YOLOv8 / Detectron2 | 类别数 ≤ 80 用 v8n |
| 中文 OCR | PaddleOCR / CRNN | 准确率高 |
| 通用 OCR | ddddocr / EasyOCR | 开箱即用 |
| 旋转角度 | ResNet18 回归 / VGG 分类 | 简单任务 |
| 3D 物体方向 | PointNet / 多视角 CNN | 复杂 |
| 零样本图文 | CLIP / open_clip | 不用训练 |
| 强语义题 | GPT-4V / Gemini / Claude Vision | 按 token 计费 |
| 鼠标轨迹生成 | TimeGAN / LSTM-GAN | 训练慢 |
| 音频识别 | Whisper (tiny~large) | 干净音频准确率高 |

## 2. 训练框架

- PyTorch + ultralytics（YOLOv8）
- PaddlePaddle（PaddleOCR）
- Tensorflow / Keras（CRNN）
- ONNX 部署

## 3. 数据集来源（自有）

- 自有站点采集 + 标注
- 公开数据集（ICDAR / COCO / 自定义）
- LLM 合成数据（GPT-4V 标注 → 微调小模型）

## 4. 模型部署

- 桌面 demo：PyTorch + Python
- 服务端：ONNX + onnxruntime
- 移动端：TFLite / NCNN / MNN
- WebAssembly：onnxruntime-web

## 5. 已知研究

- [NEEDS_VERIFICATION] github.com/sml2h3/dddd_trainer
- [NEEDS_VERIFICATION] github.com/ultralytics/ultralytics
- [NEEDS_VERIFICATION] github.com/PaddlePaddle/PaddleOCR

## 来源

- [NEEDS_VERIFICATION] 上述开源项目 README

---

## 6. R5 追加：DeepSeek-OCR + LLM 视觉验证码

> 2026-05 趋势观察：以 **DeepSeek-OCR / GPT-4V / Gemini Vision** 为代表的多模态大模型，正在重写"语义点选 / 复杂逻辑题"的解法。
> 本节归档 R5 (CSDN + GitHub) 命中的关键资料。

### 6.1 DeepSeek-OCR（开源、端侧友好）

- 命中量级：CSDN 325 篇专题，**几乎全部直接绑定"验证码识别"主题**
- 模型规格：3B 参数级 OCR 视觉模型，单图 < 200ms（A10）
- 优势：开源权重，可本地推理；中文/数字/汉字识别准确率追平商用 OCR
- 劣势：**几何理解弱** — 对滑块缺口位置回归仍需配合 YOLOv8

**适用题型**：
- ✅ 字符识别（含变形、扭曲、加噪声）
- ✅ 中文文本验证码
- ✅ 表格/票据型综合验证
- ⚠️ 点选汉字（需要二次坐标校正）
- ❌ 滑块距离（不擅长几何回归）

**已存档 articleid**：158309744 / 157855732 / 158111453 / 158113017 / 157786719 / 157886837 / 157755402 / 158026484（连号 8 篇 R5 命中文章）

### 6.2 GPT-4V（GPT-4 Vision，OpenAI）

- 命中量级：CSDN 1914 篇（很多综述）
- 关键论文/事件：
  - 多模态大模型识破 GPT-4V 验证码（CSDN 133801689）— 报道"AI 搞定谷歌验证码"
  - GPT-4o 验证码挡不了，最强 SOTA 模型成功率近 40%（CSDN 148472089）
  - GPT-4V 学着用键盘鼠标玩游戏（CSDN 134225632）— 与轨迹生成相关

**特点**：
- 商用 API，按 token 计费（$0.01/图）
- 强语义理解：能解"找出图中所有交通信号灯" / "把这些图片按时间排序"等强逻辑题
- **限制**：OpenAI 安全策略对"验证码 / CAPTCHA"提示词有时直接拒答，需要包装

**适用题型**：
- ✅ reCAPTCHA v2 image 强语义（消火栓/红绿灯/出租车）
- ✅ Arkose Labs 3D 旋转 + 拼图组合题
- ✅ hCaptcha 多步组合题
- ⚠️ 需要做提示词包装，避免触发安全过滤

### 6.3 Gemini Vision（Google）

- 命中量级：CSDN 124 篇，**包含 1 篇 hCaptcha 专题**（160721862：AI 视觉模型实战 hCaptcha）
- 关键对比：
  - Qwen3-VL vs Gemini-Pro-Vision（CSDN 157002267）— 国产模型对标
  - Gemini-1.5-Pro vs Qwen3-VL（CSDN 157863882）

**特点**：
- 长上下文（1M token）→ 可一次塞入完整滑块系列截图做时间序列分析
- 免费额度高于 GPT-4V（开发期友好）
- 多语种识别比 GPT-4V 略弱，但在数学/几何/物理题型上更强

### 6.4 三模型对比矩阵

| 维度 | DeepSeek-OCR | GPT-4V | Gemini Vision |
|------|-------------|--------|---------------|
| 部署 | 本地（开源） | 商用 API | 商用 API |
| 单次成本 | ~$0.0002（电费） | ~$0.01 | ~$0.005 |
| 延迟 | 200ms | 2-5s | 1-3s |
| 字符 OCR | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 强语义题 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 几何回归 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 反审查 | 无 | 易触发拒答 | 中等 |

### 6.5 推荐组合

- **批量字符 OCR**：DeepSeek-OCR（成本最低）
- **复杂语义场景**：GPT-4V / Gemini Vision（按预算选）
- **极致准确率**：DeepSeek-OCR 初筛 + GPT-4V 二次确认
- **新型题型探路**：Gemini Vision（长上下文一次看完整流程）

### 6.6 与本技能其他笔记的关联

- `types/click-character.md` / `types/click-icon.md`：点选题用 Gemini/GPT-4V 一步定位
- `types/space-reasoning.md`：空间推理题（让多模态 LLM 直接给坐标）
- `types/3d-object-select.md`：3D 物体方向已是大模型擅长场景
- `vendors/hcaptcha.md`：hCaptcha 强语义题首选 LLM 视觉
- `techniques/ocr-template-match.md`：传统 OCR 与本节模型形成"快慢两挡"

## 7. R5 追加来源

- CSDN 158309744 / 157855732 / 158111453 / 158113017 / 157786719 / 157886837 / 157755402 / 158026484（DeepSeek-OCR 验证码系列）
- CSDN 133801689 / 148472089 / 134225632 / 133638554（GPT-4V 验证码系列）
- CSDN 160721862（Gemini AI 视觉模型实战 hCaptcha）
- CSDN 157002267 / 157863882（Qwen3-VL vs Gemini 对比）
