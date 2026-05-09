---
name: captcha-bypass-analysis
description: 用于在合法授权前提下分析与审计各类人机验证（CAPTCHA / 滑块 / 点选 / 旋转 / 3D 选物 / 9 格图块 / 音频 / 无感行为 / PoW / 空间推理 / 语义点选）系统。覆盖 Google reCAPTCHA v2/v3/Enterprise、hCaptcha、Arkose FunCaptcha、极验 GeeTest v3/v4、腾讯防水墙 TCaptcha/TDC、网易易盾、数美 Shumei、顶象 Dingxiang、Vaptcha、阿里云盾、Akamai Bot Manager (_abck/sensor_data/bmak/bmp_v2)、Cloudflare Turnstile (cf_clearance/managed challenge)、PerimeterX/HUMAN (_px3/_pxhd)、DataDome (dd cookie)、Kasada (x-kpsdk-ct)、Imperva Incapsula (reese84)、F5 Shape (__TS01__)、FriendlyCaptcha PoW、mCaptcha、MTCaptcha、Yandex SmartCaptcha、AWS WAF Captcha、Apple Private Access Token (PAT)、Privacy Pass IETF。涉及 OpenCV 模板匹配 / 缺口距离 / Canny / Sobel、Siamese 孪生网络、ddddocr、YOLOv5/v8、CLIP 零样本、贝塞尔曲线鼠标轨迹、三段式（加速-匀速-减速）轨迹、GAN 轨迹生成、Whisper 音频识别、curl_cffi/tls-client/hrequests/azuretls 模拟 JA3/JA4/JA4H、camoufox/patchright/nodriver/botright/playwright-stealth/puppeteer-extra-stealth/undetected-chromedriver、Canvas/WebGL/AudioContext/Font/WebRTC/UA-CH/HTTP2/HTTP3 指纹、CreepJS/FpJS pro/BrowserGap、navigator.webdriver/CDP/Runtime.evaluate/iframe sandbox 检测、PoW SHA256/MD5 暴力、reCAPTCHA 音频通道、token 复用、IP 信誉评分等场景。当任务涉及"过滑块 / 过点选 / 过验证码 / 过 reCAPTCHA / 过 hCaptcha / 过 FunCaptcha / 过极验 / 过防水墙 / 过 Akamai / 过 Cloudflare / 过 DataDome / 过 PerimeterX / 过 Kasada / 浏览器指纹对抗 / TLS 指纹模拟 / 鼠标轨迹生成 / 滑块缺口识别 / 点选目标检测 / 行为评分 / 无感校验 / PoW 计算 / 验证码 OCR / 图片识别"等合法授权下的研究、安全审计、自有业务红蓝对抗、漏洞研究时使用。
---

# 过人机验证分析（captcha-bypass-analysis）

把已收集（中文社区 + 国外社区 + 厂商官方 + 学术线，详见 references/）的各类"人机验证机制"资料，整理为一套可复用的合法授权下的分析工作流。把"人机验证黑盒"拆成可解释的几层：识别厂商 → 抓包 → 题型分类 → JS 解混淆/补环境 → 采集字段定位 → CV/轨迹/PoW/音频各路径 → 回放验证 → 横向迁移。

> ⚡ **想快速找东西？读 [`INDEX.md`](INDEX.md)**（22+ 厂商速查表 / 12 题型决策树 / 11+ 通用技巧目录 / 13 个教学 demo）。

## 厂商速查（22+ 厂商，按 cookie/字段一眼识别）

