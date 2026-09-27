frappe.provide("frappe.ui.form");

frappe.ui.form.on("PMO Grant", {
	refresh(frm) {
		frm.set_df_property("grant_name", "label", "Agreement Name");
	},
});
