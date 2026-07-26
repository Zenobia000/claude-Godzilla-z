# Changelog

版本號的唯一真相源是 [README](README.md) 的 version badge；本檔記錄完整沿革。模板庫（`VibeCoding_Workflow_Templates/`）在 v6.0 之後曾獨立編號（templates v4.0–v8.4），自本檔建立起併入 repo 版本、不再獨立編號，其歷史條目保留於下方「Templates 歷史版本」。

## Unreleased（refactor/document-driven-ecosystem）

- 借鏡 skills 生態系設計，收斂單一真相源：pipeline 圖唯一權威 `.claude/WORKFLOW.md`、`/specify` 硬閘 checklist 唯一權威 `workflow_manual.md` §8、追溯 ID 主鏈唯一權威 `architecture.md` §7.1，其餘位置改為引用。
- 版本標記單源化：README badge 為唯一版本號，模板 INDEX／workflow_manual／template_standard 撤下獨立版本，版本沿革併入本檔。
- `.claude/CLAUDE.md` 改寫為維護契約（不變量清單）；`skills/INDEX.md` 升級為情境路由器。
- 大型 `sunnydata-*` skill（skill-authoring、infrastructure、testing、api-design、code-review）拆分為精簡 SKILL.md＋`references/` 漸進揭露。
- 新增 `.out-of-scope/` 知識庫：記錄已拒絕的機制與理由（TaskMaster hooks、流程型 output-styles、requirement_decision_record MD 版、plugin 打包）。
- 新增 `specify/references/bdd-format.md`：BDD 場景輕量格式（v8.0 移除 bdd_guide 模板後 `/specify` 步驟 4 的授權格式）。
- 修正 stale 引用：specify `argument-hint` 與 skills/INDEX 撤下已刪除的模板名、rules 數量描述、CLAUDE_TEMPLATE 舊模板編號、PROJECT_STRUCTURE 目錄樹。
- 新增 rules：`thinking-boundary.md`（速通/深思模式）；追蹤簿重構為三本角色追蹤簿。
- 補 dev→prod 晉升規範：`sunnydata-infrastructure` 新增 Environment Promotion（build-once-promote-artifact、per-env gate、expand-contract migration）；`deployment_and_operations` 模板新增 §2.1 環境晉升表，production 晉升證據接 `/verify`＋②執行證據＋③Gate 與 Release 狀態軸。

## Repo 版本

| 版本 | 日期 | 重點 |
|---|---|---|
| v6.0 | 2026-07-24 | 文件驅動四階段、Excel 欄位級 SSOT、runtime 解耦、Word/Vibe/Excel 整合 |
| v5.1 | 2026-05-10 | 架構 review skill 與 SunnyData 能力庫 |
| v5.0 | 2026-04-06 | Skills MECE 與 Git 品質流程 |
| v4.x | 2026-03 | Agents、Commands、Hooks、StatusLine 生態系 |

## Templates 歷史版本（已併入 repo 版本，停止獨立編號）

| 版本 | 日期 | 變更 |
|---|---|---|
| v8.4 | 2026-07-26 | 新增 `03_architecture/diagrams/`：drawio 溝通級大圖模板（solution_overview、c4_context、c4_container、deployment_topology、ai_guardrails 可選）＋視覺規範、style 字串庫、`_tools/` 程式化生成與版面驗收管線（drawio_kit＋analyze_layout）、`_examples/` ACME 虛構專案 few-shot 錨點（score=0）；mermaid/drawio 單一 owner 分工，工程細圖（L3/sequence/dataflow/ER/狀態機）維持 mermaid 正典 |
| v8.3 | 2026-07-26 | 實例化規則入法：每份模板 Metadata 標「單例／每 X 一份」，多實例分支 key 限穩定錨點（頁面/決策/Aggregate/症狀/服務），禁止 per-feature 資料夾樹（功能視角＝ID 骨幹） |
| v8.2 | 2026-07-26 | 地毯式正規化：新增 _meta/template_standard（六要素＋密度紀律），15 份全部補齊 TOC／語域／追溯段、統一編號；sad 501→199 行；lld 復活承載 Code 地圖與狀態機（自 api_spec 遷入） |
| v8.1 | 2026-07-26 | 復活瘦身版 information_architecture（只留全站結構：頁面總覽、導航、路由表含認證/角色、跨頁資料載體）；補回整併遺失錨點：api_spec §6 狀態機、prd 允收改 Given/When/Then、ui_spec 導航入出口、ux_research 轉換率目標欄 |
| v8.0 | 2026-07-26 | 收斂到 Pilot 核心 13 份＋3 追蹤簿：移除 product_vision/roadmap、bdd_guide、information_architecture/frontend_technical_design、nfr、sds/lld/event_spec＋asyncapi、security_and_readiness、monitoring/incident、07_governance 全部；企業級文件未來依 Word 指南增建 |
| v7.0 | 2026-07-26 | 退役 requirement_decision_record（權威併入 requirements_tracker ①需求決策＋③Gate＋②決策沿革，硬閘 checklist 移入 workflow_manual §8）；Profile 改為開發階段（雛型／Pilot／企業級），雛型期心流優先 |
| v6.1 | 2026-07-26 | 整併舊模板：project_structure＋file_dependencies＋class_relationships 併入 lld；CHANGELOG 模板併入 release_note；code_review 與 documentation_and_maintenance 退役（職責在 git-workflow 規則與 Skills） |
| v6.0 | 2026-07-26 | 全面對齊 Word 指南：補 00_strategy、BRD/SRS、UX/UI Spec、NFR、DB/Event、Test/UAT、Runbook/Monitoring/Postmortem、Release/CR；檔名改用指南詞彙（sad、sds、api_spec…）；00_meta 改為 _meta |
| v5.0 | 2026-07-24 | 依 Word 九層分類把模板從扁平編號改為 `00`–`07` 資料夾＋語義命名；結構取代對照表 |
| v4.1 | 2026-07-24 | 新增需求決策紀錄；01 吸收 Word 治理智慧；需求/工程決策硬邊界 |
| v4.0 | 2026-07-24 | 整合 Word catalog、Excel 欄位級 SSOT、四個 Action Skills 與風險式裁剪 |
