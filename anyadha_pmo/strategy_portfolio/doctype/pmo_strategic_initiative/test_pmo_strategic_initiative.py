# Copyright (c) 2026, Anyadha and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


def _ensure_company(name="U4 Initiative Company", abbr="U4I"):
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


class IntegrationTestPMOStrategicInitiative(IntegrationTestCase):
	def test_initiative_company_must_match_plan(self):
		company_a = _ensure_company()
		company_b = _ensure_company("U4 Initiative Company B", "U4IB")
		plan = frappe.get_doc(
			{
				"doctype": "PMO Strategic Plan",
				"plan_name": "U4 Initiative Plan",
				"company": company_a,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "PMO Strategic Initiative",
					"initiative_name": "U4 Mismatch Initiative",
					"company": company_b,
					"strategic_plan": plan.name,
					"status": "Draft",
				}
			).insert(ignore_permissions=True)
