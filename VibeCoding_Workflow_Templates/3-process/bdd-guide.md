# BDD 行為驅動情境指南

> **版本:** v1.0 | **更新:** YYYY-MM-DD

---

## Gherkin 語法速查

| 關鍵字 | 用途 |
| :--- | :--- |
| `Feature` | 高層次功能，對應 PRD 中的 Epic |
| `Scenario` | 具體業務場景/測試案例 |
| `Given` | 初始狀態 (Arrange) |
| `When` | 使用者操作 (Act) |
| `Then` | 預期結果 (Assert) |
| `And/But` | 連接多個步驟 |
| `Background` | 所有 Scenario 共用的前置步驟 |
| `Scenario Outline` + `Examples` | 參數化多組資料測試 |

---

## 範本

**檔案名稱**: `[feature_name].feature`

```gherkin
Feature: [功能名稱]
  # 對應 PRD: [Link]

  Background:
    Given [共用前置條件]

  @happy-path @smoke-test
  Scenario: [正常流程描述]
    Given [前置狀態]
    When [使用者操作]
    Then [預期結果]

  @sad-path
  Scenario: [異常流程描述]
    Given [前置狀態]
    When [錯誤操作]
    Then [錯誤處理結果]

  @edge-case
  Scenario Outline: [邊界情況描述]
    When I fill in "<field>" with "<value>"
    Then I should see "<message>"

    Examples:
      | field | value | message |
      | ...   | ...   | ...     |
```

---

## 最佳實踐

1. **一個 Scenario 只測一件事**
2. **使用陳述式** -- `Then I should be redirected to...` (非 `Then the system redirects...`)
3. **避免 UI 細節** -- `When I confirm my order` (非 `When I click the green button`)
4. **從使用者角度編寫** -- 非技術人員也能讀懂
