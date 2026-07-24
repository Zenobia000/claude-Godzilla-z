---
description: 調整 Agent 建議的頻率和密度，控制人機協作模式。
---

# 建議模式控制

## 模式說明

| 模式 | 說明 | 適用場景 |
| :--- | :--- | :--- |
| `high` | 每個任務節點都建議 Agent | 新手、學習中 |
| `medium` | 僅在關鍵決策點建議（預設） | 日常開發 |
| `low` | 僅在必要時建議 | 熟練開發者 |
| `off` | 關閉自動建議 | 心流模式、快速原型 |

## 使用方式

```
/suggest-mode high      # 每步都建議
/suggest-mode medium    # 關鍵點建議（預設）
/suggest-mode low       # 最少建議
/suggest-mode off       # 關閉建議
```

## 模式行為

### high
- 每完成一個函式 → 建議 code-quality-specialist
- 每次 git commit 前 → 建議 security-infrastructure-auditor
- 每個新功能 → 建議 tdd-guide

### medium（預設）
- 完成整個功能後 → 建議 code-quality-specialist
- 準備 PR 時 → 建議安全檢查

### low
- 僅在偵測到風險時建議（安全漏洞、測試缺失）

### off
- 完全不主動建議，只在你呼叫 `/hub-delegate` 時才啟動
