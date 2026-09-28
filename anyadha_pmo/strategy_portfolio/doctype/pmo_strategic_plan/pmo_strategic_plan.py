import frappe
from frappe.model.document import Document


class PMOStrategicPlan(Document):
	def validate(self):
		self._sync_status_from_workflow()
		self._validate_period()
		self._validate_version()
		self._validate_approval()
		self._validate_parent_strategic_plan()

	def _sync_status_from_workflow(self):
		if getattr(self, "workflow_state", None) and hasattr(self, "status"):
			self.status = self.workflow_state

	def _validate_period(self):
		if self.period_from and self.period_to and self.period_from > self.period_to:
			frappe.throw("Period To cannot be earlier than Period From.")

	def _validate_version(self):
		if self.version is not None and self.version < 1:
			frappe.throw("Version must be at least 1.")

	def _validate_approval(self):
		if self.status == "Approved" and not self.approved_by:
			frappe.throw("Approved By is required when the Strategic Plan is Approved.")

	def _validate_parent_strategic_plan(self):
		if not self.parent_strategic_plan:
			return
		if self.name and self.parent_strategic_plan == self.name:
			frappe.throw("A Strategic Plan cannot be its own parent.")
		if not frappe.db.exists("PMO Strategic Plan", self.parent_strategic_plan):
			return

		# Parent may be another Company (holding cascade). Block cycles only.
		visited = set()
		if self.name:
			visited.add(self.name)
		current = self.parent_strategic_plan
		while current:
			if current in visited:
				frappe.throw("Parent Strategic Plan link creates a cycle.")
			visited.add(current)
			current = frappe.db.get_value("PMO Strategic Plan", current, "parent_strategic_plan")
