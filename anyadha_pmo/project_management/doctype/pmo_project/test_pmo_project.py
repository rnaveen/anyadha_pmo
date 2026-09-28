# Copyright (c) 2026, Anyadha and Contributors
# See license.txt

import frappe
from frappe.tests import UnitTestCase


class UnitTestPMOProjectAmounts(UnitTestCase):
	def test_validate_amounts_accepts_string_percent_and_currency(self):
		"""Desk/API often deliver Percent/Currency as strings; must not TypeError."""
		doc = frappe.get_doc(
			{
				"doctype": "PMO Project",
				"percent_complete": "45",
				"approved_budget": "1000",
				"actual_cost": "0",
			}
		)
		doc._validate_amounts()

	def test_validate_amounts_rejects_out_of_range_string_percent(self):
		doc = frappe.get_doc({"doctype": "PMO Project", "percent_complete": "150"})
		with self.assertRaises(frappe.ValidationError):
			doc._validate_amounts()

	def test_validate_amounts_rejects_negative_string_budget(self):
		doc = frappe.get_doc({"doctype": "PMO Project", "approved_budget": "-1"})
		with self.assertRaises(frappe.ValidationError):
			doc._validate_amounts()
