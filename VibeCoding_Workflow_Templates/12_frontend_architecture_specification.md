# 前端架構規範 - [專案名稱]

> **版本:** v2.0 (MECE 重切) | **更新:** 2026-05-26 | **狀態:** 草稿/已批准
> **相關文檔:** [前端資訊架構 (17)](./17_frontend_information_architecture_template.md)
>
> **MECE 邊界**：本文件**只談技術視角**（stack / 分層 / 量化指標 / 工程化）。
> 使用者視角（頁面職責、旅程、導航、路由內容）全部在 **17_frontend_information_architecture**。
>
> | 你想找的 | 看這份 |
> |---|---|
> | 用什麼框架、怎麼分層 | 12（本檔）§2 |
> | 設計令牌、元件分層（Atoms→Templates）| 12（本檔）§3 |
> | LCP / FID / CLS 數字目標 | 12（本檔）§4 |
> | 響應式斷點、a11y 標準 | 12（本檔）§5 |
> | 專案 file 組織、測試框架 | 12（本檔）§6 |
> | API client 技術選型 | 12（本檔）§7 |
> | 哪些**頁面**存在、頁面職責 | **17** §3 §6 |
> | 使用者旅程、導航結構 | **17** §4 §5 |
> | URL 命名規則、路由表 | **17** §7 |

---

## 第 1 部分: 架構目標（量化）

| 維度 | 目標 | 衡量指標 |
| :--- | :--- | :--- |
| **效能** | 載入速度與回應速度 | LCP, FID/INP, CLS, TTI |
| **技術可用性** | 各裝置/輔助技術可達 | 響應式覆蓋率、a11y 通過率 |
| **可維護性** | 團隊迭代效率 | 複雜度、覆蓋率、技術債 |
| **可靠性** | 各環境穩定運行 | 錯誤率、崩潰率、MTBF |

> 「使用者完成目標的難易度」屬於 IA 視角（質化）→ 見 17 §2 §4。

---

## 第 2 部分: 系統化分層

```
用戶感知層    -- 視覺元件、樣式系統、動畫
互動邏輯層    -- 事件處理、表單驗證
狀態管理層    -- 全局狀態、本地狀態、Server State、URL State
資料通訊層    -- API 客戶端、資料轉換、快取
基礎設施層    -- 建置工具、測試框架、監控、CI/CD
```

### 各層職責與技術選型

| 層級 | 職責 | 技術選項 |
| :--- | :--- | :--- |
| 感知層 | 渲染 UI、視覺一致性 | [React/Vue/Svelte] + [CSS Modules/Tailwind/Styled] |
| 互動層 | 使用者輸入、表單驗證 | [React Hook Form/Formik] |
| 狀態層 | 全局/Server State/URL State | [Zustand/Redux/Pinia] + [React Query/SWR] |
| 通訊層 | API 呼叫與快取 | [Axios/fetch] + [React Query/Apollo] |
| 基礎設施 | 建置與品質 | [Vite/webpack] + [Vitest/Jest] + [Playwright] |

> 路由器（React Router / Vue Router）的**選型**列在這裡是必要的；但**具體有哪些路由、路由表、URL 命名**屬於 IA → 見 17 §7。

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

### 元件分層 (Atomic Design — Atoms → Templates 為止)

```
原子 (Atoms)      → Button, Input, Icon, Badge
分子 (Molecules)  → SearchBar, FormField, Card
組織 (Organisms)  → Header, Sidebar, DataTable
模板 (Templates)  → DashboardLayout, AuthLayout
```

> **Pages 不在這份文件**。Pages 是 IA 概念（內容容器 + 導航節點）→ 見 17 §3 「頁面總覽」、§6 「頁面規格」。
> 技術上 Pages 是 `Templates + 資料注入`；組成規則的描述在 17。

---

## 第 4 部分: 效能策略（量化）

### Core Web Vitals 目標

| 指標 | 目標 | 優化策略 |
| :--- | :--- | :--- |
| LCP | < 2.5s | 圖片優化、預載關鍵資源、SSR/SSG |
| INP (取代 FID) | < 200ms | Code Splitting、Web Worker、減少主執行緒阻塞 |
| CLS | < 0.1 | 圖片/影片設定尺寸、避免動態插入內容 |
| TTI | < 3s (4G) | 同上 |

