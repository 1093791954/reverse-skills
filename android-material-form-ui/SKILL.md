---
name: android-material-form-ui
description: Optimize native Android XML forms built with Material Components, especially TextInputLayout/TextInputEditText layouts with overlapping labels, hints, helper text, password fields, and cramped mobile spacing.
---

# Android Material Form UI

Use this skill when an Android app screen has native XML form fields that look crowded, where `TextInputLayout` floating labels, `TextInputEditText` hints, helper/default-value copy, or password fields overlap.

## Retrieval Notes

Verified on 2026-05-11 with:

- Google: `Material Design TextInputLayout supporting text label hint Android`
- Bing: `Material Design Android TextInputLayout helper text hint label`
- Primary source: Android Developers `TextInputLayout` API reference.

## Core Rules

- Put the field label on `TextInputLayout` via `android:hint`.
- Do not also put a competing long hint on the child `TextInputEditText`; overlapping label/hint text is a common cause of visual clutter.
- Use `app:placeholderText` for a short example value, such as `https://example.com/v1`.
- Use `app:helperText` for defaults, constraints, and explanatory copy. Helper text belongs under the field, not inside the input area.
- Prefer `app:boxBackgroundMode="outline"` when several fields are stacked; it makes field boundaries easier to scan.
- Use at least `12dp` to `16dp` vertical spacing between text fields when helper text is visible.
- For password or API-key fields, use `app:endIconMode="password_toggle"` when the value may need visual confirmation.
- Keep button spacing larger than field spacing, usually `16dp` or more above the primary action.

## XML Pattern

```xml
<com.google.android.material.textfield.TextInputLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginTop="14dp"
    android:hint="@string/label_api_base"
    app:boxBackgroundMode="outline"
    app:boxCornerRadiusBottomEnd="8dp"
    app:boxCornerRadiusBottomStart="8dp"
    app:boxCornerRadiusTopEnd="8dp"
    app:boxCornerRadiusTopStart="8dp"
    app:helperText="@string/helper_api_base"
    app:placeholderText="@string/hint_api_base">

    <com.google.android.material.textfield.TextInputEditText
        android:id="@+id/et_api_base"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:imeOptions="actionNext"
        android:inputType="textUri"
        android:singleLine="true" />
</com.google.android.material.textfield.TextInputLayout>
```

## Kotlin Runtime Rule

Avoid setting long `EditText.hint` values in code after inflation when the XML already uses a `TextInputLayout` label. If runtime defaults must be shown, update helper text on the parent `TextInputLayout` instead.

## Review Checklist

- Empty fields show one clean label and one optional short placeholder.
- Focused fields do not place two text strings on the same baseline.
- Filled fields keep the collapsed label clear of entered text.
- Helper/default copy is readable below the field.
- The bottom action button does not visually attach to the final helper line.
- Password/API-key fields have an explicit visibility affordance if useful.

## Source Links

- https://developer.android.com/reference/com/google/android/material/textfield/TextInputLayout
- https://m2.material.io/develop/android/components/text-fields/
