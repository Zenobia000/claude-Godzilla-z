# 語域與角色定位（Language Register）

不同文件面對不同讀者，語域（用詞、抽象層級、語氣）必須跟著讀者切換。

## 三層語域

| 層 | 名稱 | 主要讀者 | 語域特徵 |
|---|---|---|---|
| **L1** | 業務語言（Business） | 業主、PM、訪談對象、末端使用者 | 以問題、價值、可觀察行為描述；名詞用領域詞彙；避免資料結構、框架、API、識別字 |
| **L2** | 橋接語言（Bridge，中介層） | 系統分析師、領域建模者、跨職能審閱者 | 業務詞與工程詞並列；顯式建立對照，不靠讀者自行腦補 |
| **L3** | 工程語言（Engineering） | 工程師、QA、維運 | 精確、可執行；直接寫介面、欄位、識別字、指令、失敗行為 |

**鐵律：L1 與 L3 之間唯一合法的轉換通道是 L2。** 不允許在業務文件裡偷渡實作細節，也不允許工程文件憑空長出沒有來源的業務主張。

對應到 `VibeCoding_Workflow_Templates/`：`02_project_brief_and_prd` 的問題／使用者／目標段是 L1；`03_behavior_driven_development_guide`、`04_architecture_decision_record`、`05_architecture_and_design_document`、`06_api_design_specification` 是 L2；`07_module_specification_and_tests` 之後的模組、結構、依賴、前端、安全、部署文件是 L3。

一份文件必須混用時（例如 PRD 同時給 PM 與工程看）：**業務語言主述，工程細節退到附註、表格或連結**，不要讓工程名詞打斷業務讀者的閱讀線。

## 各語域的該與不該

- **L1**：用領域名詞與使用者可觀察的結果描述；不出現 schema、class、endpoint、環境變數、框架名。
- **L2**：每個工程名詞旁註對應的業務詞，每個業務詞給一個穩定定義；衝突與待確認顯式標記。
- **L3**：精確到欄位、指令、失敗路徑；不把未驗證推論寫成事實。

> POC 階段不強制穩定 ID 追溯鏈。需要 `SRC-* → REQ-* → ACPT-*` 這類可稽核追溯時，走 Pilot／企業級路線（`refactor/document-driven-ecosystem` 分支）。
