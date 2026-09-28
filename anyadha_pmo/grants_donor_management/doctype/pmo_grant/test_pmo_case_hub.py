# Copyright (c) 2026, Anyadha and Contributors
# See license.txt

import frappe
from frappe.tests import UnitTestCase

from anyadha_pmo.grants_donor_management.doctype.pmo_grant.pmo_grant import (
	get_case_context,
	make_deliverable_from_agreement,
	make_project_from_agreement,
)
from anyadha_pmo.project_management.doctype.pmo_project.pmo_project import (
	get_agreement_for_project,
	link_project_to_agreement,
	make_agreement_from_project,
)
from anyadha_pmo.proposal_dpr.doctype.pmo_proposal.pmo_proposal import (
	get_agreements_for_proposal,
	make_agreement_from_proposal,
)


def _company():
	existing = frappe.db.get_value("Company", {}, "name", order_by="creation asc")
	if existing:
		return existing
	frappe.throw("Need at least one Company on the site to run case hub tests.")


def _funding_party(name="U3 Hub Funder"):
	if frappe.db.exists("PMO Donor", name):
		return name
	party = frappe.get_doc(
		{
			"doctype": "PMO Donor",
			"donor_name": name,
			"party_type": "Donor",
			"contacts": [
				{
					"contact_name": "Primary Contact",
					"email": "hub-funder@example.com",
					"role": "Finance",
					"is_primary": 1,
				}
			],
		}
	)
	party.insert(ignore_permissions=True)
	return party.name


class UnitTestPMOCaseHub(UnitTestCase):
	def test_make_project_and_deliverable_from_agreement(self):
		company = _company()
		party = _funding_party()

		agreement = frappe.get_doc(
			{
				"doctype": "PMO Grant",
				"grant_name": "U3 Hub Agreement",
				"agreement_type": "Grant",
				"company": company,
				"funding_party": party,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		project_name = make_project_from_agreement(agreement.name)
		agreement.reload()
		self.assertEqual(agreement.projects[0].project, project_name)

		ctx = get_case_context(agreement.name)
		self.assertEqual(ctx["project_count"], 1)
		self.assertEqual(ctx["open_deliverable_count"], 0)

		deliverable_name = make_deliverable_from_agreement(agreement.name, project_name)
		self.assertTrue(frappe.db.exists("PMO Project Deliverable", deliverable_name))
		self.assertEqual(
			frappe.db.get_value("PMO Project Deliverable", deliverable_name, "project"),
			project_name,
		)

		ctx = get_case_context(agreement.name)
		self.assertEqual(ctx["open_deliverable_count"], 1)

	def test_promote_proposal_to_agreement(self):
		company = _company()
		party = _funding_party()

		proposal = frappe.get_doc(
			{
				"doctype": "PMO Proposal",
				"proposal_title": "U3 Hub Proposal",
				"donor": party,
				"requested_amount": 50000,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		agreement_name = make_agreement_from_proposal(
			proposal.name, company=company, agreement_type="CSR"
		)
		agreement = frappe.get_doc("PMO Grant", agreement_name)
		self.assertEqual(agreement.proposal, proposal.name)
		self.assertEqual(agreement.funding_party, party)
		self.assertEqual(agreement.agreement_type, "CSR")
		self.assertEqual(agreement.contracted_total, 50000)

		linked = get_agreements_for_proposal(proposal.name)
		self.assertEqual(len(linked), 1)
		self.assertEqual(linked[0].name, agreement_name)

	def test_project_link_and_create_agreement(self):
		company = _company()
		party = _funding_party()

		project = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"project_title": "U3 Hub Standalone Project",
				"company": company,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		self.assertIsNone(get_agreement_for_project(project.name))

		agreement_name = make_agreement_from_project(
			project.name,
			grant_name="U3 From Project",
			agreement_type="Grant",
			funding_party=party,
		)
		linked = get_agreement_for_project(project.name)
		self.assertEqual(linked.name, agreement_name)

		project_b = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"project_title": "U3 Hub Link Project",
				"company": company,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		link_project_to_agreement(project_b.name, agreement_name)
		self.assertEqual(get_agreement_for_project(project_b.name).name, agreement_name)
