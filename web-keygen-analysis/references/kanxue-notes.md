# 看雪精读笔记（kanxue-notes）

> 从 `kanxue-search-log.md` 列出的高价值候选中抽取的技术要点。
> 每篇按"目标 / 关键发现 / 工作流 / 可复用结论"四段式记录。
> URL 模式：`https://bbs.kanxue.com/thread-<id>.htm`

---

## 287819 — Akamai 逆向分析 part1（台山仔）

**目标**：Akamai bmp-2 的 `_abck` cookie 验证流程还原；通过分析 `sensor_data` 来源完成"补 cookie"。

**关键发现**：

1. **触发与验证流程**：拿到 doc 响应后，目标 JS 链接会发起至少 2 次 POST `sensor_data`；只有 `_abck` 末尾出现 `||0||` 才算通过。
2. **核心对象 `cKH`**：`sensor_data` 由 `cKH` 序列化得到，`cKH` 包含几十个键，是 Akamai 的"参数地狱"。
3. **常量提取技巧**：`CP()["E"].apply(null, [569,86,259,81])` 这类调用，结果是每个 JS 版本固定的字符串。先把它们全跑一次缓存下来；同理 `XX(5)`、`FK()["qH"](1780,58)`。 hook 函数 `setFuncKeyMap`，把所有此类 key→fn 的映射写进字典。
4. **算法可行性判断**：连续多次抓 `cKH`，对比结构和值是否稳定；只要"对象结构 + 处理逻辑"基本不变，就走纯算法还原；否则补环境。
5. **键的值有"周更"特征**：同一版本算法中部分键值每周变一次（不是每次请求变），所以纯算法甚至能找到"变动规律"自动迭代。
6. **sensor_data 落到的关键子对象**：
   - `ver`：当前 JS 算法版本标记，由 `OCH`（一堆 `CP()["E"]` 拼出来）确定
   - `ajr`：由 `AJH = L3H(p7H)`，`p7H = Yc(31, [...一堆固定数据])`；最终内含 `totVel/jS()/Ib`，本质是 `[随机数, base64编码]` 拼出来的字符串如 `MTQ5OTI3NDk4MA==|18970|79034`
   - `din`：由对象 `O4H` 的 values 数组拼接而成，包含 `hz1/dau/nap/wih/swi/wiw/ash/asw/wow/ua/she/...`，对应排版引擎、ua、屏幕尺寸等
   - `mst`：由对象 `MIH` 的多键拼成（含 `kevl/mevl/tevl/dd2/sts/dvc/...`）；`dd2 = A2H` 由 `nj(53,[])` 取固定值
   - `sde = "0,0,0,0,1,0,0"` 由 `EfH` 生成，可写死
   - `eem = "do_en,dm_en,t_en"` 形式固定
   - `ffs / inf` 为鼠标轨迹模拟字符串：每段 `0,0,0,0,4819,113,0;`
   - `dvc` 涉及 vmp，留 part2

**工作流提炼**：

```
1) 替换 JS 拦截 → 多次抓 cKH 比对结构稳定性
2) hook 所有 setFuncKeyMap 把固定 key→fn 缓存为字典
3) 把 CP()["E"].apply / XX(n) / FK()["qH"] 这种"伪动态实际固定"的调用全脱敏
4) 按 cKH 中每个键反向追踪函数（搜索变量名 → 找赋值处 → 看 switch case）
5) 区分"每 JS 固定值/每周变值/每次变值/真随机"四类
6) 最后剩下 vmp 形态的 dvc 单独走 jsvmp 还原
7) 算法还原 + 真实 cKH 字段对比定位差异
```

**可复用结论**：
- Akamai 这类商业风控的"参数 50+ 海洋"必须先用 hook 把"伪动态固定值"打成字典再人脑分析。
- 几乎所有键最终都对应 `dau/nap/wih/swi/screen.*/ua/storage` 等浏览器原生属性 — 即"用 JS 序列化 navigator + screen + 鼠标轨迹 + 时间差"。
## 281237 — WEB 逆向 X-Bogus 纯算+补环境（mb_inldragb）

**目标**：抖音 web 端 `X-Bogus` 与 `msToken` 还原；选"纯算法 / 补环境"两条路径并完整跑通纯算路径。

**关键发现**：

1. **`msToken`**：来自 cookie，Token 化设计，可写死或随机生成（107 字节，字符集 `A-Za-z0-9=`）。
   ```python
   def get_ms_token(randomlength=107):
       base = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
       return ''.join(random.choice(base) for _ in range(randomlength))
   ```
