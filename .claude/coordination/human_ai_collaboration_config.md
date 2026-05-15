# 🤖⚔️ 人機協作配置檔

## 🎛️ 建議模式設定

**當前模式**: `SUGGEST_MEDIUM` （可由人類調整）

**模式說明**:
- `SUGGEST_HIGH` - 每次重要節點都建議 Subagent
- `SUGGEST_MEDIUM` - 只在關鍵點建議（預設）
- `SUGGEST_LOW` - 只在必要時建議
- `SUGGEST_OFF` - 關閉自動建議

## 📋 VibeCoding 範本審視觸發器

### 🎯 觸發條件與建議

| 情境 | VibeCoding 範本 | 建議 Subagent | 觸發閾值 |
|------|----------------|---------------|----------|
| **專案規劃階段** |
| 專案初始化 | `4-exploration/PRD-0000-prd.template.md` | documentation-specialist | HIGH |
| 架構重大決策 | `1-decisions/ADR-0000-adr.template.md` | workflow-template-manager | HIGH |
| 功能驗收規劃 | `3-process/PROC-0002-bdd-guide.md` | e2e-validation-specialist | MEDIUM |
| **開發階段** |
| 完成核心功能 | `1-decisions/ARCH-0000-architecture-overview.template.md` | code-quality-specialist | MEDIUM |
| API 變更/新增 | `2-contracts/API-0000-api-spec.template.md` | documentation-specialist | HIGH |
| 測試相關 | `2-contracts/MC-0000-module-contract.template.md` | test-automation-engineer | HIGH |
| 專案結構變更 | `5-views/VIEW-0001-project-structure.template.md` | workflow-template-manager | LOW |
| **程式碼分析階段** |
| 複雜依賴關係 | `5-views/VIEW-0002-file-dependencies.template.md` | code-quality-specialist | MEDIUM |
| 類別結構設計 | `5-views/VIEW-0003-class-relationships.template.md` | code-quality-specialist | MEDIUM |
| **品質保證階段** |
| 安全考量 | `3-process/PROC-0004-security-readiness-checklist.md` | security-infrastructure-auditor | HIGH |
| 準備部署 | `3-process/PROC-0004-security-readiness-checklist.md` | deployment-expert | HIGH |

### 🔍 審視邏輯

```markdown
1. Claude 分析當前程式碼變更
2. 對照 VibeCoding 範本檢查點
3. 根據建議模式決定是否提示
4. 輸出 emoji 標註建議
5. 等待人類確認
```

## 🎮 人機協作指令映射

### 快速指令實作

| 入口 | 類型 | 實作方式 | 範例 |
|------|------|---------|------|
| `/suggest-mode [level]` | command | 更新此配置檔 | `/suggest-mode low` |
| `vibecoding-code-review` | skill | 基於 VibeCoding 範本分析 | 自然語言觸發或 Skill tool |
| `sunnydata-code-review` + `sunnydata-architecture-review` | skill | 通用品質與架構檢查 | Skill tool |
| `/template-check [name]` | command | 檢查特定範本合規性 | `/template-check api` |

## 🚦 協作流程控制

### 建議輸出格式

```
📊 基於 VibeCoding 範本的建議：

🎯 偵測情境：[具體情境描述]
📋 相關範本：1-decisions/ARCH-0000-architecture-overview.template.md
🤖 建議 Subagent：
  🟡 code-quality-specialist - 程式碼重構機會
  🔴 security-infrastructure-auditor - 安全檢查點

❓ 是否執行建議？
  [1] 啟動 code-quality-specialist
  [2] 啟動 security-infrastructure-auditor
  [3] 全部啟動
  [N] 跳過

請輸入選擇：
```

### 人類回應處理

- **數字選擇** → 啟動對應 Subagent
- **'N' 或 'n'** → 跳過建議
- **'all' 或 'a'** → 啟動所有建議的 Subagent
- **空白輸入** → 使用預設行為（跳過）

## 🎯 實作範例

### 🗣️ 自然語言意圖識別邏輯

