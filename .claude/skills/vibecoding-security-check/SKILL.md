---
name: vibecoding-security-check
description: Run a security checklist covering authn/authz, input validation, secrets, dependencies. Triggers on 'security check', 'OWASP review', '安全檢查', 'pre-launch security'.
template-ref: VibeCoding_Workflow_Templates/3-process/PROC-0004-security-readiness-checklist.md
stability-tier: 3-process
origin: migrated-from-output-style
---

> **Template reference:** `VibeCoding_Workflow_Templates/3-process/PROC-0004-security-readiness-checklist.md`
> **Stability tier:** `3-process` — read tier README for usage policy.
> Load the referenced template for the canonical structure; this skill provides the generation procedure.


# 指令 (你是安全工程師)

以 OWASP Top 10、隱私法規 (GDPR/CCPA)、生產環境最佳實踐為基準,輸出全面的安全與上線檢查清單。所有項目必須可驗證、可追蹤。

## 交付結構

### 1. 安全檢查總覽

```markdown
## 安全檢查報告

**專案名稱**: [專案名稱]
**審查日期**: 2025-10-13
**審查者**: [安全工程師名稱]
**環境**: Staging / Production

**風險等級分佈**:
- 🔴 高風險 (Critical): 0 項
- 🟠 中風險 (High): 2 項
- 🟡 低風險 (Medium): 5 項
- 🟢 資訊 (Low): 3 項

**整體評估**: ✅ 可以上線 / ⚠️ 需修正後上線 / 🔴 不可上線

**必修項目 (Blockers)**:
- 🔴 [OWASP-A01] 修正 SQL 注入漏洞
- 🟠 [OWASP-A02] 實作 API Rate Limiting

**建議項目 (Nice-to-Have)**:
- 🟡 [SECURITY-01] 啟用 HTTPS Strict Transport Security (HSTS)
- 🟡 [MONITORING-01] 增加異常登入告警
```

### 2. OWASP Top 10 (2021) 檢查

#### A01:2021 - Broken Access Control (存取控制失效)

```markdown
### A01 - 存取控制失效

- [ ] **認證機制**
  - [ ] 使用行業標準認證 (OAuth 2.0, OpenID Connect, SAML)
  - [ ] 密碼複雜度要求 (最少 8 字元,含大小寫+數字+特殊符號)
  - [ ] 密碼使用強哈希演算法 (bcrypt/Argon2,禁止 MD5/SHA1)
  - [ ] 實作帳號鎖定機制 (連續 5 次失敗鎖定 15 分鐘)
  - [ ] 實作多因素認證 (MFA) 或至少提供選項

- [ ] **授權檢查**
  - [ ] 所有 API 端點都有授權檢查 (不依賴前端隱藏)
  - [ ] 使用基於角色/屬性的存取控制 (RBAC/ABAC)
  - [ ] 驗證資源所有權 (用戶只能存取自己的資源)
  - [ ] API 返回數據前進行權限過濾
  - [ ] 防止水平越權 (用戶 A 不能存取用戶 B 的資源)
  - [ ] 防止垂直越權 (普通用戶不能存取管理功能)

**測試案例**:
```bash
# 測試水平越權
# 1. 用戶 A 登入,獲取 token_A
# 2. 嘗試用 token_A 存取用戶 B 的訂單
curl -H "Authorization: Bearer $TOKEN_A" \
     https://api.example.com/orders/user_B_order_id

# 預期: 403 Forbidden 或 404 Not Found
# ❌ 如果返回 200 且有用戶 B 的數據 = 水平越權漏洞
```
```

#### A02:2021 - Cryptographic Failures (加密機制失效)

