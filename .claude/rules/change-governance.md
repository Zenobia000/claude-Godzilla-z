# Change Governance Rule

> AI 加速時代真正要治理的不是「程式碼產出速度」，而是「需求變更如何被吸收、追蹤、驗證、同步」。沒有這層治理，AI 會把矛盾文件腦補成「合理版本」，把「看起來合理」的錯誤訊息產出量產化——這就是 AI slop 的根源。

---

## TL;DR — three lines

1. **變更涉及 flow / contract / data / architecture → 先跑 Change Impact Analysis (CIA)**，不可直接改 code。
2. **CIA §8 列出「Human Decisions Required」→ 等使用者決策後才動 code**。
3. **文件衝突或文件 status: deprecated/superseded → 停下來回報，不腦補**。

---

## Hard Gate — When CIA is required

AI 在實作 code 變更前，若任務涉及以下任一面向，**必須**先呼叫 `sunnydata-change-impact-analysis` skill 產出 CIA：

| 觸發面向 | 涵蓋範圍 |
|---|---|
| **User flow / Business flow** | 新增/修改 BF/UF/SF；改變主流程或例外流程 |
| **API contract** | 新增/刪除 endpoint；request/response schema 變動；error code 變動；版本升級 |
| **Domain model** | 新增 entity / value object；改變既有 entity 的 invariant、關聯、生命週期 |
| **DB schema** | 新增/刪除 table、column、index；任何需要 migration 的變更 |
| **External integration** | 新接 vendor；改變既有 vendor 的 callback rule、retry policy、auth 機制 |
| **Test plan** | 新增測試類別；改變覆蓋率目標；改變 CI quality gate |
| **Architecture boundary** | 新增 module / service；移動 bounded context 邊界；引入新 infra（queue、cache、search）|

### Exempted（不需 CIA）

- 純 typo、註解、log message 字面修改
- 無語意的格式調整（縮排、引號、import 排序）
- 純內部 refactor，**且**無 contract 變動，**且**有現有測試覆蓋
- 修 bug，**且** bug 範圍明確在單一 function 內，**且**無 contract 影響
- Documentation-only 編輯到 tier-3 process guide

---

## Workflow when CIA fires

```
使用者描述變更
    │
    ▼
AI 偵測到觸發面向 → 呼叫 sunnydata-change-impact-analysis skill
    │
    ▼
skill 產出 CIA → 寫入 docs/4-exploration/CR-NNNN-<short>.md
    │
    ▼
AI 顯示 CIA + 🛑 等待人類決策
    │
    ▼
使用者填寫 §8 「Human Decisions Required」
    │
    ▼
AI 依 §9 「Suggested Implementation Order」逐步實作
    │
    ▼
實作完成 → 更新 TM-0000-traceability-matrix.template.md 對應 row
    │
    ▼
跑 sunnydata-doc-freshness 確認 tier-2 contract 都同步
```

---

## Source of Truth Conflict — 處理規則

當文件之間或文件與 code 矛盾：

- ❌ **不要**：自己腦補「合理版本」
- ❌ **不要**：靜默選一邊（哪怕看起來明顯）
- ✅ **要**：停下來回報衝突 + **引用具體 ID**（BF-0001、API-0007、TC-0023）+ 等使用者裁決

回報格式範例：

> 🛑 **Source of Truth 衝突偵測**
>
> - `BF-0001 §4 step 3` 描述：訂單建立後立即扣庫存
> - `SF-0001 §3 inputs` 描述：訂單建立後**保留**庫存（reserve），付款後才扣
> - `src/inventory/service.py:142` 實作：保留庫存
>
> 三方不一致。建議裁決方向：
> 1. 把 BF-0001 §4 step 3 改為「保留庫存」（與 SF/code 一致）
> 2. 或：開 CR 把行為改回「立即扣庫存」（推翻 SF/code）
>
> 等待你決定哪個是 source of truth。

---

## Stale Doc — 處理規則

讀到帶以下 frontmatter 的文件：