| 看到这个特征 | 大概率是 | 笔记 |
|-------------|---------|------|
| `_abck` / `bm_sz` / `sensor_data` | Akamai BMP | `vendors/akamai-bmp.md` |
| `cf_clearance` / `__cf_bm` / `cf-turnstile-response` | Cloudflare Turnstile | `vendors/cloudflare-turnstile.md` |
| `_px3` / `_pxhd` / `_pxff_*` | PerimeterX (HUMAN) | `vendors/perimeterx-human.md` |
| `datadome` cookie | DataDome | `vendors/datadome.md` |
| `reese84` | Imperva Incapsula | `vendors/imperva-incapsula.md` |
| `__TS01****` / `x-shape-pi` | F5 Shape | `vendors/f5-shape.md` |
| `x-kpsdk-ct` / `x-kpsdk-cd` | Kasada | `vendors/kasada.md` |
| `recaptcha/api.js` / `g-recaptcha-response` | Google reCAPTCHA | `vendors/recaptcha.md` |
| `hcaptcha.com` / `n-data` | hCaptcha | `vendors/hcaptcha.md` |
| `client-api.arkoselabs.com` / `bda` | Arkose FunCaptcha | `vendors/arkose-funcaptcha.md` |
| `friendlycaptcha.com/pow` | FriendlyCaptcha PoW | `vendors/friendlycaptcha.md` |
| `mtcaptcha-verifiedtoken-v1:` | MTCaptcha | `vendors/mtcaptcha.md` |
| `captcha-api.yandex.ru` | Yandex SmartCaptcha | `vendors/yandex-smartcaptcha.md` |
| `aws-waf-token` | AWS WAF Captcha | `vendors/aws-waf-captcha.md` |
| `geetest.com` / `gcaptcha4` / `w` | 极验 GeeTest | `vendors/geetest.md` |
| `tcaptcha.qq.com` / `tdc.js` / `eks` / `collect` | 腾讯防水墙 | `vendors/tencent-tcaptcha.md` |
| `dun.163.com` / `cb` / `acToken` | 网易易盾 (NECaptcha) | `vendors/netease-yidun.md` |
| `shumei.tv` / `smid` | 数美 | `vendors/shumei.md` |
| `dingxiang-inc.com` / `constId` | 顶象 | `vendors/dingxiang.md` |
| `vaptcha.com` | Vaptcha | `vendors/vaptcha.md` |
| `aliyundun` / `bxet` / `x231` / `x82Y` / `_bx-v` | 阿里云盾 | `vendors/aliyun-captcha.md` |
| `fp.tongdun.net` / blackbox | 同盾 BlackBox | `vendors/tongdun-blackbox.md` |
| URL 后缀动态参数 + `XMLHttpRequest` 重写 | 瑞数 (Botgate) v4/v5/v6 | `vendors/ruishu.md` |

## 边界（Boundary）

- 仅用于**自有站点 / 受邀渗透 / 漏洞研究 / 安全合规审计 / 红蓝对抗 / 个人教学**等已授权场景。
- 不为绕过商业风控产品（reCAPTCHA Enterprise / hCaptcha Enterprise / Akamai BMP / Cloudflare Turnstile / Arkose / DataDome / PerimeterX / Kasada / Imperva / F5 Shape / 极验 / 防水墙 / 网易易盾 / 数美 / 顶象 等）以"批量爬取 / 批量注册 / 薅羊毛 / 套利 / 撞库"提供成品脚本。
- 不集成第三方打码平台（2captcha / capsolver / anti-captcha / yescaptcha / nopecha / cap-monster 等）的 API 调用代码，仅做"存在性 + 合规边界"说明。
- 当请求是"过 xxx 验证 / 还原 xxx 参数"，先在内部翻译为：①样本归属与授权确认 → ②抓包侦察 → ③厂商指纹识别 → ④题型分类 → ⑤JS 解混淆 → ⑥采集字段追源 → ⑦CV/轨迹/PoW/音频/无感各路径选择 → ⑧回放验证 → ⑨撰写分析备忘。
- 若用户没有给出授权来源，仅停留在"机制解释 + 工作流"层面，不给具体目标的可运行脚本。

姊妹技能：
- `web-keygen-analysis` — Web 加密参数还原（sign / x-bogus / x-s / h5st / sensor_data / _abck），本技能与之**互补**：那边重 JS 算法还原；这边重"题型 + 行为 + CV/轨迹/PoW"。
- `app-riskcontrol-analysis` — 移动端风控（x-gorgon / x-argus / mtgsig / Frida / unidbg），本技能在移动端验证码场景与之交叉。
- `jshook-skill` — JS Hook / 浏览器调试，本技能 Path 10/11 多次复用其能力。

