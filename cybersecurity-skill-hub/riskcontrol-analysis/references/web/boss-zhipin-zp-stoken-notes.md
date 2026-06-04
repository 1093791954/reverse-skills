# Boss 直聘 __zp_stoken__ - notes

## 摘要

Boss 直聘是国内 Web jsvmp 强混淆代表之一：

| 参数 | 含义 |
|---|---|
| `__zp_stoken__` | 长会话 cookie（最关键） |
| `zp_stoken` | 短期 cookie |
| `zp_token` | 一次性 token |

**特征**：
- jsvmp 控制流平坦化（OLLVM 风格）。
- 动态代码：每次返回的 challenge JS 内容会变（变量名、字节序列）。
- 反 nodejs 检测：`__filename` / `Buffer` / `process` 在浏览器是 undefined 但在 nodejs 是 truthy → 直接补环境会被识别。

## 识别签名

- Cookie 含 `__zp_stoken__` 长串（base64 风格），长度 ~700 字符。
- 接口域 `www.zhipin.com`、`mp.zhipin.com`。
- F12 启动时会闪退（反开发者工具）。
- 触发 challenge 时返回 401 + Set-Cookie 一次性。

## 还原方法

1. **DrissionPage**：用真浏览器（CDP）跑一次，直接拿 cookie。最简单可靠。
2. **补环境**：必须 hide nodejs 特征（`__filename`、`Buffer`、`process`、`require` 都得 undefined）。`pysunday/sdenv` 已经处理了这些。
3. **纯算**：jsvmp 控制流平坦化要先用 `d-810`/`Triton` 还原。
4. **关键 hook 点**：搜 `__zp_stoken__` 字符串的位置打日志断点，跟到 `function generateStoken(args)` 类入口。

## raw-hits 来源

- 见 [raw-hits/android-batch2.md Q13](../raw-hits/android-batch2.md)。

## 关键 URL

入门：
- [boss 直聘 __zp_stoken__ 生成补环境 (CSDN 2024-02)](https://blog.csdn.net/qq_57325259/article/details/136320269)
- [boss 直聘最新版 zp_stoken 逆向 (知乎 2021)](https://zhuanlan.zhihu.com/p/425180886) — nodejs 检测 `__filename`/`Buffer`

进阶：
- [[原创] boss 直聘 __zp_stoken__ 控制流平坦化纯算 (看雪 2025-09)](https://bbs.kanxue.com/thread-288403-1.htm)
- [DrissionPage 爬 boss 直聘绕 __zp_stoken__ (技术栈 2026-03)](https://jishuzhan.net/article/2032643926889398273)
- [boss 直聘 __zp_stoken__ JS 混淆+AST (阿里云 2023-09)](https://developer.aliyun.com/article/1328914)

公开仓库：
- [zwgFF/zp_stoken_jsLearn (GitHub)](https://github.com/zwgFF/zp_stoken_jsLearn)

## 工作流建议

1. 先决定攻击面：浏览器自动化（DrissionPage / undetected-chromedriver / playwright stealth）能解决 90% 需求。
2. 真要纯算：先 D810 去 OLLVM 平坦化，再写 jsvmp dispatcher 还原。
3. `__zp_stoken__` 与 IP/UA 绑定，浏览器导出后不能换设备使用。
4. 留意 Boss 反 F12：用 chrome devtools 的 sources override 把 `setInterval/debugger` 这段无脑替换成 NOP。
