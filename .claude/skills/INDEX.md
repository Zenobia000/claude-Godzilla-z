# Skills Catalog & Router

Skills 是這套生態系的能力資料庫。它們分成「人工啟動的流程入口」與「按任務載入的專業能力」，不再與 Rules、Agents 或 Output Styles 重複。本檔同時是**路由器**：改動任何 skill 時必須同步更新本檔（見 `.claude/CLAUDE.md` 維護契約——索引說謊視為缺陷）。

## Action Skills

這四個入口會顯示為 slash commands，並以 `disable-model-invocation: true` 保留人類階段控制：

| Skill | 輸入 | 主要產出 | 邊界 |
|---|---|---|---|
| `/intake` | Excel／需求訪談來源 | 來源登錄、需求候選、待確認項 | 唯讀原始工作簿；保留 sheet/row/cell |
| `/specify` | 已核准需求 | 依風險裁剪的工程契約（PRD、BDD、SAD、ADR，加選 SRS/BRD/API/DB/LLD/UI）與追溯 | 不實作 production code |
| `/deliver` | 已核准 REQ／Scenario | 一個可驗收垂直切片 | 本機實作；外部行動另行授權 |
| `/verify` | 變更範圍／REQ ID | 各 gate 證據與 verdict | 預設唯讀，不順手修復 |

詳細流程見 [../WORKFLOW.md](../WORKFLOW.md)。

## 路由：情境 → 入口

| 你面對的情境 | 走這裡 | 不是這裡（為什麼） |
|---|---|---|
| 拿到訪談表／Excel／口頭構想，要正規化成需求候選 | `/intake` | 不是 `/specify`——owner 還沒拍板，工程化會越過需求決策硬邊界 |
| 需求已由 owner 核准，要翻成工程契約 | `/specify` | 不是直接寫 code——沒有 FR/ACPT 的實作無法驗收 |
| 規格已核准，要動手實作 | `/deliver` | 不是 `sunnydata-design`——探索已在 specify 完成；deliver 按需載入能力 skill |
| 要判定「做完了沒」 | `/verify` | 不是相信 agent 自報告——verify 只收新鮮命令輸出與 trace 證據 |
| 遇到 bug／測試失敗 | `sunnydata-debugging` | 不是直接修——鐵律：先根因，後修復 |
| 變更完成要自查／請求審查 | `sunnydata-code-review` | 不是 `sunnydata-architecture-review`——後者看系統級 smells，不看單次 diff |
| 系統架構健檢、設計債盤點 | `sunnydata-architecture-review` | 不是 `architect` agent——agent 用於需要隔離 context 的第二意見 |
| 模糊問題要先探索方案 | `sunnydata-design` | 不是 `/specify`——specify 吃的是已核准需求，不做開放探索 |
| 多來源查證、需要引用 | `sunnydata-deep-research` | 不是 `sunnydata-parallel-agents`——後者是平行「做」，前者是平行「查」 |
| 要新增或修 skill 本身 | `sunnydata-skill-authoring` | — |
| 回答太長太散、要馬上拍板或動手 | `adhd-dev-mode` | 不是 Output Style——style 一選用就污染每個後續回答（見 `.out-of-scope/workflow-output-styles.md`）；本 skill 按需啟用 |
| 使用者說「白話」「所以呢」，或問的是決策問題而非定位問題 | `sunnydata-plain-explain` | 不是 `adhd-dev-mode`——後者壓縮密度但保留工程語彙；前者換語域，把答案翻到決策層 |

## 輸出治理

| Skill | 使用時機 | 邊界 |
|---|---|---|
| `adhd-dev-mode` | 需要「可以馬上動手或馬上拍板」的高密度輸出 | 永遠管**密度**；只在速通模式管**誰做決定**。深思模式下不給建議，只攤開決策空間 |
| `sunnydata-plain-explain` | 確定要白話之後，怎麼寫 | 只管**方法**；何時該白話、何時禁用由 [../rules/plain-language-answers.md](../rules/plain-language-answers.md) 管 |

四個權威分工，互不重疊：

| 權威 | 管什麼 |
|---|---|
| [../rules/thinking-boundary.md](../rules/thinking-boundary.md) | 誰思考（速通／深思） |
| [../rules/plain-language-answers.md](../rules/plain-language-answers.md) | 何時換語域（含與 `adhd-dev-mode` 的仲裁：定位問題不白話） |
| `adhd-dev-mode` | 輸出密度與收斂 |
| `sunnydata-plain-explain` | 白話的寫法 |

**已知張力**：`adhd-dev-mode` 要求給 `file:line` 與確切指令，`plain-explain` 要求「用動作講機制、不用元件名」。仲裁在 `plain-language-answers.md` 的「何時不可以白話」第一條——使用者要定位時不白話。

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
| 白話解釋 | `sunnydata-plain-explain` | 把已查證的結論翻譯到讀者的決策層 |

Action Skill 只載入當前步驟必要的能力；不要為了「完整」一次預載全部。大型 skill（skill-authoring、infrastructure、testing、api-design、code-review）已拆為精簡 SKILL.md＋`references/` 漸進揭露，依 SKILL.md 內的指示按需讀取。

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

- 每次任務都必須遵守嗎？才放 `rules/`
- 是知識、清單或可重用做法嗎？放 Skill
- 是人工觸發的端到端流程嗎？做 Action Skill
- 需要獨立 context、工具或權限嗎？使用 Agent，並預載現有 Skill
- **只是**回答格式、且要無條件一直生效嗎？放 Output Style。若同時承載判準（證據分級、決策歸屬、安全下限），就放 Skill 按需啟用——`adhd-dev-mode` 屬後者
- 是確定、快速、低頻且無隱性狀態的自動化嗎？才考慮 Hook
- 曾被拒絕過嗎？先讀 `.out-of-scope/` 對應檔再提案

## 擴充與來源

新增 Skill 時保留來源、授權與更新方式，先檢查是否已有重疊能力。可參考：

- [obra/superpowers](https://github.com/obra/superpowers)
- [Anthropic skills](https://github.com/anthropics/skills)
- [Trail of Bits skills](https://github.com/trailofbits/skills)
- [shadcn/ui skills](https://github.com/shadcn-ui/ui/tree/main/skills/shadcn)
