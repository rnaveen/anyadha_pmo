import frappe


def execute():
	"""One-shot: copy legacy Agreement/Project/Funding Party fields into U3 shape."""
	_migrate_agreements()
	_migrate_funding_parties()
	_migrate_project_budgets()


def _migrate_agreements():
	if not frappe.db.has_column("PMO Grant", "funding_party"):
		return

	rows = frappe.db.sql(
		"""
		select name, donor, project, grant_amount, funding_party, contracted_total
		from `tabPMO Grant`
		""",
		as_dict=True,
	)
	for row in rows:
		updates = {}
		if not row.funding_party and row.donor:
			updates["funding_party"] = row.donor
		if row.contracted_total in (None, "") and row.grant_amount not in (None, ""):
			updates["contracted_total"] = row.grant_amount
		if updates:
			frappe.db.set_value("PMO Grant", row.name, updates, update_modified=False)

		if row.project:
			exists = frappe.db.exists(
				"PMO Agreement Project Link", {"parent": row.name, "project": row.project}
			)
			if not exists:
				doc = frappe.get_doc("PMO Grant", row.name)
				doc.append("projects", {"project": row.project})
				doc.flags.ignore_mandatory = True
				doc.save(ignore_permissions=True)


def _migrate_funding_parties():
	if not frappe.db.has_column("PMO Donor", "party_type"):
		return

	frappe.db.sql(
		"""
		update `tabPMO Donor`
		set party_type = 'Donor'
		where ifnull(party_type, '') = ''
		"""
	)

	donors = frappe.get_all(
		"PMO Donor",
		fields=["name", "contact_person", "email", "donor_name"],
	)
	for donor in donors:
		if not (donor.contact_person or donor.email):
			continue
		if frappe.db.exists("PMO Funding Party Contact", {"parent": donor.name}):
			continue
		doc = frappe.get_doc("PMO Donor", donor.name)
		if doc.contacts:
			continue
		doc.append(
			"contacts",
			{
				"contact_name": donor.contact_person or donor.donor_name,
				"email": donor.email,
				"role": "Other",
				"is_primary": 1,
			},
		)
		doc.flags.ignore_mandatory = True
		doc.save(ignore_permissions=True)


def _migrate_project_budgets():
	if not frappe.db.exists("DocType", "PMO Project Budget Line"):
		return

	if not frappe.db.table_exists("PMO Project Budget"):
		return

	budgets = frappe.get_all(
		"PMO Project Budget",
		fields=[
			"name",
			"project",
			"budget_head",
			"approved_amount",
			"revised_amount",
			"utilized_amount",
			"variance",
			"variance_percent",
			"currency",
		],
	)
	by_project = {}
	for row in budgets:
		if not row.project:
			continue
		by_project.setdefault(row.project, []).append(row)

	for project_name, lines in by_project.items():
		if not frappe.db.exists("PMO Project", project_name):
			continue
		doc = frappe.get_doc("PMO Project", project_name)
		if doc.get("budget_lines"):
			continue
		for line in lines:
			doc.append(
				"budget_lines",
				{
					"budget_head": line.budget_head,
					"approved_amount": line.approved_amount,
					"revised_amount": line.revised_amount,
					"utilized_amount": line.utilized_amount,
					"variance": line.variance,
					"variance_percent": line.variance_percent,
					"currency": line.currency,
				},
			)
		doc.flags.ignore_mandatory = True
		doc.save(ignore_permissions=True)
