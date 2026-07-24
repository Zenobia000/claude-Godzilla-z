---
name: sunnydata-testing
description: Risk-based test development workflow with unit, integration, and E2E patterns. Use Red-Green-Refactor where it improves feedback, and apply project-defined coverage and evidence thresholds when writing features, fixing bugs, or setting up test infrastructure.
origin: merged(tdd-workflow + e2e-testing)
---

<!-- 繁中摘要：此技能整合 TDD 與 Playwright E2E，依風險選擇單元、整合、E2E 層級；覆蓋率門檻由專案政策與關鍵行為決定。 -->

# Testing

> Project-wide evidence rules are in `.claude/rules/golden-rules.md`; this Skill
> owns testing methods. Discover thresholds from project configuration, CI, NFRs,
> or approved quality policy instead of inventing a universal percentage.

## Overview

Prefer a failing test or reproducible check before implementation when practical,
then implement and refactor with feedback. Choose the test layers needed to cover
approved behavior and material risk:

- **Unit tests** — individual functions, utilities, components
- **Integration tests** — API endpoints, database operations, service interactions
- **E2E tests** — critical user flows via Playwright browser automation

## TDD Workflow (Red-Green-Refactor)

### When to Apply

- Writing new features or functionality
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring existing code
- Adding API endpoints or new components

### The 7-Step Cycle

**Step 1: Write User Journey**
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for markets semantically,
so that I can find relevant markets even without exact keywords.
```

**Step 2: Derive Test Cases**
```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => { /* ... */ })
  it('handles empty query gracefully', async () => { /* ... */ })
  it('falls back to substring search when Redis unavailable', async () => { /* ... */ })
  it('sorts results by similarity score', async () => { /* ... */ })
})
```

**Step 3: Run Tests (RED — they must fail)**
```bash
npm test
# Expected: tests fail — implementation does not exist yet
```

**Step 4: Implement Minimal Code**
```typescript
// Write only enough code to make tests pass
export async function searchMarkets(query: string) {
  // minimal implementation
}
```

**Step 5: Run Tests (GREEN — they must pass)**
```bash
npm test
# Expected: all tests pass
```

**Step 6: Refactor**
- Remove duplication
- Improve naming and readability
- Optimize performance
- Keep tests green throughout

**Step 7: Verify Coverage**
```bash
npm run test:coverage
# Compare with the repository's configured thresholds and changed-risk areas.
```

### Coverage Thresholds (optional project policy example)

The following `80` values are an example only. Keep existing repository
thresholds, or have the responsible team approve new ones.

```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

### Watch Mode and Pre-Commit Hook
```bash
# During development
npm test -- --watch

# Pre-commit hook
npm test && npm run lint
```

---

## Unit Tests

### Pattern (Jest/Vitest + Testing Library)
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### Mocking External Services

**Supabase**
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}))
```

**Redis**
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

**OpenAI**
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // mock 1536-dim embedding
  ))
}))
```

---

## Integration Tests

### API Endpoint Pattern
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)
    expect(response.status).toBe(400)
  })

  it('handles database errors gracefully', async () => {
    // mock database failure, then verify error response shape
    const request = new NextRequest('http://localhost/api/markets')
    // assert 500 response with consistent error envelope
  })
})
```

---

## E2E Tests (Playwright)

### Directory Structure
```
tests/
├── unit/
├── integration/
└── e2e/
    ├── auth/
    │   ├── login.spec.ts
    │   ├── logout.spec.ts
    │   └── register.spec.ts
    ├── features/
    │   ├── browse.spec.ts
    │   ├── search.spec.ts
    │   └── create.spec.ts
    └── api/
        └── endpoints.spec.ts
fixtures/
├── auth.ts
└── data.ts
playwright.config.ts
```

### Page Object Model (POM)
```typescript
import { Page, Locator } from '@playwright/test'

export class ItemsPage {
  readonly page: Page
  readonly searchInput: Locator
  readonly itemCards: Locator
  readonly createButton: Locator

  constructor(page: Page) {
    this.page = page
    this.searchInput = page.locator('[data-testid="search-input"]')
    this.itemCards = page.locator('[data-testid="item-card"]')
    this.createButton = page.locator('[data-testid="create-btn"]')
  }

  async goto() {
    await this.page.goto('/items')
    await this.page.waitForLoadState('networkidle')
  }

  async search(query: string) {
    await this.searchInput.fill(query)
    await this.page.waitForResponse(resp => resp.url().includes('/api/search'))
    await this.page.waitForLoadState('networkidle')
  }

  async getItemCount() {
    return await this.itemCards.count()
  }
}
```

### Test Structure with POM
```typescript
import { test, expect } from '@playwright/test'
import { ItemsPage } from '../../pages/ItemsPage'

test.describe('Item Search', () => {
  let itemsPage: ItemsPage

  test.beforeEach(async ({ page }) => {
    itemsPage = new ItemsPage(page)
    await itemsPage.goto()
  })

  test('should search by keyword', async ({ page }) => {
    await itemsPage.search('test')

    const count = await itemsPage.getItemCount()
    expect(count).toBeGreaterThan(0)
    await expect(itemsPage.itemCards.first()).toContainText(/test/i)
    await page.screenshot({ path: 'artifacts/search-results.png' })
  })

  test('should handle no results', async ({ page }) => {
    await itemsPage.search('xyznonexistent123')

    await expect(page.locator('[data-testid="no-results"]')).toBeVisible()
    expect(await itemsPage.getItemCount()).toBe(0)
  })
})
```

### Playwright Configuration
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['junit', { outputFile: 'playwright-results.xml' }],
    ['json', { outputFile: 'playwright-results.json' }]
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
})
```

