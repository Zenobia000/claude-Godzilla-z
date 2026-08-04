---
name: wayfind
description: Chart a map for work too big and too foggy for one session — name the destination, ticket the decisions you can state now, and resolve them one per session until the way is clear enough to hand off to /intake or /specify.
disable-model-invocation: true
argument-hint: "<loose idea> | <map path> [ticket-id]"
---

# Wayfind

一個想法太大了，而且**還隔著霧**——從這裡到終點的路還看不見。這個 Skill 不衝向終點，它**找路**：把路畫成一張地圖，然後一次解一張**決策 ticket**，直到路清楚為止。

`/intake` 吃的是已經存在的來源（Excel、訪談表）。`/wayfind` 處理的是**來源還不存在、連要問什麼都還不確定**的階段。它的產出是**決策，不是交付物**。

寫作語域：地圖與 ticket 用 **L1／L2**（見 [../../rules/language-register.md](../../rules/language-register.md)）。這裡還沒到工程層——出現 schema、endpoint、檔名就是跑太前面了。

## 規劃，不是動手

Wayfind **預設只規劃**：每張 ticket 解決一個決策，地圖完成的條件是「路清楚了，動手之前沒有東西要再決定」。

想直接把事情做掉的衝動，通常是訊號：**你已經走到地圖邊界，該交棒了**。某個 effort 可以在地圖的 `Notes` 明文覆寫這條，把執行也納進地圖；沒寫就一律產出決策。

## 兩種模式

### A. 開圖（使用者帶著一個模糊的想法來）

1. **命名終點。** 用 `sunnydata-design` 的探索與一問一答，把「這張圖要找到什麼」釘死——一份可交接的規格、一個要先鎖定的決策、或一次就地的改動。**終點決定範圍，所以先定終點。**
2. **掃前緣。** 再問一輪，這次**廣度優先**：橫向掃過整個空間，而不是往任何一條線深挖，找出開放的決策與現在就能踏出的第一步。
   **如果掃不出霧**——路已經清楚、整趟小到一個 session 就能走完——**你不需要地圖**。停下來告訴使用者，建議直接走 `/intake` 或 `/specify`。
3. **建立地圖**，格式見 [references/map-contract.md](references/map-contract.md)：終點與 Notes 填好，`已決定` 留空，霧寫進 `尚未成形`。
4. **建立現在說得出來的 ticket**，然後**第二遍**再連依賴邊（ticket 要先有編號才能互相引用）。連完就分成前緣與被擋住的；說不出來的留在霧裡。
5. **派出 research 子代理。** 剛建立的每張 `research` ticket，用 `sunnydata-deep-research` 平行解，findings 落成帶引用的檔案，ticket 只留連結。
6. **停。** 開圖是一個 session 的工作，它不解任何 ticket。

### B. 走圖（使用者帶著一張地圖來）

1. 載入**地圖**——低解析度的全貌，不是每張 ticket 的內文。
2. 選 ticket。使用者指定就用它；否則取前緣第一張。**先認領**（寫上認領者與時間），再開始任何工作。
3. 解它——**按需放大**：要用到哪張相關或已關閉的 ticket，才去讀它的完整內容；載入 `Notes` 指名的 skill。拿不定主意時用 `sunnydata-design` 的一問一答。
4. 記錄結果：把答案寫進該 ticket 的 `答案` 欄位、狀態轉 `已解決`，並在地圖的 `已決定` 追加一行摘要＋連結。
5. 新浮現的 ticket 就建（先建再連邊）；答案讓某片霧變得說得出來了，就把它畢業成 ticket，並從 `尚未成形` 移除。若答案顯示某張 ticket 其實在終點之外，**判它出界**而不是在路上解掉它。決策若讓地圖其他部分失效，就更新或刪掉那些 ticket。

**一個 session 只解一張 ticket**（research 除外）。這是刻意的限制不是效能瓶頸——狀態活在地圖裡，不活在 context window 裡。

## Ticket 四型

每張 ticket 不是 **HITL**（人在場，由本人發言）就是 **AFK**（agent 獨力完成）。HITL 的 ticket **只能透過真實對話解決，agent 絕不代替人回答**——這是 [../../rules/thinking-boundary.md](../../rules/thinking-boundary.md) 深思模式「只 provoke 不給答案」在 ticket 層的落地。

| 型別 | 誰在場 | 什麼時候用 |
|---|---|---|
| `research` | AFK | 決策等著一個**外部事實**：文件、第三方 API、既有系統。用 `sunnydata-deep-research` 子代理解 |
| `prototype` | HITL | 關鍵問題是「該長什麼樣」或「該怎麼動」。做一個便宜、粗糙、可反應的東西來提高討論解析度 |
| `grilling` | HITL | 對話。**預設型別** |
| `task` | 兩者皆可 | 決策前必須先發生的手工工作（開通服務、取得存取權、搬資料看形狀）。它**做事**而非決策，靠解鎖一個決策換得存在資格 |

## 霧（Fog of War）

地圖**刻意不完整**：看不見的就別畫。live ticket 之外是霧——你知道要來、但還釘不住的決策，因為它們掛在還沒解的問題上。

**霧還是 ticket？判準是「你現在能不能把問題講精準」，不是「你現在能不能回答」。**

- **開 ticket**：問題已經夠銳利——即使它被擋住、現在還不能動。
- **留在霧裡**：還講不了那麼精準。**不要把霧預先切成 ticket 大小**——它比 ticket 粗，一片霧將來可能畢業成好幾張，也可能一張都沒有。

`尚未成形` 不放已決定的、已是 live ticket 的、以及出界的。

## 出界（Out of Scope）

霧只往**終點**的方向聚集。終點固定了範圍，所以終點之外的工作是**出界**——它不是霧，不屬於 `尚未成形`，有自己的區塊。是**範圍**而不是**清晰度**把它放到那裡。

出界的工作**永不畢業**。它只有在終點被重畫時才回來，而且是一個新的 effort，不是續作。

已存在的 ticket 被發現在終點之外時：**關掉它**（關閉的 ticket 明確不在前緣），並在 `出界` 留一行——摘要加上為什麼出界，連到那張關閉的 ticket。它不進 `已決定`：`已決定` 記的是真正走過的路，範圍邊界不是路上的一步。

## 交棒

地圖完成——沒有 ticket 了，路清楚了——**它交棒，不動手**：

| 終點是 | 交給 |
|---|---|
| 一組可以正規化的需求候選 | `/intake`（把決策落成 `DEC-*`，等 owner 拍板） |
| 已經由 owner 拍板、只差工程化的決策 | `/specify` |
| 一次就地的改動（資料結構遷移之類） | `/deliver` |

**把地圖直接迴圈進 `/deliver` 會跳過收束、丟掉連結的細節。** 只有在 effort 最後證明其實很小的時候，才直接走 `/deliver`。

## Completion

- 終點寫下來了，而且每張 ticket 都可以對照它判斷相關性。
- `尚未成形` 只剩真正還說不清的；說得清的都已經是 ticket。
- 每張已解決的 ticket 都有答案，且地圖的 `已決定` 有對應的一行＋連結。
- 出界項有理由，且不在 `已決定` 裡。
- 交棒對象已指名，且該 skill 的輸入條件已滿足。

## Attribution

移植自 [mattpocock/skills](https://github.com/mattpocock/skills) `wayfinder`（MIT, © 2026 Matt Pocock）。地圖改為 repo 內的 markdown＋單一 ticket 表（上游用 issue tracker 的原生 blocking 與 query）、L1/L2 語域約束、與 `/intake`／`/specify`／`/deliver` 的交棒對照為本專案新增。
