# 抖音 Web X-Bogus / _signature / msToken - notes

## 摘要

抖音 Web 端是字节系 Web 风控的旗舰，参数：

| 参数 | 含义 |
|---|---|
| `X-Bogus` | 主签名（webmssdk.js jsvmp 算出） |
| `_signature` | 老版签名，部分接口仍校验 |
| `msToken` | 会话 token（接口返回，cookie 持续） |
| `X-Argus` / `X-Ladon` | 部分高敏接口启用 |
| `a_bogus` | X-Bogus 的演进版（部分接口启用） |
| `X-Gnarly` | 设备指纹检测（Webmssdk.js + 日志钩子） |
| `x-tt-params` | 加密 query string |

## 识别签名

- Query 含 `X-Bogus`，长度 28 字符。
- 接口形如 `aweme.snssdk.com`、`douyin.com/aweme/v1/...`。
- jsvmp 主文件：`webmssdk.js`（关键字）。

## 还原方法

1. 抓 HTML → `<script src="...webmssdk.js">` → 拉下来。
2. 该 jsvmp 是字节自家 vmp，与 obfuscator.io 不一样：dispatcher + 大字节码数组 + register 风格。
3. 三选一：
   - **RPC**：开 jsdom + flask/express 暴露接口，最快。
   - **补环境**：用 sdenv/jsdom，mock document/navigator/canvas，注意 `Math.random()` 做风控不能 mock 成固定值（要给真随机）。
   - **纯算**：插桩取字节码，Python 复现 dispatcher。
4. **TLS 指纹**：抖音 Web 校验 JA3，必走 `curl_cffi`。

## raw-hits 来源

- 见 [raw-hits/android-batch2.md Q12](../raw-hits/android-batch2.md)。
- App 端关联：见 [bytedance-x-gorgon-x-argus-notes.md](../android/bytedance-x-gorgon-x-argus-notes.md)。

## 关键 URL

入门：
- [抖音下载视频+X-Bogus 参数 JS 逆向 (博客园 fuchangjiang)](https://www.cnblogs.com/fuchangjiang/p/17891223.html)
- [JS 逆向案例 X-Bogus 补环境 (lyy077)](https://lyy077.github.io/JS逆向案例——某音X-Bogus参数逆向分析之补环境/)

进阶：
- [[原创] WEB 逆向 X-Bogus 纯算+补环境 (看雪)](https://bbs.kanxue.com/thread-281237.htm)
- [Python 逆向 TikTok msToken+X-Bogus+signature (e-com-net)](https://www.e-com-net.com/article/1902557145006665728.htm)
- [TK X-Gnarly：AI 辅助 JSVMP 纯算还原 (zeeklog 2026-04)](https://zeeklog.com/tk-x-gnarly-ji-yu-ai-fu-zhu-de-jsvmp-chun-suan-huan-yuan-fang-an-2)
- [JSVMP 纯算还原 X-Bogus (K 哥爬虫 博客园 2022)](https://www.cnblogs.com/ikdl/p/16807224.html)

公开仓库：
- [B1gM8c/X-Bogus](https://github.com/B1gM8c/X-Bogus)
- [pysunday/sdenv (补环境框架)](https://github.com/pysunday/sdenv)

## 工作流建议

1. 入门看 K 哥那篇 JSVMP 教程，建立"插桩 → opcode 序列 → dispatcher 还原"的概念。
2. 同一份 webmssdk.js 大约一两周更新一次，需要写自动 diff/重还原工具。
3. msToken 由 `/web/common/msToken` 接口返回，必须保持 cookie 连贯。
4. 实际生产用 Cookie+device_id+UA 三者绑定，单个绕过往往不够。
