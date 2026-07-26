# 非功能需求 (NFR) - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/審核中/已批准
> **Owner:** PM / Architect / QA / SRE 共同簽核
> **原則:** 每條 NFR 必須有量化指標與驗證方法；寫不出怎麼驗證的 NFR 是願望，不是需求。

---

## 1. NFR 主表

| ID | 類別 | 指標 | 目標值 | 驗證方法 | 適用範圍 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| NFR-001 | 效能 Performance | API p95 延遲 | < [X] ms | [負載測試腳本／工具] | [核心端點] |
| NFR-002 | 可用性 Availability | 月可用率 | [99.9]% | [uptime 監控] | [對外服務] |
| NFR-003 | 安全 Security | [認證／加密／稽核要求] | [標準] | [`../05_qa/security_and_readiness.md`] | 全系統 |
| NFR-004 | 可觀測性 Observability | [log／trace 覆蓋] | [關鍵路徑 100%] | [`../06_ops/monitoring_spec.md`] | |
| NFR-005 | 擴展性 Scalability | [併發／資料量上限] | [目標值] | [壓測報告] | |

---

## 2. 取捨與依據

| NFR | 為什麼是這個數字 | 代價 | 決策紀錄 |
| :--- | :--- | :--- | :--- |
| NFR-001 | [SLA 條款 / 使用者研究] | [成本、複雜度] | ADR-*** |

---

## 3. 階段適用

- **雛形／MVP:** 只承諾 [列出的最小集合]；其餘標 TO-BE，不假裝已滿足。
- **Production:** 全表生效，Gate 需附驗證證據（`/verify`）。

---

## 4. 追溯

- 來源需求：SRS §2（`../01_requirements/srs.md`）引用本表 ID，不重複維護數字。
- 架構落地：SAD 品質屬性章節（[`sad.md`](./sad.md)）說明每條 NFR 的架構手段。
- 驗證證據：QA 追蹤簿（`../05_qa/qa_tracker.xlsx`）以 NFR-* 關聯測試。