2. **`X-Bogus = 28 字节定长**`。从断点处 `_0x2458f0['apply'](_0xc26b5e, _0x1f1790) == 28` 切入。最终入口是 jsvmp 字节码 + 派发 W 函数。
3. **补环境路径**（最简）：扣全部 jsvmp 代码 + 在入口位置赋值 `arguments`，按"缺啥补啥"补 `window/document/navigator.userAgent`，~6 行就够。
4. **纯算路径核心规律**：
   - `X-Bogus` 是按"4 字符为一组"输出（共 7 组 = 28 字符）。
   - 每 3 字节明文 → 4 字符密文。
   - 字符表：`Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=`（注意有 `-` 替换 `+`）。
   - 一组的拼装公式（典型 base64 风变体）：

   ```js
   const tab = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=";
   let xb = "";
   for (let i = 0; i <= 20; i += 3) {
       const c1 = enc.charCodeAt(i), c2 = enc.charCodeAt(i+1), c3 = enc.charCodeAt(i+2);
       const v = c3 | (c2 << 8) | (c1 << 16);
       xb += tab[(v & 0xFC0000) >> 18] + tab[(v & 0x3F000) >> 12] +
             tab[(v & 0xFC0) >> 6]    + tab[v & 0x3F];
   }
   ```
5. **明文 enc 的 19 字节构造**：
   - 前 4 字节：固定值
   - 第 5~10 字节：`md5_hex(msToken)` 派生 → 切片
   - 第 11~18 字节：时间戳 + canvas 固定值拼接
   - 第 19 字节：前 18 字节签名
   - 最后用 `String.fromCharCode.apply(null, Uint8Array(19))` 输出
6. **RC4 风格初始化函数**（论坛贴出原码）：标准 RC4 KSA + PRGA，注入字符串然后异或。

**工作流提炼**：

```
1) 抓包定位接口；记下要逆向的 X-Bogus 长度（28）
2) Initiator 跳进 jsvmp，条件断点 .apply(...).length == 28
3) 看派发函数 W：长 switch + 流程控制；判断条件由 arguments 末位驱动
4) 给关键 case 打日志断点（不要乱删 debugger，会卡死）
5) 反向追"X-Bogus 赋值处"：发现是字符 4 个 4 个一组生成 → 找拼装函数
6) 推出 (combined & mask) >> shift + charAt(table) 的 base64 变体
7) 反向追 19 字节 enc 的来源：固定 / md5 / 时间戳 / canvas / 签名
8) 把 RC4 + Uint8Array(19) 编码扣下来重写
```

**可复用结论**：
- 头部短字符串（28 字节、48 字节、64 字节）通常是 **base64 变体**——先看字符表是否是 64 字符替换表，发现就直接套 `(v >> shift) & 63` 公式。
- jsvmp 类的"长 switch + 字节码 + 总入口 W"，先用条件断点 + 日志断点抽出每个 case 输入输出，再做 AST 还原。
- "msToken cookie 写死也能用"是国内多个站点共性 — Token 是会话标记而非签名。
## 272487 — 利用 AST 技术还原 JS 混淆代码（rushmaster）

**目标**：用 Babel + AST 系统还原 JS 混淆，作为 web 逆向的基础工具方法。

**关键发现 / 工具栈**：

- 在线 AST 浏览器：`https://astexplorer.net/`
- 编译三阶段：词法分析（拆 token）→ 语法分析（拼成 AST）→ 代码生成（重新写回）
- Babel 5 件套：
  - `@babel/parser`：JS → AST（`parse` / `parseExpression`）
  - `@babel/generator`：AST → JS（`generate(ast, opts, code)`）
  - `@babel/traverse`：遍历 + visitor 模式修改节点
  - `@babel/types`：构建新节点
  - `@babel/core`：以上三模块的总入口
- 常用 visitor 写法：

  ```js
  const visitor = {
      NumericLiteral(path) { path.node.value = (path.node.value + 100) * 2; },
      StringLiteral(path)  { path.node.value = "I Love JavaScript!"; }
  };
  traverse(ast, visitor);
  ```

- 多类型联合：`"NumericLiteral|StringLiteral"(path)`
- `path.toString() / path.node / path.parent / path.parentPath / path.type`
- enter / exit：默认 enter；要在退出时改用 `{ enter, exit }` 写法
- `types.identifier(name)`、`types.variableDeclarator(id, init)`、`types.variableDeclaration(kind, declarations)`、`path.insertAfter(node)`、`path.replaceWith(node)`、`path.remove()`
- `parser.parse(code, { sourceType: 'module', errorRecovery: true, allowImportExportEverywhere: true })`
- `generate(ast, { compact, concise, minified, retainLines, comments })`