---

## 总体工作流（Workflow）

按下列 14 步推进；每一步都有对应的 Path 段落详细展开。

1. **样本归类与授权确认**：站点域名、目标接口、可疑风控产品、关键 cookie/header 名。
2. **厂商指纹快速识别**（Path 1）：搜 cookie / JS 路径 / 字符串特征 / 接口域名，确定面对的是 reCAPTCHA / hCaptcha / Arkose / 极验 / 防水墙 / Akamai / Cloudflare / DataDome / PerimeterX / Kasada 中的哪一个。
3. **题型分类**（Path 2）：按"滑块（缺口/拼图）/ 点选（汉字/图标）/ 旋转 / 3D / 9 格图块 / 音频 / 无感（v3/Turnstile）/ PoW（FriendlyCaptcha）/ 空间推理 / 语义点选"分支。
4. **抓包侦察**：列出验证发起 → 验证回填 → 业务接口三段链路；记录 method、URL、headers、body、cookies。
5. **JS 文件清单与混淆分级**：用 web-keygen-analysis 的 L1~L6 标签初判混淆等级。
6. **JS 解混淆**：复用 `web-keygen-analysis` Path 2 的 9 个 Babel pass。
7. **采集字段追源**：定位"指纹采集 / 轨迹采集 / token 生成"三段函数。
8. **CV 路径**（Path 3 / Path 5 / Path 8 / Path 9）：滑块距离 / 点选 / 旋转 / 3D 选物 / 空间推理 / 语义。
9. **轨迹路径**（Path 4）：三段式 / 贝塞尔 / GAN 鼠标轨迹建模。
10. **指纹路径**（Path 10 / Path 11）：Canvas/WebGL/Audio/Font/WebRTC/UA-CH 浏览器指纹；JA3/JA4/JA4H TLS 指纹；HTTP/2 frame 指纹；HTTP/3 指纹。
11. **音频路径**（Path 6）：reCAPTCHA / Yandex audio 通道 + Whisper/Vosk ASR。
12. **PoW 路径**（Path 12）：FriendlyCaptcha / mCaptcha / Cloudflare Turnstile 计算挑战。
13. **Token 复用与 IP 信誉**（Path 13）：跨设备 token 共享、proxy 池信誉评分。
14. **回放验证 + 横向迁移**：脱机环境复现密文；与真实抓包对比；同站点姊妹接口（register / login / cfg）通常共用风控参数。

---

## Path 1：厂商指纹快速识别（Vendor Fingerprint Path）

适用：拿到站点的第一件事——快速判断面对哪个验证厂商。

**通过 cookie 名识别**（最快）：

| Cookie | 厂商 | 说明 |
|--------|------|------|
| `_abck`, `bm_sz`, `bm_sv`, `ak_bmsc` | Akamai BMP | sensor_data 验证后下发 |
| `cf_clearance`, `__cf_bm` | Cloudflare | Turnstile / Bot Fight |
| `_px3`, `_pxhd`, `_pxff_*` | PerimeterX (HUMAN) | px collector |
| `datadome`, `dd_cookie` | DataDome | 滑块挑战返回 |
| `reese84` | Imperva Incapsula | TLS + JS 双因子 |
| `__TS01__`, `f5avraaaaaaaaaaaaaa_` | F5 Shape | shape JS |
| `kpsdk-*`, `x-kpsdk-ct/cd/v` | Kasada | header 而非 cookie |
| `__zlcmid` | Zendesk | 误报，不是风控 |

**通过 JS URL / 字符串识别**：

