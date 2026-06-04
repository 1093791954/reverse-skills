# Toolchain：SSL Pinning Bypass (Android & iOS) - notes

## 一、Android 端

### Pinning 机制
1. **TrustManager**：自定义 X509TrustManager 校验证书。
2. **OkHttp CertificatePinner**：固定 SHA256 fingerprint。
3. **Retrofit**：基于 OkHttp。
4. **Volley**：基于 HttpURLConnection。
5. **Network Security Config**：Android 7+ 标准方式（`<pin-set>`）。
6. **Native Pinning (BoringSSL/OpenSSL)**：在 SO 内部直接验签，最难绕。

### 经典 Frida hook 点

- `javax.net.ssl.SSLContext.init`
- `javax.net.ssl.X509TrustManager.checkServerTrusted`
- `okhttp3.CertificatePinner.check`
- `okhttp3.internal.tls.OkHostnameVerifier.verify`
- `com.android.org.conscrypt.TrustManagerImpl.verifyChain`

### 工具

- **objection**：`objection -g <pkg> explore` → `android sslpinning disable`，一键搞定 Java 层 pinning。
- **Frida Universal SSL Pinning Bypass 脚本**：[CYRUS-STUDIO/frida-ssl-pinning-bypass](https://github.com/CYRUS-STUDIO/frida-ssl-pinning-bypass) Java+Native 全自动。
- **codeshare**：`frida --codeshare Q0120S/bypass-ssl-pinning -f <pkg>`。
- **apk-mitm**：`shroudedcode/apk-mitm`，自动 patch APK 让用户证书被信任。
- **MagiskTrustUserCerts**：把用户证书移到 system 证书目录（Android 7+ 用户证书默认不被信任）。
- **AlwaysTrustUserCerts (Xposed)**：Xposed 模块版。

### Android 7+ 用户证书问题
- Android 7 起，Network Security Config 默认拒绝信任用户安装的 CA。
- 解决：
  1. 改 manifest `android:networkSecurityConfig` + 自定义 NSC（要重打包）。
  2. 用户证书移到 `/system/etc/security/cacerts/` （需要 root）。
  3. Magisk 模块 MagiskTrustUserCerts 自动化第 2 种。
  4. apk-mitm 自动 patch APK + NSC。

## 二、iOS 端

### Pinning 机制
- `NSURLSession`：默认 ATS。
- `CFNetwork`：底层。
- `Security.framework`：`SecTrustEvaluate*`。
- `BoringSSL`：iOS 14+ 部分库走。
- `Network.framework`：iOS 12+。
- `Alamofire/AFNetworking`：第三方网络库。

### 工具

- **SSL Kill Switch 2**：越狱设备最方便，系统级 disable pinning。`Lessica/SSL-Kill-Switch-2-Reborn` 是当前维护版。
- **objection**：`ios sslpinning disable`，跨多个网络栈。
- **pritessh/iOS-SSL-Pinning-Bypass**：iOS 17 + 现代框架（Security.framework / BoringSSL / Network.framework / Alamofire）。
- **frida codeshare**：`lichao890427/ios-ssl-bypass`。

### iOS 17+ 的难点
- BoringSSL 内部 pinning 很多 App 自带，标准 Frida 脚本不够。
- 需要 hook `boringssl_session_set_socket_bio` / `SSL_set_verify` / `SSL_CTX_set_verify` 等多个底层函数。

## raw-hits 来源

- Android：[toolchain-batch1.md Q5](../raw-hits/toolchain-batch1.md)。
- iOS：[ios-batch1.md Q5](../raw-hits/ios-batch1.md)。

## 关键 URL

Android：
- [CYRUS-STUDIO/frida-ssl-pinning-bypass Java+Native (GitHub)](https://github.com/CYRUS-STUDIO/frida-ssl-pinning-bypass)
- [Bypass SSL Pinning (frida codeshare Q0120S)](https://codeshare.frida.re/@Q0120S/bypass-ssl-pinning/)
- [Frida Android SSL Pinning 实战 7 (技术栈 2025-11)](https://jishuzhan.net/article/1991704466169593858)
- [Android15 Frida 绕过 SSL (CN-SEC 2025-04)](https://cn-sec.com/archives/3916232.html)
- [Android 证书绑定绕过 (CSDN)](https://blog.csdn.net/qq_30135181/article/details/119677157)
- [FridaBypassKit SSL Pinning (DeepWiki)](https://deepwiki.com/okankurtuluss/FridaBypassKit/4.2-ssl-pinning-bypass)

iOS：
- [Bypassing SSL Pinning on iOS (redfoxsec 2025-08)](https://www.redfoxsec.com/blog/bypassing-ssl-pinning-on-ios-applications)
- [pritessh/iOS-SSL-Pinning-Bypass iOS17 (GitHub)](https://github.com/pritessh/iOS-SSL-Pinning-Bypass)
- [iOS SSL Bypass (lichao890427 codeshare)](https://codeshare.frida.re/@lichao890427/ios-ssl-bypass/)
- [iOS 安装 SSL Kill Switch 2 (知乎)](https://zhuanlan.zhihu.com/p/409394356)
- [Bypassing SSL Pinning iOS Comprehensive (Medium)](https://medium.com/@sachin.hack/bypassing-ssl-pinning-on-ios-devices-a-comprehensive-guide-2fb6cef461aa)
- [iOS 突破 SSL Pinning 抓包 (极客文档)](https://geekdaxue.co/read/sunj3t@uaxxwi/tu-po-ssl-pinning-jin-xing-zhua-bao)
- [SSL Kill Switch 2 Reborn](https://github.com/Lessica/SSL-Kill-Switch-2)

## 工作流建议

1. **先 objection 一刀**：`android sslpinning disable` / `ios sslpinning disable`，能搞定 70% 的 App。
2. **不行**：Frida codeshare 几个通用 universal 脚本试一遍。
3. **还不行**：自己在 SSL_CTX_set_verify / SSL_set_verify / 关键 BoringSSL 函数 hook。
4. **最难**：Native pinning 在 SO 内部 → 反编译找校验函数 → 直接 patch 跳过。
5. **抓不到包**：还要看是不是 mtls 或 mmtls 之类自定义协议（如微信），不是标准 TLS 那 SSL Pinning bypass 没用。