**常见混淆类别（文章列出）**：

1. **字符串还原**：把 `_0xABCD[idx]` 还原为字面量
2. **表达式还原**：常量折叠、运算预求值
3. **删除未使用变量**：`scope.bindings` + 引用计数
4. **删除冗余代码**：永真/永假分支裁剪
5. **switch-case 反控制流平坦化**：识别 dispatcher 变量、按 case 顺序拉平

**可复用结论**：
- AST 是 JS 逆向**所有方法论的基础**，做一切站点逆向之前都建议先建立"原始 JS → 解混淆 JS"的可重复管线（一份 `pass1.js`、`pass2.js`、`pass3.js`，按 9 个 Pass 循环跑通）。
- 字符串解密器、控制流平坦化、混淆变量重命名都可以做成可复用的 Pass 模块。

---

## 289940 — 小红书 x-s 4.3.1 mns0301（Tsuru，需登录回复看完整）

**目标**：跟踪小红书 web 端 `x-s` 在 4.3.1 版本的更新点。

**可见摘要**：

- 入口：`window.mnsv2` 对应的 vmp，在 for 循环的"第一个 else"打断点。
- **数组长度演变**：4.2.6 = **124 位**；4.2.9 = **135 位**；4.3.1 = **144 位** = `124 + 20`。
- 20 位数组结构：`4 位 + 16 位`；4 位数组 = `len('a3') + 'a3' + 后续数组长度 16`。
- 16 位数组 = 另一个 24 位数组经过 `_0xfca8c3()` 处理；
- 24 位数组 = `时间戳 + md5(api)`（这一构造从 4.2.9 沿用至今）；
- `_0xfca8c3` 内部又是一个独立 vmp，关键词出现 `IV` / `build_block`，本质是 MD5 形态被嵌进 vmp 字节码。
- 详细完整算法在登录回复后才能看（属于会员墙）。

**可复用结论**：
- 小红书 x-s 系列的"数组长度变化"是版本指纹，看到 124/135/144 直接判断版本。
- "时间戳 + md5(api) → 24B → vmp 内 build_block → 16B → 拼成 20B → 拼成 144B" 是核心管线。
- 内嵌 md5 形态指标：日志中出现 4 个无符号整数串、`IV`、`build_block` 字样。

---

## 289806 — 京东 h5st 多态 VM AI 还原（y2k）

**目标**：京东 `h5st` 协议从 0 还原；作者强调"多态 VM"必须 AI 辅助。

**关键发现**：

1. **多态 VM 与单 VM 的区别**：
   - 单 VM：`case 2 → 永远是 PUSH`，`case 5 → 永远是 POP`
   - 多态 VM（京东）：30+ 个独立 dispatcher，**同一个数字 opcode 在不同 VM 中含义完全不同**
     - `VM_A: case 2 → PUSH`
     - `VM_B: case 2 → STORE`
     - `VM_C: case 2 → CALL`

2. **AI 辅助流程**：`Gemini 识别混淆类型 → Claude Code 编写 AST 脚本 → 迭代优化`，作者把 450KB 混淆代码分 9 个 Pass 处理（与 thread-272487 思路一致）：
   - Pass 1 字符串解密函数还原
   - Pass 2 字符串数组还原（`_1w8l4[42] → "appid"`）
   - Pass 3 常量折叠
   - Pass 4 逗号表达式展开
   - Pass 5 变量语义重命名（`_2n8l4 → Bytecode`）
   - Pass 6 对象字典展开（`_$wR.add(x,y) → x + y`）
   - Pass 7-9 死代码 + 未使用变量清理

3. **AI 指挥 + 人工执行**协作模式：

   ```
   AI:「SHA256 结果不对，在 _append 入口设断点」
   人:「参数 'test'，但 this.buffer 变成 'testXXXXXX'」
   AI:「_append 内部有额外处理，分析」
   AI:「找到了，_append 调用了 _eData」
   人:「_eData 返回原字符串 + 固定后缀」
   AI:「这就是第二层魔改！」
   ```

4. **京东魔改 SHA256 完整链路**：

   ```
   jd_sha256(input)
     ↓ _seData1(input)        ← 追加 10 字符动态后缀（按字符码累加+映射自定义字符表）
     ↓ _eData(result)         ← 追加固定后缀（隐藏在 _append 中！标准实现里 _append 只是简单追加）
     ↓ 标准 SHA256
     ↓ swap(byte[0], byte[2]) ← 字节交换
     ↓ 输出 64 hex
   ```