| frontmatter | AI 該怎麼做 |
|---|---|
| `status: draft` | 警告使用者「此文件尚未 active」；可參考但不視為事實 |
| `status: deprecated` | 警告，並建議遷移到指定替代品；不引用為事實 |
| `status: superseded` | 直接跳到 `superseded_by` 指向的文件；不再讀原文 |
| `status: archived` | 完全忽略（除非使用者明確要求看歷史） |
| 無 status frontmatter | 視為 active，但提示使用者該補 frontmatter |

`sunnydata-doc-freshness` skill 會掃出沒有正確 status 的 contract 並建議補上。

---

## Rewrite vs Refactor — 三層決策

不是所有變更都該用 CIA + 局部修改處理。當變動規模大時，先跑這個打分表決定是要**修文件**、**重組模組**、還是**開新主幹**。

### 打分維度（每項 0-2 分）

| 維度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| 產品目標是否改變？ | 沒變 | 局部變 | 大幅改 |
| 核心 User Flow 是否改變？ | 沒變 | 新增分支 | 主流程重寫 |
| Domain Model 是否改變？ | 沒變 | 新增概念 | 核心概念改 |
| API Contract 是否大量破壞？ | 少量 | 多 endpoint 變動 | 全面不相容 |
| DB Schema 是否需重建？ | 不用 | migration 可處理 | migration 很痛 |
| 模組邊界是否錯誤？ | 清楚 | 有些混亂 | 根本切錯 |
| 測試是否可信？ | 可信 | 部分可信 | 幾乎不可信 |
| 文件是否可信？ | 可信 | 部分過期 | 大量矛盾 |
| 團隊/AI 是否還理解系統？ | 理解 | 少數人懂 | 幾乎沒人懂 |

### 判斷

| 總分 | 行動 |
|---|---|
| **0–6 分** | 改文件 + 局部重構（CIA + 一次性實作） |
| **7–12 分** | 架構重審 + 模組拆分（多 CR + 跨 sprint） |
| **13 分以上** | 考慮新專案 / 新主幹（freeze 舊系統，重建） |

「**改文件只是修正地圖；當地圖描述的世界已經不是原本那個世界，就要開新專案**」。13 分以上不是逃避，是承認原本的產品假設已經死了。

---

## How AI signals change-governance awareness

- ✅ "This change touches `API-0003` schema → invoking `sunnydata-change-impact-analysis` skill before implementing."
- ✅ "Read `BF-0001` and `SF-0001` — they conflict on inventory timing. Stopping to report (see above)."
- ✅ "Document `docs/2-contracts/legacy-payment.md` is `status: superseded` → following pointer to `payment-v2.md` instead."
- ❌ Silently reconciling conflicting docs by writing "the obviously correct" code
- ❌ Implementing a feature that touches `BF-0001` without producing a CIA first
- ❌ Updating an `status: deprecated` document instead of its replacement

---

## Anti-patterns to refuse

| Anti-pattern | Why bad | What to do instead |
|---|---|---|
| AI sees a CR and starts coding immediately | Skips the gate; produces drift | Invoke CIA skill first, stop at §8 |
| CR touches API but skips contract update | Code & spec diverge silently | CIA §4 forces explicit API entry |
| Implementer skips updating traceability matrix | Coverage view rots; "CI green = OK" lie | CIA §9 step "update traceability" is mandatory |
| Editing a `status: deprecated` doc | Effort wasted; downstream still confused | Edit the `superseded_by` doc; or write new ADR if reviving |
| "Just one more field" without CIA | 50 small changes = 1 silent contract break | Even single-field additions need CIA when on tier-2 contract |

---

## See also

- `rules/context-stability.md` — what tier each artifact lives in (CIA outputs go to tier-4)
- `rules/primitive-selection.md` — when CIA, when skill, when command
- `skills/sunnydata-change-impact-analysis/SKILL.md` — gate execution skill
- `VibeCoding_Workflow_Templates/0-principles/PRIN-0001-flow-id-conventions.md` — Flow ID system used in CIA
- `VibeCoding_Workflow_Templates/4-exploration/CIA-0000-change-impact-analysis.template.md` — CIA structure
- `VibeCoding_Workflow_Templates/2-contracts/TM-0000-traceability-matrix.template.md` — must be updated post-implementation
- `VibeCoding_Workflow_Templates/3-process/QG-0000-quality-gates.md` — gates that change-governance interacts with