| 特征 | 厂商 |
|------|------|
| `recaptcha/api.js`, `recaptcha/enterprise.js` | reCAPTCHA |
| `hcaptcha.com/1/api.js`, `hcaptcha.com/checkcaptcha` | hCaptcha |
| `client-api.arkoselabs.com`, `funcaptcha` | Arkose FunCaptcha |
| `geetest.com`, `gt.js`, `slide.7.x.x.js`, `gcaptcha4.js` | 极验 |
| `tcaptcha.qq.com`, `tdc.js`, `TDC.setData`, `__TENCENT_CHAOS_STACK` | 腾讯防水墙 |
| `dun.163.com`, `cb.js`, `acb.js` | 网易易盾 |
| `shumei.tv`, `fp.shumei.tv`, `smid` | 数美 |
| `dingxiang-inc.com`, `ds.js`, `constId` | 顶象 |
| `vaptcha.com`, `v3.js` | Vaptcha |
| `aliyundun`, `ic.js`, `nvc` | 阿里云盾 |
| `challenges.cloudflare.com/turnstile` | Cloudflare Turnstile |
| `friendlycaptcha.com/pow` | FriendlyCaptcha PoW |
| `mtcaptcha.com` | MTCaptcha |
| `captcha-api.yandex.ru` | Yandex SmartCaptcha |

**通过接口域名识别**：见 `references/vendors/<厂商>.md` 中的"关键端点与字段"段落。

→ 详见 `references/vendors/` 下每个厂商的笔记。

---

## Path 2：题型分类决策树（Challenge Type Path）

```
拿到挑战图/挑战配置
├─ 有图片 + 滑块条
│   ├─ 缺口形状是图块                 → 缺口滑块（极验 v3 / 易盾 / 顶象） → Path 3
│   └─ 拼图块 + 母图                 → 拼图滑块                          → Path 3
├─ 有图片 + 多个文字/图标提示点击
│   ├─ 提示是汉字/字母                → 点选汉字（极验 v3）               → Path 5
│   ├─ 提示是图标语义                 → 点选图标（极验 v4 icon）          → Path 5
│   └─ 提示是抽象语义（"按顺序点"）   → 语义点选 / 空间推理（极验 v4）    → Path 5 + Path 9
├─ 有 3D 物体需要旋转/选择           → FunCaptcha rotate / 3D selector  → Path 8
├─ 有 9 格图（"selecione..."）        → reCAPTCHA v2 image grid          → Path 6
├─ 有耳机图标 / 音频按钮              → reCAPTCHA / Yandex audio         → Path 6 + Path 11
├─ 无可见 UI（隐式 / score 评分）     → reCAPTCHA v3 / Turnstile / Akamai → Path 7
└─ 浏览器卡顿几秒（"verifying"）      → PoW（FriendlyCaptcha / Turnstile）→ Path 12
```

→ 详见 `references/types/` 下每种题型的笔记。

---

## Path 3：滑块距离识别（Slider CV Path）

适用：缺口滑块 / 拼图滑块。

**输入**：背景大图 url + 滑块小图 url。
**输出**：缺口 x 坐标（px）。

**算法栈（按精度从低到高）**：

1. **像素差分**：背景 - 模板 → 灰度图 → 找最大梯度区。准确率 ~70%，仅适合无干扰底图。
2. **Canny 边缘 + 模板匹配**：cv2.Canny → cv2.matchTemplate(method=TM_CCOEFF_NORMED)。准确率 ~90%，老牌通用方案。
3. **Sobel 边缘 + ROI 限制**：先用滑块块的 alpha 通道剪出形状，再 Sobel + match。处理"重叠透明缺口"准确率 ~95%。
4. **Siamese / 孪生网络**：训练对比学习模型，判断 patch-pair 是否同源。鲁棒性最强（应对复杂底图、噪点、伪缺口）。
5. **YOLO 缺口检测**：把缺口当作目标，YOLOv5/v8 训练。需要标注数据，但精度高、速度快。
6. **ddddocr**：开源现成模型 `slide_match()` / `slide_comparison()`，5 行代码即可，准确率 ~85%。

→ 详见 `references/types/slider-distance.md` + `scripts/opencv_slider_gap.py` + `scripts/opencv_slider_siamese.md` + `scripts/ddddocr_demo.py`。

