"""Revert Desk UI soft-hide from a ui_soft_hide snapshot.

Restores Workspace / Desktop Icon / DocType flags, Workspace Link hidden,
and **Workspace Sidebar items** (left menu).

Run from bench console (you run; agent does not):

    bench --site <SITE> console
    >>> exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/revert.py").read(), globals())

Named snapshot:

    >>> SOFT_HIDE_SNAPSHOT = "20260928T120000Z"
    >>> exec(open(".../ui_soft_hide/revert.py").read(), globals())
"""

from __future__ import annotations


def run(snapshot: str | None = None) -> str:
	"""Restore UI from snapshot. Returns path used."""
	import json
	from pathlib import Path

	import frappe

	pack_dir = Path("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide")
	snapshots_dir = pack_dir / "snapshots"

	if snapshot:
		stem = snapshot.removesuffix(".json")
		path = snapshots_dir / f"{stem}.json"
		if not path.is_file():
			path = snapshots_dir / snapshot
	else:
		path = snapshots_dir / "latest.json"
		if not path.is_file():
			candidates = sorted(
				p for p in snapshots_dir.glob("*.json") if p.name != "latest.json"
			)
			if not candidates:
				frappe.throw(f"No snapshots in {snapshots_dir}")
			path = candidates[-1]

	if not path.is_file():
		frappe.throw(f"Snapshot not found: {path}")

	data = json.loads(path.read_text(encoding="utf-8"))

	for name, flags in (data.get("workspaces") or {}).items():
		if not frappe.db.exists("Workspace", name):
			print(f"skip workspace (missing): {name}")
			continue
		value = int(flags.get("is_hidden", 0))
		frappe.db.set_value("Workspace", name, "is_hidden", value, update_modified=False)
		print(f"workspace restore is_hidden={value}: {name}")

	for name, flags in (data.get("desktop_icons") or {}).items():
		if not frappe.db.exists("Desktop Icon", name):
			print(f"skip desktop icon (missing): {name}")
			continue
		value = int(flags.get("hidden", 0))
		frappe.db.set_value("Desktop Icon", name, "hidden", value, update_modified=False)
		print(f"desktop icon restore hidden={value}: {name}")

	for name, flags in (data.get("doctypes") or {}).items():
		if not frappe.db.exists("DocType", name):
			print(f"skip doctype (missing): {name}")
			continue
		value = int(flags.get("in_create", 1))
		frappe.db.set_value("DocType", name, "in_create", value, update_modified=False)
		print(f"doctype restore in_create={value}: {name}")

	by_workspace: dict[str, list[dict]] = {}
	for row in data.get("workspace_links") or []:
		by_workspace.setdefault(row["workspace"], []).append(row)

	for ws_name, rows in by_workspace.items():
		if not frappe.db.exists("Workspace", ws_name):
			print(f"skip links (workspace missing): {ws_name}")
			continue
		ws = frappe.get_doc("Workspace", ws_name)
		changed = False
		for row in rows:
			link_to = row["link_to"]
			target_hidden = int(row.get("hidden", 0))
			for link in ws.links or []:
				if link.type == "Link" and link.link_to == link_to:
					if int(link.hidden or 0) != target_hidden:
						link.hidden = target_hidden
						changed = True
					print(
						f"workspace link restore hidden={target_hidden}: "
						f"{ws_name} → {link_to}"
					)
		if changed:
			prev_flag = frappe.flags.in_import
			frappe.flags.in_import = True
			try:
				ws.save(ignore_permissions=True)
			finally:
				frappe.flags.in_import = prev_flag

	# Restore left menus
	for name, block in (data.get("workspace_sidebars") or {}).items():
		if not frappe.db.exists("Workspace Sidebar", name):
			print(f"skip sidebar (missing): {name}")
			continue
		doc = frappe.get_doc("Workspace Sidebar", name)
		items = block.get("items") or []
		doc.set("items", [])
		for idx, row in enumerate(items, start=1):
			payload = dict(row)
			payload["idx"] = idx
			doc.append("items", payload)
		prev_flag = frappe.flags.in_import
		frappe.flags.in_import = True
		try:
			doc.save(ignore_permissions=True)
		finally:
			frappe.flags.in_import = prev_flag
		print(f"sidebar restore: {name} ({len(items)} items)")

	# Restore right Workspace card links (full child table when snapshotted)
	for ws_name, block in (data.get("workspace_cards") or {}).items():
		if not frappe.db.exists("Workspace", ws_name):
			print(f"skip cards (workspace missing): {ws_name}")
			continue
		ws = frappe.get_doc("Workspace", ws_name)
		links = block.get("links") or []
		ws.set("links", [])
		for idx, row in enumerate(links, start=1):
			payload = dict(row)
			payload["idx"] = idx
			ws.append("links", payload)
		prev_flag = frappe.flags.in_import
		frappe.flags.in_import = True
		try:
			ws.save(ignore_permissions=True)
		finally:
			frappe.flags.in_import = prev_flag
		print(f"workspace cards restore: {ws_name} ({len(links)} links)")

	frappe.clear_cache()
	frappe.db.commit()
	print(f"reverted from: {path}")
	print("done — hard-refresh Desk")
	return str(path)


_auto = globals().get("SOFT_HIDE_WHAT", True)
if _auto is not False:
	_snap = globals().get("SOFT_HIDE_SNAPSHOT")
	run(_snap)
