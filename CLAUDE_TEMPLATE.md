<!-- CLAUDE_CODE_PROJECT_TEMPLATE_V4 -->

# Claude Code 專案初始化範本

> **版本:** v4.1 | **作者:** Sunny | **模式:** 人類主導

當 Claude Code 偵測到此檔案時：
1. 顯示範本資訊
2. 詢問：「偵測到專案初始化範本，要開始設定嗎？」
3. 同意後執行 `/task-init`
4. 完成後刪除此檔案

---

## Phase 1: 基礎資訊收集

```
1. 專案名稱？ → [PROJECT_NAME]
2. 專案簡述？ → [PROJECT_DESCRIPTION]
3. 主要語言？ (Python/TypeScript/Go/Java/其他)
4. 設定 GitHub？ (新建/現有/跳過)
```

## Phase 2: VibeCoding 7 問快速澄清

```
1. 核心問題：這個專案主要解決什麼問題？
2. 核心功能：3-5 個最重要的功能？
3. 技術約束：技術偏好和限制？
4. 使用體驗：期望的使用體驗？
5. 規模需求：預期用戶規模和效能？
6. 時程資源：時間和資源限制？
7. 成功標準：如何衡量成功？
```

## Phase 3: 確認設定

```
推薦結構：[簡易/標準/AI-ML]
建議密度：[HIGH/MEDIUM/LOW]
複雜度：[依分析結果]

確認？(y/N)
```

---

## 初始化執行

Claude Code 在使用者確認後：

1. **建立專案結構** -- 依選擇的類型
2. **生成 CLAUDE.md** -- 包含專案資訊和開發規則
3. **載入 VibeCoding 模板** -- 依專案類型選擇
4. **初始化 Git** -- .gitignore + 初始 commit
5. **設定 GitHub** -- 如使用者選擇
6. **建立 WBS** -- 任務分解結構
7. **刪除此範本**

---

## CLAUDE.md 生成模板

初始化後產生的 CLAUDE.md 應包含：

```markdown
# CLAUDE.md - [PROJECT_NAME]

> **專案:** [PROJECT_NAME]
> **描述:** [PROJECT_DESCRIPTION]
> **語言:** [LANGUAGE]
> **建立:** [DATE]

## 開發流程

遵循 `.claude/WORKFLOW.md` 的標準流程：
/task-next → superpowers:writing-plans (skill) → superpowers:test-driven-development (skill) → /verify

## 專案規則

已載入 `.claude/rules/` 中的通用規則（自動生效）：
- coding-style: 不可變性、檔案大小
- development-workflow: 研究先行、Plan-TDD-Review
- security: commit 前安全檢查
- testing: 80%+ 覆蓋率
- git-workflow: Conventional Commits

## 禁止事項

- 不在根目錄建立原始碼檔案 → 使用 src/
- 不建立重複檔案 (v2, enhanced_, new_) → 擴展現有
- 不硬編碼可配置的值 → 使用環境變數
- 不靜默吞噬錯誤 → 明確處理
- 不複製貼上程式碼 → 提取共用函式

## 強制要求

- 每完成一個功能後 commit
- 先搜尋現有實作再建立新檔案
- 超過 30 秒的操作使用 Task Agent
- 3 步驟以上的任務先用 TodoWrite 拆解

## 專案結構

[依選擇的類型填入]

## 技術棧

[依收集的資訊填入]
```

---

## 專案結構範本

### 簡易型
```
project/
├── CLAUDE.md
├── src/
│   ├── main.[ext]
│   └── utils.[ext]
├── tests/
├── docs/
└── output/
```

### 標準型
```
project/
├── CLAUDE.md
├── src/
│   ├── core/        # 核心邏輯
│   ├── utils/       # 工具函式
│   ├── models/      # 資料模型
│   ├── services/    # 服務層
│   └── api/         # API 端點
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── configs/
└── scripts/
```

### AI/ML 型
```
project/
├── CLAUDE.md
├── src/
│   ├── core/
│   ├── models/
│   ├── training/
│   ├── inference/
│   └── evaluation/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── experiments/
├── tests/
└── docs/
```

---

## GitHub 設定

初始 commit 後詢問：

```
GitHub 儲存庫設定：
1. 建立新的 GitHub repo
2. 連接現有 repo
3. 跳過（僅本地 Git）
```

選 1 或 2 後自動設定 remote 和推送。

---

## 初始化完成後顯示

```
專案 "[PROJECT_NAME]" 初始化成功！

配置：
- CLAUDE.md 規則生效
- 7 條自動載入規則 (.claude/rules/)
- 13 個專業 Agent 就緒
- 17 個 Slash Command 可用
- GitHub: [啟用/未啟用]

下一步：
1. /task-next                          取得第一個任務 (command)
2. superpowers:writing-plans            規劃實作步驟 (skill)
3. superpowers:test-driven-development  開始開發 (skill)
```

<!-- CLAUDE_CODE_INIT_END -->
