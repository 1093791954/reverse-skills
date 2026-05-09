# Browser Stealth 启动模板（教学）

配套 SKILL.md Path 10。本文档汇总常见 stealth 浏览器框架的"最小启动代码"，
仅作教学；调用时建议设置浏览器 user-data-dir 隔离测试 profile。

合规边界：仅在自有站点 / 受邀渗透 / 漏洞研究 / 红蓝对抗下使用。

---

## 1. playwright-stealth (Python)

```python
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    stealth_sync(page)              # 注入 stealth 补丁
    page.goto("https://your-test-site.example.com")
    print(page.evaluate("navigator.webdriver"))  # 应为 false 或 undefined
```

主要打的补丁：navigator.webdriver、navigator.plugins、navigator.languages、
chrome.runtime、Permissions API、WebGL vendor、iframe contentWindow。

---

## 2. puppeteer-extra-stealth (Node.js)

```js
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://your-test-site.example.com');
})();
```

---

## 3. undetected-chromedriver (Selenium)

```python
import undetected_chromedriver as uc

driver = uc.Chrome(version_main=131)
driver.get("https://your-test-site.example.com")
print(driver.execute_script("return navigator.webdriver"))
```

注意：uc 已停更频繁，新项目建议用 `nodriver`（同作者，无 Selenium 依赖）。

---

## 4. nodriver (uc 后续)

```python
import nodriver as uc
import asyncio

async def main():
    browser = await uc.start()
    page = await browser.get("https://your-test-site.example.com")
    elem = await page.find("input[type=submit]", best_match=True)
    await elem.click()

asyncio.run(main())
```

特点：直接用 CDP，零 Selenium / WebDriver，反检测面更小。

---

## 5. camoufox (Firefox 重编译反指纹版)

```python
from camoufox.sync_api import Camoufox

with Camoufox(headless=False, humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://your-test-site.example.com")
```

特点：从 Firefox 内核改 Canvas/WebGL/Audio/Font/Screen/Hardware 等指纹，
能一键开 GeoIP-based locale/timezone 自动同步。

---

## 6. patchright (Playwright 的 stealth 重编译版)

```python
from patchright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_context(viewport={"width": 1920, "height": 1080}).new_page()
    page.goto("https://your-test-site.example.com")
```

---

## 7. botright (多策略融合)

```python
import botright

botright_client = botright.Botright()
browser = botright_client.new_browser()
page = browser.new_page()
page.goto("https://your-test-site.example.com")
```

botright 内置 hCaptcha / reCAPTCHA / GeeTest 求解器（合规边界自查）。

---

## 检测自查清单（重启后第一时间用 CreepJS / browserleaks 自检）

1. https://abrahamjuliot.github.io/creepjs/  — Trust Score 应 ≥ 70%
2. https://browserleaks.com/canvas         — Canvas Hash 不能与 chrome 默认值一致
3. https://browserleaks.com/webgl          — WEBGL_debug_renderer_info 应正常
4. https://tls.peet.ws/api/clean            — JA3/JA4 应为 chrome 主流值
5. https://amiunique.org/                   — 唯一性 < 1% 是目标

## 参考链接（待重启联网后补充）

- [NEEDS_VERIFICATION] github.com/AtuboDad/playwright_stealth
- [NEEDS_VERIFICATION] github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth
- [NEEDS_VERIFICATION] github.com/ultrafunkamsterdam/undetected-chromedriver
- [NEEDS_VERIFICATION] github.com/ultrafunkamsterdam/nodriver
- [NEEDS_VERIFICATION] github.com/daijro/camoufox
- [NEEDS_VERIFICATION] github.com/Kaliiiiiiiiii-Vinyzu/patchright
- [NEEDS_VERIFICATION] github.com/Vinyzu/Botright
