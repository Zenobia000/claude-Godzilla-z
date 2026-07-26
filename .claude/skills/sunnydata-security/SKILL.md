---
name: sunnydata-security
description: Comprehensive security review — OWASP Top 10 classification, implementation checklists, and language-specific best practices. Use when implementing auth, handling user input, creating API endpoints, working with secrets, or doing security assessments.
origin: merged (security-review + owasp-web-security + security-best-practices-openai)
---

> **繁體中文說明**：此技能整合三個安全技能為一體，涵蓋 OWASP 分類（第一層）、具體實作清單（第二層）、語言框架特定參考（第三層）。

# Security

> Project-wide safety principles are in `.claude/rules/golden-rules.md`; this
> Skill owns the detailed, technology-specific security workflow.

## Overview

Three-layer security skill covering the full review lifecycle:

- **Layer 1 — Classify**: Map findings to OWASP Top 10 (2021) taxonomy and CWE identifiers.
- **Layer 2 — Implement**: Apply concrete checklists and code patterns for each vulnerability class.
- **Layer 3 — Language-specific**: Load framework-specific guidance from `references/` and write secure-by-default code.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Security assessment, threat modeling, or design review
- User requests OWASP-aligned review, ASVS, SAMM, or CWE mapping
- User requests a security report or secure-by-default help (supported: Python, JavaScript/TypeScript, Go)

---

## Layer 1: Classification (OWASP)

Use these **official category names** when reporting or triaging findings. Assign an A01–A10 label (and CWE when helpful). Note if multiple categories apply.

### OWASP Top 10 (2021)

| ID | Category | Common Examples |
| :--- | :--- | :--- |
| A01:2021 | Broken Access Control | Missing authz checks, IDOR, path traversal, CORS misconfiguration |
| A02:2021 | Cryptographic Failures | Cleartext transmission, weak algorithms, hardcoded secrets |
| A03:2021 | Injection | SQL injection, XSS, command injection, template injection |
| A04:2021 | Insecure Design | Missing rate limiting, insecure design patterns, no threat modeling |
| A05:2021 | Security Misconfiguration | Default creds, verbose errors, open cloud storage, missing headers |
| A06:2021 | Vulnerable and Outdated Components | Unpatched deps, EOL libraries, `npm audit` findings |
| A07:2021 | Identification and Authentication Failures | Weak passwords, credential stuffing, broken session management |
| A08:2021 | Software and Data Integrity Failures | Unsigned artifacts, insecure deserialization, CI/CD compromise |
| A09:2021 | Security Logging and Monitoring Failures | No audit trail, sensitive data in logs, no alerting |
| A10:2021 | Server-Side Request Forgery (SSRF) | Unvalidated URLs, internal metadata endpoint exposure |

### API Security Top 10 (OWASP)

For API-specific reviews, also reference the [OWASP API Security Top 10](https://owasp.org/API-Security/) (object-level authz, broken function-level authz, mass assignment, etc.).

### Scoping Checklist

Cover all surfaces before mapping findings:

- [ ] Web UI (rendering, DOM, client-side scripts)
- [ ] Backend APIs (REST, GraphQL, gRPC)
- [ ] Auth flows (login, registration, password reset, OAuth callbacks)
- [ ] File uploads and downloads
- [ ] Admin paths and privileged operations
- [ ] Third-party callbacks and webhooks (SSRF surface)
- [ ] Supply chain (dependencies, CI/CD pipeline)

### Official References

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)

---

## Layer 2: Implementation Checklist

### 1. Secrets Management (A02)

```typescript
// NEVER: hardcoded secrets
const apiKey = "sk-proj-xxxxx"

// ALWAYS: environment variables with startup guard
const apiKey = process.env.OPENAI_API_KEY
if (!apiKey) throw new Error('OPENAI_API_KEY not configured')
```

- [ ] No hardcoded API keys, tokens, or passwords in source
- [ ] All secrets in environment variables or a secret manager
- [ ] `.env.local` / `.env` in `.gitignore`
- [ ] No secrets in git history
- [ ] Production secrets stored in hosting platform (Vercel, Railway, etc.)
- [ ] Secrets validated at startup (fail-fast)

### 2. Input Validation (A03, A04)

```typescript
import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

export async function createUser(input: unknown) {
  const validated = CreateUserSchema.parse(input)  // throws ZodError on invalid
  return db.users.create(validated)
}
```

