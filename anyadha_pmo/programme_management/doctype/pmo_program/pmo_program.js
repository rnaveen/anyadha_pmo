frappe.ui.form.on("PMO Program", {
	portfolio(frm) {
		if (!frm.doc.portfolio) return;
		frappe.db.get_value("PMO Portfolio", frm.doc.portfolio, "company", (r) => {
			if (r && r.company) {
				frm.set_value("company", r.company);
			}
		});
	},
	setup(frm) {
		frm.set_query("portfolio", () => {
			if (!frm.doc.company) return {};
			return { filters: { company: frm.doc.company } };
		});
	},
});
