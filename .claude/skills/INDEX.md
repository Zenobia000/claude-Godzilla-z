# Skills Catalog

Skills 是這套生態系的能力資料庫。它們分成「人工啟動的流程入口」與「按任務載入的專業能力」，不再與 Rules、Agents 或 Output Styles 重複。

## Action Skills

這四個入口會顯示為 slash commands，並以 `disable-model-invocation: true` 保留人類階段控制：

| Skill | 輸入 | 主要產出 | 邊界 |
|---|---|---|---|
| `/intake` | Excel／需求訪談來源 | 來源登錄、需求候選、待確認項 | 唯讀原始工作簿；保留 sheet/row/cell |
| `/specify` | 已核准需求 | PRD、BDD、SAD、ADR、追溯 | 不實作 production code |
| `/deliver` | 已核准 REQ／Scenario | 一個可驗收垂直切片 | 本機實作；外部行動另行授權 |
| `/verify` | 變更範圍／REQ ID | 各 gate 證據與 verdict | 預設唯讀，不順手修復 |

詳細流程見 [../WORKFLOW.md](../WORKFLOW.md)。

## SunnyData 能力庫

| 類別 | Skill | 使用時機 |
|---|---|---|
| 探索與設計 | `sunnydata-design` | 模糊問題、方案探索、複雜計畫 |
| API | `sunnydata-api-design` | API 契約與介面設計 |
| UI | `sunnydata-shadcn-ui` | shadcn/ui 元件與組合 |
| 測試 | `sunnydata-testing` | Unit／Integration／E2E、test-first |
| 除錯 | `sunnydata-debugging` | 可重現失敗與根因分析 |
| 安全 | `sunnydata-security` | 信任邊界、auth、輸入、秘密、供應鏈 |
| Code Review | `sunnydata-code-review` | 變更完成後的高信心審查 |
| 架構 Review | `sunnydata-architecture-review` | 架構 smells、principles、fixes |
| 基礎設施 | `sunnydata-infrastructure` | 容器、CI/CD、部署與生產就緒 |
| 分支生命週期 | `sunnydata-branch-lifecycle` | worktree、commit、PR／merge 收尾 |
| 深度研究 | `sunnydata-deep-research` | 需要多個權威來源的調查 |
| 平行協作 | `sunnydata-parallel-agents` | 2 個以上真正獨立且可安全合併的子任務 |
| Skill 作者工具 | `sunnydata-skill-authoring` | 新增、裁剪與驗證 Skill |

Action Skill 只載入當前步驟必要的能力；不要為了「完整」一次預載全部。

## Community 能力庫

| Skill | 用途 |
|---|---|
| `community-a11y-audit` | 可存取性稽核 |
| `community-frontend-design` | 前端視覺與互動設計 |
| `community-react-composition` | React composition patterns |
| `community-react-native` | React Native 實務 |
| `community-react-performance` | React／Next.js 效能 |
| `community-ui-design-system` | UI/UX 設計系統與資料庫 |
| `community-ux-bencium-controlled` | 保守、受控的 UX 規格 |
| `community-ux-bencium-innovative` | 創新型 UX 規格 |
| `community-web-guidelines` | Web interface guidelines |

這些是資料庫，不代表每個專案都要啟用。

## 責任檢查

新增內容前先判斷：

- 每次任務都必須遵守嗎？才放 `rules/golden-rules.md`
- 是知識、清單或可重用做法嗎？放 Skill
- 是人工觸發的端到端流程嗎？做 Action Skill
- 需要獨立 context、工具或權限嗎？使用 Agent，並預載現有 Skill
- 只是回答格式嗎？放 Output Style
- 是確定、快速、低頻且無隱性狀態的自動化嗎？才考慮 Hook

## 擴充與來源

新增 Skill 時保留來源、授權與更新方式，先檢查是否已有重疊能力。可參考：

- [obra/superpowers](https://github.com/obra/superpowers)
- [Anthropic skills](https://github.com/anthropics/skills)
- [Trail of Bits skills](https://github.com/trailofbits/skills)
- [shadcn/ui skills](https://github.com/shadcn-ui/ui/tree/main/skills/shadcn)

舊版 runtime prompts 保存在 `docs/legacy/claude-runtime/`，不會自動載入。
