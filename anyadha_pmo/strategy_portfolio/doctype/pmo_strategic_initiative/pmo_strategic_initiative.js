frappe.ui.form.on("PMO Strategic Initiative", {
	strategic_plan(frm) {
		if (!frm.doc.strategic_plan) return;
		frappe.db.get_value("PMO Strategic Plan", frm.doc.strategic_plan, "company", (r) => {
			if (r && r.company) {
				frm.set_value("company", r.company);
			}
		});
	},
});
