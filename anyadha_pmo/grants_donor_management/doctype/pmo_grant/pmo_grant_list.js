frappe.listview_settings["PMO Grant"] = {
	add_fields: ["agreement_type", "company", "status", "funding_party"],
	get_indicator(doc) {
		const colours = {
			Draft: "gray",
			Open: "blue",
			"In Progress": "orange",
			Approved: "green",
			Completed: "green",
			Closed: "darkgrey",
			Cancelled: "red",
			Rejected: "red",
		};
		return [__(doc.status || "Draft"), colours[doc.status] || "gray", "status,=," + doc.status];
	},
};
