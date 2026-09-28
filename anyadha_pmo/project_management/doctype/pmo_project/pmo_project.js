frappe.ui.form.on("PMO Project", {
	refresh(frm) {
		if (frm.is_new()) {
			return;
		}
		frm.trigger("render_agreement_strip");
	},

	render_agreement_strip(frm) {
		frappe.call({
			method:
				"anyadha_pmo.project_management.doctype.pmo_project.pmo_project.get_agreement_for_project",
			args: { project: frm.doc.name },
			callback(r) {
				const agreement = r.message;
				if (agreement) {
					anyadha_pmo.case_hub.set_status_strip(frm, [
						frm.doc.status,
						frm.doc.company,
						__("Agreement: {0}", [agreement.grant_name || agreement.name]),
					]);
					anyadha_pmo.case_hub.add_case_button(frm, "Open Agreement", () => {
						anyadha_pmo.case_hub.open_doc("PMO Grant", agreement.name);
					});
					return;
				}

				anyadha_pmo.case_hub.set_status_strip(frm, [
					frm.doc.status,
					frm.doc.company,
					__("No Agreement linked"),
				]);

				anyadha_pmo.case_hub.add_case_button(frm, "Link Agreement", () => {
					frappe.prompt(
						{
							label: __("Agreement"),
							fieldname: "agreement",
							fieldtype: "Link",
							options: "PMO Grant",
							reqd: 1,
							get_query: () => ({
								filters: {
									company: frm.doc.company,
								},
							}),
						},
						(values) => {
							frappe.call({
								method:
									"anyadha_pmo.project_management.doctype.pmo_project.pmo_project.link_project_to_agreement",
								args: {
									project: frm.doc.name,
									agreement: values.agreement,
								},
								freeze: true,
								callback() {
									frm.reload_doc();
								},
							});
						},
						__("Link Agreement")
					);
				});

				anyadha_pmo.case_hub.add_case_button(frm, "Create Agreement", () => {
					frappe.prompt(
						[
							{
								label: __("Agreement Name"),
								fieldname: "grant_name",
								fieldtype: "Data",
								default: frm.doc.project_title,
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
							{
								label: __("Funding Party"),
								fieldname: "funding_party",
								fieldtype: "Link",
								options: "PMO Donor",
								reqd: 1,
							},
						],
						(values) => {
							frappe.call({
								method:
									"anyadha_pmo.project_management.doctype.pmo_project.pmo_project.make_agreement_from_project",
								args: {
									project: frm.doc.name,
									grant_name: values.grant_name,
									agreement_type: values.agreement_type,
									funding_party: values.funding_party,
								},
								freeze: true,
								callback(r) {
									if (r.message) {
										anyadha_pmo.case_hub.open_doc("PMO Grant", r.message);
									}
								},
							});
						},
						__("Create Agreement")
					);
				});
			},
		});
	},
});