### Flaky Test Diagnosis and Isolation

**Quarantine a flaky test**
```typescript
test('flaky: complex search', async ({ page }) => {
  test.fixme(true, 'Flaky - Issue #123')
  // test code...
})

test('conditional skip in CI', async ({ page }) => {
  test.skip(process.env.CI, 'Flaky in CI - Issue #123')
  // test code...
})
```

**Reproduce flakiness locally**
```bash
npx playwright test tests/search.spec.ts --repeat-each=10
npx playwright test tests/search.spec.ts --retries=3
```

**Race conditions**
```typescript
// Bad: assumes element is ready immediately
await page.click('[data-testid="button"]')

// Good: auto-wait locator
await page.locator('[data-testid="button"]').click()
```

**Network timing**
```typescript
// Bad: arbitrary timeout
await page.waitForTimeout(5000)

// Good: wait for specific network condition
await page.waitForResponse(resp => resp.url().includes('/api/data'))
```

**Animation timing**
```typescript
// Bad: click during animation
await page.click('[data-testid="menu-item"]')

// Good: wait for element stability
await page.locator('[data-testid="menu-item"]').waitFor({ state: 'visible' })
await page.waitForLoadState('networkidle')
await page.locator('[data-testid="menu-item"]').click()
```

### Artifact Management

**Screenshots**
```typescript
await page.screenshot({ path: 'artifacts/after-login.png' })
await page.screenshot({ path: 'artifacts/full-page.png', fullPage: true })
await page.locator('[data-testid="chart"]').screenshot({ path: 'artifacts/chart.png' })
```

**Traces**
```typescript
await browser.startTracing(page, {
  path: 'artifacts/trace.json',
  screenshots: true,
  snapshots: true,
})
// ... test actions ...
await browser.stopTracing()
```

**Video (playwright.config.ts)**
```typescript
use: {
  video: 'retain-on-failure',
  videosPath: 'artifacts/videos/'
}
```

### CI/CD GitHub Actions Workflow
```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
        env:
          BASE_URL: ${{ vars.STAGING_URL }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Unit CI/CD (Jest coverage upload)
```yaml
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

### Web3 / Wallet Testing
```typescript
test('wallet connection', async ({ page, context }) => {
  await context.addInitScript(() => {
    window.ethereum = {
      isMetaMask: true,
      request: async ({ method }) => {
        if (method === 'eth_requestAccounts')
          return ['0x1234567890123456789012345678901234567890']
        if (method === 'eth_chainId') return '0x1'
      }
    }
  })

  await page.goto('/')
  await page.locator('[data-testid="connect-wallet"]').click()
  await expect(page.locator('[data-testid="wallet-address"]')).toContainText('0x1234')
})
```

### Financial / High-Risk Flow Testing
```typescript
test('trade execution', async ({ page }) => {
  // Never run against production — real money at stake
  test.skip(process.env.NODE_ENV === 'production', 'Skip on production')

  await page.goto('/markets/test-market')
  await page.locator('[data-testid="position-yes"]').click()
  await page.locator('[data-testid="trade-amount"]').fill('1.0')

  const preview = page.locator('[data-testid="trade-preview"]')
  await expect(preview).toContainText('1.0')

  await page.locator('[data-testid="confirm-trade"]').click()
  await page.waitForResponse(
    resp => resp.url().includes('/api/trade') && resp.status() === 200,
    { timeout: 30000 }
  )

  await expect(page.locator('[data-testid="trade-success"]')).toBeVisible()
})
```

---

## Common Mistakes

### Test behavior, not implementation details
```typescript
// Wrong: internal state
expect(component.state.count).toBe(5)

// Correct: what users see
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### Use semantic selectors
```typescript
// Wrong: brittle CSS class
await page.click('.css-class-xyz')

// Correct: stable semantic selectors
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### Isolate every test
```typescript
// Wrong: tests share state
test('creates user', () => { /* sets up shared user */ })
test('updates same user', () => { /* depends on previous test */ })

// Correct: each test owns its data
test('creates user', () => {
  const user = createTestUser()
  // ...
})
test('updates user', () => {
  const user = createTestUser()
  // ...
})
```

### Never use arbitrary timeouts
```typescript
// Wrong
await page.waitForTimeout(5000)

// Correct: wait for a deterministic condition
await page.waitForResponse(resp => resp.url().includes('/api/data'))
await page.locator('[data-testid="result"]').waitFor({ state: 'visible' })
```

### Test error paths, not just happy paths
```typescript
// Always include: null input, empty arrays, network failures, boundary values
it('handles empty query gracefully', async () => { /* ... */ })
it('returns 400 on invalid parameters', async () => { /* ... */ })
```

---

## Success Metrics

- Project-defined coverage gates pass, with critical paths and changed risk
  directly exercised
- All applicable tests pass; skipped or disabled tests have an explicit reason
- Test feedback time meets the repository or CI budget
- E2E tests cover all critical user flows
- No flaky tests in CI (quarantine with tracked issue if needed)
- Tests catch regressions before production