**File upload validation:**
```typescript
function validateFileUpload(file: File) {
  const MAX_SIZE = 5 * 1024 * 1024  // 5 MB
  if (file.size > MAX_SIZE) throw new Error('File too large (max 5MB)')

  const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif']
  if (!ALLOWED_TYPES.includes(file.type)) throw new Error('Invalid file type')

  const ALLOWED_EXT = ['.jpg', '.jpeg', '.png', '.gif']
  const ext = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!ext || !ALLOWED_EXT.includes(ext)) throw new Error('Invalid file extension')
}
```

- [ ] All user inputs validated with schemas (whitelist, not blacklist)
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct user input in queries or system calls
- [ ] Error messages do not leak sensitive info

### 3. SQL Injection Prevention (A03)

```typescript
// NEVER: string concatenation
const q = `SELECT * FROM users WHERE email = '${userEmail}'`

// ALWAYS: parameterized queries
await db.query('SELECT * FROM users WHERE email = $1', [userEmail])

// ORM (Supabase / Prisma)
const { data } = await supabase.from('users').select('*').eq('email', userEmail)
```

- [ ] All database queries use parameterized queries or ORM
- [ ] No string concatenation in SQL

### 4. Authentication & Authorization (A01, A07)

```typescript
// NEVER: localStorage for tokens (XSS exposure)
localStorage.setItem('token', token)

// ALWAYS: httpOnly cookies
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)

// ALWAYS: check authorization before acting
export async function deleteUser(userId: string, requesterId: string) {
  const requester = await db.users.findUnique({ where: { id: requesterId } })
  if (requester.role !== 'admin') {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 403 })
  }
  await db.users.delete({ where: { id: userId } })
}
```

**Row Level Security (Supabase):**
```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_view_own"  ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "users_update_own" ON users FOR UPDATE USING (auth.uid() = id);
```

- [ ] Tokens in httpOnly cookies (never localStorage)
- [ ] Authorization check before every sensitive operation
- [ ] Role-based access control implemented
- [ ] Row Level Security enabled (Supabase)
- [ ] Session management secure

### 5. XSS Prevention (A03)

```typescript
import DOMPurify from 'isomorphic-dompurify'

function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

**Content Security Policy (Next.js):**
```typescript
// next.config.js
const csp = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
`.replace(/\s{2,}/g, ' ').trim()
```

- [ ] User-provided HTML sanitized before rendering
- [ ] CSP headers configured
- [ ] React's built-in escaping used; `dangerouslySetInnerHTML` only with sanitized input

### 6. CSRF Protection (A01)

```typescript
export async function POST(request: Request) {
  const token = request.headers.get('X-CSRF-Token')
  if (!csrf.verify(token)) {
    return NextResponse.json({ error: 'Invalid CSRF token' }, { status: 403 })
  }
}

// Cookie: SameSite=Strict is the baseline defence
res.setHeader('Set-Cookie', `session=${id}; HttpOnly; Secure; SameSite=Strict`)
```

- [ ] CSRF tokens on all state-changing operations
- [ ] SameSite=Strict on session cookies

### 7. Rate Limiting (A04)

```typescript
import rateLimit from 'express-rate-limit'

app.use('/api/', rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }))
app.use('/api/search', rateLimit({ windowMs: 60 * 1000, max: 10 }))
```

- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on expensive operations (search, AI, exports)
- [ ] Both IP-based and user-based limits where applicable

### 8. Sensitive Data Exposure (A02, A09)

```typescript
// NEVER: log sensitive fields
console.log('User login:', { email, password })

// ALWAYS: redact
console.log('User login:', { email, userId })

// NEVER: leak stack traces to clients
catch (error) {
  return NextResponse.json({ error: error.message, stack: error.stack }, { status: 500 })
}

// ALWAYS: generic client error, detailed server log
catch (error) {
  console.error('Internal error:', error)
  return NextResponse.json({ error: 'An error occurred.' }, { status: 500 })
}
```

- [ ] No passwords, tokens, or card numbers in logs
- [ ] Generic error messages for clients
- [ ] Stack traces only in server-side logs

### 9. Dependency Security (A06)

```bash
npm audit           # detect known vulnerabilities
npm audit fix       # auto-fix where possible
npm outdated        # identify stale packages
npm ci              # reproducible installs in CI
```

- [ ] `npm audit` clean (or known exceptions documented)
- [ ] Lock files (`package-lock.json`) committed
- [ ] Dependabot or equivalent enabled

### 10. Resource IDs

Use random UUIDs (v4) or random hex strings for any resource ID exposed to the internet. Never use auto-incrementing integers — they reveal resource counts and are trivially enumerable (A01: IDOR).

### 11. TLS Note

Do not report missing TLS as a finding for local dev environments. Add an env flag to toggle `Secure` cookie attribute rather than hard-coding it, to avoid breaking non-TLS dev setups. Avoid recommending HSTS without understanding its lasting impact.

