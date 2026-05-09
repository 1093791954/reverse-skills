# 快手 __NS_sig3 / __NStokensig - notes

## 摘要

快手 App 与 Web 共用 `libsgmain.so`（与阿里同名同源不同算法），核心三件套：

| 参数 | 含义 |
|---|---|
| `__NS_sig3` | 主签名（48 字节 hex） |
| `__NStokensig` | 令牌签名 |
| `sig` | 基础签名 |
| `kpf` / `kpn` | 平台标识 + App 名（明文常量） |
| `did` / `egid` | 设备 ID |

**核心算法**：libsgmain.so 0x2d4b6 处是魔改 SHA256，sub_3FDA4 是后处理（base64x2），最终拼成 sig3。

## 识别签名

- Header / query 出现 `__NS_sig3`+`__NStokensig`。
- SO：`libsgmain.so`（注意与阿里同名，但实现不同）。
- 接口 host：`*.kuaishou.com`、`*.kwaixiaodian.com`、`*.gifshow.com`。
- App 包名：`com.smile.gifmaker`、`com.kuaishou.nebula`、`com.kuaishou.athena`。

## 还原方法

1. **App native**：jadx → 找 `com.kuaishou.android.security.SafetyManager` → JNI 调用 → libsgmain.so。
2. **黑盒**：unidbg 直接 invoke libsgmain 导出函数。
3. **trace 关键函数**：sub_3FDA4 是 SHA256 → base64 → base64 链路。
4. **frida-rpc**：simple 在真机 hook 关键函数，按 device_id 派发计算。
5. Web 端用 jsvmp（强度低于 App），关键函数好定位，直接走 RPC 或扣码。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q8](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [逆向实战：用 Python 复现快手 sig3 和 tokensig (CSDN 2026)](https://blog.csdn.net/weixin_26757939/article/details/160879607)
- [快手 __NS_sig3 接口动态参数 (掘金 2025-04)](https://juejin.cn/post/7490973048242749490)

进阶：
- [[原创] 某手 910 版本 sig3 48 位算法逆向 (看雪)](https://bbs.kanxue.com/thread-271489.htm) — sha256 魔改特征定位
- [快手极速版逆向 sig & NStokensig (YBlog 2025-01)](https://blog.2zxz.com/archives/nebula_sig_nstokensig)
- [ks/sig3 分析 (x14nuy 2025-07)](https://x14nuy.github.io/2025/07/01/ks-sig3分析/)
- [快手 __NS_sig3 sig3 算法分析 (CFANZ)](https://www.cfanz.cn/mobile/resource/detail/DoqWOxGoQzkyp)

公开仓库：
- [gaozhenqiang/kwai-ns_sig3 (GitHub)](https://github.com/gaozhenqiang/kwai-ns_sig3)

## 工作流建议

1. 锁定接口（视频列表/直播/评论）。
2. 抓 SO，先静态找 sha256 魔改特征（`0x428a2f98` 等 K 常量被改的话特别明显）。
3. 用 Frida hook 0x2d4b6 + sub_3FDA4 双断点，记录输入/输出。
4. Python 重写：`def sig3(data, salt, did): h = sha256_modified(data+salt+did); s = mod_b64(h); return mod_b64(s)`。
5. 与 Boss/Datawhale 类似，快手对 device_id 高度敏感，跨设备复用会被风控。
