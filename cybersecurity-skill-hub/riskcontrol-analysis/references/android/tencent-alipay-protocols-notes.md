# 综合：腾讯系（QQ / 微信 mmtls）+ 支付宝 mPaaS - notes

## 一、QQ 协议（wtlogin）

### 关键
- `__NS_sig3` 不属于 QQ；QQ 的关键是 wtlogin 协议中的 `sign`。
- wtlogin 包含 TLV 结构：每个字段是 `T(2B) L(2B) V`。
- `wtlogin.login` 包要带 `sign` 签名+`tail`（尾签）。
- 客户端协议文件：`com.tencent.mobileqq:libsec.so` / `wtlogin_a.so`。
- 现役协议版本对账号要求严格（旧版本无法登录）。

### 还原
- `qsign` 系列工具（如 [QSign 9.0.56](https://mirai.mamoe.net/topic/2685/qsign-9-0-56-本地搭建方式开源)）封装 wtlogin 签名。
- 看雪有完整 wtlogin TLV 分析帖子。
- 注意：有些版本检测重打包+签名校验（"hidekey" 类的反破解）。

### URL
- [[原创] 最新 QQ APK 逆向重打包 (看雪 2015)](https://bbs.kanxue.com/thread-206742.htm)
- [腾 xQ 协议逆向 TLV 分析 (CSDN 2023-07)](https://blog.csdn.net/weixin_44320760/article/details/132007272)
- [QQ 协议纪实 (fuqiuluo 2024-04)](https://blog.xinrao.moe/archives/qqxie-yi-ji-shi)
- [NTQQ Windows 解密 (QQDecrypt)](https://qqbackup.github.io/QQDecrypt/decrypt/NTQQ%20(Windows).html)
- [QSign 9.0.56 本地搭建 (MiraiForum 2024-07)](https://mirai.mamoe.net/topic/2685/qsign-9-0-56-本地搭建方式开源)
- [后协议时代 QQ Bot 生存指南 (Misa Liu 2024-01)](https://blog.misaliu.top/archives/142/)

## 二、微信 mmtls (基于 TLS 1.3 草案)

### 概念
- 微信不直接用标准 TLS——用基于 TLS 1.3 草案设计的 `mmtls`（移动 mTLS）。
- 协议文件公开在 [WeMobileDev/article 仓库](https://github.com/WeMobileDev/article/blob/master/基于TLS1.3的微信安全通信协议mmtls介绍.md)。
- 网络库 `Mars`（[Tencent/mars](https://github.com/Tencent/mars)）开源，但 mmtls 实际私钥+证书在客户端硬编码。

### 设计
- 砍掉算法选择，固定一套 cipher。
- RTT-1 协商完成（比标准 TLS 1.3 更快）。
- 只 server 单向认证，不验证 client。

### 抓包
- 标准 mitmproxy 抓不到（不是标准 TLS）。
- 通过 Frida hook Java 层收发包函数 → 输出 Protobuf 数据（不解密 mmtls 直接拿明文）。
- 车载微信抓包思路（理论全版本通杀）：jadx 定位日志类 → hook 网络代码 → dump payload。

### URL
- [基于 TLS1.3 的 mmtls 介绍 (官方)](https://github.com/WeMobileDev/article/blob/master/基于TLS1.3的微信安全通信协议mmtls介绍.md)
- [[原创] mmtls 分析研究 (看雪 2020)](https://bbs.kanxue.com/thread-257942.htm)
- [mmtls 详解 (CSDN 2020)](https://blog.csdn.net/u014431237/article/details/109616876)
- [车载微信抓包通杀 (吾爱破解 2025-11)](https://www.52pojie.cn/thread-2071262-1-1.html)
- [车载微信抓包 (zone.ci 2026-01)](https://zone.ci/secarticles/wx/490170.html)
- [逆向 WeChat mars (博客园 bbqzsl 2024-05)](https://www.cnblogs.com/bbqzsl/p/18209439)
- [mmtls 分析 (杜某某 2019-12)](https://blog.dujiajun.site/2019/12/23/微信安全通信协议mmtls分析/)
- [Mmtls 协议分析 (tcc0lin 2023)](https://tcc0lin.github.io/posts/mmtls协议分析/)

### 工作流
1. 抓包前先确认是 mmtls（看 Wireshark 内 TLS handshake 有没有标准 ClientHello）。
2. 不是 mmtls 就走 SSL Pinning Bypass + 标准抓包。
3. 是 mmtls 就走 Frida 在 Java 层 hook 收发包函数 dump 明文。
4. mars 库与 mmtls 实现都开源，可以本地编译做调试。

## 三、支付宝 / 阿里 mPaaS

### 关键参数
- `APDID`：阿里账号设备 ID（mPaaS 体系，跨支付宝/钉钉/淘宝）。
- `umid` / `umidtoken`：阿里聚安全设备 ID。
- `rds` / `riskidx`：风控参数。
- `sign`：mtop 协议签名（与淘宝同源，详见 [taobao-libsgmain-notes.md](../android/taobao-libsgmain-notes.md)）。

### 关联
- 支付宝 SDK 其实是基于淘宝 SecurityGuard 的衍生。
- mPaaS 是蚂蚁的移动开发平台 SDK，含小程序内核+RPC+sign。

### URL
- [DebugKingXXX/Taobao-Reverse-algorithm-service (GitHub)](https://github.com/DebugKingXXX/Taobao-Reverse-algorithm-service)
- [支付宝小程序 sign 验签参数 (吾爱破解 2021)](https://www.52pojie.cn/thread-1482566-1-1.html)
- [支付宝证书签名+验签 Python (腾讯云 2022)](https://cloud.tencent.com/developer/article/2082915)
- [支付宝 v3 自签名实现 (博客园)](https://www.cnblogs.com/yjdmx/p/17918400.html)
- [支付宝 RSA + AES 双重 (阿里云)](https://developer.aliyun.com/article/862208)
- [支付宝官方自行实现签名](https://opendocs.alipay.com/common/057k53)

### 工作流
- 支付宝相关接口签名：见官方文档 + 阿里 mtop 同源（详见 taobao 篇）。

## raw-hits 来源

- QQ：[android-batch3.md Q8](../raw-hits/android-batch3.md)
- 微信 mmtls：[android-batch3.md Q6](../raw-hits/android-batch3.md)
- 支付宝：[android-batch3.md Q7](../raw-hits/android-batch3.md)
