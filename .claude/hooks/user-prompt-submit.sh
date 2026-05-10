#!/bin/bash

# TaskMaster User Prompt Submit Hook
# 當用戶提交 prompt 時檢查是否包含 TaskMaster 相關命令

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

# 解析用戶輸入
if command -v jq >/dev/null 2>&1; then
    USER_INPUT=$(echo "$INPUT" | jq -r '.content // .message // ""')
else
    USER_INPUT=""
fi

log "🪝 TaskMaster User Prompt Submit Hook 觸發"

# 檢查用戶輸入是否包含 TaskMaster 相關命令
if [[ "$USER_INPUT" == *"/task-"* ]]; then
    log "🎯 偵測到 TaskMaster 命令: $USER_INPUT"

    # 解析命令類型
    if [[ "$USER_INPUT" == *"/task-init"* ]]; then
        log "🚀 偵測到專案初始化命令"

        # 確保 TaskMaster 系統準備就緒
        if [ ! -d "$CLAUDE_DIR/taskmaster-data" ]; then
            log "📁 創建 TaskMaster 資料目錄"
            mkdir -p "$CLAUDE_DIR/taskmaster-data"
        fi

        # 觸發初始化準備
        if [ -f "$CLAUDE_DIR/taskmaster.js" ]; then
            log "🔗 調用 TaskMaster 初始化準備"
            cd "$PROJECT_ROOT"
            node "$CLAUDE_DIR/taskmaster.js" --hook-trigger=user-prompt --message="$USER_INPUT"
        fi

    elif [[ "$USER_INPUT" == *"/task-status"* ]]; then
        log "📊 偵測到狀態查詢命令"

    elif [[ "$USER_INPUT" == *"/task-next"* ]]; then
        log "➡️ 偵測到下個任務命令"

    elif [[ "$USER_INPUT" == *"/task-review"* ]]; then
        log "🔍 偵測到文檔審查命令"
    fi

    exit 0
fi

# 檢查是否包含文檔相關操作
if [[ "$USER_INPUT" == *"docs/"* ]] || [[ "$USER_INPUT" == *".md"* ]]; then
    log "📄 偵測到文檔相關操作"

    # 如果 TaskMaster 已初始化，檢查是否需要更新狀態
    if [ -f "$CLAUDE_DIR/taskmaster-data/project.json" ]; then
        log "🔄 可能需要更新 TaskMaster 狀態"

        # 觸發狀態檢查
        if [ -f "$CLAUDE_DIR/taskmaster.js" ]; then
            cd "$PROJECT_ROOT"
            node "$CLAUDE_DIR/taskmaster.js" --hook-trigger=document-related --message="$USER_INPUT"
        fi
    fi
fi

log "✅ User Prompt Submit Hook 處理完成"
exit 0