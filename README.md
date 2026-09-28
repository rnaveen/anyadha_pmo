# Anyadha PMO

Anyadha Enterprise PMO application for Frappe Framework v16+ and ERPNext v16+.

## Business modules

1. PMO Masters
2. Governance
3. Strategy Portfolio
4. Proposal DPR
5. Programme Management
6. Project Management
7. Monitoring Evaluation *(legacy module folder — desk merged into Outcomes)*
8. Grants Donor Management
9. CSR Management
10. Risk Internal Controls
11. Compliance Regulatory
12. Audit Assurance
13. SOP Document Control
14. Performance MIS *(legacy module folder — desk merged into Outcomes)*

**Funding spine (U3):** one Agreement DocType (`PMO Grant`, desk label Agreement) with `agreement_type`; Project holds budget and funder child lines; Deliverable is the unified reporting artifact. Grants/CSR desks filter by type. Case hub on the Agreement form (promote from Proposal; link/create from Project). See `docs/USER_MANUAL.md`.

**Strategy nesting (U4):** Company-scoped Strategic Plan with optional parent plan; Portfolio → Project nesting; Programme remains optional. See `docs/USER_MANUAL.md`.

**Outcomes direction (U5):** one **Outcomes and Performance** workspace; Indicator/KPI DocTypes remain until O-6. Design note: `frappe/design/pmo_outcomes/`. See `docs/USER_MANUAL.md`.

## v16 navigation

Public Workspaces are shipped under `anyadha_pmo/` module `workspace/` folders.
Curated v16 Workspace Sidebar records are shipped under `anyadha_pmo/workspace_sidebar/`.

## Dependencies

ERPNext is required. India Compliance, HRMS, Raven, Agriculture and other apps remain optional integrations.

## Local migrate (test bench)

After pulling this branch on the **test** bench only:

```bash
bench --site <test-site> migrate
```

Do not migrate prod until the test demo passes.
