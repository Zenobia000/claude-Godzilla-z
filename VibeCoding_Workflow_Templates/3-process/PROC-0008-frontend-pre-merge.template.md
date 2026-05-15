---
id: PROC-0008
title: "Frontend Pre-Merge Checklist"
status: draft
tier: 3-process
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---
# Frontend Pre-Merge Checklist

> **Tier**: 3-process — frontend pre-merge quality gate
>
> **Purpose**: 統一前端 PR 合入前的 quality gate；對齊 `tier 0` 的 quality attributes 與 `tier 2` 的合約。
>
> **Source**: realigned from `5-views/frontend-architecture.template.md` §6.測試+§9 + `frontend-information-architecture.template.md` §9 per [ADR-0001](../1-decisions/ADR-0001-frontend-template-tier-realignment.md).

---

## 1. 測試策略（合入前必須通過）

| 類型 | 工具 | 覆蓋率目標 | 測試內容 |
| :--- | :--- | :--- | :--- |
| 單元 | Vitest / Jest | 80%+ | 工具函式、Hooks、Store |
| 元件 | Testing Library | 核心元件 | 渲染、互動、狀態 |
| E2E | Playwright | 關鍵流程 | 使用者旅程（每個 PG-* 至少 1 個） |
| 視覺 | Storybook + Chromatic | 設計系統 | 元件外觀回歸 |

> 覆蓋率 < 80% 或 E2E 漏掉新 PG-NNNN → **block merge**。

---

## 2. 程式碼合入清單

- [ ] TypeScript 無錯誤 (`tsc --noEmit`)
- [ ] ESLint 無 error 級別違規
- [ ] Prettier 格式已套用
- [ ] 所有單元/元件測試通過
- [ ] E2E 關鍵流程通過
- [ ] 覆蓋率達標（或附說明）
- [ ] 無 `console.log` / `debugger` 殘留
- [ ] 無未引用的 import / 死碼

---

## 3. 品質檢查清單

- [ ] 響應式設計在 xs/sm/md/lg/xl 都驗證過
- [ ] 鍵盤導航可完成主要 CTA
- [ ] 螢幕閱讀器宣告正確（語意 + ARIA）
- [ ] 色彩對比度 ≥ 4.5:1（body）/ 3:1（large text）
- [ ] 效能預算未超標（bundle size、LCP、INP）
- [ ] 安全 checklist（依 `2-contracts/DS-0000-frontend-design-system.template.md §5`）通過

---

## 4. 資訊架構檢查清單

- [ ] 新 / 修改頁面已建立 `2-contracts/PC-0000-page-contract.template.md` 條目
- [ ] 所有頁面定義單一職責與使用者目標
- [ ] 核心使用者旅程已映射並有 E2E 覆蓋
- [ ] 導航結構清晰且一致（主導航 / 麵包屑 / Footer）
- [ ] URL 結構語義化且 SEO 友善
- [ ] 導航深度 ≤ 3 層
- [ ] 每頁只有 1 個主要 CTA
- [ ] 麵包屑導航可回溯
- [ ] 404 / error / empty 頁面有引導文案

---

## 5. 文檔同步

- [ ] 變更若觸動 tier-2 合約 → 已更新 `last-synced-with` frontmatter
- [ ] 跑 `sunnydata-doc-freshness` 確認無未同步漂移
- [ ] CHANGELOG / release notes 已更新（若為使用者可見變動）

---

## 6. 例外處理

- 任一項打勾失敗 → 在 PR description 標註 `Skip-Reason:` 並 link 對應 ADR / issue
- 重複 skip 同一項 → 觸發 ADR 評估「是否該降低標準或改善工具鏈」