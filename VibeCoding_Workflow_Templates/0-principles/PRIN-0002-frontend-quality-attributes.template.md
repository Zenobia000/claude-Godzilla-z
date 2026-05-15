---
id: PRIN-0002
title: "Frontend Quality Attributes"
status: draft
tier: 0-principles
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---
# Frontend Quality Attributes — `<PROJECT_NAME>`

> **Tier**: 0-principles — frontend performance, a11y, and monitoring quality bars

---

## 1. Architecture Goals

| Dimension | Goal | KPI |
| :--- | :--- | :--- |
| **Performance** | Load and response speed | LCP, FID, CLS, TTI |
| **Usability** | Difficulty of completing user goals | Task success rate, SUS score |
| **Maintainability** | Team iteration efficiency | Cyclomatic complexity, coverage, tech debt |
| **Reliability** | Stable across environments | Error rate, crash rate, MTBF |

---

## 2. Core Web Vitals Targets

| Metric | Target | Optimization Strategy |
| :--- | :--- | :--- |
| LCP | < 2.5s | Image optimization, preload critical resources, SSR/SSG |
| FID | < 100ms | Code splitting, Web Worker, reduce main-thread blocking |
| CLS | < 0.1 | Set image/video dimensions, avoid dynamic content insertion |

### Loading Optimization

- **Code Splitting**: route-level + component-level lazy loading
- **Asset Optimization**: image compression (WebP/AVIF), font subsetting, tree shaking
- **Caching Strategy**: Service Worker, HTTP Cache, API caching

### Runtime Optimization

- **Rendering**: virtualized lists, debounce/throttle, memo/useMemo
- **State**: avoid unnecessary re-renders, normalize state shape

---

## 3. Accessibility (A11y) Requirements

- **WCAG 2.1 AA** baseline (move to AA+ where regulated)
- Semantic HTML; ARIA labels where semantic HTML insufficient
- Full keyboard navigation; visible focus indicators
- Color contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text
- Screen reader and assistive-tech support verified per release

---

## 4. Responsive Breakpoints

| Name | Width | Target Device |
| :--- | :--- | :--- |
| xs | < 576px | Mobile (portrait) |
| sm | ≥ 576px | Mobile (landscape) |
| md | ≥ 768px | Tablet |
| lg | ≥ 992px | Laptop |
| xl | ≥ 1200px | Desktop |

---

## 5. Internationalization (i18n)

- Tooling: `[react-intl / vue-i18n / next-intl]`
- Date/number formatting via `Intl` API
- RTL layout support if region requires

---

## 6. Frontend Monitoring SLOs

| Concern | Tooling Class | SLO |
| :--- | :--- | :--- |
| Performance | Core Web Vitals collection (`web-vitals` library) | p75 LCP < 2.5s, p75 INP < 200ms |
| Errors | Error boundary + remote sink (e.g. Sentry) | < 0.1% sessions with uncaught error |
| Behavior | Page-view + interaction telemetry | All critical CTAs instrumented |

---

## 7. Override Rules

- These attributes are **hard constraints**. To deviate (e.g. relax LCP target for an internal tool), write a tier-1 ADR justifying the override.
- Tier-2 contracts and tier-3 process docs **must not** silently relax these targets.