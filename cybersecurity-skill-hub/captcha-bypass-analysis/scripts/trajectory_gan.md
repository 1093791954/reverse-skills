# GAN 鼠标轨迹生成（教学笔记）

配套 SKILL.md Path 4。当三段式 / 贝塞尔模型已经被对手风控的"统计学检测"识破时，
转向 GAN：用真实人类轨迹数据训练生成器，使输出在统计意义上不可区分。

## 1. 数据采集（合规版）

- 在自有站点放一个"用户主动同意被采集"的滑块 demo，记录真实用户的：
  - 时间戳序列 t_i
  - x, y 坐标序列
  - 触摸/鼠标 event 类型（mousedown / mousemove / mouseup / pointerdown / ...）
  - pressure / radiusX / tiltX（移动端）
- 1000~10000 条真实样本即可启动训练。
- 学术数据集（待验证）：BB-MAS / RHU Keystroke、Touch & Trajectory dataset。

## 2. 模型选型

### 2.1 LSTM-GAN
- 生成器：LSTM 输出 (Δx, Δy, Δt) 序列。
- 判别器：双向 LSTM + 全连接，输出"真/假"。
- 简单、训练快，但容易塌陷。

### 2.2 TimeGAN（专用于时间序列）
- 三个网络：embedder / recovery / generator + supervisor。
- 同时优化"自编码重构 + 监督一步预测 + 对抗"，时间序列保真度高。

### 2.3 WaveGAN / DCGAN（把轨迹当一维信号）
- 简单直接但忽略事件含义。

## 3. 训练 tips

- 对 (Δx, Δy, Δt) 标准化到 [-1, 1] 区间。
- 每条轨迹长度归一化到 64 / 128 步（pad / sample）。
- 生成的 Δt 必须 ≥ 1 ms（clamp）。
- 起始静止 100~300ms、结束静止 100~300ms 由后处理添加，不让 GAN 学。

## 4. 与传统方法 hybrid 用法

实战中往往：
- 大方向用三段式（保证 X 单调到位、加速度合理）。
- 抖动 / 微速度变化交给 GAN 生成的"局部噪声"。
- 这种 hybrid 比纯 GAN 训练成本低、可控。

## 5. 风险与防御者视角

- 对手可以用同样方法训练判别器；如果你的 GAN 训练数据有泄露 → 判别器精度 ~99%。
- 一个有效的防御：对手定期更换"行为评分模型"，让旧 GAN 失效。

## 6. 开源实现（待联网验证）

- [NEEDS_VERIFICATION] github.com/jsyoon0823/TimeGAN
- [NEEDS_VERIFICATION] github.com/flier-dev/mouse-gan
- [NEEDS_VERIFICATION] arxiv 论文："Generating Synthetic Mouse Movements with GANs"
