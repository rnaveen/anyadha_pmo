# Copyright (c) 2026, Anyadha and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


def _ensure_company(name="U3 Test Company"):
	if frappe.db.exists("Company", name):
		return name
	company = frappe.get_doc(
		{
			"doctype": "Company",
			"company_name": name,
			"abbr": "U3T",
			"default_currency": "INR",
			"country": "India",
		}
	)
	company.insert(ignore_permissions=True)
	return company.name


def _ensure_funding_party(name="U3 Test Funder"):
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
					"email": "funder@example.com",
					"role": "Finance",
					"is_primary": 1,
				}
			],
		}
	)
	party.insert(ignore_permissions=True)
	return party.name


class IntegrationTestPMOGrantFundingSpine(IntegrationTestCase):
	def test_agreement_project_budget_deliverable_happy_path(self):
		company = _ensure_company()
		party = _ensure_funding_party()

		project = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"project_title": "U3 Spine Project",
				"company": company,
				"status": "Draft",
				"budget_lines": [
					{
						"budget_head": "Personnel",
						"approved_amount": 100000,
						"utilized_amount": 10000,
					}
				],
				"funder_lines": [
					{
						"funding_party": party,
						"contribution_type": "External",
						"amount": 100000,
						"restriction_note": "Restricted to personnel",
					}
				],
			}
		)
		project.insert(ignore_permissions=True)
		self.assertEqual(project.budget_lines[0].variance, 90000)

		agreement = frappe.get_doc(
			{
				"doctype": "PMO Grant",
				"grant_name": "U3 Grant Agreement",
				"agreement_type": "Grant",
				"company": company,
				"funding_party": party,
				"contracted_total": 100000,
				"status": "Draft",
				"projects": [{"project": project.name}],
			}
		)
		agreement.insert(ignore_permissions=True)
		self.assertEqual(agreement.projects[0].project, project.name)

		deliverable = frappe.get_doc(
			{
				"doctype": "PMO Project Deliverable",
				"project": project.name,
				"deliverable": "Q1 UC",
				"deliverable_type": "UC",
				"status": "Draft",
			}
		)
		deliverable.insert(ignore_permissions=True)
		self.assertEqual(deliverable.deliverable_type, "UC")

	def test_company_mismatch_rejected(self):
		company_a = _ensure_company("U3 Company A")
		if not frappe.db.exists("Company", "U3 Company B"):
			frappe.get_doc(
				{
					"doctype": "Company",
					"company_name": "U3 Company B",
					"abbr": "U3B",
					"default_currency": "INR",
					"country": "India",
				}
			).insert(ignore_permissions=True)
		party = _ensure_funding_party("U3 Mismatch Funder")

		project = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"project_title": "U3 Other Company Project",
				"company": "U3 Company B",
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		agreement = frappe.get_doc(
			{
				"doctype": "PMO Grant",
				"grant_name": "U3 Mismatch Agreement",
				"agreement_type": "CSR",
				"company": company_a,
				"funding_party": party,
				"projects": [{"project": project.name}],
			}
		)
		self.assertRaises(frappe.ValidationError, agreement.insert)

	def test_dormant_twins_no_create_for_grants_manager(self):
		meta = frappe.get_meta("PMO CSR Agreement")
		perm = next(p for p in meta.permissions if p.role == "CSR Manager")
		self.assertFalse(perm.create)

		grant_meta = frappe.get_meta("PMO Grant Agreement")
		gperm = next(p for p in grant_meta.permissions if p.role == "Grants Manager")
		self.assertFalse(gperm.create)