```markdown
### A02 - 加密機制失效

- [ ] **傳輸加密**
  - [ ] 所有端點強制使用 HTTPS (HTTP 自動重定向到 HTTPS)
  - [ ] TLS 版本 ≥ 1.2 (禁用 TLS 1.0/1.1)
  - [ ] 使用強加密套件 (禁用 RC4, DES, 3DES)
  - [ ] 配置 HSTS Header (`Strict-Transport-Security: max-age=31536000; includeSubDomains`)
  - [ ] 證書有效且未過期

- [ ] **存儲加密**
  - [ ] 敏感數據加密存儲 (密碼、信用卡、身分證號等)
  - [ ] 使用行業標準加密算法 (AES-256, RSA-2048+)
  - [ ] 密鑰管理機制 (使用 KMS,如 AWS KMS, Azure Key Vault)
  - [ ] 密鑰輪換策略 (至少每年輪換一次)
  - [ ] 禁止硬編碼密鑰/密碼在代碼中

- [ ] **敏感資訊保護**
  - [ ] PII (個人識別資訊) 最小化收集
  - [ ] 敏感欄位遮罩顯示 (信用卡只顯示後 4 碼)
  - [ ] 日誌中不記錄敏感資訊 (密碼、信用卡、Token)
  - [ ] 數據庫備份加密

**檢查方式**:
```bash
# 檢查 HTTPS 配置
openssl s_client -connect api.example.com:443 -tls1_2

# 檢查 HSTS Header
curl -I https://api.example.com | grep -i strict-transport-security

# 檢查是否有硬編碼密鑰
grep -r "password.*=.*" src/
grep -r "api[_-]key.*=.*" src/
```
```

#### A03:2021 - Injection (注入攻擊)

```markdown
### A03 - 注入攻擊

- [ ] **SQL 注入防護**
  - [ ] 所有數據庫查詢使用參數化查詢/Prepared Statement
  - [ ] 禁止字串拼接 SQL
  - [ ] 使用 ORM 的安全 API
  - [ ] 最小權限原則 (數據庫用戶只有必要權限,禁止 root/sa)
  - [ ] 輸入驗證 (白名單優於黑名單)

**反例與正例**:
```typescript
// ❌ SQL 注入漏洞
const sql = `SELECT * FROM users WHERE username = '${username}'`;
db.query(sql);
// 攻擊: username = "admin' OR '1'='1"

// ✅ 參數化查詢
const sql = 'SELECT * FROM users WHERE username = $1';
db.query(sql, [username]);

// ✅ ORM 安全 API
await userRepo.findOne({ where: { username } });
```

- [ ] **NoSQL 注入防護**
  - [ ] 輸入類型驗證 (MongoDB 防範 `$where`, `$ne` 注入)
  - [ ] 使用 Schema 驗證

```typescript
// ❌ NoSQL 注入
db.users.find({ username: req.body.username });
// 攻擊: { "username": { "$ne": null } } 返回所有用戶

// ✅ 類型驗證
if (typeof req.body.username !== 'string') {
  throw new ValidationError('username must be string');
}
db.users.find({ username: req.body.username });
```

- [ ] **命令注入防護**
  - [ ] 避免調用 shell 命令 (使用程式庫替代 `exec`, `system`)
  - [ ] 必須調用時使用白名單驗證參數
  - [ ] 禁止用戶輸入直接進入命令

- [ ] **LDAP/XML 注入防護**
  - [ ] 使用安全的 XML 解析器 (禁用外部實體)
  - [ ] LDAP 查詢使用轉義函式
```

#### A04:2021 - Insecure Design (不安全設計)

```markdown
### A04 - 不安全設計

- [ ] **威脅模型分析**
  - [ ] 已識別核心資產 (用戶數據、交易記錄、API 密鑰)
  - [ ] 已繪製數據流圖 (DFD)
  - [ ] 已識別信任邊界
  - [ ] 已列舉威脅 (使用 STRIDE 模型)
    - Spoofing (偽裝)
    - Tampering (篡改)
    - Repudiation (否認)
    - Information Disclosure (資訊洩露)
    - Denial of Service (阻斷服務)
    - Elevation of Privilege (權限提升)

- [ ] **安全設計原則**
  - [ ] 最小權限原則 (Principle of Least Privilege)
  - [ ] 深度防禦 (Defense in Depth)
  - [ ] 預設安全 (Secure by Default)
  - [ ] 失敗安全 (Fail Securely)
  - [ ] 職責分離 (Separation of Duties)

- [ ] **業務邏輯安全**
  - [ ] 防止重複提交 (訂單、支付使用冪等性 Token)
  - [ ] 金額驗證在服務端 (不信任前端傳來的金額)
  - [ ] 庫存檢查使用樂觀鎖或悲觀鎖
  - [ ] 防止競態條件 (Race Condition)
  - [ ] 實作交易超時機制
```

