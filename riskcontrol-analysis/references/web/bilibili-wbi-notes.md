# bilibili wbi 签名 (Web/iOS) - notes

## 摘要

B 站从 2023 年 3 月起在 Web 端启用 WBI 签名鉴权（独立于 APP/Cookie 鉴权），表现在 REST API 请求 query 中追加 `w_rid` 和 `wts` 字段。

| 参数 | 含义 |
|---|---|
| `w_rid` | 32 字符 hex（query 排序+key+MD5） |
| `wts` | UNIX 时间戳（秒） |
| `buvid3` / `buvid_fp` | 设备指纹 cookie |
| `bili_ticket` | 长期 session token |

## 识别签名

- Query 同时出现 `w_rid`+`wts`，长度 32 hex+10 数字。
- 接口含 `/x/web-interface/`、`/x/v2/`、`/x/space/`、`/x/v3/api/`。
- 错误码 `-352` 是典型 wbi 校验失败。

## 算法（已公开稳定）

```
1. 拉 /x/web-interface/nav 取 wbi_img.img_url, sub_url。
2. imgKey = basename(img_url, '.png')；subKey = basename(sub_url, '.png')。
3. 把 imgKey+subKey 拼接，按固定 mixinKeyTab 重排成 mixin_key（取前 32 字符）。
4. 把请求参数（含 wts=now）按 key 排序、URL-encode、拼接，最后追加 mixin_key。
5. w_rid = md5(那一串)。
```

mixinKeyTab 是公开常量；mixin_key 每天会随 imgKey/subKey 变化，但算法本身稳定。

## raw-hits 来源

- 见 [raw-hits/android-batch1.md Q7](../raw-hits/android-batch1.md)。

## 关键 URL

入门：
- [WBI 签名 (BAC Document)](https://sessionhu.github.io/bilibili-API-collect/docs/misc/sign/wbi.html)
- [B 站 WBI 签名逆向实战 + Python (CSDN 2026-03)](https://blog.csdn.net/weixin_29323365/article/details/158674255)

进阶：
- [浅度剖析 B 站新 -352 风控策略 (Salty Fish)](https://im.salty.fish/index.php/archives/revengr-bilibili-352.html)
- [bilibili-API-collect (GitHub - 协议汇总)](https://github.com/SocialSisterYi/bilibili-API-collect)

## 工作流建议

1. 入门级，建议作为 Skill 的"练手案例"。
2. 拉一次 nav 接口取 imgKey/subKey 后缓存（每天换一次）。
3. mixin_key 计算可参考社区库 [bilibili-API-collect/wbi.md](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md)。
4. 注意：`buvid3` cookie 是设备指纹，部分接口也校验它，纯 wbi 通过不一定能取数据。
