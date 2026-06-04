# 拼多多 anti_content (PDD anti-bot) - notes

## 摘要

拼多多最核心的反爬参数：

| 参数 | 含义 | 形态 |
|---|---|---|
| `anti_content` | 反爬令牌（base64 嵌套+多层 zlib+WASM） | POST body / Query |
| `Sec-Ch-Ua` 等 UA-CH | 风控辅助 | Header |

**特征**：
- 起始字符常见 `0CN0H...`、`0asA...`，长度 800-2000 字符。
- 内含 base64 → zlib decompress → 一段 binary blob，是 WebAssembly 模块的输入。
- 部分版本的小程序+H5 共用，但 App 端有 Native SO 独立实现。

## 识别签名

- POST body 含 `anti_content`，长度 ≥ 800。
- 浏览器报 CSP-Report-Only（小程序逆向时常见的拦路虎，需要绕开 CSP 才能跑 jsvmp 调试）。
- App 抓包头里常见 `pdd-mt-platform`/`pdd-mt-version`+sec-* cookie 群。
- 端 SO 名：`libcore-dev.so` / `libc++_shared.so` 旁边的 `libpdd*` 系列。

## 还原方法

1. **Web/H5**：
   - 搜 `anti_content`→定位生成函数→跟栈分析。
   - jsvmp dispatcher 较多，建议先 AST 解混淆（webcrack 工具）。
   - WASM 部分用 `wabt`/`wasmtime` 反编译 + 静态分析（数十 KB 不大）。
   - 小程序里函数名相近但文件结构不同。
2. **App**：
   - 走 unidbg 黑盒最稳。
   - 关键是 device_id 与 anti_content 强绑定，复用要保证设备一致。
3. **补环境**：
   - 拼多多重度依赖 `document.createElement('canvas')`、`Image`、`XMLHttpRequest`、`navigator.userAgent`，缺一会拒。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q5](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [JS 逆向某多多 anti_content (博客园 sbhglqy 2025-06)](https://www.cnblogs.com/sbhglqy/p/18919287)
- [JavaScript 逆向 拼多多 anti_content (知乎)](https://zhuanlan.zhihu.com/p/654954767)

进阶：
- [拼多多 anti_content 全链路解析与动态对抗 (东大)](http://www.chinadongda.com/j/?weixin_29323365/article/details/158958178)
- [拼多多 anti-content 核心算法解密+修复 (术之多)](https://www.shuzhiduo.com/A/lk5aZjpod1/)
- [拼夕夕小程序 anti_content (看雪 2024-08)](https://bbs.kanxue.com/thread-283125.htm)

公开仓库：
- [gitbenxing/anti-content](https://github.com/gitbenxing/anti-content)

视频：
- [拼多多爬虫逆向 25 年最新 anti-content (B 站 2026-04)](https://www.bilibili.com/video/BV1QKbxzLEqG/)

## 工作流建议

1. 先确定攻击面是 Web、小程序还是 App。
2. Web: chrome devtools + 关掉 CSP（用 chrome flag --disable-web-security 或 mitmproxy override）。
3. 关键的几个 sub-call: `_p.encrypt()`, `_p.compress()`, `WebAssembly.instantiate(...)`. hook 它们能拿 input/output。
4. WASM 模块体积小，可以直接静态反编译 → 重写成 JS/Python。
5. device_id+anti_content+Cookie 三者绑定，单独复用 anti_content 会被风控反爬。

## 关键术语

- **CSP-Report-Only**：拼多多 H5 设了 Content-Security-Policy，加 `eval`/`new Function` 时会报警，但还能跑——逆向时要避免污染日志。
- **0CN0H**：anti_content 第一段 base64 解码后的特征字节。
