---
name: sunnydata-architecture-review
description: Architecture-level code review using a three-phase smells → principles → fixes flow. Use when reviewing existing system architecture, identifying design debt, evaluating refactor candidates, or auditing module boundaries and dependencies. Complements sunnydata-code-review (line-level) and architect agent (greenfield design).
---

> **繁體中文說明**：此技能提供「架構級」code review 的結構化流程 — 先掃壞味道 (smells) → 反向對應違反的原則 (principles) → 推薦具體修法 (fixes)。三階段順序固定，不可跳過。本 skill 補充 `sunnydata-code-review`（行級實作審查）與 `architect` agent（全新設計）之間的空缺：**對既有系統做結構性、有證據的、可決策的架構審查**。

# Architecture Review

## Overview

Three phases, fixed order. Skipping a phase invalidates the review.

```
Detect Smells → Map to Principles → Propose Fixes → Output Report
```

**Why this order is mandatory:**

- 沒有 smells = 沒有要修的東西，不要硬找。
- 找到 smells 卻對應不上原則 = 主觀判斷，必須剔除。
- 對應上原則卻沒有具體 fix = 抱怨而非審查。

**Core principles across all phases:**

- **Evidence before claims** — 每個 finding 必須有檔案路徑＋行號或可驗證的指標。
- **Severity over sentiment** — 用 Critical/High/Medium/Low 分級，不用「好/不好」。
- **Vocabulary over vibes** — 必須使用業界共通行話（見 `terminology.md`），不接受自創詞。

**When to invoke:**

- 模組／服務合併到 main 前的架構守門
- 技術債盤點與重構優先級排序
- 新人 onboarding 走讀既有系統
- 評估「要重寫還是要修」的決策依據
- PR 觸及 3+ 模組或新增 100+ 行時的結構性審查

**When NOT to invoke:**

- 行級實作審查 → 用 `sunnydata-code-review`
- 全新系統的架構設計 → 用 `architect` agent
- 模板合規檢查 → 用 `template-check` command
- Bug 修復、typo、單檔小改 → 直接審查不需此流程

---

## Phase 1: Detect Smells

### Iron Rule

```
NO SMELL WITHOUT EVIDENCE
```

「感覺有問題」「好像不對」不算證據。每個 smell 必須附：

1. **檔案路徑＋行號** 或
2. **可量化指標**（方法行數、圈複雜度、依賴數量、N+1 查詢次數、p99 延遲等）

### Five-Dimension Scan Matrix

掃描必須覆蓋全部 5 個維度。即使某維度無 finding，也要在報告中明確聲明 "no findings"。

| 維度 | 對應 smell（節錄自 terminology.md） | 證據蒐集指令範例 |
| :--- | :--- | :--- |
| **Dependency 依賴** | Cyclic Dependency、Big Ball of Mud、Inappropriate Intimacy、Parallel Inheritance | `rg -l "import.*from"` / 模組依賴圖 / `git log --follow` |
| **Modularity 模組化** | God Object、Long Method、Large Class、Feature Envy、Divergent Change、Shotgun Surgery | `wc -l` / 函式行數分布 / 同檔案修改頻率 |
| **Performance 效能** | N+1 查詢、Switch Statements、Primitive Obsession（在熱路徑上） | `rg "for.*\.find"` / APM trace / DB query log |
| **Distributed reliability 分散式可靠性** | 缺 Circuit Breaker、缺 Idempotent Consumer、缺 Outbox、缺 DLQ、雙寫不一致、Backpressure 缺失 | `rg "retry\|circuit\|idempot"` / 訊息系統設定 |
| **Technical debt 技術債** | Lava Flow、Speculative Generality、Refused Bequest、Comments Smell、Middle Man、Temporary Field | `git blame` / `rg "TODO\|FIXME\|HACK"` / 死碼掃描 |

### Severity Definitions

| 等級 | 定義 | 範例 |
| :--- | :--- | :--- |
| **Critical** | 立即危害正確性或可用性，或會導致資料遺失 | 雙寫不一致、缺 idempotent 導致重複扣款、循環依賴致無法部署 |
| **High** | 6 個月內必修，否則阻礙可擴展性／團隊速度 | God Object 已 1500+ 行、缺 Circuit Breaker 在外部依賴上 |
| **Medium** | 影響可維護性，但可規劃 1-2 季處理 | Long Method、N+1 在非熱路徑、過多 switch |
| **Low** | 風格或可讀性問題 | 命名不一致、過度註解、Temporary Field |

### Smell Output Template

