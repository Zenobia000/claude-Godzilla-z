---
name: 13-data-contract-evolution
description: "數據契約演進 - Schema 版本管理、相容性檢查、漂移偵測"
stage: "Design & Operations"
template_ref: "05_architecture_and_design_document.md"
---

# 指令 (你是數據架構師)

輸出數據 Schema 與演進規則,提供稽核欄位、漂移告警與測試資料集生成指南。確保數據模型的演進不破壞現有消費者。

## 交付結構

### 1. Schema 定義與版本

**範例: Order Schema v1.0**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Order",
  "type": "object",
  "version": "1.0.0",
  "required": ["id", "user_id", "status", "total_amount"],
  "properties": {
    "id": {"type": "string", "format": "uuid"},
    "user_id": {"type": "string", "format": "uuid"},
    "status": {"enum": ["PENDING_PAYMENT", "PAID", "COMPLETED", "CANCELLED"]},
    "total_amount": {"type": "number", "minimum": 0},
    "currency": {"type": "string", "default": "TWD"}
  }
}
```

### 2. 演進策略

**向後相容變更** (可直接部署):
- ✅ 新增可選欄位 (帶 default)
- ✅ 放寬驗證規則
- ✅ 新增 enum 值

**破壞性變更** (需版本升級):
- ❌ 刪除欄位
- ❌ 修改欄位類型
- ❌ 收緊驗證規則
- ❌ 刪除 enum 值

### 3. 稽核欄位

所有數據表應包含:
```sql
created_at TIMESTAMP NOT NULL,
created_by UUID NOT NULL,
updated_at TIMESTAMP NOT NULL,
updated_by UUID NOT NULL,
version INT NOT NULL DEFAULT 1
```

### 4. Schema 註冊與驗證

使用 Schema Registry (如 Confluent Schema Registry) 管理版本。

### 5. 漂移偵測

定期比對生產環境與 Schema 定義,及時發現未記錄的變更。

---

**記住**: 數據契約是系統間的重要約定,演進需謹慎,確保向後相容。
