# 知乎 x-zse-96 - notes

## 摘要

知乎 Web/H5 端核心签名：

| 参数 | 含义 |
|---|---|
| `x-zse-93` | 客户端版本指示 |
| `x-zse-96` | 主签名（jsvmp + SM4 + 自定义编码） |
| `x-zst-81` | 设备/会话上下文 token |
| `d_c0` | 长期设备指纹 cookie |
| `__zse_ck` | 二级风控 cookie |

**算法概览**：
```
plain = "{ver}+{path}+{cookie_d_c0}+{x-zst-81}"
md5 = MD5(plain)
sm4_ct = SM4_CBC_modified(md5, hardcoded_key, hardcoded_iv)
x-zse-96 = "{ver}_" + custom_b64(sm4_ct)
```

`SM4_CBC_modified` 是魔改 SM4：常量、S 盒、轮密钥派生都改了；`custom_b64` 也是非标准编码（位混洗+替换表）。

## 识别签名

- Header `x-zse-96` 长度 ~80 字符，前缀 `2.0_`。
- 接口路径 `/api/v4/...`、`/api/v3/...`。
- jsvmp dispatcher：`window.zhuanlan` / `c.encrypt` 类入口。

## 还原方法

1. **打 XHR 断点**：搜 offset 参数的 XHR 断点，进入 jsvmp 的 dispatcher。
2. **AI 还原**：2026 年开始 K 哥/CN-SEC 等给出基于 AI 辅助的纯算还原方案（CN-SEC 2026-04 那篇含 SM4-CBC 拆解 + 位混洗公式）。
3. **补环境**：`jsdom` 模拟，`d_c0` 必须真实（用 chrome 跑一次取出来）。
4. **纯算还原**：把 SM4 的修改部分还原（找常量），然后整套用 Python 复现。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q9](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [知乎 x-zse-96 算法 (二进制之旅 2026-03)](https://blog.xzregister.cn/2026/03/18/zh/) — okhttp3 hook + com.zhihu.android.o.a.a 定位
- [知乎 x-zse-96 算法 (知乎专栏)](https://zhuanlan.zhihu.com/p/419576219)

进阶：
- [Ai 还原 x-zse-96 vmp 纯算 (CN-SEC 2026-04)](https://cn-sec.com/archives/5184884.html) — SM4-CBC + 位混洗公式 + ZK 篡改
- [Ai 还原 x-zse-96 vmp 纯算 (ZONE.CI)](https://zone.ci/secarticles/wx/522564.html)
- [保姆级教程 Node.js+jsdom (CSDN 2026)](https://blog.csdn.net/weixin_42531925/article/details/160814927)
- [知乎 x-zse-96 Python (hey99 mirror 2026-02)](https://www.hey99.cn/shot/CSDN_158014576)

## 工作流建议

1. 在 Chrome DevTools Sources 面板打 `XHR/fetch breakpoint`，访问任意接口被断住。
2. 一路 step-out 到 dispatcher 入口，下条件断点观察 plain 内容。
3. 拿到 plain 后单独 MD5，对比 server 期望的 sig 第一段，验证 plain 拼接顺序。
4. SM4 魔改部分用 KCipher 工具或 `pycryptodome` 自定义 sbox 手工实现。
5. `x-zst-81` 与 `d_c0` 是会话级，必须连贯采集。
