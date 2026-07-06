# Skills 索引

MECE 架構：13 個 skill 對齊開發生命週期，統一 `sunnydata-` 前綴。

## 命名原則

```
sunnydata-{lifecycle-phase}
```

| 前綴 | 意義 |
| :--- | :--- |
| `sunnydata-` | SunnyData 團隊標準 skill |

## 開發生命週期

| 階段 | Skill | 用途 | 觸發時機 |
| :--- | :---- | :--- | :------- |
| THINK+PLAN+DO | **sunnydata-design** | 探索意圖 → 撰寫計畫 → 依檢查點執行 | 新功能、多步驟實作前 |
| BUILD (API) | **sunnydata-api-design** | REST API 設計最佳實踐 | 設計 API 端點 |
| BUILD (UI) | **sunnydata-shadcn-ui** | shadcn/ui 元件管理與規則 | 前端 UI 開發 |
| BUILD+TEST | **sunnydata-testing** | TDD 流程 + Unit/Integration/E2E (Playwright) | 寫功能、修 bug、建測試 |
| VERIFY (安全) | **sunnydata-security** | OWASP 分類 + 實作 checklist + 語言特定實踐 | 安全審查、auth、輸入處理 |
| VERIFY (審查) | **sunnydata-code-review** | 驗證 → 發起 review → 消化回饋 | 完成任務、commit/PR 前 |
| SHIP (基礎設施) | **sunnydata-infrastructure** | Docker + CI/CD + 部署策略 + 生產就緒 | 容器化、部署規劃 |
| SHIP (分支) | **sunnydata-branch-lifecycle** | 建立 worktree → 收尾分支 (merge/PR/cleanup) | 功能隔離、分支收尾 |
| DEBUG | **sunnydata-debugging** | 四階段結構化除錯 | bug、測試失敗、異常行為 |
| RESEARCH | **sunnydata-deep-research** | 多來源深度研究 (firecrawl/exa MCP) | 複雜問題調查 |
| ORCHESTRATE | **sunnydata-parallel-agents** | 獨立任務平行派發 | 2+ 個不相關問題同時處理 |
| META | **sunnydata-skill-authoring** | 撰寫/驗證 SKILL.md | 新增或修改 skill |

## 永遠生效的規則（非 skill）

以下在 `.claude/rules/` 目錄，每次對話自動載入：

| 檔案 | 涵蓋 |
| :--- | :--- |
| `coding-style.md` | 不可變性、檔案組織、命名慣例、品質清單 |
| `security.md` | commit 前安全檢查、秘密管理 |
| `testing.md` | 最低覆蓋率 80%、TDD 強制 |
| `git-workflow.md` | Conventional Commits、PR 流程 |
| `patterns.md` | 骨架專案策略、Repository Pattern、API 信封格式 |
| `development-workflow.md` | 研究 → 規劃 → TDD → 審查 → 提交 |
| `performance.md` | 模型選擇、Context Window 管理 |

## 擴充方式

```bash
cp -r /path/to/skill-folder .claude/skills/sunnydata-<name>/
```

| 情境 | 建議來源 |
| :--- | :------- |
| 合約/深度安全審計 | `trailofbits/skills` 依 plugin 挑選 |
| 更多 Superpowers | [obra/superpowers](https://github.com/obra/superpowers) |
| shadcn 元件 | [shadcn-ui/ui skills](https://github.com/shadcn-ui/ui/tree/main/skills/shadcn) |
