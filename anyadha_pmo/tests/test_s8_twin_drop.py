from pathlib import Path

import frappe
from frappe.tests.utils import FrappeTestCase

from anyadha_pmo.patches.v2_2.drop_s8_funding_twins import S8_FUNDING_TWINS, non_empty_twins


class TestS8TwinDrop(FrappeTestCase):
	def test_twin_list_is_funding_only(self):
		# IRM DocTypes stay for S7 hard-retire — must not be in S8 list.
		for name in S8_FUNDING_TWINS:
			self.assertFalse(name.startswith("PMO Compliance"))
			self.assertFalse(name.startswith("PMO Enterprise Risk"))
			self.assertFalse(name.startswith("PMO Audit"))

	def test_twin_modules_removed_from_app(self):
		app_root = Path(frappe.get_app_path("anyadha_pmo"))
		for doctype in S8_FUNDING_TWINS:
			folder = doctype.lower().replace(" ", "_")
			matches = list(app_root.glob(f"**/doctype/{folder}"))
			self.assertEqual(matches, [], f"S8 twin folder still in app: {doctype}")

	def test_canonical_path_doctypes_remain(self):
		for doctype in (
			"PMO Grant",
			"PMO Project",
			"PMO Project Budget Line",
			"PMO Project Deliverable",
			"PMO Donor",
		):
			self.assertTrue(frappe.db.exists("DocType", doctype), doctype)

	def test_non_empty_helper_after_db_drop(self):
		# Passes once migrate has run drop_s8_funding_twins; skip while DB still has twins.
		if any(frappe.db.exists("DocType", dt) for dt in S8_FUNDING_TWINS):
			self.skipTest("S8 DB drop not applied yet — run bench migrate")
		self.assertEqual(non_empty_twins(), [])
