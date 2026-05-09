# 淘宝/阿里系 sign / wua / x-sgext / x-mini-wua - notes

## 摘要

阿里系 App（淘宝、天猫、咸鱼、1688、阿里巴巴、菜鸟、盒马等）共用一套加密栈，核心 SO 是 `libsgmain.so`，对应 mtop 网关协议。

| 参数 | 含义 |
|---|---|
| `x-sign` | 主签名（基于 AppKey + Token + body） |
| `x-sgext` | 扩展签名（设备/环境绑定） |
| `x-umt` / `umidtoken` | 阿里聚安全设备 ID |
| `x-mini-wua` | mini wua（带硬件参数，新设备无需账号也可获取部分数据） |
| `wua` / `x-features` | wua/security guard 衍生 |
| `_m_h5_tk` / `_tb_token_` | h5 端 mtop token |
| `bx-v` / `bx-c` | 阿里盾 challenge cookie |
| `isg` | session 风控 cookie |

**版本演进**：6.2 大量公开方案；6.3 算法变了，公开资料较少；7+ 加大 OLLVM。

## 识别签名

- Header 同时出现 `x-sign`+`x-t`+`x-appKey`+`x-sid`+`x-features`——必阿里系 mtop。
- SO：`libsgmain.so` / `libsgmainsoa.so` / `libsgmainso-6.4.x.so`。
- HTTP host 形如 `acs.m.taobao.com`、`api.m.taobao.com`、`acs.tmall.com`、`acs.youku.com`。
- Web mtop：`ua` 参数 + `_m_h5_tk` cookie + 接口路径含 `/h5/...` 或 `/gw/...`。

## 还原方法

1. **App native**：
   - jadx 找 `Lcom/taobao/wireless/security/adapter/JNICLibrary;` 类，`doCommandNative(int, ...)` 是入口。
   - command id 区分功能：sign/sgext/wua 各自 cmd id 不同。
   - libsgmain 重度 OLLVM，需要 `d-810` + `Triton` 去平坦化。
2. **黑盒**：unidbg 调用 `JNICLibrary.doCommandNative` + 提供 mock JNIEnv，得到输出。
3. **frida-rpc**：在真机上 hook `JNICLibrary.doCommandNative`，远程调用，简单可靠。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q6](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [淘宝 app 协议四神加密 (CSDN 2025-05)](https://blog.csdn.net/2501_92178017/article/details/148240665)
- [淘宝 app 协议四神 (知乎)](https://zhuanlan.zhihu.com/p/1910467398500348477)
- [app 安卓逆向 x-sign/x-sgext/x_mini_wua/x_umt (IoTWord)](https://www.iotword.com/13150.html)

进阶：
- [[原创] 淘宝 x-mini-wua 分析与破解 (看雪)](https://bbs.kanxue.com/thread-274616.htm)
- [电视淘宝 x-sign/x-umt/wua/x-mini-wua (灰信网)](https://www.freesion.com/article/10951592141/)

## 工作流建议

1. 抓包→记录 `x-sign` / `x-sgext` / `wua` 与 URL/AppKey/Token/timestamp 的依赖关系。
2. 注意 mtop h5 端用随机分配令牌 `_m_h5_tk`，每次取数据前会先调 `mtop.com.taobao.client.h5.getToken`。
3. App 端攻击：jadx → JNICLibrary.doCommandNative → cmd id 分类 → unidbg 模拟。
4. Web 端 ua 参数：先看是否依赖浏览器环境（Canvas+UA+Plugin 拼接），再走补环境路线。
5. 阿里盾 `bx-v`/`bx-c` 与 mtop sign 是两条不同的风控线，分别处理。

## 关键术语

- **mtop**：阿里移动开放平台协议，所有 App 接口都走它。
- **AppKey**：每个 App 一个固定值，与 sign 算法 key 一一对应。
- **doCommandNative**：libsgmain 的总入口，cmd id 决定子算法。
- **SecurityGuard SDK**：阿里聚安全的客户端 SDK，包含设备指纹+sign+加解密。