---

## Path 4：鼠标/触摸轨迹建模（Trajectory Path）

适用：所有需要"模拟人移动"的场景。检测维度通常是：速度曲线、加速度峰值、抖动、停留点、起停延迟、X 轴单调性。

**三种主流模型**：

1. **三段式（加速 → 匀速 → 减速）**：经典物理模型。
   - 阶段 1：a₁ ∈ [800, 1500] px/s²，持续 30%~40% 距离
   - 阶段 2：恒速 ~600 px/s，持续 20%~30%
   - 阶段 3：a₂ ∈ [-1000, -1800] px/s²，持续 30%~40%
   - 末端**过冲再回退**（人通常会冲过去再拉回）。

2. **贝塞尔曲线**：取 4 个控制点，t ∈ [0, 1] 采样。优点：天然平滑、Y 轴抖动自然。

3. **GAN 生成**：用真实人类轨迹数据训练 GAN，生成器输出"统计意义上不可区分"的轨迹。最高级，但训练成本高。

**反检测要点**：
- 时间戳间隔不要等距（人类是 ~16ms ± 5ms 的不规则采样）
- 必须有 Y 轴扰动（即使理论上是水平直线）
- 起点和终点要有 100~300ms 的"鼠标静止"时间
- 触摸事件要包含 pressure / radiusX / radiusY / tiltX / tiltY 字段（移动端）

→ 详见 `references/techniques/trajectory.md` + `scripts/trajectory_bezier.py` + `scripts/trajectory_three_seg.py` + `scripts/trajectory_gan.md`。

---

## Path 5：点选 / 图标 / 语义识别（Click CV Path）

适用：极验 v3 点选汉字 / v4 icon / 语义点选 / reCAPTCHA 9 格图块语义题。

**算法栈**：

1. **YOLOv5 / v8 目标检测**：标注 100~500 张训练数据 → 微调 YOLO → 输出每个目标的 bbox。适合"固定 N 个汉字 / 固定 N 类图标"。
2. **CRNN / OCR**：识别汉字内容（需先 detect 出每个字符 box）。`paddleocr` / `easyocr` / `ddddocr` 都可。
3. **CLIP 零样本**：把"提示文字"和"图块"投到同一向量空间，cosine 相似度排序。适合语义点选。
4. **多模态 LLM（Vision API）**：把题目图 + 提示文字一起喂给 GPT-4V / Gemini / Claude Vision，让 LLM 直接返回点击坐标。最贵但最稳。
5. **空间推理**：极验 v4"按提示顺序点击"——需要"先 detect → 再按语义排序"两段式。

→ 详见 `references/types/click-character.md`、`click-icon.md`、`semantic-text.md`、`space-reasoning.md`、`scripts/click_yolo_demo.md`、`scripts/click_clip_demo.md`。

---

## Path 6：reCAPTCHA v2 image / 9 格题（reCAPTCHA Path）

**v2 流程**：
1. `anchor` 加载 → 用户点 checkbox → 后端评分。
2. 若 score 不够 → 弹 challenge → 9 格图（"select all images with bus"）或 4×4 图块（点击直到没有 bus）。
3. 也可切换到 audio 通道（耳机图标）。

**分析方向**：
- **图片通道**：YOLO 训练 80 类（COCO 类目和 reCAPTCHA 题目集高度重合）。
- **音频通道**（最高效）：下载 mp3 → Whisper 识别 → 直接填答案。Google 官方对此长期未做强干扰。
- **行为评分**（v3）：见 Path 7。

→ 详见 `references/vendors/recaptcha.md` + `references/types/grid-image-select.md` + `references/types/audio-captcha.md` + `scripts/audio_whisper_demo.py`。

---

## Path 7：reCAPTCHA v3 / 无感行为（Invisible Behavior Path）

v3 没有可见挑战，只返回 score ∈ [0, 1]，由站点自己定阈值（通常 0.5）。

