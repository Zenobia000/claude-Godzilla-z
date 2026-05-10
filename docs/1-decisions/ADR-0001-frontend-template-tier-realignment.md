---
id: ADR-0001
status: accepted
date: 2026-05-10
decider: Sunny
related-cr: CR-0001
supersedes: null
superseded_by: null
---

# ADR-0001: Frontend Template Tier Realignment

> **Tier**: 1-decisions → architectural decision record
> **Triggered by**: [CR-0001](../4-exploration/CR-0001-frontend-template-tier-realignment.md)
> **Authority**: `.claude/rules/context-stability.md`、`VibeCoding_Workflow_Templates/5-views/README.md`

---

## 1. 背景與問題

### 上下文

`VibeCoding_Workflow_Templates/5-views/` 內有兩份前端模板：

- `frontend-architecture.template.md`（194 行，9 個區塊）
- `frontend-information-architecture.template.md`（156 行，9 個區塊）

### 問題

兩份模板所在的 **tier 5 (views)** 在 `5-views/README.md` 與 `rules/context-stability.md` 中明文定義為：

> Derived from code. **Never hand-maintained.** Stale by default. Treat as cache, not source of truth.

但實際內容大半是**規範性目標**（technical SLO、A11y 標準、設計原則、頁面合約），不是從 code derive 的快照。這違反 tier 5 定義，導致：

- AI 後續援引 tier 5 內容當作可信規範來源（違反「code wins on disagreement」）
- 文件無法 dogfooding 自家規則（context-stability.md）
- 下游使用模板的專案會繼承此誤分類

### 驅動因素 / 約束

- `.claude/rules/context-stability.md`（已上線）強制 tier 分離
- `5-views/README.md` 已宣告 tier 5 不可手工維護
- 必須維持模板向下相容（對下游已 instantiate 的專案影響可控）

---

## 2. 考量的選項

### 選項一：保留現狀，僅輕度去重

**描述**：把兩份模板的路由表/頁面總覽（~5% 重疊）合併到 IA 一份，其餘不動。

- **優點**：零搬動、零下游影響
- **缺點**：仍違反 tier 5 原則，AI slop 風險未解
- **成本/複雜度**：低

### 選項二：兩份合併為一份「Frontend Spec」加 tier 標記

**描述**：合成一份大檔，每章節標 `[tier 1]` `[tier 5]` 標記。

- **優點**：減少檔案數
- **缺點**：違反 tier 分離核心原則（一檔多 tier），下游 AI 仍會混淆
- **成本/複雜度**：中

### 選項三（採用）：細拆到 tier 0/1/2/3，tier 5 只留 derived 部分

**描述**：依內容性質拆解到正確 tier，tier 5 只保留路由表/頁面樹/資料流（這些確實能從 router config derive）。

- **優點**：完全對齊 stability tiers 原則；dogfooding 自家規則
- **缺點**：搬動大、需更新 8 處引用點
- **成本/複雜度**：中

---

## 3. 決策

**選擇**：選項三 — 細拆到 tier 0/1/2/3，tier 5 只留 derived 部分。

**理由**：

1. **教育性 > 便利性**：此 repo 是 meta-template，下游會繼承這套分類。錯誤分類會被放大複製。
2. **規則一致性**：context-stability.md 是新加的硬規則，本 repo 必須 dogfooding，否則規則本身可信度受損。
3. **拆解粒度可控**：實際拆出 6 個新檔 + 1 個修訂，不會檔案泛濫。
4. **rollback 容易**：純文檔搬移，git revert 可完整還原。

---

## 4. 拆解映射表（決策核心）

### 4.1 `frontend-architecture.template.md` 的去處

