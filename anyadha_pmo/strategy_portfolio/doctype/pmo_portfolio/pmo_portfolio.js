frappe.ui.form.on("PMO Portfolio", {
	refresh(frm) {
		render_linked_projects(frm);
	},
});

function render_linked_projects(frm) {
	if (frm.is_new() || !frm.doc.name) {
		frm.get_field("linked_projects_html").$wrapper.html(
			"<p class='text-muted'>Save the Portfolio to see linked Projects.</p>"
		);
		return;
	}
	frappe.call({
		method: "anyadha_pmo.strategy_portfolio.doctype.pmo_portfolio.pmo_portfolio.get_linked_projects_html",
		args: { portfolio: frm.doc.name },
		callback(r) {
			frm.get_field("linked_projects_html").$wrapper.html(r.message || "");
		},
	});
}
