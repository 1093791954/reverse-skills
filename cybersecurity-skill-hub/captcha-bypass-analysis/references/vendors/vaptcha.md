# Vaptcha

## 1. 产品形态
- 主打人机验证 SaaS：传统点选、滑块、空间推理、3D 旋转、人脸朝向、语义点选；行为式无感（`mode=invisible`）。
- 域名：`v.vaptcha.com`、`v3.vaptcha.com`、`api.vaptcha.com`、`assets.vaptcha.com`。
- 前端 SDK：`https://v3.vaptcha.com/v3.js`，对外暴露 `vaptcha(option).then(obj => obj.render()/validate())`。

## 2. 检测维度
- **行为轨迹**：traceData，鼠标/触摸 dx,dy,t；分布 KDE 与人类样本对照。
- **环境指纹**：Canvas/WebGL/Audio/UA-CH/Font/插件。
- **频次**：同一 vid + IP 在窗口内最多 N 次。
- **题目池**：人脸朝向、动物方向、空间推理（"找远的"/"上面的"）；语义图很多。
- **token chain**：`vid`, `gt`, `challenge`, `data`, `verify`。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/v3.js` | SDK 主体 |
| `/api/v3/down/<vid>` | 下发题目 + `challenge` + 图片 url |
| `/api/v3/verify/<vid>` | 提交 `data`(轨迹+答案), `challenge`, `lang`, `appkey`, `referer` |
| `/api/v3/server` | invisible 模式直传 |

**data 加密**：AES-CBC + base64，key 由 `challenge` 派生；明文 JSON 含 `passes`(轨迹), `time`(总时长), `answer`(答案，按题型不同)。

## 4. 已公开研究
- CSDN「vaptcha 逆向」相关 30 篇结果，包含「Vaptcha 滑块验证码逆向分析」「Vaptcha 三代 verify 接口」「Vaptcha 空间推理题型识别」等。
- GitHub `vaptcha-research` 协议级整理。
- 看雪个别帖讨论 Vaptcha 3D 旋转题的角度回归（ResNet-18）。

## 5. 防御性分析思路
1. SDK 主体不深度混淆（相对极验/数美），更易做静态分析。
2. 轨迹：从 `down` → mouseup → `verify` 的总耗时分布，人类多在 1.5~5s。
3. 空间推理：题目是 4-9 张候选图 + 一句中文 prompt（"选出最像花的"），可用 CLIP 做语义匹配。
4. 3D 旋转：ResNet 或 ViT 做角度回归；训练数据可从 `assets` 拉。
5. 人脸朝向：MediaPipe FaceMesh + 角度计算很稳。

## 6. 已知缓解 / 更新历史
- 2021 v3 上线，统一题型容器。
- 2023 推空间推理 + 3D 旋转。
- 2024 上线人脸朝向题，需 CV-3D 配合识别。
- 增强对 `headless`/`Permissions.query`/`webdriver` 的检测。

## 7. 待研究问题
- 题型权重切换的服务端策略。
- 3D 旋转题图是否带 watermark 反训练。
- invisible 模式失败兜底升级到哪种题型的优先级。
