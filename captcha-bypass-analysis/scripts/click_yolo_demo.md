# YOLOv8 点选目标检测（教学笔记）

配套 SKILL.md Path 5 + Path 9。

## 1. 适用场景

- 极验 v3 点选汉字 / v4 icon
- reCAPTCHA v2 9 格 / 4×4 图块（"select all bus"）
- 顶象 / 数美 / 网易易盾 点选题

## 2. 数据集准备

- 自有站点 / 受邀渗透：自己跑 captcha 接口，拿到题图 + 答案。
- 标注工具：labelImg / labelme / Roboflow。
- 至少 500 张/类，类别 ≤ 80 时 YOLOv8n（nano）足够。

## 3. 训练

```python
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="captcha.yaml", epochs=100, imgsz=320)
```

`captcha.yaml`：
```yaml
path: ./dataset
train: images/train
val: images/val
nc: 80                         # 类别数
names: [ "bus", "traffic light", "..."]
```

## 4. 推理

```python
res = model("challenge.png")
for r in res:
    for box in r.boxes:
        cls = int(box.cls)
        conf = float(box.conf)
        x1, y1, x2, y2 = box.xyxy[0].tolist()
```

## 5. 与 reCAPTCHA 类目的对应

reCAPTCHA 题目集与 COCO 80 类高度重合：bus、car、truck、traffic light、
crosswalk、fire hydrant、stairs、palm tree、bicycle、boat、motorcycle、parking meter。
所以预训练 YOLOv8 + COCO 已能解决 70% 题目，剩下加几百张 fine-tune 即可。

## 6. 与 OCR 配合

点选汉字：
- 第 1 步：YOLO 检测每个文字 box。
- 第 2 步：把每个 box 裁剪出来 → ddddocr/paddleocr 识别字符。
- 第 3 步：根据"提示文字"找位置。

## 7. 已知公开实现（待联网验证）

- [NEEDS_VERIFICATION] github.com/ultralytics/ultralytics
- [NEEDS_VERIFICATION] github.com/sml2h3/ddddocr_objdet 思路
- [NEEDS_VERIFICATION] roboflow.com 上若干 captcha 公开数据集
