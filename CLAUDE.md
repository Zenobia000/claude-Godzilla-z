# Claude Code Godzilla

這個 repo **本身就是那套 harness**——文件驅動、能力按需、證據閉環的 Claude Code 軟體工程生態系。在這裡工作，多半是在**改這套系統**，而不是用它開發別的產品。

動 `skills/`、`rules/`、模板之前，先看 [.claude/CLAUDE.md](.claude/CLAUDE.md) 的**維護契約**（router 不說謊、單一真相源、常駐面要有證據）——那裡也寫了每個元件各自負責什麼。

## 開始一輪工作

主線 `業務來源 → /intake → /specify → /deliver → /verify`；想法太大、連要問什麼都還不確定時，先走匝道 `/wayfind`。

| 要知道什麼 | 去哪 |
|---|---|
| 各入口的輸入、完成條件、流程結構 | [.claude/WORKFLOW.md](.claude/WORKFLOW.md)（唯一權威） |
| 實際怎麼跑一輪：走查、決策點、常見錯誤 | [.claude/PLAYBOOK.md](.claude/PLAYBOOK.md) |
| 哪個 Skill 何時載入、相似入口怎麼區辨 | [.claude/skills/INDEX.md](.claude/skills/INDEX.md) |
| 工程文件怎麼填、這個階段該填哪幾份 | [VibeCoding_Workflow_Templates/INDEX.md](VibeCoding_Workflow_Templates/INDEX.md) |

## 預設節奏

1. **先確認分支再動 code**——在 main 上、有未提交變更、或使用者沒指定分支就要改，停下來問（`.claude/rules/git-workflow.md`）。
2. **有適用的 Skill 先載入再行動**；同一件事不同時套多個流程型 Skill。
3. **以證據宣告完成**——沒實際跑過的檢查不得描述為通過（`.claude/rules/golden-rules.md` #4）。

## 帶進新專案

複製 `.claude/` 與 `VibeCoding_Workflow_Templates/`，再照 [`_meta/new_project_bootstrap.md`](VibeCoding_Workflow_Templates/_meta/new_project_bootstrap.md) 建立來源登錄、選文件深度、生成那個專案自己的 `CLAUDE.md`。

**這一份不要整份複製過去**——它描述的是 Godzilla 本身。
