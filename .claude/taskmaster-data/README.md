# TaskMaster Runtime（已退役）

舊版 TaskMaster 以 Hook、WBS、session snapshot 與 timelog 維護另一套專案狀態。這個流程不再是模板的執行期依賴。

目前替代方式：

- 需求與優先序：核准的 Excel／PRD／WBS 文件
- 當前工作：Claude Code 原生 Task list
- 跨 session 工作：明確的 issue、規格、ADR 或版本控制紀錄
- 完成判定：`/verify` 產生的實際測試與證據

`.session-start`、`.session-snapshot`、`timelog.jsonl` 若仍存在，只是本機舊資料；Git 會忽略它們，StatusLine 與 Hooks 不會讀寫。
