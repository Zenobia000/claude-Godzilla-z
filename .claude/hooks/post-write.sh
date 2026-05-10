#!/bin/bash

# TaskMaster Post Write Hook
# 當 Claude Code 寫入檔案後觸發，特別關注文檔生成

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

# 確保 logs 目錄存在
mkdir -p "$CLAUDE_DIR/logs" 2>/dev/null

# 日誌函數
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$CLAUDE_DIR/logs/hooks.log"
}

# 從 stdin 讀取 hook JSON 輸入
INPUT=$(cat)

# 解析寫入的檔案路徑
if command -v jq >/dev/null 2>&1; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
else
    FILE_PATH=""
fi

log "🪝 TaskMaster Post Write Hook 觸發: $FILE_PATH"

# 檢查是否為文檔檔案
if [[ "$FILE_PATH" == *.md ]]; then
    log "📄 偵測到 Markdown 文檔寫入: $FILE_PATH"

    # 檢查是否為專案文檔目錄
    if [[ "$FILE_PATH" == *"docs/"* ]]; then
        log "📋 專案文檔更新: $FILE_PATH"

        # 如果 TaskMaster 已初始化，通知文檔生成完成
        if [ -f "$CLAUDE_DIR/taskmaster-data/project.json" ]; then
            log "🔔 通知 TaskMaster 文檔生成完成"

            # 觸發文檔生成完成處理
            if [ -f "$CLAUDE_DIR/taskmaster.js" ]; then
                cd "$PROJECT_ROOT"
                node "$CLAUDE_DIR/taskmaster.js" --hook-trigger=document-generated --file="$FILE_PATH"
            fi

            # 顯示駕駛員審查提示
            cat << EOF

┌──────────────────────────────────────────────────────────┐
│  📄 文檔生成完成通知                                      │
│                                                          │
│  檔案: $(basename "$FILE_PATH")                          │
│  路徑: $FILE_PATH                           │
│                                                          │
│  🔍 駕駛員審查檢查點                                      │
│  請檢查生成的文檔內容，確認品質後：                      │
│                                                          │
│  ✅ 批准: /task-review approve                           │
│  🔄 修改: /task-review revise                            │
│  ⏸️ 暫停: /task-review pause                             │
│                                                          │
└──────────────────────────────────────────────────────────┘

EOF
        fi
    fi

    # 檢查是否為 VibeCoding 範本更新
    if [[ "$FILE_PATH" == *"VibeCoding_Workflow_Templates"* ]]; then
        log "🎨 VibeCoding 範本更新: $FILE_PATH"

        # 如果 TaskMaster 已初始化，可能需要重新評估任務
        if [ -f "$CLAUDE_DIR/taskmaster-data/project.json" ]; then
            log "🔄 範本更新，可能需要重新評估任務"
        fi
    fi

    # tier-2 contract 文件：自動更新 last-synced-with / synced-at frontmatter
    # 守門：避免 hook 自身觸發遞迴
    if [[ "$FILE_PATH" == *"docs/2-contracts/"* ]] && [ -z "${FRONTMATTER_AUTO_UPDATE:-}" ] && [ -f "$FILE_PATH" ]; then
        if head -1 "$FILE_PATH" | grep -q "^---$"; then
            CURRENT_SHA=$(cd "$PROJECT_ROOT" && git rev-parse HEAD 2>/dev/null || echo "no-git")
            CURRENT_DATE=$(date '+%Y-%m-%d')

            export FRONTMATTER_AUTO_UPDATE=1
            # in-place 更新 frontmatter 內的兩個欄位（若存在）
            if grep -q "^last-synced-with:" "$FILE_PATH"; then
                sed -i.bak "s|^last-synced-with:.*|last-synced-with: $CURRENT_SHA|" "$FILE_PATH"
            fi
            if grep -q "^synced-at:" "$FILE_PATH"; then
                sed -i.bak "s|^synced-at:.*|synced-at: $CURRENT_DATE|" "$FILE_PATH"
            fi
            rm -f "${FILE_PATH}.bak"
            unset FRONTMATTER_AUTO_UPDATE
            log "🔄 Auto-updated contract frontmatter: $FILE_PATH (sha=$CURRENT_SHA)"
        fi
    fi
fi

# 檢查是否為 WBS 檔案更新
if [[ "$FILE_PATH" == *"taskmaster-data/wbs.md"* ]]; then
    log "📋 WBS 任務清單已更新: $FILE_PATH"

    # 記錄 WBS 更新歷史
    WBS_LOG="$CLAUDE_DIR/taskmaster-data/wbs-history.log"
    mkdir -p "$CLAUDE_DIR/taskmaster-data" 2>/dev/null
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WBS 更新" >> "$WBS_LOG"

    cat << EOF

┌──────────────────────────────────────────────────────────┐
│  📋 WBS 任務清單已同步                                    │
│                                                          │
│  檔案: .claude/taskmaster-data/wbs.md                    │
│  時間: $(date '+%Y-%m-%d %H:%M:%S')                     │
│                                                          │
│  📊 /task-status  查看最新狀態                            │
│  ➡️  /task-next    取得下一個任務                          │
└──────────────────────────────────────────────────────────┘

EOF
fi

# 檢查是否為 TaskMaster 核心檔案更新
if [[ "$FILE_PATH" == *".claude/taskmaster"* ]] && [[ "$FILE_PATH" != *"taskmaster-data"* ]]; then
    log "🔧 TaskMaster 核心檔案更新: $FILE_PATH"

    # 可以在這裡加入核心檔案更新後的處理邏輯
    # 例如：重新載入配置、驗證系統狀態等
fi

# 檢查是否為 hooks 配置更新
if [[ "$FILE_PATH" == *"hooks-config.json"* ]] || [[ "$FILE_PATH" == *"settings.local.json"* ]]; then
    log "⚙️ Hooks 配置檔案更新: $FILE_PATH"

    # 可以在這裡加入配置更新後的處理邏輯
fi

log "✅ Post Write Hook 處理完成"
exit 0