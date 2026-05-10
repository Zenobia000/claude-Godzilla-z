# 前端架構規範 - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/已批准

---

## 第 1 部分: 架構目標

| 維度 | 目標 | 衡量指標 |
| :--- | :--- | :--- |
| **效能** | 載入速度與回應速度 | LCP, FID, CLS, TTI |
| **可用性** | 使用者完成目標的難易度 | 任務成功率、SUS 分數 |
| **可維護性** | 團隊迭代效率 | 複雜度、覆蓋率、技術債 |
| **可靠性** | 各環境穩定運行 | 錯誤率、崩潰率、MTBF |

---

## 第 2 部分: 系統化分層

```
用戶感知層    -- 視覺元件、樣式系統、動畫
互動邏輯層    -- 事件處理、表單驗證、路由
狀態管理層    -- 全局狀態、本地狀態、Server State、URL State
資料通訊層    -- API 客戶端、資料轉換、快取
基礎設施層    -- 建置工具、測試框架、監控、CI/CD
```

### 各層職責與技術選型

| 層級 | 職責 | 技術選項 |
| :--- | :--- | :--- |
| 感知層 | 渲染 UI、視覺一致性 | [React/Vue/Svelte] + [CSS Modules/Tailwind/Styled] |
| 互動層 | 使用者輸入、路由導航 | [React Router/Vue Router] + [React Hook Form/Formik] |
| 狀態層 | 狀態管理 | [Zustand/Redux/Pinia] + [React Query/SWR] |
| 通訊層 | API 呼叫與快取 | [Axios/fetch] + [React Query/Apollo] |
| 基礎設施 | 建置與品質 | [Vite/webpack] + [Jest/Vitest] + [Playwright] |

---

## 第 3 部分: 設計系統

### 設計令牌 (Design Tokens)

| 類別 | 定義位置 | 範例 |
| :--- | :--- | :--- |
| 色彩 | `tokens/colors` | primary, secondary, error, warning |
| 字體 | `tokens/typography` | heading, body, caption |
| 間距 | `tokens/spacing` | xs(4), sm(8), md(16), lg(24), xl(32) |
| 陰影 | `tokens/shadows` | sm, md, lg |
| 圓角 | `tokens/radius` | sm(4), md(8), lg(16), full |

### 元件分層 (Atomic Design)

```
原子 (Atoms)      → Button, Input, Icon, Badge
分子 (Molecules)  → SearchBar, FormField, Card
組織 (Organisms)  → Header, Sidebar, DataTable
模板 (Templates)  → DashboardLayout, AuthLayout
頁面 (Pages)      → HomePage, LoginPage, Dashboard
```

---

## 第 4 部分: 效能策略

### Core Web Vitals 目標

| 指標 | 目標 | 優化策略 |
| :--- | :--- | :--- |
| LCP | < 2.5s | 圖片優化、預載關鍵資源、SSR/SSG |
| FID | < 100ms | Code Splitting、Web Worker、減少主執行緒阻塞 |
| CLS | < 0.1 | 圖片/影片設定尺寸、避免動態插入內容 |

### 載入優化
- **Code Splitting**: 路由級 + 元件級懶載入
- **資源優化**: 圖片壓縮(WebP/AVIF)、字型子集化、Tree Shaking
- **快取策略**: Service Worker、HTTP Cache、API 快取

### 執行時優化
- **渲染**: 虛擬列表、防抖/節流、memo/useMemo
- **狀態**: 避免不必要的重渲染、正規化狀態結構

---

## 第 5 部分: 可用性與無障礙

### 響應式設計斷點

| 名稱 | 寬度 | 目標裝置 |
| :--- | :--- | :--- |
| xs | < 576px | 手機 (直向) |
| sm | >= 576px | 手機 (橫向) |
| md | >= 768px | 平板 |
| lg | >= 992px | 筆電 |
| xl | >= 1200px | 桌面 |

### 無障礙 (A11y) 要求
- WCAG 2.1 AA 等級
- 語義化 HTML、ARIA 標籤
- 鍵盤導航完整支援
- 色彩對比度 >= 4.5:1
- 焦點管理與螢幕閱讀器支援

### 國際化 (i18n)
- 工具: [react-intl / vue-i18n / next-intl]
- 日期/數字格式化使用 Intl API
- RTL 佈局支援 (如需要)

---

## 第 6 部分: 工程化實踐

### 專案結構

```
src/
├── assets/          # 靜態資源
├── components/      # 共用元件 (Atomic Design)
│   ├── atoms/
│   ├── molecules/
│   └── organisms/
├── features/        # 功能模組 (按功能組織)
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── types/
├── hooks/           # 共用 Hooks
├── layouts/         # 佈局元件
├── pages/           # 頁面路由
├── services/        # API 客戶端
├── stores/          # 狀態管理
├── styles/          # 全域樣式/Design Tokens
├── types/           # 型別定義
└── utils/           # 工具函式
```

### 程式碼品質
- Linter: ESLint + Prettier
- 型別: TypeScript strict mode
- 提交: Conventional Commits + commitlint
- 分支: Git Flow / Trunk-Based

### 測試策略

| 類型 | 工具 | 覆蓋率目標 | 測試內容 |
| :--- | :--- | :--- | :--- |
| 單元 | Vitest/Jest | 80%+ | 工具函式、Hooks、Store |
| 元件 | Testing Library | 核心元件 | 渲染、互動、狀態 |
| E2E | Playwright | 關鍵流程 | 使用者旅程 |
| 視覺 | Storybook | 設計系統 | 元件外觀回歸 |

---

## 第 7 部分: 前後端協作

### API 通訊規範
- 統一使用 API Client 封裝 (不直接呼叫 fetch)
- 請求/回應型別自動生成 (從 OpenAPI)
- 統一錯誤處理 + 使用者提示

### 認證與授權
- Token 儲存: httpOnly Cookie (優先) / Memory
- 自動重整 Token 機制
- 路由守衛 (認證/角色)

---

## 第 8 部分: 監控與安全

### 前端監控
- 效能: Core Web Vitals 收集 (web-vitals)
- 錯誤: Sentry / 全局錯誤邊界
- 行為: 頁面瀏覽、點擊追蹤

### 前端安全
- [ ] XSS 防護 (框架自動跳脫 + CSP)
- [ ] CSRF 防護 (SameSite Cookie / Token)
- [ ] 敏感資料不存 localStorage
- [ ] 依賴掃描 (npm audit / Snyk)
- [ ] Subresource Integrity (CDN 資源)

---

## 第 9 部分: 開發檢查清單

### 新功能上線前
- [ ] TypeScript 無錯誤
- [ ] 單元/元件測試通過
- [ ] 響應式設計驗證
- [ ] 無障礙基本檢查
- [ ] 效能預算未超標
- [ ] 安全檢查清單通過
- [ ] Code Review 通過
