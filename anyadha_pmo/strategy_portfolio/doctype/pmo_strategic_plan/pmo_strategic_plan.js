frappe.ui.form.on("PMO Strategic Plan", {
	setup(frm) {
		frm.set_query("parent_strategic_plan", () => ({
			filters: frm.doc.name ? { name: ["!=", frm.doc.name] } : {},
		}));
	},
});
