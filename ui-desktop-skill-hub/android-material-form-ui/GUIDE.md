# Material Design 3 文本输入框：常见问题与最佳实践

> **来源**：Material Design 3 官方文档 + Google AI 概览 + 实战踩坑（2026-05-11）
> 配合 `SKILL.md` 使用。本文档覆盖 floating label vs adjacent label、helper/placeholder/error 三态切换、密码字段、API 配置表单等场景。

## 1. Label 模式选型

Material 3 文档明确支持两种 label 模式：

### 1.1 Floating label（浮动 label，默认）
```xml
<com.google.android.material.textfield.TextInputLayout
    android:hint="API Base URL"
    app:boxBackgroundMode="outline">
    <com.google.android.material.textfield.TextInputEditText ... />
</com.google.android.material.textfield.TextInputLayout>
```
- **空时** label 在框中央
- **聚焦/有值时** label 上浮到框顶部
- 适合 **简短 label**（1-2 个中文词或 1-2 个英文单词）

### 1.2 Adjacent label（独立外置 label）
```xml
<TextView
    android:text="API Base URL"
    android:textStyle="bold"
    android:textSize="14sp" />
<com.google.android.material.textfield.TextInputLayout
    app:placeholderText="https://example.com/v1"
    app:helperText="示例: https://example.com/v1">
    <com.google.android.material.textfield.TextInputEditText ... />
</com.google.android.material.textfield.TextInputLayout>
```
- 独立 TextView 作为 label
- 适合 **长 label / 中文表单**（floating label 浮起后会被截断）
- M3 官方文档：「A text field doesn't require a label if the field's purpose is indicated by a separate, adjacent label」

### 1.3 选择标准（按场景）

| 场景 | 推荐 |
|---|---|
| 登录表单（用户名/密码）| Floating（短 label）|
| 搜索框 | Floating |
| **配置表单（含技术术语）** | **Adjacent**（长 label + 详细 helper） |
| 移动端 1080×2400 配置页 | Adjacent（floating 浮起时易遮内容）|
| 多语种自动切换 | Adjacent（floating 在长翻译下崩布局） |

## 2. 三态文本系统

每个 TextInput 字段最多有 **3 层文字**，**绝不能让它们重叠**：

| 层 | 属性 | 何时显示 | 内容规则 |
|---|---|---|---|
| Label | `android:hint`（在 TextInputLayout）或独立 TextView | 始终 | 字段名（如 "API Key"）|
| Placeholder | `app:placeholderText` | 聚焦且为空 | 短示例（如 `sk-...`）|
| Helper | `app:helperText` | 始终 | 说明 / 默认值 / 约束 |
| Error | 通过 `tilLayout.error = "..."` 在代码里设 | 触发校验失败时 | 错误描述 |

**关键**：error **会替换** helper（不会同时存在），所以 helper 高度即 error 高度，**布局不会跳**。

```xml
<com.google.android.material.textfield.TextInputLayout
    android:hint="API Key"                                  <!-- Label -->
    app:placeholderText="sk-..."                            <!-- Placeholder -->
    app:helperText="留空则使用默认值"                       <!-- Helper -->
    app:helperTextEnabled="true">
    <com.google.android.material.textfield.TextInputEditText
        ...
        android:inputType="textPassword" />                 <!-- 不要再设 hint -->
</com.google.android.material.textfield.TextInputLayout>
```

代码里设 error 示范：
```kotlin
binding.tilApiKey.error = if (apiKey.isBlank()) "必填" else null
```

## 3. 重叠 Bug 的 4 个常见根因

源自 Stack Overflow + Material GitHub Issues + 实战：

### 3.1 Layout 和 EditText 都设了 hint
```xml
<!-- ❌ 错误：两个 hint 都激活，互相覆盖 -->
<TextInputLayout android:hint="API Base URL">
    <TextInputEditText android:hint="https://..." />  <!-- 多余 -->
</TextInputLayout>
```
**修复**：只在 TextInputLayout 设 hint。EditText 留空。

### 3.2 代码里又 setHint
```kotlin
// ❌ 错误
binding.etApiBase.hint = "默认: ..."  // 这会让 EditText 的 hint 跟 TextInputLayout 的 hint 重叠
```
**修复**：用 helperText 替代：
```kotlin
binding.tilApiBase.helperText = "默认: ..."
```

### 3.3 XML 里 `android:text="默认值"` 不触发 label 浮起
**根因**：TextInputLayout 没监听到 inflate 阶段的 setText
**修复**：从 XML 移除 `android:text`，改代码里设：
```kotlin
binding.etApiBase.setText("默认值")  // 这会触发 hint 上浮
```

### 3.4 Material 库版本过老
- 1.2.0-alpha02 之前的 OutlinedBox 有 stroke + hint 重叠 bug
- **修复**：`implementation("com.google.android.material:material:1.11.0")` 以上

## 4. 密码 / API Key 字段

```xml
<com.google.android.material.textfield.TextInputLayout
    android:hint="API Key"
    app:endIconMode="password_toggle"          <!-- 👀 自动加眼睛图标 -->
    app:placeholderText="sk-..."
    app:helperText="留空则使用默认 Key">
    <com.google.android.material.textfield.TextInputEditText
        android:inputType="textPassword"       <!-- ⚠️ 必须配合 endIconMode -->
        android:imeOptions="actionNext"
        android:singleLine="true" />
</com.google.android.material.textfield.TextInputLayout>
```

