# 專案結構指南 - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD

---

## 設計原則

- **按功能組織**: 相關功能放一起 (非按類型分散)
- **明確職責**: 每個目錄單一職責
- **一致命名**: 目錄 `kebab-case`、Python `snake_case.py`、測試 `test_` 開頭
- **配置外部化**: 配置與程式碼分離
- **根目錄簡潔**: 原始碼放 `src/`，根目錄只放專案級檔案

---

## 頂層結構

```plaintext
[project-root]/
├── .github/              # CI/CD 工作流程
├── configs/              # 環境配置
├── docs/                 # 專案文檔、ADR
├── scripts/              # 開發/運維腳本
├── src/[app_name]/       # 應用程式原始碼
├── tests/                # 測試程式碼
├── .gitignore
├── pyproject.toml        # (或 package.json / Cargo.toml)
└── README.md
```

---

## 原始碼結構 (Clean Architecture)

```plaintext
src/[app_name]/
├── main.py                     # 入口點
├── core/                       # 跨功能共享 (config, security)
├── domains/                    # Domain Layer: 業務模型
│   └── [feature]/
│       ├── entities.py         # 業務實體
│       ├── aggregates.py       # 聚合根
│       └── exceptions.py       # 領域例外
├── application/                # Application Layer: 應用邏輯
│   └── [feature]/
│       ├── use_cases.py        # 用例/服務
│       ├── dtos.py             # 資料傳輸物件
│       └── validators.py       # 輸入驗證
└── infrastructure/             # Infrastructure Layer: 外部實現
    ├── web/                    # Controllers/Routers
    └── persistence/            # ORM models, Repository 實現
```

---

## 測試結構

```plaintext
tests/
├── conftest.py               # 全局 fixtures
├── unit/                     # 單元測試
├── integration/              # 整合測試
└── features/                 # 功能測試 (對應 src 結構)
    └── [feature]/
        ├── test_router.py
        └── test_service.py
```

---

## 文檔結構

```plaintext
docs/
├── adrs/                     # 架構決策記錄
├── design/                   # 設計文檔
└── images/                   # 文檔圖片
```

---

## 演進原則

- 本結構是起點，依專案發展調整
- 頂層結構的重大變更需 ADR 記錄
- 一致性比嚴格遵守特定模式更重要
