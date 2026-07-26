# Plugin 打包與 Marketplace 發佈

把 `.claude/`（skills、agents、rules）打包成 Claude Code plugin（`.claude-plugin/plugin.json`＋marketplace），以安裝／釘版取代 clone-as-template。

## 為什麼不做

- 本 repo 的定位是**啟動寶（startup kit）**：使用者 clone 後把它改造成自己的專案基底，模板、追蹤簿與文件樹都要被改寫——這與 plugin「唯讀、跟隨上游更新」的模型相反。
- 生態系一半的價值在 `VibeCoding_Workflow_Templates/`、`docs/document-system/` 與根目錄治理文件，plugin manifest 只覆蓋 `.claude/` 資產，打包必然把生態系切成兩半。
- 維護成本（版本同步、marketplace、release CI）超過單 repo 模板的現實收益。

## 先例

- 2026-07-27 借鏡 skills 生態系分析時由 owner 拍板：維持 clone-as-template，只做版本號單源化（README badge＋根目錄 `CHANGELOG.md`）。

## 替代出口

要跟隨更新 → 以本 repo 為 template repository 後手動同步；要版本可追 → 讀 `CHANGELOG.md`。若日後使用情境變成「多專案共用、不改內容」，再帶新論據翻案。
