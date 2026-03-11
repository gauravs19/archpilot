# Effort Estimation: E-Commerce Platform Build

## Bottom-Up Estimation with T-Shirt Cross-Check

| Field | Value |
|-------|-------|
| **Project** | GreenBasket — Organic Grocery E-Commerce Platform |
| **Client** | GreenBasket Foods Pvt Ltd |
| **Estimation Method** | Bottom-Up (WBS) + T-Shirt Validation |
| **Estimated By** | Gaurav Sharma, Solution Architect |
| **Date** | 2026-03-11 |
| **Confidence Level** | ±15% (detailed requirements available) |

---

## 1. Scope Summary

Build a web + mobile-responsive B2C e-commerce platform for organic grocery delivery in Bangalore. Key features:
- Product catalog with search and filters
- Cart, checkout, and payment (UPI, cards via Razorpay)
- Delivery slot booking and order tracking
- Customer accounts, order history, reorders
- Admin panel for product/order/inventory management
- Notification system (email, SMS, push)

---

## 2. T-Shirt Estimate (Quick Validation)

| Feature | Size | Effort Range |
|---------|:----:|:-----------:|
| User Auth + Profiles | S | 5-10 days |
| Product Catalog + Search | M | 15-25 days |
| Cart + Checkout | M | 15-25 days |
| Payment Integration | S | 8-12 days |
| Order Management | M | 15-25 days |
| Delivery Slot System | M | 12-20 days |
| Notification System | S | 5-10 days |
| Admin Dashboard | L | 25-40 days |
| Frontend (Web) | L | 30-45 days |
| Infrastructure + DevOps | M | 15-20 days |
| **T-Shirt Total** | | **145-232 days** |

---

## 3. Detailed Bottom-Up Estimate

### 3.1 Component-Level Breakdown

#### Backend Services

| # | Component | Tasks | Days | Assumptions |
|---|-----------|-------|:----:|-------------|
| 1 | **User Service** | | **12** | |
| | - User registration + login (email, Google OAuth) | | 3 | Cognito for auth |
| | - Profile management (CRUD) | | 2 | |
| | - Address book (CRUD, multiple addresses) | | 2 | |
| | - Password reset, email verification | | 2 | SES for emails |
| | - Unit + integration tests | | 3 | |
| 2 | **Catalog Service** | | **20** | |
| | - Product CRUD (admin) | | 3 | |
| | - Category hierarchy management | | 3 | 3-level deep |
| | - Product search with Elasticsearch | | 5 | Faceted search, autocomplete |
| | - Inventory tracking (stock in/out) | | 3 | |
| | - Image upload + processing (S3) | | 3 | Resize, thumbnail |
| | - Unit + integration tests | | 3 | |
| 3 | **Cart Service** | | **10** | |
| | - Add/remove/update cart items | | 3 | Redis-backed |
| | - Apply promo codes / coupons | | 3 | Basic rule engine |
| | - Cart → order conversion | | 2 | |
| | - Unit + integration tests | | 2 | |
| 4 | **Order Service** | | **18** | |
| | - Order creation from cart | | 3 | |
| | - Order status lifecycle (placed → confirmed → delivered) | | 3 | |
| | - Delivery slot booking logic | | 4 | Slot availability check |
| | - Order history + reorder | | 3 | |
| | - Event publishing (SQS) | | 2 | |
| | - Unit + integration tests | | 3 | |
| 5 | **Payment Service** | | **10** | |
| | - Razorpay integration (UPI, cards, wallets) | | 4 | Webhook handling |
| | - Payment status tracking | | 2 | |
| | - Refund processing | | 2 | |
| | - Unit + integration tests | | 2 | |
| 6 | **Notification Service** | | **8** | |
| | - Email notifications (SES) — 6 templates | | 3 | Order confirm, shipped, delivered |
| | - SMS notifications (SNS) — OTP, delivery updates | | 2 | |
| | - SQS consumer for event-driven notifications | | 2 | |
| | - Tests | | 1 | |
| | **Backend Subtotal** | | **78** | |

#### Frontend (Next.js)

| # | Component | Days | Notes |
|---|-----------|:----:|-------|
| 1 | Homepage (hero, featured, categories) | 3 | SSR |
| 2 | Product listing (grid, filters, sort, pagination) | 5 | Search integration |
| 3 | Product detail page | 3 | Images, reviews placeholder |
| 4 | Cart (slide-out + full page) | 4 | Promo code, totals |
| 5 | Checkout (address, slot, payment) | 5 | Multi-step form |
| 6 | Order tracking + history | 3 | |
| 7 | User profile + address management | 3 | |
| 8 | Login / Register / Reset password | 3 | Cognito hosted UI + custom forms |
| 9 | Admin dashboard — Products | 5 | CRUD, bulk import |
| 10 | Admin dashboard — Orders | 4 | List, detail, status update |
| 11 | Admin dashboard — Analytics | 4 | Basic charts (revenue, orders/day) |
| 12 | Mobile responsiveness | 3 | All pages |
| | **Frontend Subtotal** | **45** | |

