# Scripts 目录索引

> **仅教学用途**。所有脚本与笔记均为合法授权研究下的公开技术示例，**不针对任何具体目标站点的商业风控**。

| 文件 | 类型 | 用途 |
|------|------|------|
| `opencv_slider_gap.py` | Python | OpenCV Canny + matchTemplate 滑块缺口距离识别 |
| `opencv_slider_siamese.md` | 笔记 | SiameseNet 孪生网络识别原理 + 训练数据说明 |
| `ddddocr_demo.py` | Python | ddddocr 调用示例（OCR / 滑块 / 点选） |
| `trajectory_bezier.py` | Python | 三阶贝塞尔鼠标轨迹生成 |
| `trajectory_three_seg.py` | Python | 三段式（加速-匀速-减速）轨迹 |
| `trajectory_gan.md` | 笔记 | GAN 鼠标轨迹原理 + 开源实现链接 |
| `click_yolo_demo.md` | 笔记 | YOLOv8 点选目标检测训练/推理框架 |
| `click_clip_demo.md` | 笔记 | CLIP 多模态零样本语义点选 |
| `audio_whisper_demo.py` | Python | reCAPTCHA / Yandex audio + Whisper ASR |
| `tls_curl_cffi_demo.py` | Python | curl_cffi 模拟 Chrome JA3/JA4 |
| `browser_stealth_demo.md` | 笔记 | 7 种 stealth 浏览器框架最小启动模板 |
| `pow_friendlycaptcha.md` | 笔记 | FriendlyCaptcha / mCaptcha / Turnstile / 极验 v4 PoW 算法 |

## 通用依赖速查

```bash
# CV / OCR
pip install opencv-python numpy ddddocr

# 音频
pip install openai-whisper torch noisereduce soundfile

# 网络指纹
pip install curl_cffi

# 浏览器自动化
pip install playwright playwright-stealth
pip install undetected-chromedriver
pip install nodriver
pip install camoufox
pip install patchright
pip install botright

# 深度学习
pip install ultralytics torch torchvision   # YOLOv8
pip install open_clip_torch                  # CLIP
```

## 运行前请确认

1. 你拥有目标站点的合法测试授权（自有 / 受邀渗透 / 红蓝对抗书面授权）。
2. 不调用第三方打码平台 API 进行批量请求。
3. 不在生产环境使用以上脚本批量提交。