每個 finding 在 Phase 1 結束時必須能填完此表：

```
Smell:    <terminology.md 中的標準名稱>
Location: <絕對或專案相對路徑:行號>
Evidence: <一行可驗證的事實或指標>
Severity: Critical | High | Medium | Low
```

**找不到 5 個以上 smell 的審查通常不可信** — 不是系統完美，是審查太淺。挑戰自己再掃一次。

---

## Phase 2: Map to Principles

### Iron Rule

```
EVERY SMELL MUST VIOLATE A NAMED PRINCIPLE
```

對應不上原則的 smell 一律剔除。可選原則必須來自 `terminology.md` 的 Principles 區段（SOLID / KISS / DRY / YAGNI / LoD / Tell-Don't-Ask / Boy Scout Rule / Clean Architecture / Hexagonal / Onion）。

### Mapping Cheat Sheet（節錄）

| Smell | 違反原則 | 為什麼 |
| :--- | :--- | :--- |
| God Object | SRP | 一個類承擔多個變更理由 |
| Feature Envy | LoD | 過度與「非直接朋友」對話 |
| Long Parameter List | KISS / Tell-Don't-Ask | 暴露內部細節給呼叫方 |
| Duplicated Code | DRY | 同邏輯多處複製 |
| Speculative Generality | YAGNI | 為不存在的需求預留彈性 |
| Cyclic Dependency | DIP / Hexagonal | 內層依賴外層或彼此糾纏 |
| Switch Statements | OCP / LSP | 新增類型必須改現有程式碼 |
| Refused Bequest | LSP | 子類無法替換父類 |
| 雙寫不一致 | Outbox（缺）/ Transaction Boundary | 跨資源無一致性保證 |
| 缺 Circuit Breaker | Bulkhead 隔艙原則 | 單點失敗會擴散 |

### Principle Match Output Template

```
Smell:        <Phase 1 finding>
Violates:     <原則名稱（terminology.md 編號）>
Why:          <一句話說明違反在哪>
Counter-evidence: <若反駁此原則違反，需提供什麼證據？>
```

`Counter-evidence` 欄位是防呆 — 強迫審查者預想反駁，避免主觀套用原則。

---

## Phase 3: Propose Fixes

### Iron Rule

```
EVERY FIX MUST CITE A PATTERN OR PRACTICE FROM terminology.md
```

不接受「重寫一下」「優化一下」這種無詞彙的建議。每個 fix 必須命名一個或多個 Pattern / Practice。

### Fix Proposal Template

```
For Smell:    <Phase 1 finding>
Violates:     <Phase 2 principle>

Option A (recommended):
  Pattern:    <terminology.md Pattern/Practice 名稱>
  Steps:      <3-5 條具體執行步驟>
  Effort:     S (< 1 day) | M (1-5 days) | L (> 1 week)
  Risk:       <破壞性 / 回歸風險 / 團隊熟悉度評估>
  ADR needed: Yes | No

Option B (alternative):
  ...同上格式...

Trade-off: <為何選 A 而非 B 的一句話>
```

**至少兩個方案**是強制要求 — 單一方案 = 沒做取捨。Trade-off 欄位必填。

### Common Smell-to-Fix Map（節錄）

| Smell | 候選 Pattern / Practice |
| :--- | :--- |
| God Object | Extract Class、Compound Pattern (Composite/Strategy) |
| Long Method | Extract Method、Replace Conditional with Polymorphism |
| Feature Envy | Move Method、Introduce Service |
| Switch Statements | Strategy、State、Polymorphism |
| Cyclic Dependency | Dependency Inversion、Anti-Corruption Layer |
| N+1 Query | Eager Loading、Batch Fetch、DataLoader Pattern |
| 缺 Idempotent | Idempotent Consumer、Idempotency Key |
| 雙寫不一致 | Outbox Pattern、Saga |
| 缺 Circuit Breaker | Circuit Breaker、Bulkhead、Retry+Backoff+Jitter |
| Lava Flow | Strangler Fig、Branch by Abstraction |
| Speculative Generality | YAGNI Cleanup、Inline 化 |

### ADR Trigger

任何形成持久架構取捨的 **Critical** 或 **High** fix 都要列為 ADR
candidate；使用目標專案的正式 ADR 目錄與既有命名。只有修 bug、沒有新決策時，
不為了嚴重度硬建 ADR。

---

## Output Format

審查最終報告必須使用此骨架，**不可省略任何區段**。

