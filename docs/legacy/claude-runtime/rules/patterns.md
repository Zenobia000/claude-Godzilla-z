# 通用模式

## 骨架專案策略

實作新功能時：
1. 搜尋經驗證的骨架專案
2. 平行評估選項（安全性、擴展性、相關性）
3. 以最佳匹配作為基礎
4. 在成熟結構中迭代

## Repository Pattern

封裝資料存取在一致介面後：
- 定義標準操作: findAll, findById, create, update, delete
- 具體實作處理儲存細節
- 業務邏輯依賴抽象介面
- 易於替換資料來源、簡化測試

## API 回應格式

所有 API 使用一致的信封格式：
- 成功/狀態指示器
- 資料酬載（錯誤時 null）
- 錯誤訊息欄位（成功時 null）
- 分頁中繼資料（total, page, limit）

完整 API 設計規範請載入 sunnydata-api-design skill。
