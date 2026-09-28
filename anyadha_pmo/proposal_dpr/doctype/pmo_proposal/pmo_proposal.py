import frappe
from frappe.model.document import Document


class PMOProposal(Document):
	pass


@frappe.whitelist()
def get_agreements_for_proposal(proposal):
	frappe.has_permission("PMO Proposal", "read", proposal, throw=True)
	return frappe.get_all(
		"PMO Grant",
		filters={"proposal": proposal},
		fields=["name", "grant_name", "agreement_type", "status", "company"],
		order_by="modified desc",
	)


@frappe.whitelist()
def make_agreement_from_proposal(proposal, company=None, agreement_type="Grant"):
	frappe.has_permission("PMO Proposal", "read", proposal, throw=True)
	frappe.has_permission("PMO Grant", "create", throw=True)

	doc = frappe.get_doc("PMO Proposal", proposal)
	if not company:
		frappe.throw("Choose a Company for the Agreement.")
	if not doc.donor:
		frappe.throw("Set Donor on the Proposal so it can map to Funding Party.")

	agreement = frappe.get_doc(
		{
			"doctype": "PMO Grant",
			"grant_name": doc.proposal_title or proposal,
			"agreement_type": agreement_type or "Grant",
			"company": company,
			"funding_party": doc.donor,
			"proposal": doc.name,
			"status": "Draft",
			"contracted_total": doc.requested_amount,
		}
	)
	agreement.insert()
	return agreement.name
