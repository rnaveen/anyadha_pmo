# Copyright (c) 2026, Anyadha and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


def _ensure_company(name="U4 Portfolio Company", abbr="U4P"):
	if frappe.db.exists("Company", name):
		return name
	company = frappe.get_doc(
		{
			"doctype": "Company",
			"company_name": name,
			"abbr": abbr,
			"default_currency": "INR",
			"country": "India",
		}
	)
	company.insert(ignore_permissions=True)
	return company.name


class IntegrationTestPMOPortfolioNesting(IntegrationTestCase):
	def test_portfolio_lists_same_company_projects(self):
		company = _ensure_company()
		other = _ensure_company("U4 Other Portfolio Co", "U4O")

		portfolio = frappe.get_doc(
			{
				"doctype": "PMO Portfolio",
				"portfolio_name": "U4 Delivery Portfolio",
				"company": company,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		linked = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"project_title": "U4 Nested Project",
				"company": company,
				"portfolio": portfolio.name,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		# Same portfolio name would be wrong company — hierarchy blocks on save
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "PMO Project",
					"project_title": "U4 Wrong Company Project",
					"company": other,
					"portfolio": portfolio.name,
					"status": "Draft",
				}
			).insert(ignore_permissions=True)

		names = [row.name for row in portfolio.get_linked_projects()]
		self.assertIn(linked.name, names)
		self.assertEqual(len(names), 1)

	def test_program_optional_on_project(self):
		company = _ensure_company()
		portfolio = frappe.get_doc(
			{
				"doctype": "PMO Portfolio",
				"portfolio_name": "U4 Optional Program Portfolio",
				"company": company,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		project = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"project_title": "U4 Project Without Programme",
				"company": company,
				"portfolio": portfolio.name,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)
		self.assertFalse(project.program)

	def test_program_company_matches_portfolio(self):
		company = _ensure_company()
		other = _ensure_company("U4 Other Portfolio Co", "U4O")
		portfolio = frappe.get_doc(
			{
				"doctype": "PMO Portfolio",
				"portfolio_name": "U4 Program Portfolio",
				"company": company,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "PMO Program",
					"program_name": "U4 Mismatch Programme",
					"company": other,
					"portfolio": portfolio.name,
					"status": "Draft",
				}
			).insert(ignore_permissions=True)