```python
# 虛擬邏輯（供 Claude 參考）
def parse_natural_language_intent(user_message):
    """解析人類自然語言，識別要啟動的 Subagent"""

    intent_keywords = {
        'code-quality-specialist': [
            '檢查程式碼', '程式碼品質', '重構', 'code quality', 'refactor',
            '程式碼審查', 'code review', '優化程式碼', '依賴分析',
            '類別關係', '模組依賴', 'dependency', 'class relationship'
        ],
        'security-infrastructure-auditor': [
            '安全', '安全檢查', '漏洞', 'security', 'vulnerability',
            '安全性', '檢查安全性', 'audit', '安全稽核'
        ],
        'test-automation-engineer': [
            '測試', '跑測試', '覆蓋率', 'test', 'testing', 'coverage',
            '單元測試', '測試分析', '模組測試', 'module test'
        ],
        'deployment-expert': [
            '部署', '上線', '發布', 'deploy', 'deployment', 'release',
            '準備部署', 'production', '就緒檢查'
        ],
        'documentation-specialist': [
            '文檔', '文件', 'documentation', 'docs', 'API文檔',
            '更新說明', '說明文件', '專案簡報', 'project brief',
            'PRD', '需求文件', 'API規範', 'api spec'
        ],
        'e2e-validation-specialist': [
            '端到端', 'e2e', 'UI測試', '使用者流程', 'user flow',
            '整合測試', 'ui test', 'BDD', '驗收測試', '場景測試'
        ],
        'workflow-template-manager': [
            '專案結構', '架構', '規劃', 'structure', 'architecture',
            'plan', '專案規劃', '架構決策', 'ADR', '技術選型',
            'decision record', '決策記錄'
        ]
    }

    # 分析用戶訊息
    message_lower = user_message.lower()

    for agent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword.lower() in message_lower:
                return {
                    'detected_agent': agent,
                    'confidence': calculate_confidence(message_lower, keyword),
                    'suggested_task': generate_task_description(agent, user_message)
                }

    return None

def respond_to_natural_language(user_message):
    """回應自然語言請求"""
    intent = parse_natural_language_intent(user_message)

    if intent:
        agent = intent['detected_agent']
        emoji = get_agent_emoji(agent)

        response = f"""
{emoji} 偵測意圖：{agent}
📋 基於：「{user_message}」
🎯 建議任務：{intent['suggested_task']}

❓ 是否啟動此 Subagent？(y/N)
"""
        return response
    else:
        return "❓ 無法識別意圖，請使用更明確的描述或查看可用指令"
```

### Claude 分析程式碼時的內建邏輯

```python
def analyze_and_suggest(code_changes, suggest_mode):
    if suggest_mode == 'SUGGEST_OFF':
        return None

    suggestions = []

    # 基於 VibeCoding 範本分析
    if detect_api_changes(code_changes):
        if suggest_mode in ['SUGGEST_HIGH', 'SUGGEST_MEDIUM']:
            suggestions.append({
                'agent': 'documentation-specialist',
                'reason': 'API 變更需要更新文檔',
                'template': '2-contracts/API-0000-api-spec.template.md',
                'emoji': '📝'
            })

    if detect_security_concerns(code_changes):
        suggestions.append({
            'agent': 'security-infrastructure-auditor',
            'reason': '偵測到安全相關程式碼',
            'template': '3-process/PROC-0004-security-readiness-checklist.md',
            'emoji': '🔴'
        })

    return format_suggestions(suggestions)
```

## 🎛️ 可調整參數

```yaml
# 人類可修改的設定
collaboration_config:
  suggest_mode: "SUGGEST_MEDIUM"
  auto_trigger_threshold: 3  # 幾個建議達到才觸發
  show_template_references: true
  emoji_annotations: true
  wait_for_confirmation: true
  suggestion_timeout: 30  # 秒，超過則自動跳過
```

---

**核心精神：Claude 是你的智能副駕駛，所有重要決定由你來下！** 🤖⚔️