| 原章節 | 內容 | 新位置 | Tier 理由 |
|---|---|---|---|
| §1 架構目標 | 4 個品質維度 + KPI | `0-principles/frontend-quality-attributes.template.md` | 規範性目標 = tier 0 hard constraint |
| §4 效能策略 | LCP/FID/CLS 目標 + 載入優化 | 同上 | 同上（SLO） |
| §5 可用性與無障礙 | WCAG / 響應式 / i18n | 同上 | 同上（無障礙是 hard principle）|
| §8 監控（前半）| Core Web Vitals 目標 | 同上 | 同上 |
| §2 系統分層 | 各層職責 + 技術選型 | `1-decisions/frontend-tech-stack.template.md` | 技術選型 = ADR |
| §6 工程實踐（前半）| 專案結構樹 + Lint/Type/Commit | 同上 | 結構決策 = ADR |
| §3 設計系統 | Design Tokens + Atomic Design | `2-contracts/frontend-design-system.template.md` | 被前端實作消費的合約 |
| §7 前後端協作 | API Client + 認證授權 | 同上 | 通訊合約 |
| §8 監控（後半）| 前端安全 checklist | 同上 | 跨團隊安全合約 |
| §6 工程實踐（測試表）| Unit/Component/E2E/Visual | `3-process/frontend-pre-merge-checklist.template.md` | quality gate 流程 |
| §9 開發檢查清單 | 上線前 checklist | 同上 | quality gate 流程 |

### 4.2 `frontend-information-architecture.template.md` 的去處

| 原章節 | 內容 | 新位置 | Tier 理由 |
|---|---|---|---|
| §1 目的範圍 | 設計原則開場 | `4-exploration/prd.template.md §6`（新增章節）| 設計意圖屬 PRD |
| §2 設計原則 | 簡化原則 / 認知負荷 | 同上 | 同上 |
| §4 核心使用者旅程 | 旅程映射表 | 同上 | 旅程屬 PRD |
| §6 頁面規格 | 每頁職責/資料/CTA/導航 | `2-contracts/page-contract.template.md` | 每頁=合約 |
| §3 資訊架構總覽 | 系統層次 + 頁面樹 | `5-views/frontend-route-map.template.md`（rename）| 從 router 可 derive |
| §5 導航結構 | 主導航 + 麵包屑 | 同上 | 同上 |
| §7 URL 結構 | 命名規範 + 路由表 | 同上 | 路由表 derive；命名規範簡化保留 |
| §8 資料流 | 頁面間資料傳遞 | 同上 | 從 store + router derive |
| §9 檢查清單 | IA 檢查項 | `3-process/frontend-pre-merge-checklist.template.md` | quality gate |

---

## 5. 後果

### 正面

- 完全對齊 stability tiers 原則，AI 後續援引文件時 tier 邊界清晰
- 下游 instantiation 會繼承正確分類
- ADR 自身也成為「如何在前端領域應用 stability tiers」的 working example

### 負面

- 一次性搬移成本：6 個新檔 + 8 個引用點更新
- 下游已基於舊路徑 instantiate 的專案需手動 migrate（本 repo 尚未 v1.0，影響面小）

### 影響範圍

- `VibeCoding_Workflow_Templates/{0,1,2,3,4,5}-*/` 多個目錄
- `VibeCoding_Workflow_Templates/INDEX.md`、`LEGACY-INDEX.md`
- `PROJECT_STRUCTURE.md`
- `.claude/commands/template-check.md`
- `.claude/skills/vibecoding-write-frontend-bdd/SKILL.md`
- `.claude/agents/workflow-template-manager.md`

### 重新評估觸發

- 若新增第 3 份「前端整合測試合約」需求，重新審視 tier 2 是否需細分
- 若 5-views 規則弱化（如改為「半 derived 半手工」），重新審視本 ADR 是否應 supersede

---

## 6. 執行計畫

由 [CR-0001 §9](../4-exploration/CR-0001-frontend-template-tier-realignment.md#9-suggested-implementation-order) 主控。

---

| 日期 | 審核人 | 備註 |
| :--- | :--- | :--- |
| 2026-05-10 | Sunny | accepted via CR-0001 |
