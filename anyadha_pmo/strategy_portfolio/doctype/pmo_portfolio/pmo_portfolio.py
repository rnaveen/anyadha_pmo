import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class PMOPortfolio(Document):
	def validate(self):
		self._sync_status_from_workflow()
		self._validate_dates()
		self._validate_budget()
		self._validate_strategic_plan_company()

	def get_linked_projects(self):
		"""Same-Company Projects that nest under this Portfolio via Project.portfolio."""
		if not self.name or not self.company:
			return []
		return frappe.get_all(
			"PMO Project",
			filters={"portfolio": self.name, "company": self.company},
			fields=["name", "project_title", "status", "program"],
			order_by="project_title asc",
		)

	def _sync_status_from_workflow(self):
		if getattr(self, "workflow_state", None) and hasattr(self, "status"):
			self.status = self.workflow_state

	def _validate_dates(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			frappe.throw("End Date cannot be earlier than Start Date.")

	def _validate_budget(self):
		if self.approved_budget is not None and self.approved_budget < 0:
			frappe.throw("Approved Budget cannot be negative.")

	def _validate_strategic_plan_company(self):
		if not self.strategic_plan or not frappe.db.exists("PMO Strategic Plan", self.strategic_plan):
			return
		plan_company = frappe.db.get_value("PMO Strategic Plan", self.strategic_plan, "company")
		if self.company and plan_company and self.company != plan_company:
			frappe.throw(
				f"Portfolio Company ({self.company}) must match Strategic Plan Company ({plan_company})."
			)


@frappe.whitelist()
def get_linked_projects_html(portfolio):
	doc = frappe.get_doc("PMO Portfolio", portfolio)
	projects = doc.get_linked_projects()
	if not projects:
		return "<p class='text-muted'>No Projects linked yet. Set Portfolio on a Project in this Company.</p>"

	rows = []
	for project in projects:
		title = frappe.utils.escape_html(project.project_title or project.name)
		status = frappe.utils.escape_html(project.status or "")
		program = frappe.utils.escape_html(project.program or "—")
		link = get_link_to_form("PMO Project", project.name, title)
		rows.append(f"<tr><td>{link}</td><td>{status}</td><td>{program}</td></tr>")

	return (
		"<table class='table table-bordered'>"
		"<thead><tr><th>Project</th><th>Status</th><th>Programme</th></tr></thead>"
		f"<tbody>{''.join(rows)}</tbody></table>"
	)