**得分提升方向**（合法授权红蓝对抗审计要点）：
1. **真浏览器 + 真账号**：score 通常 ≥ 0.7。
2. **冷启动账号**：score 0.3~0.5。
3. **代理 IP 信誉**：住宅 IP > 移动 4G > 数据中心 IP。
4. **cookie warming**：先访问几个普通页面，让 Google 认识这台浏览器。
5. **行为采集时长**：v3 在页面上至少要采集 ≥ 2s 鼠标 / 滚动 / 焦点事件。
6. **siteverify 响应字段**：`success`、`score`、`action`、`hostname`、`error-codes`，注意 `action` 必须和站点 grecaptcha.execute() 调用时一致。

**Turnstile / Akamai 等"无感"产品类似**：见对应 vendor 笔记。

→ 详见 `references/types/invisible-behavior.md`。

---

## Path 8：FunCaptcha / Arkose 3D 旋转（Arkose Path）

Arkose 题型很多（rotate、roller、selector、3D-rollball、tiles），由 `gameType` 字段决定。

**核心检测面**：
1. **bda token**：浏览器收集 100+ 项指纹后 AES 加密的 blob，发到 `/fc/gt2/public_key/<sitekey>`。
2. **题目通过率**：每个 gameType 都需要 1~10 轮挑战；前几轮失败概率高。
3. **行为画像**：旋转/拖拽的速度、加速度、停顿。

**分析路径**：
- 3D rollball：CV 方向梯度（找最佳对齐角度）。
- 静态 rotate：枚举角度 → CLIP / VGG 相似度找原图。
- selector：YOLO + 类别匹配。

→ 详见 `references/vendors/arkose-funcaptcha.md` + `references/types/rotate-image.md` + `references/types/3d-object-select.md`。

---

## Path 9：极验 v4 空间推理 / icon（GeeTest v4 Path）

v4 引入了"icon-crush"、"按提示顺序点击"、"空间推理"题型。

**关键参数**：
- `w`：包含浏览器指纹 + 轨迹 + 答案的加密 payload，AES-CBC + Base64 + URL-safe。
- `captcha_id` / `lot_number` / `risk_type` / `pow_msg` / `pow_sign`。
- v4 同时引入 PoW（pow_msg = HMAC-SHA256 + 难度位）。

**分析路径**：
- 把 v4 当成 v3 的超集 → 复用 v3 的滑块/点选 CV 模型。
- 空间推理：YOLO + 顺序约束（用 LLM 解析提示文字得到"先 A 再 B 再 C"序列）。
- PoW：纯算（见 Path 12）。

→ 详见 `references/vendors/geetest.md` + `references/types/space-reasoning.md`。

---

## Path 10：浏览器指纹对抗（Browser Fingerprint Path）

**最常被检测的 13 类指纹**（按重要性）：

1. **navigator.webdriver** — 必须为 false / undefined。
2. **chrome.runtime** — 普通 Chrome 不存在，Headless 默认存在。
3. **window.outerWidth/outerHeight = 0** — Headless 默认 0，必须改。
4. **Canvas 指纹** — 2D drawText → toDataURL → MD5。需要 noise（每次微扰一个像素）。
5. **WebGL 指纹** — `WEBGL_debug_renderer_info` → vendor / renderer 字符串（"Google Inc. (Intel)" 等）。
6. **AudioContext 指纹** — OscillatorNode → 频谱 → 求和。
7. **Font 指纹** — measureText('mmmmmm').width 列表 vs 200+ 候选字体。
8. **WebRTC 真实 IP 泄露** — STUN 收集 host candidate IP。
9. **UA-CH (Sec-CH-UA / Sec-CH-UA-Platform)** — 与 UA 必须一致。
10. **navigator.plugins / mimeTypes** — Chrome 必有 PDF Viewer。
11. **screen.colorDepth / pixelDepth** — 通常 24。
12. **timezone offset 与 IP 地理位置一致** — 否则风控扣分。
13. **CDP 检测**：`Runtime.evaluate` 触发 `Object.toString()` 异常分支；或检测 `console.debug` 是否为原生。

