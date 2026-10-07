frappe.provide("frappe.ui.form");

frappe.ui.form.on("PMO Grant", {
	refresh(frm) {
		frm.set_df_property("grant_name", "label", "Agreement Name");
		if (frm.is_new()) {
			return;
		}
		frm.trigger("render_case_hub");
	},

	render_case_hub(frm) {
		frappe.call({
			method: "anyadha_pmo.grants_donor_management.doctype.pmo_grant.pmo_grant.get_case_context",
			args: { agreement: frm.doc.name },
			callback(r) {
				const ctx = r.message || {};
				anyadha_pmo.case_hub.set_status_strip(frm, [
					frm.doc.agreement_type,
					frm.doc.status,
					frm.doc.company,
					frm.doc.funding_party,
					__("Projects: {0}", [ctx.project_count || 0]),
					__("Open deliverables: {0}", [ctx.open_deliverable_count || 0]),
					ctx.proposal_title ? __("Proposal: {0}", [ctx.proposal_title]) : null,
				]);
			},
		});

		anyadha_pmo.case_hub.add_case_button(frm, "Create Project", () => {
			frappe.call({
				method: "anyadha_pmo.grants_donor_management.doctype.pmo_grant.pmo_grant.make_project_from_agreement",
				args: { agreement: frm.doc.name },
				freeze: true,
				callback(r) {
					if (!r.message) {
						return;
					}
					frm.reload_doc();
					anyadha_pmo.case_hub.open_doc("PMO Project", r.message);
				},
			});
		});

		anyadha_pmo.case_hub.add_case_button(frm, "Create Deliverable", () => {
			const projects = (frm.doc.projects || []).map((row) => row.project).filter(Boolean);
			if (!projects.length) {
				frappe.msgprint(__("Link at least one Project on this Agreement first."));
				return;
			}
			const run = (project) => {
				frappe.call({
					method:
						"anyadha_pmo.grants_donor_management.doctype.pmo_grant.pmo_grant.make_deliverable_from_agreement",
					args: { agreement: frm.doc.name, project },
					freeze: true,
					callback(r) {
						if (r.message) {
							anyadha_pmo.case_hub.open_doc("PMO Project Deliverable", r.message);
						}
					},
				});
			};
			if (projects.length === 1) {
				run(projects[0]);
				return;
			}
			frappe.prompt(
				{
					label: __("Project"),
					fieldname: "project",
					fieldtype: "Select",
					options: projects.join("\n"),
					reqd: 1,
				},
				(values) => run(values.project),
				__("Create Deliverable")
			);
		});

		if (frm.doc.proposal) {
			anyadha_pmo.case_hub.add_case_button(frm, "Open Proposal", () => {
				anyadha_pmo.case_hub.open_doc("PMO Proposal", frm.doc.proposal);
			});
		}

		if (frm.doc.funding_party) {
			anyadha_pmo.case_hub.add_case_button(frm, "Funding Party", () => {
				anyadha_pmo.case_hub.open_doc("PMO Donor", frm.doc.funding_party);
			});
		}

		const projects = (frm.doc.projects || []).map((row) => row.project).filter(Boolean);
		if (projects.length) {
			anyadha_pmo.case_hub.add_case_button(frm, "Deliverables", () => {
				anyadha_pmo.case_hub.open_list("PMO Project Deliverable", {
					project: ["in", projects],
				});
			});
		}

		frm.trigger("render_seam_assist");
	},

	render_seam_assist(frm) {
		if (!frappe.model.can_read("GRC Obligation")) {
			return;
		}
		frappe.call({
			method: "grc_core.grc.seam.agreement_obligations.get_seam_flags",
			callback(r) {
				const flags = r.message || {};
				if (!flags.suggest) {
					return;
				}
				anyadha_pmo.case_hub.add_case_button(frm, "Suggest Obligations", () => {
					frappe.call({
						method:
							"grc_core.grc.seam.agreement_obligations.suggest_obligations_from_agreement",
						args: { agreement: frm.doc.name },
						freeze: true,
						callback(resp) {
							const result = resp.message || {};
							const created = result.created || [];
							const skipped = result.skipped || [];
							if (created.length) {
								frappe.show_alert({
									message: __("Created {0} Obligation(s)", [created.length]),
									indicator: "green",
								});
								anyadha_pmo.case_hub.open_doc("GRC Obligation", created[0]);
								return;
							}
							if (skipped.length) {
								frappe.msgprint(
									__("No new Obligations — conditions already linked.")
								);
								return;
							}
							frappe.msgprint(__("Add Agreement conditions before suggesting Obligations."));
						},
					});
				});
			},
		});
	},
});
