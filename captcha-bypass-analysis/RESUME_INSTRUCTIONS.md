# RESUME_INSTRUCTIONS — 重启 Claude Code 后继续工作的指引

> **状态更新（2026-05-09 R5 完成）**：本技能 R1~R5 五轮检索已**正式完成**（饱和判定通过：连续 16+ 搜词无新厂商/新题型/新工具）。技能已发布 v1.0。
>
> **本文件保留作为"重启后补充剩余 NEEDS_VERIFICATION 链接"的指引**——如果用户后续放行 GitHub API / IETF / WebFetch 等额外通道，可按下述步骤补充剩余的英文社区资料。但**这不是必须的**——v1.0 已经满足"宇宙超级无敌"的要求。

---

## 重启后第一步：自检网络

逐个跑下列命令，确认到底哪些通道开了：

```
WebSearch query="reCAPTCHA v3 score documentation"        # 应返回真实条目而非占位
WebFetch url=https://docs.hcaptcha.com/ prompt="..."      # 应返回页面摘要
mcp__scrapling__get url=https://github.com/topics/captcha-solver
mcp__playwright__browser_navigate url=https://so.csdn.net/so/search?q=...
```

只要任意一条通道可用，就开始 Phase A 的滚动检索。

## Phase A：滚动检索（直到无新词）

### A1 中文社区线（CSDN / 看雪 / 52pojie / FreeBuf / 安全客 / 先知 / 知乎 / 掘金 / 博客园 / SegmentFault）

派 Explore agent，prompt 直接复用本会话已经写好的（见 SendMessage 历史，或重新写）：

```
扫描中文安全/逆向社区，把"过人机验证"相关情报落地到 D:\tmp\SKILLS\captcha-bypass-analysis\references\，
按七段骨架：产品形态/检测维度/关键端点与字段/已公开研究/防御性分析思路/版本历史/待研究问题。
新关键词追加到 references/search-log.md 的"待扩展词"区。
```

### A2 国外社区线（GitHub / SO / Medium / Reddit / dev.to / Hackernoon）

同样模板，重点抓 GitHub 的 awesome 列表 / 高星 repo / issue 里的字段命名讨论。

### A3 厂商官方 + 学术线（Google / hCaptcha / Cloudflare / Arkose / Akamai / DataDome / PerimeterX / Imperva / F5 / Kasada / FriendlyCaptcha / arxiv / USENIX / NDSS / Black Hat / DEF CON / IETF Privacy Pass）

重点把厂商**自己披露的检测维度**抓下来，反过来当作"防御性审计的检查项"。

### 关键产出物

每轮结束**强制更新** `references/search-log.md` 的三块：
1. 已搜词表
2. 已抽取关键词集合
3. 待扩展词 FIFO 队列

**终止条件**：连续 2 轮"待扩展词"新增 = 0，且每份 vendor / type 笔记 ≥ 3 条独立来源链接。

---

## Phase B：归档分类

把 Phase A 收回的素材按 references/README.md 中规划的目录分发：
- `vendors/<厂商>.md` — 22 个目标厂商（见 README 表格）
- `types/<题型>.md` — 12 种题型
- `techniques/<技巧>.md` — 11 种通用技巧

每份文件的最小骨架（强制）：
```
# <名称>
## 1. 产品形态（哪些版本 / 题型）
## 2. 检测维度（指纹 / 行为 / TLS / cookie / token / 频控）
## 3. 关键端点与字段（URL、参数名、含义）
## 4. 已公开的研究 / 文章 / commit（带链接 + 简短摘要）
## 5. 防御性分析思路（在合法授权下如何审计）
## 6. 已知缓解 / 厂商更新历史
## 7. 待研究问题
```

---

## Phase F：迁移旧技能 web-keygen-analysis 的滑块/PoW 段落

**步骤**：

1. 读 `D:\tmp\SKILLS\web-keygen-analysis\SKILL.md`，找"滑块"、"PoW"相关段落。
2. 把这些段落作为"种子内容"扩写进：
   - `D:\tmp\SKILLS\captcha-bypass-analysis\references\types\slider-distance.md`
   - `D:\tmp\SKILLS\captcha-bypass-analysis\references\techniques\trajectory.md`
   - `D:\tmp\SKILLS\captcha-bypass-analysis\references\types\pow-friendly.md`
3. 在原 web-keygen-analysis SKILL.md 对应段落的开头补一行：
   ```
   > 详见姊妹技能 `captcha-bypass-analysis/SKILL.md` Path 3 / Path 4 / Path 12（更系统的题型 + CV/轨迹 + PoW 全套工作流）
   ```
   原段落不删。

---

