import frappe

from anyadha_pmo.security.roles import PMO_ROLES


def ensure_roles():
    """Create PMO roles if they do not already exist.

    Existing roles are never overwritten. This makes installation and
    migration idempotent and safe for an already-running site.
    """

    for role_name, desk_access in PMO_ROLES:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc(
                {
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": desk_access,
                }
            ).insert(ignore_permissions=True)

    frappe.db.commit()


def ensure_u3_labels():
    """Desk labels for canonical DocTypes that keep legacy technical names."""
    for source, translated in (
        ("PMO Grant", "Agreement"),
        ("PMO Donor", "Funding Party"),
    ):
        name = frappe.db.exists(
            "Translation", {"source_text": source, "language": "en"}
        )
        if name:
            frappe.db.set_value("Translation", name, "translated_text", translated)
        else:
            frappe.get_doc(
                {
                    "doctype": "Translation",
                    "language": "en",
                    "source_text": source,
                    "translated_text": translated,
                }
            ).insert(ignore_permissions=True)


def after_install():
    ensure_roles()
    ensure_u3_labels()


def after_migrate():
    ensure_roles()
    ensure_u3_labels()
