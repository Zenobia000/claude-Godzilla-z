# Markdown 版需求決策紀錄模板

以 MD 模板（舊 `requirement_decision_record.md` / 模板 18）作為需求決策的權威載體。

## 為什麼不做

- 需求決策的 owner 是業務／PM，他們的簽核表面是 Excel，不是 Git 裡的 MD；MD 版會造成雙權威，違反「一檔一 owner」。
- 決策、沿革、Gate 簽核天生是表格資料，Excel 的視覺對焦與下拉狀態欄比 MD 合適。

## 先例

- 模板於 v4.1（commit `a8a256e`）新增，v7.0（commit `b7e3a51`）退役：權威併入 `requirements_tracker.xlsx` ①需求決策＋③Gate＋②決策沿革，硬閘 checklist 移入 `workflow_manual.md` §8。

## 替代出口

決策可獨立成檔時用 `DEC-NNN-<slug>.md` 命名慣例（見 workflow_manual §10）；長決策理由寫 ADR 或 PRD 附註，追蹤簿只留一句話＋連結。