5. **签名 VM 调用链**（作者梳理出 17 个核心 VM）：
   - 入口：`signSync() → l34 (签名入口) → l31 (h5st 组装)`
   - 子调用：`l24 (密钥) → l25` / `l28 (签名计算) → jd_sha256` / `l30 (签名数据)` / `wm_encode (自定义 Base64)` / `l27 (最终组装)`
   - 6 个签名核心 VM + 6 个加密算法 VM + 5 个辅助 VM（含 `l23` 环境检测）

6. **`l23` 环境检测项**（被编入 h5st 的第 8 个字段 envData）：
   - 运行时检测：`window/document/navigator` 真实性、性能时序
   - 浏览器指纹：UA / Canvas / WebGL / 屏幕尺寸 / 时区
   - 风控但**不影响签名验证**——可以直接固定 envData 复用

**可复用结论（从京东案例提炼为通法）**：

- **多态 VM 检测特征**：在反编译 / 解混淆代码里看到大量结构相似的 dispatcher（`while + switch`），且 opcode 表互不通用。检测方法：随机抽两个 dispatcher，比对 case 2 / case 5 等常用 opcode 的实现是否一致。
- **魔改 SHA256/MD5 必查 4 个点**：
  1. 输入预处理（`_seData1` 追加动态后缀）
  2. 内部 `_append` 是否被替换（追加固定后缀）
  3. IV 是否被改
  4. 输出后处理（字节交换 / 重排）
- **风控字段优先级**：env/trace/canvas 等"风控字段"有时**不参与签名计算**，可固定写死；先验证签名的最小集，把风控当成可选项。
## 288946 — 瑞数"异步"解决方案：浏览器脚本 + MITM 拦截（mb_taxuwpol）

**目标**：避开瑞数复杂 JS 还原，把瑞数当**黑盒**，让浏览器自己生成正确的请求参数和 Cookie，再用中间人代理截下来给爬虫复用。

**核心思路**：
- 瑞数会重写 `XMLHttpRequest.prototype.send` / `fetch`，在发包前动态加上参数和更新 Cookie。
- 让浏览器执行一个简单的"触发"脚本（`fetch(目标URL?params=trigger', {headers:{...}})`）。
- 用 mitmproxy / Burp / Fiddler 拦截这个被瑞数处理后的请求，提取出动态 URL 后缀和 Cookie。
- 把这些值塞给主程序（Python requests 等）。

**异步问题与解法**：
- 这是**异步**架构（不是 RPC 同步等）。需要共享存储：
  - 方案 A：MITM 插件 → 写入本地文件 / 数据库 → 主程序监控读取
  - 方案 B：MITM 插件 → 调本地 API 服务 POST → 主程序 GET 拿值

**可复用结论**：
- 任何重写了 `XMLHttpRequest.send` / `fetch` 的风控都可以套这个"黑盒+MITM"思路，无需还原算法。
- 缺点是吞吐受限、无法扩展（每个请求都要走真实浏览器），但**对低频高价值场景**（如登录/注册/获取关键 token）是性价比最高的方案。
- "异步派发"模型适合数据采集、低 QPS；高 QPS 场景仍需纯算还原。

---

## 285959 — Apple Account 注册之生成 sign（mb_ufezmkch）

**目标**：iOS Apple ID 注册链路中 `X-MMe-Nas-Qualify` 签名的生成方法。

**关键发现**：

1. **签名字段**：`X-MMe-Nas-Qualify`（重要接口都加签，是苹果通用方法）。
2. **生成位置**：`AuthKit` 的 `-[AKAppleIDServerResourceLoadDelegate signRequest:withCompletionHandler:]` 中的 block 调用 `t1Uu`。
3. **`t1Uu` 5 个参数**：`context (客户端证书) / bytes (待加密 body) / length / 两个接收结果的 out 参数`。
4. **逆向方法**：IDA 无法解析 → Xcode + lldb 一步步调试还原字节码（耗时半月级）→ Python 还原。
5. **Frida 定位 hook**：

   ```js
   defineHandler({
     onEnter(log, args, state) {
       var key = ObjC.Object(args[3]);
       var value = ObjC.Object(args[2]);
       if (key == 'X-MMe-Nas-Qualify') {
         log('\tBacktrace:\n\t' +
           Thread.backtrace(this.context, Backtracer.ACCURATE)
             .map(DebugSymbol.fromAddress).join('\n\t'));
       }
       log(`-[NSMutableURLRequest setValue:${value} forHTTPHeaderField:${key}]`);
     }
   });
   // frida-trace -U "Settings" -m "*[*Request *forHTTPHeaderField*]"
   ```

