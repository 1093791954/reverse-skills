# Stealth 浏览器（patchright / nodriver / camoufox / botright / playwright-stealth）

## 1. 工具地图
| 工具 | 底座 | 语言 | 维护状态 (2024-2026) | 强项 |
|------|------|------|---------|------|
| patchright | Patchright (Playwright fork) | Py/JS | 活跃 | Chromium，针对 playwright 字符串 patch |
| nodriver | CDP 底层重写 | Py | 活跃 | 真 Chrome，无 webdriver 标志 |
| camoufox | Firefox fork | Py | 活跃 | 反 detector 角度独特，Firefox 内核对部分网站更友好 |
| botright | playwright + 内嵌 solver | Py | 活跃但争议（带商业 solver） | 集成 captcha 解决 |
| undetected-chromedriver | Selenium 补丁 | Py | 维护放缓 | 老牌、用例广 |
| playwright-stealth | playwright + js patch | Py/JS | 半活跃 | 入门简单，老 detector 还行 |
| puppeteer-extra-stealth | puppeteer plugin | JS | 半活跃 | Node 生态 |
| Helium | Selenium 上层 | Py | 一般 | 写脚本简洁 |

## 2. 主要检测点（被各 stealth 工具修补）
- `navigator.webdriver`（最经典）。
- `navigator.plugins.length` / `navigator.languages`。
- Chrome runtime 字段：`window.chrome.runtime` 完整性。
- Permissions：`Notification.permission` 在 headless 默认值 `denied` 应改 `default`。
- WebGL UNMASKED_VENDOR/RENDERER（headless 默认 SwiftShader）。
- iframe contentWindow 一致性。
- `Function.prototype.toString` 不能改写后丢失 `[native code]`。
- `console.debug` 调试器检测。
- `Element.prototype.attachShadow` 篡改痕迹。
- CDP detection：连接 CDP 时某些 console 行为异常。

## 3. 已公开研究
- CSDN「playwright-stealth 使用教程」：项目结构与隐身策略。
- CSDN「Playwright Stealth 使用指南」：Python 自动化反爬。
- CSDN「Playwright Stealth 项目常见问题解决方案」：兼容性。
- CSDN「nodriver 切换普通的 iframe 和隐藏的 iframe」：跨域 iframe 处理。
- CSDN「大模型安全（三十四）：核心技术栈之 Selenium/Playwright 自动化与反爬对抗」：Selenium vs Playwright 对比。
- CSDN「Nstbrowser 指纹浏览器全方位实战指南」：商业指纹浏览器。
- GitHub `Vinyzu/Botright`、`daijro/camoufox`、`ultrafunkamsterdam/nodriver`、`ultrafunkamsterdam/undetected-chromedriver`、`Kaliiiiiiiiii-Vinyzu/patchright`。
- 官方 blog 多篇关于 detector 进展。

## 4. 防御性分析建议
1. 选型：先 patchright/nodriver 起步；目标站点对 Chromium 检测狠则上 camoufox；快速集成则用 botright。
2. 验证：CreepJS、bot.sannysoft.com、fingerprint.com、abrahamjuliot/creepjs 自托管页面跑一圈。
3. 不要混用：playwright-stealth + 自定义 launch args 可能冲突。
4. 真硬件 + 真显卡很重要：headless --use-gl=angle 比 swiftshader 真。
5. 长期：每次 Chrome 大版本更新（M+1）都重测一次。

## 5. 缓解 / 趋势
- 厂商对 stealth 工具有针对性 detector：找它们的特征字符串/调用栈。
- patchright 等持续打补丁；攻防节奏短（数周）。
- camoufox 因为 Firefox 流量小，被针对力度低于 patchright，部分场景反而更稳。
- 商业指纹浏览器（Multilogin/AdsPower）走「真硬件 + 真用户配置」路线，对企业级风控更稳但贵。

## 6. 待研究
- patchright 与 nodriver 在 Cloudflare Turnstile 上的实测通过率差异。
- camoufox vs patchright 在 Akamai/DataDome 上的对比基准。
- 商业指纹浏览器的指纹库构建方法（是否爬真实用户数据）。