**工具栈**：
- `playwright-stealth` / `puppeteer-extra-stealth` — 经典补丁集合。
- `undetected-chromedriver` — Selenium 衍生。
- **camoufox** — Firefox 重编译版，从内核改指纹（强）。
- **patchright** — Playwright 的 stealth 重编译版。
- **nodriver** — undetected 后续，无 Selenium 依赖。
- **botright** — 多策略融合。

→ 详见 `references/techniques/fingerprint-bypass.md` + `references/techniques/browser-stealth.md` + `references/techniques/webdriver-detection.md` + `scripts/browser_stealth_demo.md`。

---

## Path 11：TLS / HTTP2 / HTTP3 指纹（Network Fingerprint Path）

**JA3 (TLS 1.2)**：`SSLVersion,Cipher,Extension,EllipticCurve,EllipticCurvePointFormat` 五元组 → MD5。
**JA4**：JA3 升级版，分 JA4 / JA4S / JA4H / JA4L / JA4X，覆盖 client、server、http、latency、cert。
**JARM**：用 10 次特殊 ClientHello 探针 server 行为，得到 server 指纹。

**HTTP/2 frame fingerprint**（Akamai 命名为"H2 fingerprint"）：
- SETTINGS frame 字段顺序与值
- WINDOW_UPDATE 大小
- HEADERS pseudo-header 顺序（`:method`, `:authority`, `:scheme`, `:path` 的相对位置）
- PRIORITY 树形结构

**工具栈（Python / Go）**：
- `curl_cffi`（Python，binding libcurl-impersonate）— 一行 `requests.get(url, impersonate="chrome131")`。**最方便**。
- `tls-client`（Python wrapper of Go GoTls）。
- `hrequests`（Python，TLS + 浏览器一体）。
- `azuretls` / `cycletls`（Go）。
- `noble-tls`（Node.js）。

→ 详见 `references/techniques/tls-ja3-ja4.md` + `references/techniques/http2-fingerprint.md` + `scripts/tls_curl_cffi_demo.py`。

---

## Path 12：PoW 计算挑战（Proof-of-Work Path）

**FriendlyCaptcha**：客户端解 N 个 SHA-256 puzzle（找哈希前 k 位为 0 的 nonce）。难度 N、k 由服务器下发。
**mCaptcha**：类似 FriendlyCaptcha，开源，自托管。
**Cloudflare Turnstile**：在某些场景也跑 PoW（检测 V8 引擎执行特征）。
**极验 v4**：HMAC-SHA256 风格 PoW，每次 ~50ms 开销。

**分析方法**：
- 抓 PoW 配置：difficulty、target、salt、algorithm。
- 纯算实现：Node.js 复用 crypto 模块即可，速度匹配 V8。
- 用 worker pool 并行（PoW 天然可并行）。

→ 详见 `references/types/pow-friendly.md` + `scripts/pow_friendlycaptcha.md`。

---

## Path 13：Token 复用与 IP 信誉（Token Reuse Path）

**很多人机验证 token 实际上可以复用**：
- reCAPTCHA token 有效期 ~120s。
- hCaptcha token ~120s。
- Cloudflare Turnstile token ~300s（一次性）。
- 极验 token 5 分钟内可复用同站点不同接口。

**IP 信誉**（厂商常用 IPQS / Spur / IP2Proxy）：
- 数据中心 IP（AWS / GCP / Azure / OVH / Hetzner）= score -30
- 公开 proxy 列表 IP = score -50
- 住宅 proxy（Bright / Oxylabs / Smartproxy）= score 0~-5
- 移动 IP（4G / 5G）= score +5

**审计建议**：业务方应主动用 IP 信誉服务校验来源 IP，并把 token 与 IP / UA 绑定。

→ 详见 `references/techniques/replay-token.md`。

---

## Path 14：第三方打码平台合规边界（Third-party Solver Boundary）

