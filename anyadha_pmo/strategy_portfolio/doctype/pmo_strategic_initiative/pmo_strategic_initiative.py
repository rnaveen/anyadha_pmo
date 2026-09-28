import frappe
from frappe.model.document import Document


class PMOStrategicInitiative(Document):
	def validate(self):
		self._sync_status_from_workflow()
		self._validate_dates()
		self._validate_strategic_plan_company()

	def _sync_status_from_workflow(self):
		if getattr(self, "workflow_state", None) and hasattr(self, "status"):
			self.status = self.workflow_state

	def _validate_dates(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			frappe.throw("End Date cannot be earlier than Start Date.")

	def _validate_strategic_plan_company(self):
		if not self.strategic_plan or not frappe.db.exists("PMO Strategic Plan", self.strategic_plan):
			return
		plan_company = frappe.db.get_value("PMO Strategic Plan", self.strategic_plan, "company")
		if self.company and plan_company and self.company != plan_company:
			frappe.throw(
				f"Initiative Company ({self.company}) must match Strategic Plan Company ({plan_company})."
			)
		if not self.company and plan_company:
			self.company = plan_company
