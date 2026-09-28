import frappe
from frappe.model.document import Document
from frappe.utils import flt


class PMOProject(Document):
	def _sync_status_from_workflow(self):
		if getattr(self, "workflow_state", None) and hasattr(self, "status"):
			self.status = self.workflow_state

	def validate(self):
		self._sync_status_from_workflow()
		self._validate_dates()
		self._validate_amounts()
		self._validate_hierarchy()
		self._validate_erpnext_project()
		self._compute_budget_line_variance()

	def _validate_dates(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			frappe.throw("End Date cannot be earlier than Start Date.")

	def _validate_amounts(self):
		if self.approved_budget is not None and flt(self.approved_budget) < 0:
			frappe.throw("Approved Budget cannot be negative.")
		if self.actual_cost is not None and flt(self.actual_cost) < 0:
			frappe.throw("Actual Cost cannot be negative.")
		if self.percent_complete is not None and not 0 <= flt(self.percent_complete) <= 100:
			frappe.throw("Percent Complete must be between 0 and 100.")

	def _validate_hierarchy(self):
		if self.program and frappe.db.exists("PMO Program", self.program):
			parent = frappe.db.get_value(
				"PMO Program", self.program, ["company", "business_unit", "portfolio"], as_dict=True
			)
			for field in ("company", "business_unit"):
				if getattr(self, field, None) and parent.get(field) and getattr(self, field) != parent.get(field):
					frappe.throw(f"Project {field.replace('_', ' ').title()} must match the selected Programme.")
			if self.portfolio and parent.get("portfolio") and self.portfolio != parent.get("portfolio"):
				frappe.throw("Project Portfolio must match the Programme Portfolio.")

		if self.portfolio and frappe.db.exists("PMO Portfolio", self.portfolio):
			parent = frappe.db.get_value(
				"PMO Portfolio", self.portfolio, ["company", "business_unit"], as_dict=True
			)
			for field in ("company", "business_unit"):
				if getattr(self, field, None) and parent.get(field) and getattr(self, field) != parent.get(field):
					frappe.throw(f"Project {field.replace('_', ' ').title()} must match the selected Portfolio.")

	def _validate_erpnext_project(self):
		if not self.erpnext_project or not frappe.db.exists("Project", self.erpnext_project):
			return
		erp_company = frappe.db.get_value("Project", self.erpnext_project, "company")
		if self.company and erp_company and self.company != erp_company:
			frappe.throw("PMO Project Company must match the linked ERPNext Project Company.")

	def _compute_budget_line_variance(self):
		for row in self.get("budget_lines") or []:
			approved = flt(row.revised_amount) if row.revised_amount not in (None, "") else flt(row.approved_amount)
			utilized = flt(row.utilized_amount)
			row.variance = approved - utilized
			row.variance_percent = (row.variance / approved * 100) if approved else 0


@frappe.whitelist()
def get_agreement_for_project(project):
	frappe.has_permission("PMO Project", "read", project, throw=True)
	agreement_name = frappe.db.get_value(
		"PMO Agreement Project Link",
		{"project": project, "parenttype": "PMO Grant"},
		"parent",
	)
	if not agreement_name:
		return None
	return frappe.db.get_value(
		"PMO Grant",
		agreement_name,
		["name", "grant_name", "agreement_type", "status", "company"],
		as_dict=True,
	)


@frappe.whitelist()
def link_project_to_agreement(project, agreement):
	frappe.has_permission("PMO Project", "write", project, throw=True)
	frappe.has_permission("PMO Grant", "write", agreement, throw=True)

	project_company = frappe.db.get_value("PMO Project", project, "company")
	agreement_doc = frappe.get_doc("PMO Grant", agreement)
	if project_company and agreement_doc.company and project_company != agreement_doc.company:
		frappe.throw("Project Company must match Agreement Company.")

	if any(row.project == project for row in agreement_doc.projects):
		return agreement

	agreement_doc.append("projects", {"project": project})
	agreement_doc.save()
	return agreement


@frappe.whitelist()
def make_agreement_from_project(project, grant_name, agreement_type, funding_party):
	frappe.has_permission("PMO Project", "write", project, throw=True)
	frappe.has_permission("PMO Grant", "create", throw=True)

	existing = get_agreement_for_project(project)
	if existing:
		frappe.throw(f"Project is already linked to Agreement {existing.name}.")

	project_doc = frappe.get_doc("PMO Project", project)
	if not project_doc.company:
		frappe.throw("Project must have a Company before creating an Agreement.")

	agreement = frappe.get_doc(
		{
			"doctype": "PMO Grant",
			"grant_name": grant_name or project_doc.project_title,
			"agreement_type": agreement_type or "Grant",
			"company": project_doc.company,
			"funding_party": funding_party,
			"status": "Draft",
			"funding_source": project_doc.funding_source,
			"projects": [{"project": project}],
		}
	)
	agreement.insert()
	return agreement.name
