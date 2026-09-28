frappe.ui.form.on("PMO Proposal", {
	refresh(frm) {
		if (frm.is_new()) {
			return;
		}
		frm.trigger("render_case_hub");
	},

	render_case_hub(frm) {
		frappe.call({
			method:
				"anyadha_pmo.proposal_dpr.doctype.pmo_proposal.pmo_proposal.get_agreements_for_proposal",
			args: { proposal: frm.doc.name },
			callback(r) {
				const agreements = r.message || [];
				anyadha_pmo.case_hub.set_status_strip(frm, [
					frm.doc.status,
					__("Agreements: {0}", [agreements.length]),
				]);

				if (agreements.length === 1) {
					anyadha_pmo.case_hub.add_case_button(frm, "Open Agreement", () => {
						anyadha_pmo.case_hub.open_doc("PMO Grant", agreements[0].name);
					});
				} else if (agreements.length > 1) {
					anyadha_pmo.case_hub.add_case_button(frm, "Open Agreements", () => {
						anyadha_pmo.case_hub.open_list("PMO Grant", { proposal: frm.doc.name });
					});
				}
			},
		});

		anyadha_pmo.case_hub.add_case_button(frm, "Promote to Agreement", () => {
			frappe.prompt(
				[
					{
						label: __("Company"),
						fieldname: "company",
						fieldtype: "Link",
						options: "Company",
						reqd: 1,
					},
					{
						label: __("Agreement Type"),
						fieldname: "agreement_type",
						fieldtype: "Select",
						options: "Grant\nCSR\nGovernment\nCommercial",
						default: "Grant",
						reqd: 1,
					},
				],
				(values) => {
					frappe.call({
						method:
							"anyadha_pmo.proposal_dpr.doctype.pmo_proposal.pmo_proposal.make_agreement_from_proposal",
						args: {
							proposal: frm.doc.name,
							company: values.company,
							agreement_type: values.agreement_type,
						},
						freeze: true,
						callback(r) {
							if (r.message) {
								anyadha_pmo.case_hub.open_doc("PMO Grant", r.message);
							}
						},
					});
				},
				__("Promote to Agreement")
			);
		});
	},
});