**主流第三方平台（仅作合规说明，不集成 API）**：
- 2captcha / capsolver / anti-captcha / yescaptcha / nopecha / cap-monster

**合规边界**：
- 平台本身合法（提供 OCR / 真人识别），但**接入这些平台进行批量爬取目标站点 = 违反目标站点 ToS**。
- 自有业务红蓝对抗：可以用平台模拟攻击者视角，但需有书面授权。
- 学术研究：需 IRB / 内部审计批准。
- **本技能不提供任何调用代码模板**。

**替代方案**（合规研究下）：
- 自己训练 OCR 模型（教学）。
- 用 OpenAI Vision / Gemini Vision API（费用 + 合规视具体题型而定）。
- 申请厂商提供的"测试模式"（例如 reCAPTCHA test keys）。

→ 详见 `references/techniques/third-party-solver.md`。

---

## 工具链速查（Tool Quick Reference）

| 用途 | 工具 |
|------|------|
| OCR / 滑块 | ddddocr, paddleocr, easyocr |
| CV 缺口 | OpenCV (Canny/Sobel/matchTemplate), SiameseNet |
| 目标检测 | YOLOv5, YOLOv8, Detectron2 |
| 多模态 | CLIP, GPT-4V, Gemini Vision, Claude Vision |
| 音频 ASR | Whisper, Vosk, wit.ai |
| TLS 模拟 | curl_cffi (Python), tls-client, hrequests, azuretls (Go) |
| Stealth 浏览器 | playwright-stealth, puppeteer-extra-stealth, undetected-chromedriver, camoufox, patchright, nodriver, botright |
| 抓包 | mitmproxy, Charles, Fiddler, Wireshark |
| JS 调试 | DevTools, jshook-skill, Frida (移动端) |
| 解混淆 | Babel pass (见 web-keygen-analysis Path 2), AST Explorer |
| 鼠标轨迹 | bezier.py, 手写三段式 |
| 指纹检测自查 | CreepJS, browserleaks, fingerprintjs.com/demo, abrahamjuliot/creepjs |

---

## 参考资料组织

- `references/vendors/` — 22+ 厂商笔记
- `references/types/` — 12+ 题型笔记
- `references/techniques/` — 11+ 通用技巧笔记
- `references/search-log.md` — 搜索日志（已搜词 / 已抽关键词 / 待扩展词 / 终止判定）
- `scripts/` — 教学性 demo（OpenCV 缺口 / 贝塞尔轨迹 / 三段式 / ddddocr / Whisper / curl_cffi / stealth 模板）

更新策略：每发现新厂商 / 新题型 / 新工具 → 新增一份 reference + 在 search-log.md 记录扩展词。当连续 2 轮"待扩展词"无新增 = 0，且每份 vendor / type 笔记 ≥ 3 条独立来源时，认为本轮搜集完成。

## 版本

- v0.1 (2026-05-09)：初版骨架。基于 web-keygen-analysis 的"滑块/PoW"段落迁移并扩展。
- v0.2 (2026-05-09 R3)：CSDN API 大批量真实检索；vendors 17 份扩成"七段骨架 + 4~8 条 articleid 引用"；types/techniques 部分补真实链接。
- v0.3 (2026-05-09 R4)：自我验证（103/104 ✅）+ 6 份新厂商笔记（同盾 BlackBox / AWS WAF / Yandex / MTCaptcha / F5 Shape / FriendlyCaptcha）+ 9 份扩充段。vendors 总数 22。
- **v1.0 (2026-05-09 R5)**：深化检索（cross-skill / DrissionPage / DeepSeek-OCR + GPT-4V + Gemini Vision）+ 8 词边角饱和复验通过（WebGPU / OffscreenCanvas / Service Worker / Trusted Types 等均无新词）→ **正式发布**。
- 终止条件已达成：连续 16+ 个搜词无新厂商 / 新题型 / 新工具；每份核心笔记 ≥ 3 条独立来源链接；唯一失败的 articleid 124388541 已修复。