```markdown
# Architecture Review: <Scope>

- **Date**: <YYYY-MM-DD>
- **Reviewer**: <agent / human>
- **Scope**: <模組路徑 / 服務名 / PR 範圍>
- **Commit range**: <git SHA range, 若適用>

## Summary

- **Smells found**: <總數> (Critical: <n>, High: <n>, Medium: <n>, Low: <n>)
- **Dimensions covered**: Dependency / Modularity / Performance / Distributed / TechDebt
- **Recommended next action**: <一句話, 例如「先修 Critical 的 Outbox 缺失再合併」>
- **ADR candidates**: <數量>

## Findings

### [Critical] Smell: <名稱>

- **Evidence**: `path/to/file.py:123` — <一行事實>
- **Violates**: <原則名稱>
- **Why it matters**: <一句話>
- **Proposed fix**:
  - Option A: <Pattern> — <Effort: S/M/L> — <Risk>
  - Option B: <Pattern> — <Effort: S/M/L> — <Risk>
  - Trade-off: <一句話>
- **ADR needed**: Yes

### [High] Smell: <名稱>
...

### [Medium] Smell: <名稱>
...

## Dimension Coverage

| 維度 | Findings | Status |
| :--- | :--- | :--- |
| Dependency | <n> | covered / no findings |
| Modularity | <n> | covered / no findings |
| Performance | <n> | covered / no findings |
| Distributed reliability | <n> | covered / no findings |
| Technical debt | <n> | covered / no findings |

## ADR Candidates

- [ ] `ADR-<NNNN>-<topic>.md` — <一句話標題與 decision owner>

## Open Questions

- <無法在審查中決定、需要 stakeholder 回答的問題>
```

---

## Forbidden Phrases

仿 `sunnydata-code-review` 規則，以下表述在審查報告中**禁止出現**：

| 禁止 | 必須 |
| :--- | :--- |
| "looks good" | "passes dimensions X, Y, Z with no findings" |
| "seems fine" | "no Critical/High findings; <n> Medium documented" |
| "should be ok" | "verified by <evidence>; pass" |
| "could be better" | "<smell name> at <location>; severity <level>" |
| "maybe consider" | "Option A: <pattern>; Option B: <pattern>; recommend A because <reason>" |
| "in my opinion" | "<principle> requires <X>; current code shows <Y>" |
| "perhaps refactor" | "Apply <Pattern> with effort <S/M/L> and risk <X>" |

---

## Integration with Other Skills

| 場景 | 流程 |
| :--- | :--- |
| PR 合併前 | `sunnydata-architecture-review` → 若無 Critical → `sunnydata-code-review`（行級） |
| 新模組設計 | `architect` agent（設計）→ 實作 → `sunnydata-architecture-review`（驗收） |
| 技術債盤點 | `sunnydata-architecture-review`（找出所有 High+）→ 排序 → 必要決策寫入正式 ADR 目錄 |
| Onboarding 走讀 | `sunnydata-architecture-review`（產出系統地圖）→ 補入 docs |
| 大型重構決策 | `sunnydata-architecture-review` → `architect` agent（重新設計受影響部分） |

---

## How to Invoke

### Direct invocation（主 agent 直接執行）

主 agent 載入此 skill，依三階段流程執行，產出報告。適合單次、範圍明確的審查。

### Via subagent（dispatch architecture-reviewer.md）

使用 `architecture-reviewer.md` 作為 subagent 模板，dispatch 給專責 agent 執行，回傳結構化報告。適合：

- 範圍大（多模組／整個服務）
- 需要與其他 subagent 平行執行
- 主 agent 想保留 context window

dispatch 後的結論回傳主 Agent 整合。只有需要長期保存的決策才依
`VibeCoding_Workflow_Templates/03_architecture/adr.md`
寫入正式 ADR；不自動建立 runtime context 報告。

### Reference loading

`terminology.md` 預設**不**載入 context — 由 reviewer 在需要查特定詞彙時主動 Read。這降低 skill 啟動成本。

---

## Quick Reference

| 我想… | 用什麼 |
| :--- | :--- |
| 找出系統有哪些壞味道 | Phase 1 + 五維度矩陣 |
| 知道某 smell 的標準名稱 | `terminology.md` Smells 區段 |
| 為某 smell 找修復模式 | `terminology.md` Patterns 區段 + Smell-to-Fix Map |
| 評估重構優先級 | Severity 表 + Effort 評估 |
| 把持久決策寫成 ADR | 目標專案正式 ADR 目錄 + VibeCoding ADR 範本 |
| 大型範圍／平行審查 | `architecture-reviewer.md` subagent |