**可复用结论**：
- 设备绑定的"客户端证书 + 待签 body"组合是 iOS / macOS 系账号注册的常见签名格式。
- "frida-trace HTTP header 设值方法 + onEnter Backtrace" 是定位任何 iOS 风控签名生成位置的通用模板。
- 字节码逆向耗时极长（半月+），考虑直接做 device farm 复用真实证书的方案。

---

## 290429 — 防水墙滑块验证码 AI 全链路自动化（xautzbl_270908）

**目标**：用 AI 辅助逆向腾讯防水墙（云证 TCaptcha）滑块验证码，从抓包到补环境到自动通过的全链路。

**站点架构**：

| 文件 | 大小 | 作用 | 混淆 |
|---|---|---|---|
| `TCaptcha.js` | - | 入口加载器 | 低 |
| `tcaptcha-frame.js` | 207KB | 主框架 | 中（webpack） |
| `dy-ele.js` | 209KB | 滑块核心 | 中（webpack） |
| `tdc.js` | 78KB | 设备指纹 | **极高（JSVMP）** |

**关键发现**：

1. **核心接口（仅 2 步）**：
   - `GET /cap_union_prehandle` → 获取 sess + 图片 + PoW 挑战
   - `POST /cap_union_new_verify` → 提交答案获取 ticket
2. **prehandle 参数**：`aid / ua(base64) / lang / entry_url / subsid / callback (JSONP)`
3. **verify 参数**：`collect / tlg / eks / sess / ans / pow_answer / pow_calc_time`
4. **`__TENCENT_CHAOS_STACK` JSVMP 形态**：
   - 自定义字节码解释器 + 数万个数字内联
   - 所有 `collect` / `eks` 加密在 VM 内
   - 直接还原 VM 指令集成本极高 → **走"补环境"绕过**
5. **TDC 接口**（设备指纹采集模块）：
   ```js
   window.TDC = {
     setData(data),       // 设置采集（轨迹、指纹）
     getData(flag),       // 加密后 collect
     getInfo(),           // { info: "eks", tokenid: "..." }
     clearTc()            // 清除
   };
   ```
6. **PoW 算法**：暴力搜 `md5(nonce + counter) === target`，返回 `{ ans: counter, duration: ms }`
7. **`ft` 浏览器特征字符串 50+ 项**（`matches in div`、`msMatchesSelector`、`window.matchMedia`、`CSS.supports`、`createRange`、`CustomEvent`、`scrollIntoView`、`getUserMedia`、`IntersectionObserver`、`ontouchstart`、`window.performance` 等）。
8. **AI 辅助补环境的优势**：
   - AI 在 chrome 中模拟执行 + 收集环境（避免漏补）
   - 本地报错时对比浏览器环境差异（避免多补）
   - AI 能模拟滑块轨迹的采样点和算法

9. **整体流程 7 步**：
   ```
   Step 1 prehandle → 拿 sess/sprite_url/bg_url/fg_elem_list
   Step 2 下载 sprite + bg
   Step 3 OpenCV 模板匹配缺口位置
   Step 4 生成轨迹（加速 70% + 减速 30% + 微调抖动）
   Step 5 PoW 暴力搜 md5
   Step 6 TDC.setData({ft}) → getData → collect / eks
   Step 7 verify → ticket + randstr
   ```
10. **事件监听器模拟**（用于在 Node 里让 TDC 拿到鼠标轨迹）：
    ```js
    document._eventListeners = {};
    document.addEventListener = function(type, fn) {
        (document._eventListeners[type] = document._eventListeners[type] || []).push(fn);
    };
    function simulateMouseTrack(track) {
        for (const p of track) {
            const evt = { type: 'mousemove', clientX: p.x, clientY: p.y, timeStamp: p.t };
            (document._eventListeners['mousemove'] || []).forEach(fn => fn(evt));
        }
    }
    ```

**可复用结论**：
- **看到 JSVMP 别硬刚 VM 指令集**：补环境 + 调原 VM 是最经济路径。
- **滑块轨迹三段式**（加速 → 减速 → 微调）是国内绝大多数滑块通杀的轨迹模板。
- **请求参数清单**应当先抓接口、列字段，再倒推哪个 JS 文件生产哪个字段（207KB / 78KB 这种"大文件包揽全部加密"是常见结构）。
- AI 协作要点：requirements.md / design.md / tasks.md 三件套，让 AI 自己写工程文档比直接让它写代码更稳。

---

