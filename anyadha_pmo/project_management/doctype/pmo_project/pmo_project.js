frappe.ui.form.on("PMO Project", {
	setup(frm) {
		frm.set_query("portfolio", () => {
			if (!frm.doc.company) return {};
			return { filters: { company: frm.doc.company } };
		});
		frm.set_query("program", () => {
			const filters = {};
			if (frm.doc.company) filters.company = frm.doc.company;
			if (frm.doc.portfolio) filters.portfolio = frm.doc.portfolio;
			return { filters };
		});
	},
});