#### A05:2021 - Security Misconfiguration (安全配置缺陷)

```markdown
### A05 - 安全配置缺陷

- [ ] **框架與函式庫安全**
  - [ ] 所有依賴更新到最新穩定版本
  - [ ] 定期掃描漏洞 (`npm audit`, `Snyk`, `Dependabot`)
  - [ ] 移除未使用的依賴
  - [ ] 禁用不必要的功能與服務

- [ ] **錯誤處理**
  - [ ] 生產環境不返回詳細錯誤堆棧
  - [ ] 使用統一錯誤響應格式
  - [ ] 錯誤訊息不洩露系統細節

```typescript
// ❌ 洩露系統資訊
res.status(500).json({
  error: error.stack,  // 洩露文件路徑、函式名
  database: 'PostgreSQL 14.2',
  server: 'AWS EC2 t3.medium'
});

// ✅ 安全的錯誤響應
res.status(500).json({
  error: {
    code: 'INTERNAL_ERROR',
    message: '服務暫時不可用,請稍後重試',
    traceId: uuid()  // 用於內部日誌查詢
  }
});
```

- [ ] **HTTP 安全標頭**
  - [ ] `X-Content-Type-Options: nosniff`
  - [ ] `X-Frame-Options: DENY` 或 `SAMEORIGIN`
  - [ ] `Content-Security-Policy` (CSP)
  - [ ] `Referrer-Policy: strict-origin-when-cross-origin`
  - [ ] `Permissions-Policy` (Feature Policy)

```nginx
# Nginx 配置範例
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

- [ ] **雲端安全配置**
  - [ ] S3 Bucket 不公開可讀 (除非有明確需求)
  - [ ] 數據庫不暴露到公網
  - [ ] 安全組規則最小化 (僅開放必要端口)
  - [ ] 啟用雲端平台的審計日誌 (AWS CloudTrail, Azure Activity Log)
```

#### A06:2021 - Vulnerable Components (易受攻擊的組件)

```markdown
### A06 - 易受攻擊的組件

- [ ] **依賴管理**
  - [ ] 所有依賴版本鎖定 (`package-lock.json`, `yarn.lock`)
  - [ ] 定期更新依賴 (至少每季度一次)
  - [ ] 自動化漏洞掃描 (CI/CD 集成 `npm audit`, `Snyk`)
  - [ ] 訂閱安全通告 (GitHub Security Advisories)

**自動化檢查**:
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

- [ ] **移除測試/除錯工具**
  - [ ] 生產環境禁用 Swagger UI (或加上認證)
  - [ ] 移除測試端點 (`/debug`, `/test`)
  - [ ] 禁用 GraphQL Playground (生產環境)
```

#### A07:2021 - Identification and Authentication Failures (識別與認證失效)

```markdown
### A07 - 識別與認證失效

- [ ] **Session 管理**
  - [ ] Session ID 足夠長且隨機 (至少 128 bits)
  - [ ] Session ID 使用 HttpOnly Cookie 存儲
  - [ ] Session ID 使用 Secure 標記 (僅 HTTPS 傳輸)
  - [ ] Session ID 使用 SameSite 標記 (防 CSRF)
  - [ ] Session 超時機制 (閒置 30 分鐘自動登出)
  - [ ] 登出時銷毀 Session

```typescript
// ✅ 安全的 Cookie 配置
res.cookie('sessionId', sessionId, {
  httpOnly: true,     // 防止 XSS 讀取
  secure: true,       // 僅 HTTPS
  sameSite: 'strict', // 防 CSRF
  maxAge: 1800000,    // 30 分鐘
  path: '/',
  domain: '.example.com'
});
```

- [ ] **JWT 最佳實踐**
  - [ ] 使用強簽名算法 (HS256, RS256,禁止 `none`)
  - [ ] Token 包含過期時間 (`exp` claim)
  - [ ] Token 生命週期短 (Access Token ≤ 15分鐘)
  - [ ] 實作 Refresh Token 機制
  - [ ] Token 存儲在 HttpOnly Cookie 或記憶體 (避免 LocalStorage)
  - [ ] 實作 Token 撤銷機制 (黑名單或版本號)

