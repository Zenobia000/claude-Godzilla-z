# Claude Code Godzilla

這個 repo **本身就是那套 harness**——快速 POC 用的 Claude Code 開發配置：完整的軟體工程能力庫，但不帶文件治理的硬邊界。在這裡工作，多半是在**改這套系統**，而不是用它開發別的產品。

設計原則：**Skills 厚、Runtime 薄。** 動 `skills/`、`rules/`、模板之前，先看 [.claude/CLAUDE.md](.claude/CLAUDE.md) 的**維護契約**（router 不說謊、常駐面要有證據、拒絕有紀錄）——那裡也寫了每個元件各自負責什麼。

## 開始一輪工作

**沒有寫死的命令序列。** 能力按任務語意載入，或由你 `/skill-name` 明確啟動。

| 要知道什麼 | 去哪 |
|---|---|
| Rules／Skills／Agents 三層怎麼一起運作 | [.claude/WORKFLOW.md](.claude/WORKFLOW.md) |
| 實際怎麼跑一輪：A 直接做／B 規劃一輪／C 先撥霧 | [.claude/PLAYBOOK.md](.claude/PLAYBOOK.md) |
| 哪個 Skill 何時載入、相似入口怎麼區辨 | [.claude/skills/INDEX.md](.claude/skills/INDEX.md) |
| 這個專案現在該寫哪幾份文件 | [VibeCoding_Workflow_Templates/INDEX.md](VibeCoding_Workflow_Templates/INDEX.md) |

## 預設節奏

1. **先確認分支再動 code**——在 main 上、有未提交變更、或使用者沒指定分支就要改，停下來問（`.claude/rules/git-workflow.md`）。
2. **有適用的 Skill 先載入再行動**；同一件事不同時套多個流程型 Skill。
3. **雛型期走 happy path**——先能動、能驗證，不前置法規、權限、邊界案的窮舉（`.claude/rules/thinking-boundary.md`）。
4. **以證據宣告完成**——沒實際跑過的檢查不得描述為通過（`.claude/rules/golden-rules.md` #4）。

先雛形 → 打掉 → 重構迭代是正常路徑，不是缺陷。衝突時，使用者直接要求的結果與 `.claude/rules/golden-rules.md` 優先。

## 帶進新專案

複製 `.claude/` 與需要的 `VibeCoding_Workflow_Templates/`，再照 [`_meta/new_project_bootstrap.md`](VibeCoding_Workflow_Templates/_meta/new_project_bootstrap.md) 收集專案資訊、選文件深度、生成那個專案自己的 `CLAUDE.md`。

**這一份不要整份複製過去**——它描述的是 Godzilla 本身。

需要可稽核的需求追溯、owner 簽核硬閘與 Excel 追蹤簿？換 `refactor/document-driven-ecosystem` 分支。
