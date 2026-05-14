# API Governance Standards

> **Purpose:** This rule file defines the full lifecycle governance of APIs — from design
> and versioning through publication, productization, and deprecation. It expands on rule 05
> (API Design) to cover organizational API strategy, developer experience, and marketplace governance.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [05 — API Design](./05-api-design.md) | Technical API design standards |
| [18 — Architecture Governance](./18-architecture-governance.md) | Broader governance framework |
| [30 — Platform Engineering](./30-platform-engineering.md) | API catalog and portal |
| [32 — Data Contracts](./32-data-contracts.md) | API as contract between producers and consumers |

---

## 1. API Strategy

### 1.1 API-First Mandate

All inter-service and external integrations MUST follow API-First:

1. **Define the contract first** (OpenAPI spec) — before writing any implementation
2. **Get contract reviewed** — consumer teams review before implementation starts
3. **Generate server stubs and client SDKs** from the contract
4. **Implement against the contract** — implementation validates to spec
5. **Publish to API catalog** — auto-synced from the approved spec

### 1.2 API Types and Governance Level

| API Type | Audience | Governance Level | SLA Required |
|----------|---------|:----------------:|:------------:|
| **Private** (internal only) | Same team | Light | No |
| **Partner** (B2B, selected external) | Known partners | Standard | Yes |
| **Public** (open internet) | All developers | Full | Yes + SLA commitment |
| **Platform** (internal across teams) | All internal teams | Standard | Yes |

---

## 2. API Lifecycle Management

### 2.1 API States

`
DESIGN ? REVIEW ? APPROVED ? PUBLISHED ? DEPRECATED ? RETIRED
`

| State | Entry Criteria | Exit Criteria |
|-------|---------------|--------------|
| **DESIGN** | OpenAPI draft created | Peer review started |
| **REVIEW** | Consumer teams notified | All feedback addressed |
| **APPROVED** | Contract signed off by consumers + architect | Version tagged in Git |
| **PUBLISHED** | Deployed to gateway, listed in catalog | Deprecation decision |
| **DEPRECATED** | Successor version available, notice sent (min 6 months) | All consumers migrated |
| **RETIRED** | Zero active consumers | Contract archived |

### 2.2 Versioning Policy

| Change Type | Version Impact | Notice Period |
|------------|:-------------:|:-------------:|
| New optional field in response | Patch (1.x.Y) | None |
| New optional request parameter | Minor (1.X.0) | None |
| New endpoint | Minor (1.X.0) | Announcement |
| Deprecated field (still present) | Minor (1.X.0) | 6 months |
| Removed field or endpoint | Major (X.0.0) | 12 months minimum |
| Changed field type or semantics | Major (X.0.0) | 12 months minimum |
| Auth mechanism change | Major (X.0.0) | 12 months minimum |

**Rule:** NEVER remove or change the meaning of a field without a major version bump.
**Rule:** Old versions MUST remain operational for the full notice period after deprecation.
**Rule:** A maximum of 2 major versions may be live simultaneously.

---

## 3. API Contract Standards

### 3.1 OpenAPI Specification Requirements

Every API MUST have an OpenAPI 3.1+ spec including:

- [ ] info.title, info.version, info.description, info.contact
- [ ] All endpoints with operationId (unique, camelCase)
- [ ] Request and response schemas with $ref components (no inline anonymous schemas)
- [ ] All possible status codes documented (200, 201, 400, 401, 403, 404, 409, 422, 429, 500, 503)
- [ ] Error response follows standard error schema (see rule 05)
- [ ] security schemes defined at spec level and applied per-operation
- [ ] x-ratelimit-* headers documented
- [ ] Pagination schema documented for all list endpoints
- [ ] deprecated: true flag on any deprecated operations
- [ ] x-api-owner and x-team custom extensions for catalog routing

### 3.2 API Contract Linting Gates

All API contracts MUST pass automated linting before merge:

| Rule | Tool |
|------|------|
| No undocumented status codes | Spectral rule: oas3-valid-media-example |
| No anonymous inline schemas | Spectral custom rule |
| OperationId required on all operations | Spectral: operation-operationId |
| No 2xx without schema | Spectral: operation-success-response |
| Security defined on all non-public ops | Spectral custom rule |
| No examples with real PII | Spectral custom rule |

---

## 4. API Developer Experience (DX)

### 4.1 DX Checklist — Every Published API

- [ ] **Getting started guide:** Working example in <10 minutes from zero
- [ ] **Interactive docs:** Swagger UI or equivalent with Try-It-Out
- [ ] **Code samples:** At least 3 languages (Python, JavaScript, curl)
- [ ] **Error catalog:** Every error code documented with cause and resolution
- [ ] **Changelog:** Machine-readable (CHANGELOG.md or equivalent)
- [ ] **Status page:** Real-time API health and historical uptime
- [ ] **Support channel:** Slack/Teams channel or ticketing path for consumers

### 4.2 SDK Standards

If providing client SDKs:

- SDKs MUST be generated from the OpenAPI spec (not hand-written)
- SDK versions MUST be pinned to API version
- SDKs MUST include: retry logic, exponential backoff, correlation ID propagation
- SDKs MUST NOT bundle credentials or environment-specific config

---

## 5. API Security Governance

### 5.1 Mandatory Security Controls per API Type

| Control | Private | Partner | Public |
|---------|:-------:|:-------:|:------:|
| Authentication (JWT/OAuth2) | ? | ? | ? |
| Rate limiting | ? | ? | ? |
| Input validation | ? | ? | ? |
| HTTPS only | ? | ? | ? |
| API key management (partner-specific) | — | ? | ? |
| Scoped OAuth2 (not wildcard) | ? | ? | ? |
| Request signing (HMAC) | — | ?? Sensitive | ?? Sensitive |
| Mutual TLS | ?? Critical | ?? Critical | — |
| WAF protection | — | ?? | ? |
| DDoS protection | — | ?? | ? |

### 5.2 API Rate Limiting Standards

| API Type | Default Limit | Burst | Per |
|----------|:------------:|:-----:|-----|
| Private | 1,000 req/min | 2× | Per service identity |
| Partner | 500 req/min | 1.5× | Per API key |
| Public (unauthenticated) | 60 req/min | 1× | Per IP |
| Public (authenticated) | 300 req/min | 2× | Per user token |

Rate limit headers MUST be returned on every response:
`
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 487
X-RateLimit-Reset: 1715678400
Retry-After: 60   (on 429 responses)
`

---

## 6. API Governance Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Spec written after code | Contract reflects implementation quirks | API-First: spec before code |
| God endpoint (does everything) | Hard to secure, version, scale | One resource = one endpoint family |
| Version in request body | Breaks REST semantics; hard to route | Version in URL path: /v2/resource |
| No deprecation notice | Breaking consumers without warning | 12-month notice for major; 6-month for minor |
| Multiple live major versions (>2) | Maintenance nightmare | Max 2 live majors; force migration |
| No error catalog | Consumers can't self-serve errors | Document every error code |
| Wildcard OAuth scopes | Over-permission; blast radius too large | Granular scopes per resource and action |

---

## 7. API Governance Checklist

- [ ] API-First workflow enforced (spec before implementation)
- [ ] OpenAPI 3.1+ spec with all mandatory fields
- [ ] Spectral linting passes on CI
- [ ] Versioning policy documented and enforced
- [ ] Deprecation notices sent with required notice periods
- [ ] Max 2 major versions live at any time
- [ ] Rate limiting configured with required headers
- [ ] Auth controls applied per API type
- [ ] DX checklist complete: getting started, interactive docs, error catalog
- [ ] API listed in developer portal catalog

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
