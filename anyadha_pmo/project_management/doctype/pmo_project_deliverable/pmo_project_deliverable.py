import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class PMOProjectDeliverable(Document):
	def before_validate(self):
		self._fold_legacy_acceptance()
		self._set_overdue()

	def _fold_legacy_acceptance(self):
		if self.acceptance_status and (not self.status or self.status == "Draft"):
			mapping = {
				"Pending": "Pending",
				"Accepted": "Accepted",
				"Rejected": "Rejected",
			}
			self.status = mapping.get(self.acceptance_status, self.status)

	def _set_overdue(self):
		if self.due_date and self.status not in ("Accepted", "Closed", "Rejected"):
			self.is_overdue = 1 if getdate(self.due_date) < getdate(today()) else 0
			if self.is_overdue and self.status in ("Draft", "Pending", "Submitted"):
				self.status = "Overdue"
		else:
			self.is_overdue = 0
