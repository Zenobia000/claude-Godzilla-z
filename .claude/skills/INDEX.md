# Skills 索引與路由

流程結構見 [../WORKFLOW.md](../WORKFLOW.md)；實際走查與決策點見 [../PLAYBOOK.md](../PLAYBOOK.md)。

這個 harness 沒有寫死的流程入口。Skills 是**按需載入的能力庫**——任務語意命中才載入，不無條件常駐。

需要 `/intake → /specify → /deliver → /verify` 這類文件驅動的流程編排、Excel 追蹤簿與簽核硬閘時，換到 Pilot／企業級路線（`refactor/document-driven-ecosystem` 分支）。

## 情境路由

| 你在做什麼 | 載入 | 別選錯 |
|---|---|---|
| 需求還模糊，要先探索方案 | `sunnydata-design` | 不是直接開寫——探索沒做完的實作會重寫 |
| 設計 API 契約 | `sunnydata-api-design` | |
| 寫測試 / 走 TDD | `sunnydata-testing` | |
| 有 bug、測試失敗、行為異常 | `sunnydata-debugging` | 不是先猜著改——先要可重現的失敗 |
| 安全敏感（auth、輸入、秘密、供應鏈） | `sunnydata-security` | |
| 變更完成，要審查 | `sunnydata-code-review` | 行級審查；架構級用 `sunnydata-architecture-review` |
| 架構有 smell，要評估重構 | `sunnydata-architecture-review` | 既有系統用它；全新設計用 `architect` agent |
| 要決定測試接縫放哪、某個抽象值不值得存在 | `sunnydata-codebase-design` | 不是 `sunnydata-architecture-review`——後者**找**哪裡痛，前者給描述解法的**詞彙**與接縫規則 |
| 想法太大、一個 session 裝不下，**連要問什麼都還不確定** | `sunnydata-wayfind` | 不是 `sunnydata-design`——後者探索一個你握得住的問題；wayfind 給你握不住的那種，而且產決策不產方案 |
| 答案在**人**身上，不在任何文件裡 | `sunnydata-questionnaire` | 不是自己猜——猜出來的被當成事實記下去，比沒答案更貴 |
| 開分支 / 收尾開 PR | `sunnydata-branch-lifecycle` | |
| 容器化、CI/CD、部署 | `sunnydata-infrastructure` | |
| 前端 UI | `sunnydata-shadcn-ui`、`community-*` | |
| 需要多來源查證 | `sunnydata-deep-research` | |
| 2 個以上真正獨立的子任務 | `sunnydata-parallel-agents` | 有共享狀態或先後依賴就不要平行 |
| 新增或修改 skill | `sunnydata-skill-authoring` | |

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
| 深模組詞彙 | `sunnydata-codebase-design` | seam 放哪、interface 該多小、抽象值不值得 |
| 撥霧 | `sunnydata-wayfind` | 太大又太模糊、一個 session 裝不下的工作 |
| 問卷 | `sunnydata-questionnaire` | 把你答不出來的決策變成給別人填的問卷 |
| 基礎設施 | `sunnydata-infrastructure` | 容器、CI/CD、部署與生產就緒 |
| 分支生命週期 | `sunnydata-branch-lifecycle` | worktree、commit、PR／merge 收尾 |
| 深度研究 | `sunnydata-deep-research` | 需要多個權威來源的調查 |
| 平行協作 | `sunnydata-parallel-agents` | 2 個以上真正獨立且可安全合併的子任務 |
| Skill 作者工具 | `sunnydata-skill-authoring` | 新增、裁剪與驗證 Skill |
| 白話解釋 | `sunnydata-plain-explain` | 把已查證的結論翻譯到讀者的決策層 |

只載入當前步驟必要的能力；不要為了「完整」一次預載全部。大型 skill（skill-authoring、infrastructure、testing、api-design、code-review、branch-lifecycle）已拆為精簡 SKILL.md＋`references/` 漸進揭露，依 SKILL.md 內的指示按需讀取。

常駐 `rules/` 下放到 skill `references/` 的條件性內容：

| 內容 | 位置 | 常駐面留下的 |
| :--- | :--- | :--- |
| Commit message 細則、PR 前置與 body、tangled history 恢復 | `sunnydata-branch-lifecycle/references/git-conventions.md` | `rules/git-workflow.md` 的鐵律與兩條 commit 約束 |
| 兩軸 review 的派工與 Fowler smell baseline | `sunnydata-code-review/references/two-axis-review.md` | SKILL.md 只留「兩軸為何分開、不得跨軸 rerank」 |
| 地圖格式、ticket 表欄位、前緣定義 | `sunnydata-wayfind/references/map-contract.md` | SKILL.md 只留兩種模式、四種 ticket 型別、霧與出界的判準 |

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

- 每次任務都必須遵守嗎？才放 `rules/`——而且要能在 [../ABLATION.md](../ABLATION.md) 填出「失敗證據」
- 是知識、清單或可重用做法嗎？放 Skill
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
- [mattpocock/skills](https://github.com/mattpocock/skills)

### 已引入的外部來源

| 本專案的 skill／內容 | 來源 | 授權 | 更新方式 |
|---|---|---|---|
| `sunnydata-codebase-design` | [mattpocock/skills](https://github.com/mattpocock/skills) `codebase-design` | MIT © 2026 Matt Pocock | 手動比對上游；接縫選擇規則為本專案新增 |
| `sunnydata-wayfind` | 同上，`wayfinder` | MIT | 地圖改為 repo 內 markdown＋單一 ticket 表；交棒對象改接 `sunnydata-design` |
| `sunnydata-questionnaire` | 同上，`to-questionnaire` | MIT | 「grill the send」方法引用；L1 語域與「回答不等於核准」邊界為本專案新增 |
| `sunnydata-code-review/references/two-axis-review.md` | 同上，`code-review` | MIT | 兩軸與 smell baseline 引用；spec 來源改為通用解析 |
| `sunnydata-design` 垂直切片段 | 同上，`to-tickets` | MIT | 切片判準與 expand-contract 序列為概念引用 |
| `sunnydata-testing` 接縫與反模式段 | 同上，`tdd` | MIT | 概念引用，措辭重寫 |
| `.claude/WORKFLOW.md` Context 衛生段 | 同上，`ask-matt` 的 context hygiene / smart zone | MIT | 概念引用，改綁 `sunnydata-design` 兩階段 |

全域共用：把 skill 目錄 symlink 到 `~/.claude/skills/`，檔案實體留在專案內（版控追得到），全域只放捷徑。
