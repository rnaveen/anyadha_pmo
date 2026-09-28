import frappe
from frappe.model.document import Document


class PMOProgram(Document):
	def validate(self):
		self._sync_status_from_workflow()
		self._validate_dates()
		self._validate_budget()
		self._validate_portfolio_company()

	def _sync_status_from_workflow(self):
		if getattr(self, "workflow_state", None) and hasattr(self, "status"):
			self.status = self.workflow_state

	def _validate_dates(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			frappe.throw("End Date cannot be earlier than Start Date.")

	def _validate_budget(self):
		if self.approved_budget is not None and self.approved_budget < 0:
			frappe.throw("Approved Budget cannot be negative.")

	def _validate_portfolio_company(self):
		if not self.portfolio or not frappe.db.exists("PMO Portfolio", self.portfolio):
			return
		portfolio = frappe.db.get_value(
			"PMO Portfolio", self.portfolio, ["company", "business_unit"], as_dict=True
		)
		for field in ("company", "business_unit"):
			if getattr(self, field, None) and portfolio.get(field) and getattr(self, field) != portfolio.get(field):
				frappe.throw(f"Programme {field.replace('_', ' ').title()} must match the selected Portfolio.")
		if not self.company and portfolio.get("company"):
			self.company = portfolio.get("company")
