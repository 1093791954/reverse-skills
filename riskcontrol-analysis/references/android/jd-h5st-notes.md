# 京东 h5st + x-api-eid-token - notes

## 摘要

京东全栈风控的核心参数：

| 参数 | 含义 | 演进 |
|---|---|---|
| `h5st` | H5/Web/小程序通用签名（8 段结构） | 3.x → 4.7 → 4.7.4 → 5.x → 5.3.2 |
| `x-api-eid-token` | 风控 token（接口返回，绑定浏览器环境/指纹） | - |
| `_jdb_` | 设备指纹 cookie | - |
| `fp` | 浏览器指纹（Canvas/WebGL/AudioContext 拼接） | - |

**h5st 8 段结构**（典型）：
```
{timestamp}-{client_token_id}-{appid}-{fp}-{body_sha256}-{ext_data}-{algo_version}-{sig}
```

各段用 `;` 或 `;` 类分隔。其中 `fp` 必须与第二段的 `client_token_id` 绑定，否则验签失败（aes 加密时用 fp 作为 key 派生输入）。

## 识别签名

- Header / Body 出现 `h5st`，分隔符明显的 8 段。
- 接口域名 `api.m.jd.com`、`apipub-search-x0.jd.com`、`isv.beans.jd.com` 等。
- jsvmp：`window.JdAjax`、`__JD_FP__`、`PaaS` 命名空间。
- 4.7.x 起，部分模块走 VMP（jsvmp），代码大数组+`switch(opcode)` 风格。

## 还原方法

1. **路径定位**：从 `XHR/Fetch breakpoint` 入手，搜 `h5st` 字符串，跟到 `function generateH5st(args)` 类入口。
2. **三选一**：
   - **RPC**：浏览器跑+Python 调，简单可靠。
   - **补环境**：扣完整 `__JD_FP__` 初始化逻辑，注意 `fp` 内含 Canvas+WebGL 字符串，必须给逼真值。
   - **纯算**：jsvmp 字节码 dispatcher 还原 + Python/Go 复现。`某东 4.7 jsvmp` 公开 writeup 给了完整流程。
3. **关键技巧**：京东 `h5st` 的 AES 加密用 `fp` 派生 key，**所以 fp 必须与第二段 client_token_id 一致**——这是网上很多复现失败的原因。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q4](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [京东 h5st 4.7 逆向分析 (FreeBuf 2024-05)](https://www.freebuf.com/articles/web/400807.html) — 含 x-api-eid-token 说明
- [爬虫&逆向 京东 h5st (博客园)](https://www.cnblogs.com/352387312-dada/p/19109300)

进阶：
- [某东 4.7 jsvmp 算法还原 (skuukzky 2024-08)](https://lpy30m.github.io/skuukzky.github.io/2024/08/23/逆向/某东4-7jsvmp-算法还原/)
- [某东签名算法 jsvmp 插桩法纯算还原 (舟涯 2025-11)](https://blog.zhx47.top/archives/1762148186443)
- [京东 h5st 5.3.2 (CSDN 2026)](https://blog.csdn.net/kevinsir2003/article/details/131904373)

视频：
- [JS 逆向-京东 H5ST 全流程 (B 站)](https://www.bilibili.com/video/BV1gE4m1d7n6/)

## 工作流建议

1. 抓 ~3 个搜索/列表/购物车请求，每个都记下 h5st 的 8 段。
2. 验证："时间戳"段是 ms；"appid"是固定值（区分 PC/M/小程序）；"fp"段每次相同（同一会话）；"body_sha256"按业务变化。
3. 锁定 jsvmp dispatcher，patch 入口插日志看 opcode 序列。
4. fp 是关键，必须真实生成（用真浏览器跑一次取出来 reuse 即可）。

## 关键术语

- **PaaS**：京东内部 jsvmp 命名空间。
- **client_token_id**：前置 `/genToken` 接口返回，与 `fp` 绑定。
