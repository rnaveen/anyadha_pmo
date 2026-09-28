frappe.provide("anyadha_pmo.case_hub");

anyadha_pmo.case_hub.set_status_strip = function (frm, parts) {
	const text = (parts || []).filter(Boolean).join(" · ");
	if (!text) {
		return;
	}
	frm.dashboard.set_headline_alert(text, "blue");
};

anyadha_pmo.case_hub.add_case_button = function (frm, label, action) {
	frm.add_custom_button(__(label), action, __("Case"));
};

anyadha_pmo.case_hub.open_doc = function (doctype, name) {
	frappe.set_route("Form", doctype, name);
};

anyadha_pmo.case_hub.open_list = function (doctype, filters) {
	frappe.route_options = filters || {};
	frappe.set_route("List", doctype);
};