注意：
- `endIconMode="password_toggle"` 必须配合 `inputType="textPassword"` 才显示眼睛图标
- 不要用 `inputType="textVisiblePassword"`（破坏 toggle 功能）

## 5. 表单整体布局规范

### 5.1 字段间距
- **同卡片内字段之间**：12-16dp（有 helper text 时取高值）
- **不同卡片之间**：12dp
- **最后一个字段和 primary button**：≥16dp

### 5.2 卡片化分组
中文配置表单建议每个语义组放进 MaterialCardView：
```xml
<com.google.android.material.card.MaterialCardView app:cardCornerRadius="12dp">
    <LinearLayout android:orientation="vertical" android:padding="16dp">
        <TextView android:text="第 X 步：..." android:textStyle="bold" />
        <!-- 输入字段 -->
        <Button android:layout_marginTop="16dp" android:text="保存" />
    </LinearLayout>
</com.google.android.material.card.MaterialCardView>
```

### 5.3 imeOptions 软键盘流转
- 中间字段：`android:imeOptions="actionNext"`
- 最后字段：`android:imeOptions="actionDone"`
- 配合 `android:singleLine="true"` 防止意外换行

## 6. 校验时机最佳实践

| 时机 | 建议 |
|---|---|
| 输入时 | **不要**实时报错（打字中干扰）|
| onFocusChange（失焦时）| 校验单字段格式（如 URL 是否合法）|
| 提交按钮点击时 | 全表单校验 + 失败字段聚焦 + Toast 提示 |
| 保存到 SharedPreferences 前 | trim + isBlank 检查必填 |

代码模板：
```kotlin
private fun saveConfig() {
    val base = binding.etApiBase.text?.toString()?.trim().orEmpty()
    val key = binding.etApiKey.text?.toString()?.trim().orEmpty()
    val model = binding.etModel.text?.toString()?.trim().orEmpty()

    // 字段级 error
    binding.tilApiBase.error = if (base.isBlank()) "必填" else null
    binding.tilApiKey.error = if (key.isBlank()) "必填" else null
    binding.tilModel.error = if (model.isBlank()) "必填" else null

    if (base.isBlank() || key.isBlank() || model.isBlank()) {
        Toast.makeText(this, "三项均为必填项", Toast.LENGTH_SHORT).show()
        return
    }
    // 保存...
}
```

## 7. 反模式（绝对不要做）

| ❌ 反模式 | ✅ 正确做法 |
|---|---|
| label / hint / helper / placeholder 用同一段长文本 | 三层各司其职 |
| label 长到换行 | 改 adjacent label 或缩短到 ≤6 个中文字 |
| supporting text 和 error 同时存在 | error 替换 supporting text |
| 在密码框旁手画 ImageView 当眼睛图标 | 用 `app:endIconMode="password_toggle"` |
| 字段紧贴底部按钮 | 至少 16dp 间距 |
| 用 EditText 而不是 TextInputEditText | 永远用后者，否则失去 TextInputLayout 集成 |

## 8. 调试技巧

### 8.1 用 uiautomator dump 检查渲染层级
```bash
adb shell uiautomator dump /sdcard/u.xml
adb pull /sdcard/u.xml .
# 看每个 TextInputLayout 的 bounds 是否有重叠
```

### 8.2 用 OCR 验证视觉效果
渲染后用 PaddleOCR/RapidOCR 识别截图。如果 OCR 把两层文字识别成一团乱码（如 "认Beepy.7hotoa bttom/example.c"），说明文字层在物理上重叠了。

### 8.3 启用 Layout Bounds 调试
开发者选项 → "显示布局边界"，可视化看每个 View 的物理区域。

## 9. 实战案例：QishuiHelper 4 步配置表单

```
第 4 步：配置 AI 接口（可选）            ← 卡片标题
┌──────────────────────────────────────┐
│  API Base URL                         │ ← Floating label (短)
│  ┌──────────────────────────────┐    │
│  │ https://example.com/v1        │    │ ← Placeholder
│  └──────────────────────────────┘    │
│  示例: https://example.com/v1         │ ← Helper text
│                                       │
│  API Key                              │
│  ┌──────────────────────────┬───┐    │
│  │ sk-...                   │ 👁│    │ ← endIconMode="password_toggle"
│  └──────────────────────────┴───┘    │
│  留空则使用内置默认 Key                │
│                                       │
│  模型名                                │
│  ┌──────────────────────────────┐    │
│  │ gpt-5.5                      │    │
│  └──────────────────────────────┘    │
│  默认: gpt-5.5（支持视觉）             │
│                                       │
│  [    保存配置    ]                   │ ← 16dp 上间距
└──────────────────────────────────────┘
```

## 10. 参考资料

- Material 3 Text Fields Guidelines: https://m3.material.io/components/text-fields/guidelines
- Android TextInputLayout API: https://developer.android.com/reference/com/google/android/material/textfield/TextInputLayout
- Stack Overflow #45453570: TextInputLayout hint overlap fixes
- GitHub material-components-android Issue #2060: focus state hint overlap
- M3 Specs: https://m3.material.io/components/text-fields/specs
