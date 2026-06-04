# 小红书 Web x-s / x-t / x-s-common - notes

## 摘要

小红书 Web 端核心签名（与 App 端 `libtiny.so` 不同栈，但同等级别风控）：

| 参数 | 含义 |
|---|---|
| `x-s` | 主签名 |
| `x-t` | 时间戳（毫秒） |
| `x-s-common` | 通用风控载荷（含 localStorage 中的设备/会话字段） |
| `x-mns` | 二级风控参数（部分接口） |
| `signSvn` | 算法版本号（53 → 55 → ...） |

**特征**：webpack 打包+jsvmp+VMP 多层混淆，每月可能更新 signSvn 版本号。x-s-common 是把 localStorage 里若干字段拼接后用 x-s 同款 sign 加密。

## 识别签名

- Header 同时出现 `x-s` + `x-t` + `x-s-common`，且接口域名是 `*.xiaohongshu.com`。
- jsvmp dispatcher：`window.mnsv2` / `window.b1`（不同版本变量名变）。
- HTML 内会 `eval(atob(...))` 注入 jsvmp 代码到 window。
- 错误码 461/300/406 是 sig 校验失败的常见返回。

## 还原方法

1. **AST 解混淆**：先用 `webcrack` 或 `de4js` 把 obfuscator.io 层面的混淆 → 再处理 jsvmp 层。
2. **三选一路线**：
   - **RPC**：jsdom 跑+本地接口暴露，简单。
   - **补环境**：注意 `mnsv2` 初始化需要 `eval` 两段代码先注入到 window。
   - **纯算**：扣 jsvmp dispatcher → Python/Go 重写。
3. **localStorage 依赖**：x-s-common 会读 `localStorage['mz_test']`、`localStorage['xsecappid']` 等等十几个字段，必须在补环境里 mock 好。

## 与 App 端 libtiny 的关系

- App 与 Web 不共栈：libtiny.so（App）走 5 行明文 + 修改版 AES + RC4/HMAC 多层；Web 走 jsvmp + SM 系算法。
- 但 device_id / session_id 跨端共享，跨端复用风控会触发异常。

## raw-hits 来源

- 见 [raw-hits/android-batch2.md Q11](../raw-hits/android-batch2.md)。
- App 详细：见 [android/xhs-libtiny-notes.md](xhs-libtiny-notes.md)（已有 932 行 deep dive）。

## 关键 URL

入门：
- [小红书 X-s X-common 算法还原 202409 (ITADN)](https://itadn.com/i0_95642614292/3518771)
- [小红书 x-s-common 算法 (CSDN 2024-09)](https://blog.csdn.net/YCHMBb/article/details/142391556)

进阶：
- [某红书 X-s X-s-common VMP 逆向 (技术栈 2026-04)](https://jishuzhan.net/article/2047492177362747393)
- [某红书 Js 逆向思路 (掘金 2025-10)](https://juejin.cn/post/7563139451804254258) — eval 两段代码初始化 window.mnsv2

公开仓库：
- [Cloxl/xhshow (GitHub)](https://github.com/Cloxl/xhshow)
- [cornanluwei/xiaohongshu (Gitee)](https://gitee.com/cornanluwei/xiaohongshu)

## 工作流建议

1. 先抓 HTML 看 inline 注入的 jsvmp 启动段（`eval(atob(...))`）。
2. 把 jsvmp 入口点 dump 到独立文件再 AST 解混淆。
3. 补环境时优先 mock：`navigator`、`document.cookie`、`document.createElement`、`localStorage` 各项、`window.location`。
4. 验证 byte-by-byte：固定 device + 固定时间戳 → x-s 应稳定。
5. signSvn 升版后必须重新跑分析。
