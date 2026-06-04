# WebDriver / CDP 自动化检测（webdriver-detection）

> 配套 SKILL.md Path 10。

## 1. WebDriver 检测点

| 检测点 | 默认值 | 应改为 |
|--------|-------|-------|
| `navigator.webdriver` | true | false / undefined |
| `window.chrome` | undefined（Headless） | 完整对象 |
| `chrome.runtime` | undefined | 模拟对象 |
| `navigator.plugins.length` | 0 | ≥ 3 |
| `navigator.languages` | [] | [`en-US`, `en`] |
| `Notification.permission` | "default" | 与 user 一致 |
| iframe `contentWindow` 属性 | 修改过 | 还原 |
| `Permissions.query({name:'notifications'})` | denied / 异常 | prompt |
| `WebGL` vendor 字符串 | "Brian Paul" 或 SwiftShader | "Google Inc." 之类 |

## 2. CDP 检测

Chrome DevTools Protocol 留下的痕迹：

1. `Runtime.evaluate` 触发 `Object.toString` 异常分支
2. `console.debug` / `console.dir` 被 inspector 替换为非原生
3. `error.stack` 中含 "Puppeteer" / "playwright"
4. `document.$$jit` 被注入
5. CDP 通讯本身可被监测（Frida / Process inspect）

## 3. iframe / window 检测

- `window.outerWidth - window.innerWidth` 应在 16~24（有滚动条）
- iframe 内 `window.top !== window.self`
- 检测某些注入的全局变量名（`__nightmare`, `__phantomas`, `cdc_*`）

## 4. 已知研究

- [NEEDS_VERIFICATION] CreepJS 源码
- [NEEDS_VERIFICATION] github.com/berstend/puppeteer-extra-plugin-stealth/tree/master/src/evasions

## 5. 防御性分析思路

- 自有站点：上 CreepJS Trust Score 作为风控信号；< 70% 的请求需额外验证。

## 来源

- [NEEDS_VERIFICATION] puppeteer-extra-plugin-stealth evasions 列表