> 質化的 UX 標準（簡化、認知負荷、每頁 1 個 CTA）→ 17 §2 §9。

### 載入優化
- **Code Splitting**: 路由級 + 元件級懶載入（哪些路由懶載 → 17 §7 路由表）
- **資源優化**: 圖片壓縮(WebP/AVIF)、字型子集化、Tree Shaking
- **快取策略**: Service Worker、HTTP Cache、API 快取

### 執行時優化
- **渲染**: 虛擬列表、防抖/節流、memo/useMemo
- **狀態**: 避免不必要的重渲染、正規化狀態結構

---

## 第 5 部分: 技術可用性（量化標準）

### 響應式設計斷點

| 名稱 | 寬度 | 目標裝置 |
| :--- | :--- | :--- |
| xs | < 576px | 手機 (直向) |
| sm | >= 576px | 手機 (橫向) |
| md | >= 768px | 平板 |
| lg | >= 992px | 筆電 |
| xl | >= 1200px | 桌面 |

### 無障礙 (A11y) 量化要求

- WCAG 2.2 AA 等級
- 語義化 HTML、ARIA 標籤
- 鍵盤導航完整支援
- 色彩對比度 >= 4.5:1 (一般文字) / >= 3:1 (大字)
- 焦點管理與螢幕閱讀器支援

### 國際化 (i18n) 工具

- 工具: [react-intl / vue-i18n / next-intl]
- 日期/數字格式化使用 Intl API
- RTL 佈局支援 (如需要)

---

## 第 6 部分: 工程化實踐

### 專案 file 組織

```
src/
├── assets/          # 靜態資源
├── components/      # 共用元件 (Atomic: Atoms/Molecules/Organisms)
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
├── layouts/         # Templates 級元件
├── pages/           # 頁面進入點 (路由內容定義 → 17 §7)
├── services/        # API 客戶端
├── stores/          # 狀態管理
├── styles/          # 全域樣式/Design Tokens
├── types/           # 型別定義
└── utils/           # 工具函式
```

> 這裡只描述 **檔案組織約定**。`pages/` 目錄下實際存在哪些 page 檔案、對應什麼路由、有什麼導航、傳什麼資料 — 全部在 17。

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
| E2E | Playwright | 關鍵流程 | 使用者旅程（旅程定義 → 17 §4）|
| 視覺 | Storybook | 設計系統 | 元件外觀回歸 |

---

## 第 7 部分: 前後端協作（技術面）

### API 通訊規範

- 統一使用 API Client 封裝 (不直接呼叫 fetch)
- 請求/回應型別自動生成 (從 OpenAPI)
- 統一錯誤處理 + 使用者提示

### 認證與授權（Token 機制）

- Token 儲存: httpOnly Cookie (優先) / Memory
- 自動重整 Token 機制
- **路由守衛實作**：機制在這（middleware / Higher-Order Route），**哪些路由需要哪些角色** → 17 §7 路由表的「認證」欄

---

## 第 8 部分: 監控與安全

### 前端監控

- 效能: Core Web Vitals 收集 (web-vitals lib)
- 錯誤: Sentry / 全局錯誤邊界
- 行為: 頁面瀏覽、點擊追蹤（事件 schema → 17 §4 旅程映射）

### 前端安全

- [ ] XSS 防護 (框架自動跳脫 + CSP)
- [ ] CSRF 防護 (SameSite Cookie / Token)
- [ ] 敏感資料不存 localStorage
- [ ] 依賴掃描 (npm audit / Snyk)
- [ ] Subresource Integrity (CDN 資源)

---

## 第 9 部分: 技術上線檢查清單

> IA / 可用性檢查清單在 **17 §9**。本清單只有技術項。

- [ ] TypeScript strict 無錯誤
- [ ] 單元/元件測試通過、覆蓋率 ≥ 80%
- [ ] 響應式覆蓋 §5 五個斷點
- [ ] WCAG 2.2 AA 自動檢測通過 (axe-core / Lighthouse)
- [ ] Core Web Vitals 達標 (§4 表格)
- [ ] 安全檢查清單 §8 通過
- [ ] Bundle size 預算未超
- [ ] Code Review 通過
