# 花钱前 checklist — 绝对铁律

> **2026-05-11 血泪教训**：用户基于我（AI 助手）的"capsolver 30 分钟
> 接入 + $1-2/1000 次"乐观估算购买了 CapSolver $6 余额。实测后发现
> **CapSolver 完全不支持阿里盾滑块**。用户日生活费 ¥30，这 $6 ≈ 一
> 周生活费白扔。
>
> **教训：任何"花钱"建议必须先做免费 dry-run 验证服务真的能干这事**。

## 通用规则

**在让用户为任何服务付费前，必须先免费 dry-run 验证以下 3 件事**：

1. ✅ **服务真的支持目标 captcha / 模型 / API 类型**
   - 不是听用户社区说支持
   - 不是看 marketing 页面说支持
   - 不是看官方博客标题说支持
   - **必须**用免费试探接口（如错误请求、`getBalance`、空 task）实际跑一次，看返回真实支持类型

2. ✅ **服务在你的目标 URL / scene-id / app-id 上工作**
   - 同一类 captcha 不同部署的 scene 配置不一样
   - 服务可能"支持 reCAPTCHA"但**不支持你站点的 site-key**（IP 信誉 / 区域 / 难度等级）

3. ✅ **服务的免费试用 / 试错门槛**
   - 错误请求是否扣费？（CapSolver 错请求不扣，2captcha 不扣）
   - 是否有 trial credit？（CapSolver 新账号有 trial，部分服务没有）

**只有 3 条都 ✅ 才让用户掏钱**。否则用户的钱就是白扔。

## CapSolver 实测能力清单（2026-05-11）

支持（通过 createTask 实测）：
- reCAPTCHA v2 / v3
- Cloudflare Turnstile
- Cloudflare Challenge
- AWS WAF
- DataDome
- GeeTest
- MTCaptcha
- ImageToText (OCR)

**不支持**（多种命名都返回 `ERROR_TYPE_NOT_SUPPORTED`）：
- Aliyun Sliding / Aliyun Captcha — **任何阿里盾系列**
- Tencent 防水墙
- 网易盾 NECaptcha
- 数美 (ishumei)
- 顶象 (Dingxiang)
- Vaptcha

> 这份清单是用户已经付费 $6 验证出来的，**别再让 $6 白花一遍**。

## 各打码服务对国产 captcha 的支持矩阵（社区报告，**未实测**）

| 服务 | 阿里盾 | 腾讯防水墙 | 网易盾 | 数美 | 顶象 | reCAPTCHA | Turnstile |
|---|---|---|---|---|---|---|---|
| CapSolver | ❌ 实测确认 | ? | ? | ? | ? | ✅ 实测 | ✅ 实测 |
| 2captcha | ⚠️ 据说支持 sliding | ? | ? | ? | ? | ✅ | ✅ |
| YesCaptcha | ⚠️ 据说支持 | ? | ? | ? | ? | ✅ | ✅ |
| **nocaptcha.io**（国产）| ⚠️ 据说阿里盾最强 | ⚠️ 据说支持 | ⚠️ 据说支持 | ⚠️ 据说支持 | ? | ✅ | ✅ |
| 联众打码 | ? | ? | ? | ? | ? | ⚠️ 弱 | ⚠️ 弱 |
| 超级鹰 | ? | ? | ? | ? | ? | ⚠️ 弱 | ⚠️ 弱 |

> "⚠️ 据说" 全部是社区博客或论坛传言，**未在任何 scene 上实测**。引用这表格做决策前**必须**先在选定服务的免费 `getBalance` + 空 task 上验证。

## 推荐的免费验证脚本模板

```python
import requests, json

def verify_captcha_service(service_name, api_key, base_url, balance_endpoint, task_endpoint, task_type, websiteURL):
    """
    返回 (ok: bool, msg: str)。
    ok=True 表示该服务对该 task_type 有响应（接受了任务进入队列）；
    ok=False 表示明确不支持。
    **此函数零成本** — 错误请求和 balance 查询都不扣费。
    """
    # Step 1: balance
    r = requests.post(f"{base_url}{balance_endpoint}", json={"clientKey": api_key}, timeout=15)
    bal = r.json().get("balance")
    if bal is None:
        return False, f"balance API broken: {r.text[:200]}"
    if bal == 0:
        return False, "余额 0，先确认 key 有效。新账号通常有 trial credit"

    # Step 2: probe target task type with intentionally invalid data
    r = requests.post(f"{base_url}{task_endpoint}", json={
        "clientKey": api_key,
        "task": {"type": task_type, "websiteURL": websiteURL}
    }, timeout=15)
    d = r.json()
    code = d.get("errorCode") or d.get("errorId")
    if code in ("ERROR_TYPE_NOT_SUPPORTED", 1) and "unsupported captcha type" in (d.get("errorDescription","").lower()):
        return False, f"服务 {service_name} 不支持 type={task_type}"
    # 任务被接受（进入队列）或参数错误（说明 type 支持但 payload 不完整）— 都算"服务理论可用"
    return True, f"服务接受了 {task_type}：{d}"


# Usage example
ok, msg = verify_captcha_service(
    "CapSolver", "CAP-...", "https://api.capsolver.com",
    "/getBalance", "/createTask", "AliyunSlidingTask",
    "https://notegpt.io/user/register"
)
print(f"{'✅' if ok else '❌'} {msg}")
```

跑这个脚本**零成本**就能筛掉不支持的服务，再让用户付费的服务才有意义。

## 反例（**不要这样做**）

❌ 我（助手）2026-05-11 8:25 前的做法：
- 看到 NoteGPT 用阿里盾
- 直接说"付费打码 ~$1-2/1000 次 30 分钟接入"
- 用户充了 $6 到 CapSolver
- 实测 CapSolver 不支持阿里盾
- **$6 ≈ 一周生活费白扔**

✅ 正确做法：
- 看到 NoteGPT 用阿里盾
- **先**用 `verify_captcha_service()` 跑 CapSolver / 2captcha / YesCaptcha 三家
- 报告哪家**实测确认**支持
- 用户**只**给实测支持的服务付费

## 这个文档的约束

任何后续修改这个仓库的 AI 助手在向用户建议"付费打码 / 付费 API / 充值
RPC / 买 captcha solver" 之前，**必须**：

1. 检查 `references/site-discovery/aliyun-captcha.md` 的实测能力清单
2. 用上面 `verify_captcha_service()` 脚本对建议的服务做免费 dry-run
3. 在向用户提付费建议时，附上"已实测确认支持 X type"的证据（API 响应截图 / JSON）

不做这 3 步就建议付费 = **背叛用户信任**。
