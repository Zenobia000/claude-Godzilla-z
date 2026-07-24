# 效能優化

## 模型選擇策略

| 模型 | 適用場景 |
| :--- | :--- |
| **Haiku 4.5** | 輕量 agent、高頻呼叫、worker agent |
| **Sonnet 4.6** | 主要開發、多 agent 編排、複雜編碼 |
| **Opus 4.6** | 架構決策、深度推理、研究分析 |

## Context Window 管理

避免在最後 20% context 中進行：
- 大規模重構
- 跨多檔案的功能實作
- 複雜互動除錯

低 context 敏感任務：
- 單檔案編輯
- 獨立工具函式
- 文檔更新
- 簡單 bug 修復

## 建置疑難排解

建置失敗時：
1. 載入 sunnydata-debugging skill
2. 分析錯誤訊息
3. 增量修復
4. 每次修復後驗證

## 平行任務處理

面對 2+ 個獨立任務時，載入 sunnydata-parallel-agents skill 進行平行派發。
