"""S8 — drop dormant Grant/CSR twin DocTypes after empty-check.

Set site_config ``s8_force_drop_funding_twins: 1`` to wipe remaining
scaffold rows and drop (owner-stated unused registers). Without that flag,
non-empty DocTypes abort the patch.
"""

from __future__ import annotations

import frappe

# FIELD_MAP D3/D6/D8/D9 + spine reporting / fund twins — not PMO IRM (S7).
S8_FUNDING_TWINS = [
	"PMO Grant Agreement",
	"PMO CSR Agreement",
	"PMO CSR Project",
	"PMO CSR Partner",
	"PMO CSR Budget",
	"PMO CSR Compliance",
	"PMO CSR Impact Assessment",
	"PMO CSR Proposal",
	"PMO CSR Utilization",
	"PMO CSR Report",
	"PMO Project Budget",
	"PMO Grant Reporting",
	"PMO Grant Budget",
	"PMO Grant Disbursement",
	"PMO Grant Utilization",
	"PMO Donor Report",
	"PMO Utilization Certificate",
	"PMO Donor Compliance",
	"PMO Fund Reconciliation",
	"PMO Restricted Fund",
]


def non_empty_twins() -> list[tuple[str, int]]:
	found: list[tuple[str, int]] = []
	for doctype in S8_FUNDING_TWINS:
		if not frappe.db.exists("DocType", doctype):
			continue
		if not frappe.db.table_exists(doctype):
			continue
		count = frappe.db.count(doctype)
		if count:
			found.append((doctype, count))
	return found


def execute():
	force = bool(frappe.conf.get("s8_force_drop_funding_twins"))
	remaining = non_empty_twins()
	if remaining and not force:
		detail = ", ".join(f"{name}={count}" for name, count in remaining)
		frappe.throw(
			"S8 twin drop blocked — non-empty DocTypes: "
			f"{detail}. Clear those rows, or set site_config "
			"s8_force_drop_funding_twins=1 to wipe scaffold data and drop."
		)

	for doctype in S8_FUNDING_TWINS:
		if not frappe.db.exists("DocType", doctype):
			continue
		if frappe.db.table_exists(doctype) and frappe.db.count(doctype):
			frappe.db.delete(doctype)
		frappe.delete_doc("DocType", doctype, ignore_missing=True, force=True)
