"""
audio_whisper_demo.py - 音频验证码识别（教学 demo）
=================================================
配套 SKILL.md Path 6 / Path 11。

适用题型：reCAPTCHA audio、Yandex SmartCaptcha audio 等"播放一段语音 → 输入听到的内容"题。
合规边界：本脚本仅展示 Whisper ASR 调用，不针对任何具体目标做自动提交。

依赖：
    pip install openai-whisper torch
    # 或：pip install faster-whisper（CPU/GPU 更快）

注意：reCAPTCHA / Yandex 等厂商可能会主动"加噪"或"变速"——
本 demo 假设拿到的是干净 mp3 文件；若有噪声，需先做噪声抑制（noisereduce 库）。
"""

import sys

try:
    import whisper
except ImportError:
    print("请先安装：pip install openai-whisper")
    sys.exit(1)


def transcribe_audio(mp3_path: str, model_name: str = "base") -> str:
    """
    把音频文件转录为文字。
    model_name: tiny / base / small / medium / large
    """
    model = whisper.load_model(model_name)
    # language="en" 提升英文识别准确率（reCAPTCHA 默认英文）
    result = model.transcribe(mp3_path, language="en", fp16=False)
    return result["text"].strip()


def transcribe_with_denoise(mp3_path: str) -> str:
    """先去噪再转录（reCAPTCHA 加噪场景）。"""
    try:
        import noisereduce as nr
        import soundfile as sf
        import numpy as np
    except ImportError:
        print("请先安装：pip install noisereduce soundfile")
        return ""

    data, sr = sf.read(mp3_path)
    # 把前 0.5s 当背景噪声估计
    noise_clip = data[: int(0.5 * sr)]
    cleaned = nr.reduce_noise(y=data, sr=sr, y_noise=noise_clip)
    out_path = mp3_path + ".cleaned.wav"
    sf.write(out_path, cleaned, sr)
    return transcribe_audio(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audio_whisper_demo.py <audio.mp3>")
        sys.exit(1)
    print(transcribe_audio(sys.argv[1]))
