# 美团 mtgsig (Meituan Risk Control) - notes

## 摘要

美团/大众点评全系列 App 与 Web 共用一套加密栈，核心参数：

| 参数 | 含义 | 出现位置 |
|---|---|---|
| `mtgsig` | 主签名（v1→v2.4→v3.0→v4.0+） | Header |
| `_token` | 老版会话 token（h5/小程序常见） | Cookie / Query |
| `riskLevel` | 风控等级（服务器返回） | Response |
| `x-mt-bx-v` | 浏览器/客户端环境签名 | Header |

**演进**：mtgsig 1.x 简单 MD5；2.4 引入 native + reflection；3.0 加入 CSEL 混淆 + 风控强化（关键函数加 `csel x9, x10, x11, NE` 等条件分派）；4.0+ 走 jsvmp + WASM（h5），4.03 是公开分析最新版本。

## 识别签名

- Header `mtgsig`，长度 ~120 字符（base64 风格）。
- Web 端 `H5guard.js` / `rohr.js` 是 jsvmp dispatcher，`H5guard` window 全局对象。
- App 端 SO：`libmtguard.so` / `libmtsec.so`。
- 接口形态：`/group/v4/poi/...`、`/api/c/v1/...`、`/api/v8/...`，请求头必带 `mtgsig`。

## 还原方法

1. **Native（App 端）**：
   - jadx 找 mtgsig OkHttp Interceptor，跟到 `MTGuardSignManager.sign(...)` 类。
   - Frida hook 打印输入参数，输出 mtgsig；observe 算法分支。
   - 关键函数会有 CSEL 条件分派混淆，需要先去 OLLVM 平坦化（参考 `d-810` / `Triton`）。
2. **Web/H5**：
   - 抓 `rohr.js`，搜 `mtgsig` 字符串，定位 `function require('rohr.js')` 的初始化点。
   - 补环境路线：用 `sdenv` / `vm2` / jsdom，把 H5guard 全局对象渲染好。
   - 纯算路线：解 jsvmp 字节码后用 Python 复现，注意 H5guard 用了 WASM 模块，需要 `wasmtime`/`wabt` 反编译。
3. **小程序**：先解包 wxapkg，分析里面的 `H5guard` 等价物。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q3](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [逆向实战：美团外卖 App mtgsig3.0 (CSDN 2026)](https://blog.csdn.net/weixin_42533120/article/details/160788291)
- [Web 美团 mtgsig 算法逆向 (教书先生)](https://blog.oioweb.cn/121.html)

进阶：
- [[原创] 某团 App mtgsig2.4 (看雪)](https://bbs.kanxue.com/thread-280779.htm) — 评论里提到 3.0 多了 CSEL 混淆
- [美团 mtgsig 4.03 (51CTO 2026-04)](https://blog.51cto.com/u_15835408/14542925)
- [某团小程序 _token + mtgsig (博客园 zichliang)](https://www.cnblogs.com/zichliang/p/18868079)

公开仓库：
- [dogsoft1990/mtgsig: 美团外面 mtgsig 3.0 大致算法 (GitHub)](https://github.com/dogsoft1990/mtgsig)

## 工作流建议

1. 锁定接口（点外卖/查商家/看评价）。
2. 抓包→记录 mtgsig 与 URL/body 的关系（同一接口、同一 body、不同时间→sig 是否变？通常会变，跟 `device_id`+`timestamp` 绑定）。
3. 选攻击面：App 端建议 unidbg 黑盒；H5 端建议先扣 H5guard 的 init 段再跟 sign。
4. CSEL 混淆是 3.0+ 的硬骨头，先用 `d-810`/`Triton` 把它平坦化掉。
5. 离线回放时注意：mtgsig 与 device_id 强绑定，多设备共用同一 device_id 会被判异常。

## 关键术语

- **CSEL 混淆**：ARM64 的条件移动指令 `csel xt, xa, xb, cond`，被用作 if-else 分派器。需要双状态 angr 模拟。
- **H5guard**：美团 web 端 jsvmp 主类。
- **rohr.js**：H5guard 加载器之一。
