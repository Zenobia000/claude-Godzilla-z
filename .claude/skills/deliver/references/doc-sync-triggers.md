# 程式碼 ↔ 文件同步觸發表

按需載入。「code 與 docs 同一個 PR」這條原則常駐在 [`../../../rules/git-workflow.md`](../../../rules/git-workflow.md)；本檔只回答**哪一類變更要動哪些文件**。

寫完 code 立刻盤點受影響的 docs 並一併修改。禁止「以後再補文件」——之後再補幾乎都會忘，最後產生 doc drift。

## 每次 commit 前 + 每次 PR 前自問

```
[ ] 這個 commit 動了哪幾類 code？
[ ] 對應觸發表，需要動哪些 docs？
[ ] 已動 / 已確認不需動 / 還沒動？
[ ] single-source-of-truth（docs/document-system/、追溯矩陣、狀態）已更新？
[ ] ADR-worthy 決策已寫或已 cross-ref？
```

## 觸發對映

文件名稱依 `docs/document-system/` 與 `VibeCoding_Workflow_Templates/` 結構。

| Code 變更類型 | 必查 docs |
| :--- | :--- |
| 新模組 / 重大目錄重組 | lld（專案結構與依賴段）、`docs/document-system/architecture.md` 權威矩陣 |
| ADR-worthy 決策（換引擎、升版、改通道等） | adr、`docs/document-system/INDEX.md` |
| Schema / DDL / 資料契約變更 | sad 資料段、db_design、api_spec／openapi.yaml、追溯矩陣 |
| 依賴升級（pyproject / package.json） | prd 依賴清單、相關 adr |
| 環境變數新增 / 改名 | `.env.example`、deployment_and_operations 的環境變數表 |
| 新 API endpoint / CLI 子命令 | api_spec／openapi.yaml、README、CLI manual |
| 新測試類別（performance / e2e） | sds 測試段、test_plan |
| 部署 / Docker / 拓撲變更 | deployment_and_operations、runbook |
| 需求 / 驗收 / 追溯變化 | intake 需求登錄、`docs/document-system/` 追溯矩陣（永遠要動） |
| 跨多檔重構 / 結構大改 | 受影響文件的版本 banner、lld 專案結構段 |

## 例外（允許延後同步）

- 純內部重構，無對外介面、無架構文件描述（但仍要更新追溯／狀態）
- WIP commit（branch 內 squash 前）——PR 提出前必須補齊
- dependency lock 自動更新（uv.lock、package-lock.json 等）
