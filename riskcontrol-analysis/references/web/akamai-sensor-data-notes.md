# Akamai Bot Manager (sensor_data / _abck) - notes

## 摘要

Akamai 是国际反爬巨头之一，国内航空、跨境电商、奢侈品站点广泛部署。

| 参数 | 含义 |
|---|---|
| `_abck` cookie | 校验状态机 (~0~ 初始 / ~-1~ 失败 / ~1~ 成功) |
| `bm_sz` | 短期会话 cookie |
| `bm_sv` | 服务器签名 cookie |
| `ak_bmsc` | 行为追踪 cookie |
| `_akamai_audience` | 受众分析 |
| `sensor_data` | POST /xx 接口的 jsvmp payload |
| `sec-cpt` | JS challenge 头 |
| `pixel challenge` | 备用 challenge |

**版本演进**：
- v1：明文 base64 拼接。
- v2：base64 + RC4-like。
- v3（当前主流）：jsvmp 字节码 dispatcher，每隔 1-2 天换 JS 文件，但算法骨架稳定。

## 识别签名

- Cookie 含 `_abck=...~0~...` 或 `~-1~`/`~1~`。
- HTML 内嵌 `<script src="*-bm-challenge.js">` 或 `<script src="*-bm-verify.js">`。
- POST `/akam/xxx` / `/somepath` 携带 `sensor_data` 字段。
- jsvmp 内出现 `cKH` 类（这是 sensor_data 第三代的标志类）。

## 还原方法

1. **抓 challenge JS**：第一次访问→202 拦截→`<script src=...>`→拉下来。
2. **解混淆**：
   - 同一 v3 版本的 cKH 类内大部分常量周变动（不是请求级变动）→纯算可行。
   - 用 `webcrack`/`AST hook` 还原变量名。
3. **拼接 sensor_data**：
   - 8 段：`{ts}+{events_md}+{events_kk}+{events_mm}+{events_pp}+{telemetry_n1}+{nav}+{checksum}`。
   - 各段含鼠标轨迹/键盘事件/timing/Canvas/WebGL/UA/插件 → 必须给逼真值。
4. **POST sensor_data → 服务器更新 `_abck`** → 状态变 `~1~`。
5. **轮询机制**：每 4-5 个请求要刷新 sensor_data，否则 cookie 失效。

## raw-hits 来源

- 见 [raw-hits/web-batch1.md Q1](../raw-hits/web-batch1.md)。

## 关键 URL

入门：
- [Akamai 3.0 反爬分析与 sensor-data (CSDN 2025-01)](https://blog.csdn.net/weixin_43845191/article/details/144977354)
- [Akamai 2.0 sensor_data 参数 (博客园)](https://www.cnblogs.com/xiaoweigege/p/17455532.html)
- [被 Akamai 反爬虐到哭 (知乎)](https://zhuanlan.zhihu.com/p/1953445818599180205)

进阶：
- [[原创] Akamai 逆向分析 part1 (看雪 2025-07)](https://bbs.kanxue.com/thread-287819.htm) — cKH 类周变动 + 纯算可行
- [Akamai 某环境 VMP 算法分析 (吾爱破解 2025-02)](https://www.52pojie.cn/thread-2009699-1-1.html)
- [js 逆向 akamai_3.0 主流程 (B 站 2026-04)](https://www.bilibili.com/video/BV1bAifYkE7i/)

公开仓库：
- [xiaoweigege/akamai2.0-sensor_data (GitHub)](https://github.com/xiaoweigege/akamai2.0-sensor_data)

## 工作流建议

1. 决定 v 版本：看 challenge JS 文件名/字节序，能查到的话直接套现成纯算。
2. 重点是鼠标轨迹/键盘事件的"真实性"——风控会校验事件 timing 间隔分布、轨迹曲率、加速度。
3. `_abck` 状态机异常时（~0~/-1~ 持续）说明 sensor_data 不被认；先排查 TLS 指纹（Akamai 也校验 JA3）。
4. 长期可用方案：纯算+真人录制轨迹模板+IP 池+UA 池。

## 关键术语

- **cKH 类**：v3 jsvmp 内的关键类，sensor_data 主要由它的 `bx-pp` 等方法生成。
- **bm_sz vs _abck**：bm_sz 短期+无状态，_abck 长期+有状态机。
