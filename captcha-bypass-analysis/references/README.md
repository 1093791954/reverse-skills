# References 索引（captcha-bypass-analysis）

> 本目录存放本技能所有"原始研究素材 / 厂商笔记 / 题型笔记 / 通用技巧笔记 / 搜索日志"。SKILL.md 中每条 Path 都会反向引用这里的至少一份笔记。

## 目录结构

- `vendors/` — 一个厂商一份笔记（按"产品形态/检测维度/关键端点/已公开研究/分析思路/版本历史/待研究"七段骨架）
- `types/` — 按题型组织（滑块/点选/旋转/3D/无感/PoW/音频/语义）
- `techniques/` — 通用技巧（OCR、轨迹、指纹、stealth、TLS、HTTP2、检测点、第三方、深度学习、token 复用、ASR）
- `search-log.md` — 已搜词 / 已抽关键词 / 待扩展词 / 终止判定记录

## 厂商总览

| 厂商 | 产品 | 类别 | 笔记 |
|------|------|------|------|
| Google | reCAPTCHA v2/v3/Enterprise | 国际 | `vendors/recaptcha.md` |
| Intuition Machines | hCaptcha | 国际 | `vendors/hcaptcha.md` |
| Arkose Labs | FunCaptcha | 国际 | `vendors/arkose-funcaptcha.md` |
| 极验 | GeeTest v3/v4 | 中国 | `vendors/geetest.md` |
| 腾讯 | 防水墙 TCaptcha | 中国 | `vendors/tencent-tcaptcha.md` |
| 网易 | 易盾 | 中国 | `vendors/netease-yidun.md` |
| 数美 | Shumei | 中国 | `vendors/shumei.md` |
| 顶象 | Dingxiang | 中国 | `vendors/dingxiang.md` |
| Vaptcha | Vaptcha | 中国 | `vendors/vaptcha.md` |
| 阿里 | 阿里云盾 | 中国 | `vendors/aliyun-captcha.md` |
| Akamai | Bot Manager (BMP) | 国际 | `vendors/akamai-bmp.md` |
| Cloudflare | Turnstile | 国际 | `vendors/cloudflare-turnstile.md` |
| PerimeterX/HUMAN | PX | 国际 | `vendors/perimeterx-human.md` |
| DataDome | DataDome | 国际 | `vendors/datadome.md` |
| Kasada | Kasada | 国际 | `vendors/kasada.md` |
| Imperva | Incapsula | 国际 | `vendors/imperva-incapsula.md` |
| F5 | Shape | 国际 | `vendors/f5-shape.md` |
| FriendlyCaptcha | FC | 国际 | `vendors/friendlycaptcha.md` |
| MTCaptcha | MT | 国际 | `vendors/mtcaptcha.md` |
| Yandex | SmartCaptcha | 国际 | `vendors/yandex-smartcaptcha.md` |
| AWS | WAF Captcha | 国际 | `vendors/aws-waf-captcha.md` |
| Apple | PAT / Privacy Pass | 国际 | (官方 IETF draft 待联网核对) |
| 同盾 | BlackBox | 中国 | `vendors/tongdun-blackbox.md` |
| 瑞数 | Botgate v4/v5/v6 | 中国 | `vendors/ruishu.md` |

## 题型总览

| 题型 | 代表厂商 | 笔记 |
|------|---------|------|
| 缺口滑块 | 极验 v3 / 网易易盾 / 顶象 | `types/slider-distance.md` |
| 拼图滑块 | 极验 / 数美 | `types/slider-puzzle.md` |
| 点选汉字/字母 | 极验 v3 / 顶象 | `types/click-character.md` |
| 点选图标 | 极验 v4 icon | `types/click-icon.md` |
| 旋转还原 | FunCaptcha / 极验 | `types/rotate-image.md` |
| 3D 选物 | FunCaptcha 3D | `types/3d-object-select.md` |
| 9 格图片 | reCAPTCHA v2 | `types/grid-image-select.md` |
| 音频 | reCAPTCHA audio | `types/audio-captcha.md` |
| 无感行为 | reCAPTCHA v3 / Turnstile / Akamai | `types/invisible-behavior.md` |
| PoW | FriendlyCaptcha / mCaptcha / Turnstile | `types/pow-friendly.md` |
| 空间推理 | 极验 v4 | `types/space-reasoning.md` |
| 语义点选 | 极验 / 数美 | `types/semantic-text.md` |

## 技巧总览

| 主题 | 笔记 |
|------|------|
| OCR / 模板匹配 | `techniques/ocr-template-match.md` |
| 鼠标轨迹 | `techniques/trajectory.md` |
| 浏览器指纹 | `techniques/fingerprint-bypass.md` |
| Stealth 浏览器（综述） | `techniques/browser-stealth.md` |
| Stealth 浏览器（深度：DrissionPage / camoufox / patchright） | `techniques/drissionpage-camoufox-patchright.md` |
| TLS 指纹（JA3 / JA4 / JA4+ 全协议） | `techniques/tls-ja3-ja4.md` |
| HTTP/2 指纹 | `techniques/http2-fingerprint.md` |
| WebDriver 检测 | `techniques/webdriver-detection.md` |
| 第三方打码（合规边界） | `techniques/third-party-solver.md` |
| 深度学习模型 + LLM 视觉（DeepSeek-OCR / GPT-4V / Gemini） | `techniques/deeplearning-models.md` |
| Token 复用 + IP 信誉 | `techniques/replay-token.md` |
| 音频 ASR | `techniques/audio-asr.md` |
| 跨技能联动（h5st / zse-96 / x-bogus） | `techniques/cross-skill-h5st-zse96-xbogus.md` |
