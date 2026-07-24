# 安全規範

## 每次 Commit 前必檢

- [ ] 無硬編碼秘密（API key、密碼、token）
- [ ] 所有使用者輸入已驗證
- [ ] SQL 注入防護（參數化查詢）
- [ ] XSS 防護（清理 HTML）
- [ ] CSRF 保護已啟用
- [ ] 認證/授權已驗證
- [ ] 速率限制已設定
- [ ] 錯誤訊息不洩露敏感資料

## 秘密管理

- 絕不在原始碼硬編碼秘密
- 使用環境變數或 secret manager
- 啟動時驗證必要秘密存在
- 輪換任何可能已暴露的秘密

## 依賴安全

- 提交 lock file（package-lock.json / yarn.lock / poetry.lock）
- 新增依賴前確認：活躍維護、無已知漏洞、授權相容
- 定期執行 `npm audit` / `pip audit` / `go vet`
- 不安裝來源不明的套件

## 安全事件回應

1. 立即停止
2. 載入 sunnydata-security skill 進行完整安全審查
3. 修復 CRITICAL 問題後才繼續
4. 輪換已暴露的秘密
5. 審查整個程式碼庫是否有類似問題
