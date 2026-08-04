# 語域寫作指引（L1 / L2 / L3 的該與不該）

按需載入。三層定義、L2 唯一通道鐵律、階段角色定位常駐在 [`../../../rules/language-register.md`](../../../rules/language-register.md)；本檔只回答**動筆寫的時候該怎麼落字**。

## 各語域的該與不該

**L1 業務**
- 該：用領域名詞、以使用者可觀察的結果描述、把限制講成業務規則
- 不該：出現 schema、class、endpoint、環境變數、框架名、內部識別字

**L2 橋接**
- 該：每個工程 ID 旁註對應的業務詞；每個業務詞給一個穩定定義與反例；衝突與待確認顯式標記
- 不該：只給工程 ID 不給業務語意，或只給業務描述卻無法追溯到工程契約

**L3 工程**
- 該：精確到欄位、指令、失敗路徑；用專案既有命名慣例
- 不該：把未驗證推論寫成事實；重述業務動機當作實作理由（動機引用 L1／L2 的 ID 即可）

## 一份文件必須混用時

例如 PRD 同時給 PM 與工程看：**業務語言主述，工程細節退到附註、表格或連結**，不要讓工程名詞打斷業務讀者的閱讀線。

## 文件語域對照

| 語域 | 文件 |
|---|---|
| **L1 業務** | product_vision／roadmap、prd 的問題／使用者／目標段、brd、ux_research_and_journey、intake 需求登錄的業務欄位、訪談紀錄、release_note |
| **L2 橋接** | bdd_guide、adr、sad、srs、api_spec／openapi.yaml、追溯矩陣、術語表（Ubiquitous Language）、prd 的 `FR/NFR/ACPT` 映射段 |
| **L3 工程** | sds、lld、db_design、event_spec、程式碼與測試、ui_spec／frontend_technical_design、test_plan、security_and_readiness、deployment／runbook／monitoring |
