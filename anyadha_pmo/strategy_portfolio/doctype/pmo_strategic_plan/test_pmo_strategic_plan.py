# Copyright (c) 2026, Anyadha and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


def _ensure_company(name, abbr):
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


class IntegrationTestPMOStrategicPlan(IntegrationTestCase):
	def test_strategy_saves_with_company_without_parent(self):
		company = _ensure_company("U4 Strategy Company", "U4S")
		plan = frappe.get_doc(
			{
				"doctype": "PMO Strategic Plan",
				"plan_name": "U4 Independent Plan",
				"company": company,
				"status": "Draft",
			}
		)
		plan.insert(ignore_permissions=True)
		self.assertEqual(plan.company, company)
		self.assertFalse(plan.parent_strategic_plan)

	def test_optional_parent_link_and_holding_cascade(self):
		holding = _ensure_company("U4 Holding Company", "U4H")
		child = _ensure_company("U4 Child Company", "U4C")

		parent = frappe.get_doc(
			{
				"doctype": "PMO Strategic Plan",
				"plan_name": "U4 Holding Plan",
				"company": holding,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)

		child_plan = frappe.get_doc(
			{
				"doctype": "PMO Strategic Plan",
				"plan_name": "U4 Child Plan",
				"company": child,
				"parent_strategic_plan": parent.name,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)
		self.assertEqual(child_plan.parent_strategic_plan, parent.name)

	def test_self_parent_rejected(self):
		company = _ensure_company("U4 Strategy Company", "U4S")
		plan = frappe.get_doc(
			{
				"doctype": "PMO Strategic Plan",
				"plan_name": "U4 Cycle Plan",
				"company": company,
				"status": "Draft",
			}
		).insert(ignore_permissions=True)
		plan.parent_strategic_plan = plan.name
		self.assertRaises(frappe.ValidationError, plan.save)
