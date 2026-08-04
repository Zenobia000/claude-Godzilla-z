# TDD and Unit Test Patterns

Load this reference when running the Red-Green-Refactor cycle, writing unit
tests, or mocking external services.

## The 7-Step Cycle (full detail)

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

## Coverage Thresholds (optional project policy example)

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

## Watch Mode and Pre-Commit Hook

```bash
# During development
npm test -- --watch

# Pre-commit hook
npm test && npm run lint
```

## Unit Test Pattern (Jest/Vitest + Testing Library)

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

## Mocking External Services

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

## Common Mistakes in Unit Tests

### Test behavior, not implementation details
```typescript
// Wrong: internal state
expect(component.state.count).toBe(5)

// Correct: what users see
expect(screen.getByText('Count: 5')).toBeInTheDocument()
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

### Test error paths, not just happy paths
```typescript
// Always include: null input, empty arrays, network failures, boundary values
it('handles empty query gracefully', async () => { /* ... */ })
it('returns 400 on invalid parameters', async () => { /* ... */ })
```
