# Output Styles Guide

Output Style 只負責「回答怎麼呈現」，不負責「工作怎麼執行」。

## 保留的樣式

| 樣式 | 用途 |
|---|---|
| `Vision Output` | 解釋架構、流程或多元件關係時，優先使用最小且有用的圖表 |

在 Claude Code 使用 `/config` 的 **Output style** 選擇或切回預設樣式；變更會寫入本機 `settings.local.json`，下一個 session 生效。沒有特殊呈現需求時，使用預設樣式即可。

## 為何移除 01–14

舊版 PRD、BDD、SAD、API、TDD、Review、Security、Database 與 CI 樣式實際上都是工作流程或文件模板。把它們設成全域 Output Style，會讓後續每個回答都持續受到不相關格式影響。

這些責任現在由下列位置承接：

- 流程編排：`.claude/skills/intake/`、`specify/`、`deliver/`、`verify/`
- 領域方法：其他 `sunnydata-*`、`community-*` Skills
- 文件格式：`VibeCoding_Workflow_Templates/`
- 企業文件選用：`software_development_documentation_guide_zh_tw.docx`

舊檔仍可由 Git 歷史取回，但不再進入 Claude Code 的執行期選單。
