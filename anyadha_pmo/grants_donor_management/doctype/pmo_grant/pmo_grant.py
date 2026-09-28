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


def _get_linked_projects(agreement_name):
	return frappe.get_all(
		"PMO Agreement Project Link",
		filters={"parent": agreement_name, "parenttype": "PMO Grant"},
		pluck="project",
	)


@frappe.whitelist()
def get_case_context(agreement):
	frappe.has_permission("PMO Grant", "read", agreement, throw=True)
	doc = frappe.get_doc("PMO Grant", agreement)
	projects = [row.project for row in doc.projects if row.project]
	open_deliverable_count = 0
	if projects:
		open_deliverable_count = frappe.db.count(
			"PMO Project Deliverable",
			{
				"project": ("in", projects),
				"status": ("not in", ["Accepted", "Closed", "Rejected"]),
			},
		)

	proposal_title = None
	if doc.proposal:
		proposal_title = frappe.db.get_value("PMO Proposal", doc.proposal, "proposal_title") or doc.proposal

	return {
		"project_count": len(projects),
		"projects": projects,
		"open_deliverable_count": open_deliverable_count,
		"proposal_title": proposal_title,
	}


@frappe.whitelist()
def make_project_from_agreement(agreement):
	frappe.has_permission("PMO Grant", "write", agreement, throw=True)
	frappe.has_permission("PMO Project", "create", throw=True)

	doc = frappe.get_doc("PMO Grant", agreement)
	if not doc.company:
		frappe.throw("Agreement must have a Company before creating a Project.")

	project = frappe.get_doc(
		{
			"doctype": "PMO Project",
			"project_title": f"{doc.grant_name} — Project",
			"company": doc.company,
			"status": "Draft",
			"funding_source": doc.funding_source,
		}
	)
	project.insert()

	doc.append("projects", {"project": project.name})
	doc.save()

	return project.name


@frappe.whitelist()
def make_deliverable_from_agreement(agreement, project=None):
	frappe.has_permission("PMO Grant", "read", agreement, throw=True)
	frappe.has_permission("PMO Project Deliverable", "create", throw=True)

	projects = _get_linked_projects(agreement)
	if not projects:
		frappe.throw("Link at least one Project on this Agreement before creating a Deliverable.")

	if project:
		if project not in projects:
			frappe.throw(f"Project {project} is not linked to Agreement {agreement}.")
	elif len(projects) == 1:
		project = projects[0]
	else:
		frappe.throw("Choose which linked Project this Deliverable belongs to.")

	agreement_name = frappe.db.get_value("PMO Grant", agreement, "grant_name") or agreement
	deliverable = frappe.get_doc(
		{
			"doctype": "PMO Project Deliverable",
			"project": project,
			"deliverable": f"{agreement_name} — Deliverable",
			"deliverable_type": "Milestone",
			"status": "Draft",
		}
	)
	deliverable.insert()
	return deliverable.name
