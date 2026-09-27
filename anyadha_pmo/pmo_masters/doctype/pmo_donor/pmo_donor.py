import frappe
from frappe.model.document import Document


class PMODonor(Document):
	def before_validate(self):
		self._migrate_legacy_contact()

	def validate(self):
		self._validate_primary_contact()

	def _migrate_legacy_contact(self):
		if (self.contact_person or self.email) and not self.contacts:
			self.append(
				"contacts",
				{
					"contact_name": self.contact_person or self.donor_name,
					"email": self.email,
					"role": "Other",
					"is_primary": 1,
				},
			)

	def _validate_primary_contact(self):
		primaries = [row for row in self.contacts if row.is_primary]
		if len(primaries) > 1:
			frappe.throw("Only one primary contact is allowed.")