- [ ] **防暴力破解**
  - [ ] 實作 Rate Limiting (登入端點每分鐘最多 5 次)
  - [ ] 帳號鎖定機制
  - [ ] CAPTCHA (連續失敗後顯示)
  - [ ] 漸進式延遲 (每次失敗增加響應延遲)
```

#### A08:2021 - Software and Data Integrity Failures (軟體與數據完整性失效)

```markdown
### A08 - 軟體與數據完整性失效

- [ ] **CI/CD 安全**
  - [ ] Pipeline 需要審批才能部署生產
  - [ ] 使用程式碼簽名
  - [ ] Docker Image 掃描漏洞
  - [ ] 使用官方 Base Image
  - [ ] Image Tag 使用具體版本而非 `latest`

- [ ] **數據完整性**
  - [ ] 關鍵操作記錄審計日誌 (誰、何時、做了什麼)
  - [ ] 敏感操作需二次確認
  - [ ] 資料修改使用樂觀鎖 (版本號)
  - [ ] 資料庫變更使用遷移腳本 (Flyway/Liquibase)
```

#### A09:2021 - Security Logging and Monitoring Failures (安全日誌與監控失效)

```markdown
### A09 - 安全日誌與監控失效

- [ ] **日誌記錄**
  - [ ] 記錄所有認證嘗試 (成功與失敗)
  - [ ] 記錄授權失敗
  - [ ] 記錄輸入驗證失敗
  - [ ] 記錄關鍵業務操作 (訂單、支付、退款)
  - [ ] 日誌包含時間戳、用戶ID、IP、操作類型、結果
  - [ ] 日誌集中管理 (ELK, Splunk, CloudWatch)

**日誌範例**:
```json
{
  "timestamp": "2025-10-13T10:30:00Z",
  "level": "WARN",
  "event": "LOGIN_FAILED",
  "userId": null,
  "username": "admin",
  "ip": "203.0.113.45",
  "userAgent": "Mozilla/5.0...",
  "reason": "INVALID_PASSWORD",
  "attemptCount": 3,
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
```

- [ ] **監控告警**
  - [ ] 異常登入告警 (異地登入、暴力破解)
  - [ ] 權限提升告警
  - [ ] 大量 4xx/5xx 錯誤告警
  - [ ] API 響應時間告警
  - [ ] 數據庫慢查詢告警
  - [ ] 磁盤/記憶體使用率告警

- [ ] **事件響應**
  - [ ] 安全事件響應流程文檔
  - [ ] 指定安全事件聯繫人
  - [ ] 定期演練事件響應流程
```

#### A10:2021 - Server-Side Request Forgery (SSRF) (服務端請求偽造)

```markdown
### A10 - SSRF

- [ ] **防護措施**
  - [ ] 白名單允許的域名/IP
  - [ ] 禁止訪問內網地址 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
  - [ ] 禁止訪問本地地址 (127.0.0.1, localhost, 169.254.169.254)
  - [ ] URL Schema 白名單 (僅允許 http/https)

```typescript
// ✅ SSRF 防護
const ALLOWED_DOMAINS = ['api.trusted-partner.com'];
const BLOCKED_RANGES = [
  '127.0.0.1',
  '169.254.169.254', // AWS metadata
  '10.0.0.0/8',
  '172.16.0.0/12',
  '192.168.0.0/16'
];

async function fetchUrl(url: string): Promise<any> {
  const parsed = new URL(url);

  // Schema 檢查
  if (!['http:', 'https:'].includes(parsed.protocol)) {
    throw new SecurityError('不允許的 URL Schema');
  }

  // 域名白名單檢查
  if (!ALLOWED_DOMAINS.includes(parsed.hostname)) {
    throw new SecurityError('不允許的域名');
  }

  // 解析 IP 並檢查是否在黑名單
  const ip = await dns.resolve4(parsed.hostname);
  if (isBlockedIP(ip[0])) {
    throw new SecurityError('不允許訪問的 IP');
  }

  return fetch(url);
}
```
```

### 3. 隱私與合規檢查

```markdown
## 隱私保護 (GDPR/CCPA/PDPA)

- [ ] **數據最小化**
  - [ ] 只收集必要的個人資訊
  - [ ] 定期清理不再需要的數據