---

## Layer 3: Language-Specific Practices

### Detection

Inspect the repository to identify all languages and frameworks in scope (frontend and backend). Use file extensions, package manifests (`package.json`, `go.mod`, `requirements.txt`, `pyproject.toml`), and import patterns.

### Reference Loading

Check `references/` for matching guidance files. Filename format:

```
<language>-<framework>-<stack>-security.md
<language>-general-<stack>-security.md
```

Available references:

| File | Covers |
| :--- | :--- |
| `golang-general-backend-security.md` | Go backend |
| `javascript-express-web-server-security.md` | Express.js |
| `javascript-general-web-frontend-security.md` | Generic JS frontend |
| `javascript-jquery-web-frontend-security.md` | jQuery |
| `javascript-typescript-nextjs-web-server-security.md` | Next.js (TS) |
| `javascript-typescript-react-web-frontend-security.md` | React (TS) |
| `javascript-typescript-vue-web-frontend-security.md` | Vue 3 (TS) |
| `python-django-web-server-security.md` | Django |
| `python-fastapi-web-server-security.md` | FastAPI |
| `python-flask-web-server-security.md` | Flask |

Load **all** files matching the detected stack (e.g., for a Next.js + React app, load both `nextjs` and `react` files). If no matching file exists, apply general web security knowledge and note the gap in any report.

### Overrides

If a project has documented reasons to bypass a best practice, respect it and do not fight the decision. You may suggest adding a comment explaining the bypass for future maintainers.

---

## Workflow

Use the three layers in sequence:

1. **Classify (Layer 1)** — Assign OWASP A01–A10 label and CWE to each finding. Scope the review surface first.
2. **Check (Layer 2)** — Run the relevant implementation checklist items. Use code patterns as the reference.
3. **Fix (Layer 3)** — Load the matching `references/` file for the detected language/framework. Write or correct code following its guidance. Fix one finding at a time. Always verify that fixes do not introduce regressions.

### Operating Modes

| Mode | When | Action |
| :--- | :--- | :--- |
| **Secure-by-default** | Writing new code | Apply Layer 2 + 3 patterns proactively |
| **Passive detection** | Working in existing codebase | Flag critical findings; ask before fixing |
| **Full report** | User requests security review | Classify all findings → severity-ordered report → offer to fix one at a time |

### Report Format

Write to `security_best_practices_report.md` (or user-specified path). Structure:

- Executive summary (2–3 sentences)
- Findings grouped by severity (Critical → High → Medium → Low)
- Each finding: numeric ID, OWASP label, one-sentence impact, file + line reference, recommended fix
- Offer to fix starting from the highest severity finding

---

## Pre-Deployment Security Checklist

Merged from all source skills, deduplicated. Run before any production deployment.

**Secrets & Config**
- [ ] No hardcoded secrets; all in env vars
- [ ] `.env` files excluded from git
- [ ] HTTPS enforced in production
- [ ] CORS properly configured (not `*` in production)
- [ ] Security headers set: `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`

**Input & Data**
- [ ] All user inputs validated with schemas
- [ ] File uploads validated (size, type, extension)
- [ ] All database queries parameterized
- [ ] User-provided HTML sanitized before rendering

**Auth & Access**
- [ ] Tokens stored in httpOnly cookies (never localStorage)
- [ ] Authorization checks before every sensitive operation
- [ ] Role-based access control in place
- [ ] Row Level Security enabled (if using Supabase)
- [ ] Session management secure

**Attack Surface**
- [ ] CSRF protection on state-changing endpoints
- [ ] Rate limiting on all API endpoints
- [ ] SSRF mitigations for any URL-fetching endpoints

**Data Hygiene**
- [ ] No sensitive data in logs (passwords, tokens, card numbers)
- [ ] Error responses generic for clients; details only in server logs
- [ ] No stack traces exposed externally

**Dependencies**
- [ ] `npm audit` (or equivalent) clean
- [ ] Lock files committed
- [ ] Dependabot / Renovate enabled

**Testing**
- [ ] Authentication-required endpoints return 401 without credentials
- [ ] Authorization-restricted endpoints return 403 for wrong role
- [ ] Input validation returns 400 for malformed requests
- [ ] Rate limiting returns 429 after threshold

**Blockchain (if applicable)**
- [ ] Wallet signatures verified before acting on transactions
- [ ] Transaction recipient, amount, and balance validated
- [ ] No blind transaction signing

---

## Resources

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [Web Security Academy (PortSwigger)](https://portswigger.net/web-security)
- [Next.js Security Docs](https://nextjs.org/docs/security)
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
