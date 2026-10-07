# Changelog — anyadha_pmo

## Unreleased

### Removed

- S8 funding twin DocTypes dropped (Grant/CSR Agreement/Project twins, reporting/budget/fund twins, CSR Partner); live path is Agreement → Project → Deliverable

### Added

- Agreement path on `PMO Grant` (label Agreement): `agreement_type`, Company, Funding Party, project link table, conditions, folded legal attach fields
- Project budget child (`PMO Project Budget Line`) and funder child (`PMO Project Funder Line`)
- Unified Deliverable fields on `PMO Project Deliverable` (type, reviewer, status, attachment, overdue)
- Funding Party shape on `PMO Donor` (party type, ERPNext Customer/Supplier links, contacts child)
- Child DocTypes: Agreement Project Link, Agreement Condition, Funding Party Contact
- Case hub on Agreement (status strip + Case create-next); thin Proposal promote and Project link/create Agreement strips
- Optional `parent_strategic_plan` on `PMO Strategic Plan` (holding cascade; not required)
- Portfolio linked-Projects HTML list (same-Company nesting via `PMO Project.portfolio`)
- Outcomes and Performance workspace (one desk for former M&E + Performance MIS links)
- `docs/ui_soft_hide/` — reversible Desk soft-hide pack (v1.3): hide hollow IRM + dormant twins + Central Approval sunset; Grants/CSR show Funding Party · Agreement · Project · Deliverable; re-apply after migrate (no schema change)
- Agreement **Case → Suggest Obligations** when GRC Settings suggest flag is on (`grc_core` installed)

### Changed

- Grants / CSR workspaces point at typed Agreement lists; dormant twin create removed for normal roles
- Portfolio Company required; Entity hidden on Portfolio / Project live path
- Agreement, Proposal, Deliverable, Funding Party, Strategy, Initiative, Programme, Portfolio, and Project forms use multi-column functional sections (Party / Books / Contacts on Funding Party; Ask columns on Proposal; Business Unit under Project Classification)
- Proposal list shows Title, Status, Donor, Amount, Project Type; form regrouped (Proposal / Classification / Ask / Description); Project Type help clarifies master classification only
- Programme Company required; Programme↔Portfolio Company match (Entity no longer checked)
- Monitoring and Evaluation + Performance MIS desks hidden; Executive PMO points at Outcomes and Performance
- Hide duplicate legacy Grants catalog workspace; keep thin Grants / CSR desks on typed Agreement
- Governance sidebar / soft-hide: Central Approval (Approval Request / Step / PMO Authority Matrix / Rule) removed from target desk — Option C group standard (Workflow + GRC Authority Rule)

### Fixed

- Agreement↔Project Company match and one-Agreement-per-Project validation
- `PMO Project` amount validation coerces Percent/Currency strings with `flt` (avoids TypeError on save)

### Internal

- Patch `migrate_u3_funding_foundation` copies legacy donor/project/amount and standalone budget rows into U3 fields
- Patch `migrate_u3_funding_foundation` ignores mandatory on legacy Agreement/Donor/Project saves so migrate completes on sparse data
- Patch `drop_s8_funding_twins` empty-check (+ optional `s8_force_drop_funding_twins`) removes twin DocTypes from DB — see `docs/S8_PROOF.md`
- O-6 Indicator/KPI field merge deferred — see `frappe/design/pmo_outcomes/O6_FIELD_MERGE.md`
