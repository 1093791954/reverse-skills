# HTTP/2 Frame Fingerprint（http2-fingerprint）

> 配套 SKILL.md Path 11。

## 1. 检测维度

HTTP/2 协议规定：客户端建立连接后会发送一系列 frames。Akamai / Cloudflare 等通过观察这些 frame 的特征来识别"是不是真浏览器":

1. **SETTINGS frame**：
   - 各 setting 字段顺序（HEADER_TABLE_SIZE, ENABLE_PUSH, MAX_CONCURRENT_STREAMS, INITIAL_WINDOW_SIZE, MAX_FRAME_SIZE, MAX_HEADER_LIST_SIZE）
   - 各字段的具体值
2. **WINDOW_UPDATE**：客户端首次发送的窗口增量大小
3. **HEADERS pseudo-header**：`:method`, `:authority`, `:scheme`, `:path` 的相对顺序（Chrome / Firefox / Safari 各不同）
4. **PRIORITY 树**：dependency tree、weight

## 2. 模拟工具

- curl_cffi（自动模拟 chrome）
- azuretls（手动配置 frame）
- hyper（Go HTTP/2 库，需要手改）

## 3. 与 TLS 指纹的协同

通常厂商会同时采集 JA3 + JA4H + H2 frame；三者必须自洽（Chrome JA3 + Firefox H2 frame 立刻被检测为伪造）。

## 4. 已知研究

- [NEEDS_VERIFICATION] Akamai 公开博文 "H2 Fingerprinting"
- [NEEDS_VERIFICATION] github.com/lwthiker/curl-impersonate
- [NEEDS_VERIFICATION] github.com/yifeikong/curl_cffi

## 来源

- [NEEDS_VERIFICATION] Akamai blog
