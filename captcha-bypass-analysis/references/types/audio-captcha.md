# 音频验证码（audio-captcha）

> 配套 SKILL.md Path 6。

## 1. 题型特征

- 用户点击"耳机"图标 → 播放一段语音 → 输入听到的内容
- reCAPTCHA / Yandex SmartCaptcha / 部分自研

## 2. 检测维度

- 答案正确性（OCR / ASR）
- 多次切换通道（image ↔ audio）的频率会被扣分
- 浏览器播放音频的 Web Audio API 调用真实性

## 3. ASR 路径

```python
import whisper
model = whisper.load_model("base")
result = model.transcribe("audio.mp3", language="en")
print(result["text"])
```

详见 `scripts/audio_whisper_demo.py`。

reCAPTCHA / Yandex 会主动加噪 → 先用 noisereduce 去噪。

## 4. 已知研究

- [NEEDS_VERIFICATION] github.com/dessant/buster
- [NEEDS_VERIFICATION] arxiv 论文：CAPTCHA audio bypass with Whisper / wit.ai

## 5. 防御性分析思路

- 自有站点：评估禁用 audio 通道的影响（无障碍合规风险）。
- 加强 audio 加噪 / 变速 / 多人混音。
- 监控"短时间内多次切换通道"事件。

## 来源

- [NEEDS_VERIFICATION] dessant/buster
- [NEEDS_VERIFICATION] OpenAI Whisper 论文
