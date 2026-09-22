"""Purchase Order portal access is supplier-only, even for dual-role contacts.

erpnext.controllers.website_list_for_contact decides which party filter/check
to use for a portal user with this priority, in both the list query
(get_transaction_list) and the single-document permission check
(has_website_permission):

    if customers:  use "customer" = [...]
    elif suppliers: use "supplier" = [...]

Purchase Order has a "customer" field (used only for drop-ship orders) in
addition to "supplier". A portal user who is registered as a Portal User on
*both* a Customer and a Supplier record (a contact who plays both roles)
therefore always gets checked against "customer", never "supplier" - even
though almost none of their purchase orders are drop-ship orders naming that
customer. The result: an empty Purchase Order list, and "Not Permitted" when
opening a PO directly, for such users - while every other portal doctype
(which has no competing "customer" field) works fine.

Purchase Order is a supplier-side document: a Customer should never see it on
the portal, only the Supplier it was raised against. This module fixes both
paths to check supplier only, ignoring any customer link entirely:
- get_list_context/get_purchase_order_list (patched onto the erpnext module
  via apply()) list only POs where the user's supplier(s) are the supplier.
- CustomPurchaseOrder.has_website_permission (wired via override_doctype_class)
  checks the supplier relationship directly for a single document, bypassing
  erpnext's buggy hooks.py-registered has_website_permission.
"""

import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder
from erpnext.controllers.website_list_for_contact import (
	get_customers_suppliers,
	get_list_for_transactions,
	post_process,
)


def get_purchase_order_list(
	doctype,
	txt=None,
	filters=None,
	limit_start=0,
	limit_page_length=20,
	order_by="creation desc",
):
	user = frappe.session.user
	base_filters = dict(filters or {})
	base_filters["docstatus"] = 1

	suppliers = get_customers_suppliers(doctype, user)[1]
	if not suppliers:
		return []

	supplier_filters = dict(base_filters)
	supplier_filters["supplier"] = ["in", suppliers]

	transactions = get_list_for_transactions(
		doctype,
		txt,
		supplier_filters,
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		ignore_permissions=True,
		order_by=order_by,
	)

	return post_process(doctype, transactions)


def get_list_context(context=None):
	from erpnext.controllers.website_list_for_contact import get_list_context as default_get_list_context

	# Mirror erpnext's own purchase_order.get_list_context exactly (same
	# show_sidebar/title/list_template keys), only swapping out "get_list".
	# Dropping list_template here would make frappe.www.list fall back to
	# meta.get_list_template(), which is None for Purchase Order and blanks
	# out context.template -> 500 error when the page tries to render.
	list_context = default_get_list_context(context)
	list_context.update(
		{
			"show_sidebar": True,
			"show_search": True,
			"no_breadcrumbs": True,
			"title": frappe._("Purchase Orders"),
			"list_template": "templates/includes/list/list.html",
		}
	)
	list_context["get_list"] = get_purchase_order_list
	return list_context


def apply():
	"""Patch erpnext's Purchase Order controller module so the website list
	renderer (frappe.website.page_renderers.list_renderer, frappe.www.list)
	picks up get_list_context above instead of the one erpnext ships with.

	Called from the before_request hook so it is guaranteed to run once
	Frappe is fully booted, and is idempotent to call on every request.
	"""
	from erpnext.buying.doctype.purchase_order import purchase_order as po_module

	po_module.get_list_context = get_list_context


class CustomPurchaseOrder(PurchaseOrder):
	"""Custom Purchase Order - fixes single-document portal read access for
	contacts who are a Portal User on both a Customer and a Supplier.

	frappe.has_website_permission() prefers a document controller's own
	``has_website_permission`` method over the doctype-keyed hooks.py
	dispatch (see frappe/__init__.py). erpnext registers
	erpnext.controllers.website_list_for_contact.has_website_permission for
	"Purchase Order" via hooks.py, but that function checks
	``if customers: ... elif suppliers: ...``, so a user linked to both a
	Customer and a Supplier gets checked against Purchase Order's
	"customer" (drop-ship) field first and denied, even when they are the
	Portal User for the actual supplier on the order.

	Purchase Order is a supplier-side document: only the order's Supplier
	should see it on the portal, never a Customer (the "customer" field
	only exists for drop-ship orders and is not a portal access grant).
	Defining has_website_permission here bypasses erpnext's hooks.py
	dispatch entirely and checks the supplier relationship only.
	"""

	def has_website_permission(self, ptype="read", user=None, verbose=False):
		if ptype != "read" or self.docstatus != 1:
			return False

		user = user or frappe.session.user
		if user == "Guest":
			return False

		if self.supplier and frappe.db.exists(
			"Portal User", {"parenttype": "Supplier", "parent": self.supplier, "user": user}
		):
			return True

		return False
