# 音频验证码 ASR 识别（reCAPTCHA audio / 兜底）

## 1. 题型描述
- 主要见于 reCAPTCHA v2（按 audio 按钮触发）：播放一段含数字/单词的英文录音，让用户输入听到的文字。
- 兜底机制：图块识别失败/视觉障碍用户启用。
- 时长 5~10 秒，含背景噪声、变速、双人对话、回响等抗 ASR 措施。

## 2. 检测维度
- 答案精确字符串匹配（容忍少量空格）。
- 多次失败后封锁 audio 模式。
- 提交字段同样附带 c/k token 与指纹。

## 3. ASR 工具
| 工具 | 范围 | 备注 |
|------|------|------|
| OpenAI Whisper（large-v3） | 多语言 | 在 reCAPTCHA audio 上 95%+ 准确率（社区研究） |
| faster-whisper | 同 Whisper，CPU/GPU 加速 | 部署友好 |
| Vosk | 多语言 | 体积小 |
| wit.ai | 商业 | API |
| Google Speech-to-Text | 商业 | 高准确率，但讽刺地用 Google 解 Google |
| Amazon Transcribe | 商业 | - |
| Mozilla DeepSpeech | 已弃维 | 历史方案 |
| Conformer / Wav2Vec2 | 论文 | 自训练 |

## 4. 流程
1. 触发 audio 模式：点击 reCAPTCHA audio 按钮，拿 mp3 url。
2. 下载 mp3 → 转 wav（16kHz mono）。
3. Whisper 识别 → 后处理（去标点、空格规整、数字转字面）。
4. 提交答案 → 验证 token。

## 5. 已公开研究
- arxiv 多篇「Whisper-based reCAPTCHA Audio Bypass」论文（2022-2024），公开数据集 + 评测。
- GitHub `dessant/buster`：Chrome 扩展，自动调用 ASR 解 audio（已停止维护）。
- GitHub `audio-recaptcha-solver`、`recaptcha-audio-solver`：参考实现。
- CSDN/medium 多篇 Whisper + reCAPTCHA audio 教学。
- BatPro 系列论文「Audio CAPTCHA bypass」综述。

## 6. 防御性分析步骤
1. 在合法授权环境采 reCAPTCHA audio 100+ 条 + 真值。
2. 用 Whisper-large-v3 跑 baseline，记录每条错位字符。
3. 对错位高的样本做后处理（如多模型投票）。
4. 评估「连续 audio 模式」的失败上限（多次失败会被关掉）。

## 7. 缓解 / 趋势
- 加入更多干扰（背景对话、变速 0.8-1.2x、回响）。
- 限制单 IP/UA audio 使用次数。
- hCaptcha 已基本去掉 audio 模式（无障碍走另外的渠道）。
- Apple Privacy Pass 给予部分用户跳过 audio 的特权。

## 8. 待研究
- Whisper-v3 vs faster-whisper-large 在 reCAPTCHA audio 实测对比。
- 后处理 prompt 工程对数字识别的提升幅度。
- 双人对话干扰下的最佳分离策略（pyannote 分离 + 单声轨识别）。