- [ ] **用戶權利**
  - [ ] 提供數據查閱功能 (用戶可查看自己的所有數據)
  - [ ] 提供數據刪除功能 (Right to be Forgotten)
  - [ ] 提供數據導出功能 (數據可攜權)
  - [ ] 提供同意撤回功能

- [ ] **同意管理**
  - [ ] 隱私政策清晰易懂
  - [ ] Cookie 使用需用戶同意
  - [ ] 行銷郵件需明確同意 (Opt-in,非 Opt-out)

- [ ] **數據處理記錄**
  - [ ] 記錄數據處理活動 (ROPA - Record of Processing Activities)
  - [ ] 數據保留策略 (多久後自動刪除)
  - [ ] 第三方數據處理協議 (DPA)
```

### 4. 生產環境就緒檢查

```markdown
## 部署與運維

- [ ] **基礎設施**
  - [ ] 高可用部署 (至少 2 個可用區)
  - [ ] 負載均衡配置正確
  - [ ] 自動擴展配置 (HPA)
  - [ ] 健康檢查端點 (`/health`, `/ready`)

- [ ] **備份與災難恢復**
  - [ ] 數據庫自動備份 (每日全量 + 增量)
  - [ ] 備份異地存儲
  - [ ] 測試備份恢復流程 (至少每季度一次)
  - [ ] RTO/RPO 目標明確

- [ ] **監控與告警**
  - [ ] APM 工具配置 (New Relic, Datadog, Prometheus)
  - [ ] 日誌集中收集 (ELK, CloudWatch)
  - [ ] 告警規則配置
  - [ ] On-call 輪值機制

- [ ] **文檔**
  - [ ] Runbook (部署、回滾、故障排除)
  - [ ] API 文檔 (OpenAPI/Swagger)
  - [ ] 架構圖 (C4 Model)
  - [ ] 安全事件響應手冊
```

## 安全檢查工具推薦

| 類別 | 工具 | 用途 |
|------|------|------|
| SAST | SonarQube, ESLint | 靜態代碼分析 |
| DAST | OWASP ZAP, Burp Suite | 動態應用安全測試 |
| SCA | Snyk, Dependabot, npm audit | 依賴漏洞掃描 |
| Secret Scan | git-secrets, TruffleHog | 密鑰洩露檢測 |
| Container Scan | Trivy, Clair | Docker 鏡像掃描 |

## 蘇格拉底檢核

1. **如果攻擊者取得一個普通用戶帳號,他能做什麼?**
   - 能存取其他用戶的數據嗎?
   - 能提升權限嗎?

2. **如果數據庫被攻破,敏感資訊會洩露嗎?**
   - 密碼是否已加密?
   - 信用卡號是否已加密?

3. **系統在壓力下會優雅降級還是崩潰?**
   - 有 Rate Limiting 嗎?
   - 有熔斷機制嗎?

4. **日誌是否足以追查安全事件?**
   - 能定位是誰在何時做了什麼嗎?
   - 日誌是否被妥善保護,無法被攻擊者刪除?

5. **第三方依賴可信嗎?**
   - 有定期更新嗎?
   - 有漏洞掃描嗎?

## 輸出格式

- 使用 Markdown 格式
- 遵循 VibeCoding_Workflow_Templates/3-process/PROC-0004-security-readiness-checklist.md 結構
- 使用 🔴 🟠 🟡 🟢 標示風險等級

## 審查清單

- [ ] 所有 OWASP Top 10 項目已檢查
- [ ] 認證授權機制安全
- [ ] 敏感資訊加密存儲與傳輸
- [ ] 輸入驗證防注入攻擊
- [ ] Rate Limiting 防暴力破解
- [ ] HTTP 安全標頭配置
- [ ] 依賴無高危漏洞
- [ ] 日誌監控告警完整
- [ ] 備份恢復流程已測試
- [ ] 隱私政策合規

## 關聯文件

- **Code Review**: PROC-0003-code-review-checklist.md (代碼層面安全)
- **API 設計**: 05-api-contract-spec.md (API 安全)
- **部署指南**: VibeCoding_Workflow_Templates/3-process/PROC-0005-deployment-runbook.template.md


**記住**: 安全是持續的過程,不是一次性檢查。定期審查、更新依賴、演練事件響應,讓系統持續保持安全狀態。
