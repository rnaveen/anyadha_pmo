"""Soft-hide unused anyadha_pmo Desk UI from manifest_v1.json.

Hides IRM Desktop Icons / Workspaces, soft-hides dormant DocTypes, and
**cleans Workspace Sidebar left menus** on keep-visible desks to the suite
target story. Snapshots for revert. Does NOT delete DocTypes or change schema.

Run from bench console (you run; agent does not):

    bench --site <SITE> console
    >>> exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/apply.py").read(), globals())

Load helpers only:

    >>> SOFT_HIDE_WHAT = False
    >>> exec(open(".../ui_soft_hide/apply.py").read(), globals())
    >>> run()
"""

from __future__ import annotations


def run() -> str:
	"""Apply soft-hide + sidebar clean. Returns snapshot path written."""
	import json
	from datetime import datetime, timezone
	from pathlib import Path

	import frappe

	pack_dir = Path("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide")
	manifest_path = pack_dir / "manifest_v1.json"
	snapshots_dir = pack_dir / "snapshots"
	snapshots_dir.mkdir(parents=True, exist_ok=True)

	if not manifest_path.is_file():
		frappe.throw(f"Missing manifest: {manifest_path}")

	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

	# Preserve original pre-hide values across re-applies
	prev_path = snapshots_dir / "latest.json"
	prev = {}
	if prev_path.is_file():
		try:
			prev = json.loads(prev_path.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			prev = {}

	workspace_names = [row["name"] for row in manifest.get("workspaces_hide") or []]
	icon_names = list(manifest.get("desktop_icons_hide") or [])
	doctype_block = manifest.get("doctypes_soft_hide") or {}
	doctype_names = [row["name"] for row in doctype_block.get("items") or []]
	in_create_target = int(doctype_block.get("in_create", 0))
	link_specs = list(manifest.get("workspace_links_hide") or [])
	sidebar_hide_specs = list(manifest.get("sidebar_links_hide") or [])
	sidebar_specs = list(manifest.get("workspace_sidebars_clean") or [])
	card_specs = list(manifest.get("workspace_cards_clean") or [])

	snapshot = {
		"version": manifest.get("version"),
		"created_at": datetime.now(timezone.utc).isoformat(),
		"workspaces": dict(prev.get("workspaces") or {}),
		"desktop_icons": dict(prev.get("desktop_icons") or {}),
		"doctypes": dict(prev.get("doctypes") or {}),
		"workspace_links": list(prev.get("workspace_links") or []),
		"workspace_sidebars": dict(prev.get("workspace_sidebars") or {}),
		"workspace_cards": dict(prev.get("workspace_cards") or {}),
		"sidebar_links_removed": list(prev.get("sidebar_links_removed") or []),
	}

	def _item_row(item) -> dict:
		keys = (
			"label",
			"link_type",
			"icon",
			"type",
			"link_to",
			"child",
			"indent",
			"collapsible",
			"keep_closed",
			"show_arrow",
			"filters",
			"route_options",
			"url",
			"navigate_to_tab",
		)
		row = {}
		for key in keys:
			val = item.get(key) if hasattr(item, "get") else getattr(item, key, None)
			if val not in (None, ""):
				row[key] = val
		# defaults needed on restore
		for key, default in (
			("type", "Link"),
			("child", 0),
			("indent", 0),
			("collapsible", 1),
			("keep_closed", 0),
			("show_arrow", 0),
		):
			row.setdefault(key, default)
		return row

	def _prune_empty_sections(items: list[dict]) -> list[dict]:
		out: list[dict] = []
		i = 0
		while i < len(items):
			item = items[i]
			if item.get("type") == "Section Break":
				j = i + 1
				chunk: list[dict] = []
				while j < len(items) and items[j].get("type") != "Section Break":
					# stop before another top-level Home workspace link
					nxt = items[j]
					if (
						nxt.get("type") == "Link"
						and nxt.get("link_type") == "Workspace"
						and not int(nxt.get("child") or 0)
					):
						break
					chunk.append(nxt)
					j += 1
				if any(c.get("type") == "Link" for c in chunk):
					out.append(item)
					out.extend(chunk)
				i = j
			else:
				out.append(item)
				i += 1
		return out

	def _save_sidebar(doc) -> None:
		# Avoid rewriting app fixtures from design-pack demo applies
		prev_flag = frappe.flags.in_import
		frappe.flags.in_import = True
		try:
			doc.save(ignore_permissions=True)
		finally:
			frappe.flags.in_import = prev_flag

	# --- workspaces ---
	for name in workspace_names:
		if not frappe.db.exists("Workspace", name):
			print(f"skip workspace (missing): {name}")
			continue
		before = frappe.db.get_value("Workspace", name, "is_hidden")
		if name not in snapshot["workspaces"]:
			snapshot["workspaces"][name] = {"is_hidden": int(before or 0)}
		if int(before or 0) != 1:
			frappe.db.set_value("Workspace", name, "is_hidden", 1, update_modified=False)
			print(f"workspace hide: {name}")
		else:
			print(f"workspace already hidden: {name}")

	# --- desktop icons ---
	for name in icon_names:
		if not frappe.db.exists("Desktop Icon", name):
			print(f"skip desktop icon (missing): {name}")
			continue
		before = frappe.db.get_value("Desktop Icon", name, "hidden")
		if name not in snapshot["desktop_icons"]:
			snapshot["desktop_icons"][name] = {"hidden": int(before or 0)}
		if int(before or 0) != 1:
			frappe.db.set_value("Desktop Icon", name, "hidden", 1, update_modified=False)
			print(f"desktop icon hide: {name}")
		else:
			print(f"desktop icon already hidden: {name}")

	# --- DocType in_create ---
	for name in doctype_names:
		if not frappe.db.exists("DocType", name):
			print(f"skip doctype (missing): {name}")
			continue
		before = frappe.db.get_value("DocType", name, "in_create")
		if name not in snapshot["doctypes"]:
			snapshot["doctypes"][name] = {
				"in_create": int(before if before is not None else 1)
			}
		if int(before if before is not None else 1) != in_create_target:
			frappe.db.set_value(
				"DocType", name, "in_create", in_create_target, update_modified=False
			)
			print(f"doctype in_create={in_create_target}: {name}")
		else:
			print(f"doctype already in_create={in_create_target}: {name}")

	# --- selective sidebar link hide (e.g. Central Approval on Governance) ---
	seen_sidebar_removes = {
		(r["sidebar"], r["link_to"]) for r in snapshot.get("sidebar_links_removed") or []
	}
	by_sidebar: dict[str, set[str]] = {}
	for spec in sidebar_hide_specs:
		by_sidebar.setdefault(spec["sidebar"], set()).add(spec["link_to"])

	for sidebar_name, hide_set in by_sidebar.items():
		if not frappe.db.exists("Workspace Sidebar", sidebar_name):
			print(f"skip sidebar hide (missing): {sidebar_name}")
			continue
		doc = frappe.get_doc("Workspace Sidebar", sidebar_name)
		if sidebar_name not in snapshot["workspace_sidebars"]:
			snapshot["workspace_sidebars"][sidebar_name] = {
				"items": [_item_row(item) for item in (doc.items or [])]
			}
		kept_items = []
		changed = False
		for item in doc.items or []:
			link_to = item.get("link_to") if hasattr(item, "get") else item.link_to
			if item.type == "Link" and link_to in hide_set:
				key = (sidebar_name, link_to)
				if key not in seen_sidebar_removes:
					snapshot["sidebar_links_removed"].append(
						{"sidebar": sidebar_name, "link_to": link_to, "row": _item_row(item)}
					)
					seen_sidebar_removes.add(key)
				changed = True
				continue
			kept_items.append(_item_row(item))
		if changed:
			kept_items = _prune_empty_sections(kept_items)
			doc.set("items", [])
			for idx, row in enumerate(kept_items, start=1):
				row = dict(row)
				row["idx"] = idx
				doc.append("items", row)
			_save_sidebar(doc)
			print(f"sidebar links hide: {sidebar_name} → {sorted(hide_set)}")
		else:
			print(f"sidebar links already clean: {sidebar_name}")

	# --- workspace card links ---
	seen_links = {
		(r["workspace"], r["link_to"]) for r in snapshot["workspace_links"]
	}
	for spec in link_specs:
		ws_name = spec["workspace"]
		link_to = spec["link_to"]
		if not frappe.db.exists("Workspace", ws_name):
			print(f"skip link (workspace missing): {ws_name} → {link_to}")
			continue
		ws = frappe.get_doc("Workspace", ws_name)
		changed = False
		found = False
		for link in ws.links or []:
			if link.type == "Link" and link.link_to == link_to:
				found = True
				key = (ws_name, link_to)
				if key not in seen_links:
					snapshot["workspace_links"].append(
						{
							"workspace": ws_name,
							"link_to": link_to,
							"hidden": int(link.hidden or 0),
							"label": link.label,
						}
					)
					seen_links.add(key)
				if int(link.hidden or 0) != 1:
					link.hidden = 1
					changed = True
		if changed:
			prev_flag = frappe.flags.in_import
			frappe.flags.in_import = True
			try:
				ws.save(ignore_permissions=True)
			finally:
				frappe.flags.in_import = prev_flag
			print(f"workspace link hide: {ws_name} → {link_to}")
		elif not found:
			print(f"skip link (not on workspace): {ws_name} → {link_to}")
		else:
			print(f"workspace link already hidden: {ws_name} → {link_to}")

	def _ensure_meta(ensure: list) -> dict:
		"""Map link_to → ensure row (label / route_options / filters)."""
		out = {}
		for ens in ensure or []:
			link_to = ens.get("link_to")
			if link_to:
				out[link_to] = ens
		return out

	def _apply_ensure_meta(row: dict, ens: dict | None) -> None:
		if not ens:
			return
		if ens.get("label"):
			row["label"] = ens["label"]
		if ens.get("route_options"):
			row["route_options"] = ens["route_options"]
		if ens.get("filters"):
			row["filters"] = ens["filters"]

	# --- left menu: Workspace Sidebar clean ---
	for spec in sidebar_specs:
		name = spec["name"]
		if not frappe.db.exists("Workspace Sidebar", name):
			print(f"skip sidebar (missing): {name}")
			continue

		doc = frappe.get_doc("Workspace Sidebar", name)
		# Always refresh snapshot from current only if never snapshotted
		if name not in snapshot["workspace_sidebars"]:
			snapshot["workspace_sidebars"][name] = {
				"items": [_item_row(item) for item in (doc.items or [])]
			}

		keep = set(spec.get("keep_doctypes") or [])
		overrides = spec.get("label_overrides") or {}
		ensure = list(spec.get("ensure") or [])
		ensure_by = _ensure_meta(ensure)

		new_items: list[dict] = []
		for item in doc.items or []:
			row = _item_row(item)
			if row.get("type") == "Section Break":
				new_items.append(row)
				continue
			if row.get("type") == "Link" and row.get("link_type") == "Workspace":
				new_items.append(row)
				continue
			if row.get("type") == "Link" and row.get("link_to") in keep:
				if row["link_to"] in overrides:
					row["label"] = overrides[row["link_to"]]
				_apply_ensure_meta(row, ensure_by.get(row["link_to"]))
				new_items.append(row)

		present = {
			r.get("link_to")
			for r in new_items
			if r.get("type") == "Link" and r.get("link_type") == "DocType"
		}
		for ens in ensure:
			link_to = ens["link_to"]
			if link_to in present:
				continue
			if not frappe.db.exists("DocType", link_to):
				print(f"sidebar ensure skip (missing DocType): {name} → {link_to}")
				continue
			row = {
				"type": "Link",
				"label": ens.get("label") or link_to,
				"link_type": ens.get("link_type") or "DocType",
				"link_to": link_to,
				"child": 1,
				"collapsible": 1,
				"indent": 0,
				"keep_closed": 0,
				"show_arrow": 0,
			}
			_apply_ensure_meta(row, ens)
			new_items.append(row)
			present.add(link_to)

		# Ensure a Master section exists if we have DocType links
		has_section = any(r.get("type") == "Section Break" for r in new_items)
		has_doctypes = any(
			r.get("type") == "Link" and r.get("link_type") == "DocType" for r in new_items
		)
		if has_doctypes and not has_section:
			# insert section after Home
			insert_at = 0
			for idx, r in enumerate(new_items):
				if r.get("type") == "Link" and r.get("link_type") == "Workspace":
					insert_at = idx + 1
					break
			new_items.insert(
				insert_at,
				{
					"type": "Section Break",
					"label": "Master Data & Transactions",
					"link_type": "DocType",
					"link_to": "",
					"child": 0,
					"collapsible": 1,
					"indent": 1,
					"keep_closed": 1,
					"show_arrow": 0,
					"icon": "database",
				},
			)

		new_items = _prune_empty_sections(new_items)

		doc.set("items", [])
		for idx, row in enumerate(new_items, start=1):
			row = dict(row)
			row["idx"] = idx
			doc.append("items", row)

		_save_sidebar(doc)
		kept = sorted(
			r.get("link_to")
			for r in new_items
			if r.get("type") == "Link" and r.get("link_type") == "DocType"
		)
		print(f"sidebar clean: {name} → {kept}")

	# --- right cards: Workspace links clean (match left suite targets) ---
	for spec in card_specs:
		ws_name = spec["name"]
		if not frappe.db.exists("Workspace", ws_name):
			print(f"skip cards (workspace missing): {ws_name}")
			continue

		keep = set(spec.get("keep_doctypes") or [])
		overrides = spec.get("label_overrides") or {}
		ws = frappe.get_doc("Workspace", ws_name)

		if ws_name not in snapshot["workspace_cards"]:
			snapshot["workspace_cards"][ws_name] = {
				"links": [
					{
						"type": link.type,
						"label": link.label,
						"link_to": link.link_to,
						"link_type": link.link_type,
						"hidden": int(link.hidden or 0),
						"onboard": int(link.onboard or 0),
						"is_query_report": int(link.is_query_report or 0),
					}
					for link in (ws.links or [])
				]
			}

		changed = False
		present = set()
		for link in ws.links or []:
			if link.type != "Link":
				continue
			link_to = link.link_to
			if link_to in keep:
				present.add(link_to)
				desired_label = overrides.get(link_to) or link.label
				if link.label != desired_label:
					link.label = desired_label
					changed = True
				if int(link.hidden or 0) != 0:
					link.hidden = 0
					changed = True
			else:
				if int(link.hidden or 0) != 1:
					link.hidden = 1
					changed = True

		# Ensure suite targets exist as visible card links
		has_card_break = any(link.type == "Card Break" for link in (ws.links or []))
		if keep and not has_card_break:
			ws.append(
				"links",
				{
					"type": "Card Break",
					"label": "Master Data & Transactions",
					"hidden": 0,
				},
			)
			changed = True

		for link_to in keep:
			if link_to in present:
				continue
			if not frappe.db.exists("DocType", link_to):
				print(f"cards ensure skip (missing DocType): {ws_name} → {link_to}")
				continue
			ws.append(
				"links",
				{
					"type": "Link",
					"label": overrides.get(link_to) or link_to,
					"link_type": "DocType",
					"link_to": link_to,
					"hidden": 0,
					"onboard": 1,
				},
			)
			present.add(link_to)
			changed = True
			print(f"workspace card ensure: {ws_name} → {link_to}")

		if changed:
			prev_flag = frappe.flags.in_import
			frappe.flags.in_import = True
			try:
				ws.save(ignore_permissions=True)
			finally:
				frappe.flags.in_import = prev_flag
			print(f"workspace cards clean: {ws_name} → {sorted(present)}")
		else:
			print(f"workspace cards already clean: {ws_name} → {sorted(present)}")

	stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
	snapshot_path = snapshots_dir / f"{stamp}.json"
	latest_path = snapshots_dir / "latest.json"
	payload = json.dumps(snapshot, indent=2, sort_keys=True)
	snapshot_path.write_text(payload + "\n", encoding="utf-8")
	latest_path.write_text(payload + "\n", encoding="utf-8")

	frappe.clear_cache()
	frappe.db.commit()
	print(f"snapshot: {snapshot_path}")
	print("done — hard-refresh Desk (clear-cache already called)")
	return str(snapshot_path)


_auto = globals().get("SOFT_HIDE_WHAT", True)
if _auto is not False:
	run()
