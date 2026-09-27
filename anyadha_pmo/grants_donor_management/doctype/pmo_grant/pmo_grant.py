import frappe
from frappe.model.document import Document


class PMOGrant(Document):
	def before_validate(self):
		self._migrate_legacy_values()

	def validate(self):
		self._validate_dates()
		self._validate_projects()

	def _migrate_legacy_values(self):
		if not self.funding_party and self.donor:
			self.funding_party = self.donor
		if self.contracted_total in (None, "") and self.grant_amount not in (None, ""):
			self.contracted_total = self.grant_amount
		if self.project and not any(row.project == self.project for row in self.projects):
			self.append("projects", {"project": self.project})

	def _validate_dates(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			frappe.throw("End Date cannot be earlier than Start Date.")

	def _validate_projects(self):
		seen = set()
		for row in self.projects:
			if not row.project:
				continue
			if row.project in seen:
				frappe.throw(f"Project {row.project} is linked more than once on this Agreement.")
			seen.add(row.project)

			project_company = frappe.db.get_value("PMO Project", row.project, "company")
			if self.company and project_company and self.company != project_company:
				frappe.throw(
					f"Project {row.project} Company ({project_company}) must match Agreement Company ({self.company})."
				)

			other = frappe.db.sql(
				"""
				select parent
				from `tabPMO Agreement Project Link`
				where project = %s and parent != %s
				limit 1
				""",
				(row.project, self.name or ""),
			)
			if other:
				frappe.throw(
					f"Project {row.project} is already linked to Agreement {other[0][0]}."
				)