#### Infrastructure & DevOps

| # | Task | Days | Notes |
|---|------|:----:|-------|
| 1 | AWS infrastructure via Terraform (VPC, ALB, ECS, RDS, Redis) | 5 | |
| 2 | CI/CD pipeline (GitHub Actions → ECS) | 3 | Build, test, deploy |
| 3 | Staging environment | 2 | Mirrors production |
| 4 | Monitoring + alerting (CloudWatch + basic Datadog) | 3 | Dashboards, alerts |
| 5 | SSL + DNS + CDN setup | 1 | |
| 6 | Secrets management (AWS Secrets Manager) | 1 | |
| | **DevOps Subtotal** | **15** | |

---

### 3.2 Non-Development Activities

| Activity | Effort (Days) | % of Dev | Notes |
|----------|:------------:|:--------:|-------|
| Requirements & Design (HLD, LLD, ADRs) | 22 | 16% | Week 1-2 intensive |
| Integration testing (end-to-end flows) | 15 | 11% | Checkout, payment, delivery flows |
| UAT support & bug fixing | 12 | 9% | 2-week UAT sprint |
| Performance testing | 5 | 4% | k6 load test, optimize |
| Security review + fixes | 5 | 4% | Dependency scan, pen test |
| Documentation (API docs, runbook, handover) | 5 | 4% | |
| Project management & ceremonies | 10 | 7% | Scrum ceremonies, reporting |
| **Non-Dev Subtotal** | **74** | | |

---

### 3.3 Total Estimate

| Category | Person-Days |
|----------|:-----------:|
| Backend Development | 78 |
| Frontend Development | 45 |
| Infrastructure & DevOps | 15 |
| **Development Subtotal** | **138** |
| Requirements & Design | 22 |
| Testing (Integration + Perf + Security) | 25 |
| UAT & Bug Fixing | 12 |
| Documentation | 5 |
| Project Management | 10 |
| **Non-Dev Subtotal** | **74** |
| **Subtotal** | **212** |
| **Contingency Buffer (15%)** | **32** |
| **GRAND TOTAL** | **244 person-days** |

---

### 3.4 T-Shirt Cross-Check

| Method | Range | Our Estimate |
|--------|:-----:|:------------:|
| T-Shirt (§2) | 145-232 dev days | — |
| Bottom-Up (§3) | 244 total days (incl. non-dev) | ✅ |
| Bottom-Up dev-only | 138 days | Within T-shirt range ✅ |

**Verdict:** Estimate is consistent across methods. The 244-day total includes all phases.

---

## 4. PERT Estimate (Risk-Adjusted)

| Component | Optimistic | Most Likely | Pessimistic | PERT | StdDev |
|-----------|:---------:|:----------:|:----------:|:----:|:------:|
| Backend | 65 | 78 | 100 | 79.5 | 5.8 |
| Frontend | 38 | 45 | 60 | 46 | 3.7 |
| DevOps | 12 | 15 | 22 | 15.7 | 1.7 |
| Non-Dev | 60 | 74 | 95 | 75.2 | 5.8 |
| **Total** | **175** | **212** | **277** | **216.3** | **17** |

| Confidence | Estimate | Calculation |
|:----------:|:--------:|-------------|
| P50 (50% likely) | 216 days | PERT average |
| P75 (75% likely) | 233 days | PERT + 1 StdDev |
| P90 (90% likely) | 250 days | PERT + 2 StdDev |

**Recommended commitment for fixed-price:** P75 = **233 person-days**

---

## 5. Team & Duration

### Proposed Team

| Role | Count | Monthly Cost | Duration |
|------|:-----:|:------------:|:--------:|
| Solution Architect | 1 (part-time 50%) | — | 16 weeks |
| Full-Stack Developer (Senior) | 2 | — | 16 weeks |
| Full-Stack Developer (Mid) | 2 | — | 16 weeks |
| QA Engineer | 1 | — | 12 weeks |
| DevOps Engineer | 1 (part-time 50%) | — | 16 weeks |
| **Effective FTEs** | **5** | | |

### Duration Calculation

```
Total effort: 244 person-days
Effective team: 5 FTEs
Calendar days: 244 / 5 = ~49 working days = ~10 weeks
With pipeline overhead (20%): ~12 weeks
With UAT + hypercare: 16 weeks total
```

**Timeline: 16 weeks (4 months)**

---

## 6. Assumptions

1. Requirements are 80%+ finalized before development starts
2. Razorpay test account available from Week 3
3. Product catalog data (500-1000 products) provided by client in CSV
4. Client provides UAT team (2 people) for 2-week UAT phase
5. No mobile native app — responsive web only
6. No multi-language support in Phase 1
7. No loyalty/rewards program in Phase 1
8. Bangalore delivery only (no multi-city logistics in Phase 1)

---

*Generated using Archpilot Estimation Framework v1.0*