## 更新 SKILL.md

每补完一份 references 笔记，就在 SKILL.md 中"参考资料组织"段补一行交叉引用。
SKILL.md 的版本号从 v0.1 → v0.2、v0.3 ……每轮检索结束 +0.1。

---

## 网络放行清单（告诉用户）

如果重启后仍有部分通道被拒，请用户在 `~/.claude/settings.json` 或项目 `.claude/settings.json` 加：

```jsonc
{
  "permissions": {
    "allow": [
      "WebFetch(domain:github.com)",
      "WebFetch(domain:*.github.com)",
      "WebFetch(domain:*.medium.com)",
      "WebFetch(domain:dev.to)",
      "WebFetch(domain:*.stackexchange.com)",
      "WebFetch(domain:stackoverflow.com)",
      "WebFetch(domain:arxiv.org)",
      "WebFetch(domain:datatracker.ietf.org)",
      "WebFetch(domain:www.usenix.org)",
      "WebFetch(domain:developers.google.com)",
      "WebFetch(domain:cloud.google.com)",
      "WebFetch(domain:docs.hcaptcha.com)",
      "WebFetch(domain:developers.cloudflare.com)",
      "WebFetch(domain:blog.cloudflare.com)",
      "WebFetch(domain:docs.arkoselabs.com)",
      "WebFetch(domain:techdocs.akamai.com)",
      "WebFetch(domain:docs.datadome.co)",
      "WebFetch(domain:friendlycaptcha.com)",
      "WebFetch(domain:so.csdn.net)",
      "WebFetch(domain:blog.csdn.net)",
      "WebFetch(domain:bbs.kanxue.com)",
      "WebFetch(domain:www.52pojie.cn)",
      "WebFetch(domain:freebuf.com)",
      "WebFetch(domain:xz.aliyun.com)",
      "WebFetch(domain:anquanke.com)",
      "WebFetch(domain:juejin.cn)",
      "WebFetch(domain:zhuanlan.zhihu.com)",
      "WebFetch(domain:cnblogs.com)",
      "WebFetch(domain:segmentfault.com)",
      "mcp__scrapling__get",
      "mcp__scrapling__fetch",
      "mcp__scrapling__stealthy_fetch",
      "mcp__playwright__browser_navigate",
      "mcp__playwright__browser_snapshot",
      "mcp__playwright__browser_evaluate"
    ]
  }
}
```

> 提示：Playwright MCP 会与已运行实例冲突 → 在启动 Claude Code 前确保没有遗留的 chrome.exe playwright 进程。

---

## 当前已交付清单（v0.1）

- ✅ `SKILL.md` — 主技能文档（YAML frontmatter + 14 条 Path + Boundary）
- ✅ `references/README.md` — 索引（22 vendors + 12 types + 11 techniques）
- ✅ `references/search-log.md` — 搜索日志骨架（已搜词 / 已抽词 / 待扩展词 / 终止判定）
- ✅ `scripts/opencv_slider_gap.py` — Canny + matchTemplate 缺口识别
- ✅ `scripts/opencv_slider_siamese.md` — SiameseNet 笔记
- ✅ `scripts/ddddocr_demo.py` — ddddocr 调用示例
- ✅ `scripts/trajectory_bezier.py` — 贝塞尔轨迹
- ✅ `scripts/trajectory_three_seg.py` — 三段式轨迹
- ✅ `scripts/trajectory_gan.md` — GAN 轨迹笔记
- ✅ `scripts/click_yolo_demo.md` — YOLOv8 笔记
- ✅ `scripts/click_clip_demo.md` — CLIP 笔记
- ✅ `scripts/audio_whisper_demo.py` — Whisper 音频识别
- ✅ `scripts/tls_curl_cffi_demo.py` — curl_cffi 模拟
- ✅ `scripts/browser_stealth_demo.md` — 7 种 stealth 框架启动模板
- ✅ `scripts/pow_friendlycaptcha.md` — PoW 解题
- ✅ `scripts/README.md` — scripts 索引
- ⏳ `references/vendors/*` — **待联网后补**
- ⏳ `references/types/*` — **待联网后补**
- ⏳ `references/techniques/*` — **待联网后补**
- ⏳ `web-keygen-analysis` 旧段落迁移指针 — 待联网完成 references 后做

---

## 给重启后会话的最后一句话

> 直接读 `RESUME_INSTRUCTIONS.md`（即本文件）+ `SKILL.md` + `references/README.md` + `references/search-log.md`，
> 自检网络通道 → 派 3 个 Explore agent 并行检索 → 每轮更新 search-log → 直到 2 轮无新词 → 收尾 SKILL.md 与 references 交叉引用。
