# CLIP 零样本语义点选（教学笔记）

配套 SKILL.md Path 5 / Path 9。当不想为每个题型都训练 YOLO，或者题目语义太杂（"按顺序点击温度高的物体"），用 CLIP 做零样本图文匹配。

## 1. CLIP 原理

OpenAI 在 4 亿图文对上预训练的双塔模型：
- 图像 encoder：ResNet50 / ViT-B/32 / ViT-L/14
- 文本 encoder：Transformer
- 投影到同一 512-d 空间，cosine 相似度。

## 2. 零样本验证码点选

```python
import torch
import open_clip
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32", pretrained="laion2b_s34b_b79k"
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")

def click_by_text(image_paths: list, prompt: str) -> int:
    """给 N 个候选图片 + 一段 prompt（"a photo of bus"），返回最匹配图片索引。"""
    images = torch.stack([preprocess(Image.open(p)) for p in image_paths])
    text = tokenizer([prompt])

    with torch.no_grad():
        img_feat = model.encode_image(images)
        txt_feat = model.encode_text(text)

    img_feat /= img_feat.norm(dim=-1, keepdim=True)
    txt_feat /= txt_feat.norm(dim=-1, keepdim=True)

    sim = (img_feat @ txt_feat.T).squeeze(-1)
    return int(sim.argmax())
```

## 3. 适用题型

- reCAPTCHA "select all images with X"（X = bus / crosswalk / stairs ...）
- 极验 v4 "按提示顺序点击"（先 detect 出每个图标 → 用 CLIP 与 prompt 排序）
- 数美 / 顶象 语义点选
- FunCaptcha selector（给文字提示找物体）

## 4. 局限

- CLIP 在"细粒度类目"（如"红色公交"vs"蓝色公交"）准确率会下降。
- 中文 prompt 用 OpenCLIP 的 multilingual 版本，或翻译成英文再喂。
- 极验 v4 的 icon 多是"抽象图标"（齿轮、闪电、水滴），需 prompt engineering。

## 5. 替代方案：多模态 LLM

把整张题目截图直接喂给 GPT-4V / Gemini Vision / Claude Vision：
```
prompt: "图中要求按提示点击物体。请输出每个目标的 bbox 坐标 (x1,y1,x2,y2)。"
```
精度 > CLIP，成本 > CLIP（按 token 计费）。

## 6. 开源实现（待联网验证）

- [NEEDS_VERIFICATION] github.com/openai/CLIP
- [NEEDS_VERIFICATION] github.com/mlfoundations/open_clip
- [NEEDS_VERIFICATION] github.com/FlagAI-Open/FlagAI （中文 CLIP）
