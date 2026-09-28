# Changelog — anyadha_pmo

## Unreleased

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

### Changed

- Grants / CSR workspaces point at typed Agreement lists; dormant twin create removed for normal roles
- Portfolio Company required; Entity hidden on Portfolio / Project live path
- Agreement, Proposal, Deliverable, Funding Party, Strategy, Initiative, Programme, Portfolio, and Project forms use multi-column functional sections
- Programme Company required; Programme↔Portfolio Company match (Entity no longer checked)
- Monitoring and Evaluation + Performance MIS desks hidden; Executive PMO points at Outcomes and Performance

### Fixed

- Agreement↔Project Company match and one-Agreement-per-Project validation

### Internal

- Patch `migrate_u3_funding_foundation` copies legacy donor/project/amount and standalone budget rows into U3 fields
- Patch `migrate_u3_funding_foundation` ignores mandatory on legacy Agreement/Donor/Project saves so migrate completes on sparse data
- O-6 Indicator/KPI field merge deferred — see `frappe/design/pmo_outcomes/O6_FIELD_MERGE.md`
