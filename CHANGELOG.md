# Changelog — anyadha_pmo

## Unreleased

### Added

- Agreement path on `PMO Grant` (label Agreement): `agreement_type`, Company, Funding Party, project link table, conditions, folded legal attach fields
- Project budget child (`PMO Project Budget Line`) and funder child (`PMO Project Funder Line`)
- Unified Deliverable fields on `PMO Project Deliverable` (type, reviewer, status, attachment, overdue)
- Funding Party shape on `PMO Donor` (party type, ERPNext Customer/Supplier links, contacts child)
- Child DocTypes: Agreement Project Link, Agreement Condition, Funding Party Contact

### Changed

- Grants / CSR workspaces point at typed Agreement lists; dormant twin create removed for normal roles
- Portfolio Company required; Entity hidden on Portfolio / Project live path
- Agreement, Proposal, and Deliverable forms use multi-column functional sections

### Fixed

- Agreement↔Project Company match and one-Agreement-per-Project validation

### Internal

- Patch `migrate_u3_funding_foundation` copies legacy donor/project/amount and standalone budget rows into U3 fields
- Patch `migrate_u3_funding_foundation` ignores mandatory on legacy Agreement/Donor/Project saves so migrate completes on sparse data

