# 字节系（抖音/TikTok/今日头条/剪映等）风控参数 - notes

## 摘要

字节系 App 在 Android/iOS/Web 三端共享一套加密栈，核心 SO 是 `libEncryptor.so` / `libmsaoidsec.so` / `libsscronet.so` / `webmssdk.js`（Web 端）。最常见的"四神"参数：

| 参数 | 含义 | 出现位置 |
|---|---|---|
| `X-Khronos` | 时间戳（秒级，明文） | Header |
| `X-Gorgon` | 校验值（V0~V5 演进，常见 0408/0404 前缀） | Header |
| `X-Argus` | 设备指纹+签名（Protobuf 序列化后加密） | Header |
| `X-Ladon` | URL/Body 派生签名（与 Gorgon/Argus 联动） | Header |
| `X-Helios` | 设备状态 protobuf | Header |
| `_signature` / `X-Bogus` / `X-Ladon` (web) | Web 端三件套 | Query / Header |
| `msToken` | mssdk_token，会话级 token | Cookie/Query |

字节 Web 端额外用 jsvmp 包了 `webmssdk.js`，从 V0~V5 演进，混淆强度逐版增大。

## 识别签名

- Header 里同时出现 `X-Gorgon` / `X-Khronos` / `X-Argus` / `X-Ladon` 四个——必字节系。
- 抓 SO，`libmsaoidsec.so` / `libEncryptor.so` / `libsscronet.so`——字节系。
- Web 端 query 里看到 `X-Bogus` / `_signature` / `msToken` / `X-Argus`——字节系。
- jsvmp 字节码 + dispatcher 模式 + 大数组 const+`switch(opcode)`，且变量名形如 `_0xa1b2`（obfuscator.io）后再被 jsvmp 包。

## 还原方法概览

1. **App 端 Native**：
   - 静态：`jadx` 看 Java 入口，找到注入 `X-Argus` 的 OkHttp Interceptor。
   - 动态：Frida hook `Java.use("Lcom/bytedance/frameworks/baselib/network/http/cronet/CronetClient;").addRequestHeader`。
   - 黑盒：`unidbg-boot-server` + 调用 SO 的导出函数，输入 URL/Body/Cookie 输出四神。
2. **Web 端**：
   - 抓 `webmssdk.js`，切到 jsvmp dispatcher 处下断点。
   - 走"三选一"：RPC 远程调用 / 补环境（用 `pysunday/sdenv` 或 jsdom）/ 纯算还原（耗时）。
3. **TLS 指纹层**：字节家的网关同时校验 JA3，Python `requests` 必走 `curl_cffi` 或 `tls-client`。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q1, Q2](../raw-hits/android-batch1.md) 和 [android-batch2.md Q12](../raw-hits/android-batch2.md)。

## 关键 URL（按入门→进阶）

入门：
- [tiktok 逆向 四神算法寻找 (博客园 2024-11)](https://www.cnblogs.com/aayr/articles/18534131)
- [tiktok 最新版四神算法 36.7.4 (CSDN 2024-10)](https://blog.csdn.net/qq_48840175/article/details/141783427)
- [抖音 X-Bogus 逆向 (B 站视频)](https://www.bilibili.com/video/BV1aF4m1P7un/)

进阶：
- [X-Argus X-Gorgon X-Ladon 抖音 ida 反反调试 (知乎)](https://zhuanlan.zhihu.com/p/625877787)
- [抖音 xgorgon 0408 数据加密算法 (Gitee liqiumeng)](https://gitee.com/liqiumeng/a20201212-111126-124)
- [unidbg 主动调用 tiktok so 生成签名 (逆想技术)](https://nixiang.tech/forum.php?mod=viewthread&tid=401)

公开仓库：
- [huaerxiela/douyin-algorithm](https://github.com/huaerxiela/douyin-algorithm)
- [B1gM8c/X-Bogus](https://github.com/B1gM8c/X-Bogus)
- [armxe/tiktok-api](https://github.com/armxe/tiktok-api)
- [wmm1996528/unidbg_douyin11](https://github.com/wmm1996528/unidbg_douyin11)（教学 unidbg 案例）

## 工作流建议

1. 抓包→确认是字节系（看四神 Header）。
2. 决定攻击面：`unidbg` 黑盒最稳，`Frida` 调试最快，`webmssdk.js` 纯算最持久。
3. trace `X-Khronos` 是明文时间戳→对齐时区。
4. 锁定 SO 入口函数（一般在 `libmsaoidsec.so` 的 `_genArgus_native` 类似命名）。
5. 用 `frida-trace -i "*Argus*"` 定位实际工作函数。
6. 离线复现时记得：device_id、msToken、Cookie 必须三者绑定，否则 server 一致性校验会拒。

## 风险提示

- 字节系是国内风控最严的之一，对抗代价非常大。
- 直接绕过会被风控+IP+账号联合检测，单纯 sig 通过不代表能用。
- 长期可用方案是"真机集群+动态指纹快照"，仅对自有授权研究有意义。
