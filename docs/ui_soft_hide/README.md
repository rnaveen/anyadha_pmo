# UI soft-hide (Desk only) — reversible

Soft-hides hollow PMO IRM desks and dormant funding twins from **Desk UI**. Does **not** delete DocTypes, change schema, or migrate.

**Lasting desk shape** (grill 2026-09-28): keep this UI going forward; S7 hard-retires IRM and S8 drops empty funding twins later. Revert only for debug. Prefer this apply over mass Workspace fixture PRs (merge-light).

You run these scripts (same pattern as [`../import_seed.py`](../import_seed.py)).

**Authority:** suite BUILD_SPEC §10 · seam §5 · FIELD_MAP_S1 D3/D6 · soft-hide grill package.

---

## What apply does

| Lever | Effect |
|---|---|
| Workspace `is_hidden = 1` | Hides Compliance / Risk / Audit / SOP + old M&E / PERF desks |
| Desktop Icon `hidden = 1` | Matching **app** icons under Anyadha PMO |
| DocType `in_create = 0` | Soft-hides Create for dormant / hollow DocTypes |
| Workspace Link hide / ensure | **Right cards** on Grants / CSR / Project match suite targets |
| **Workspace Sidebar items** | **Left menu** on keep-visible desks — suite-target DocTypes only |
| Agreement `route_options` | Grants sidebar → `agreement_type=Grant`; CSR → `CSR` |

**Grants:** Funding Party · Agreement · Project · Deliverable · Funding Source  
**CSR:** Funding Party · Agreement · Project · Deliverable  

Governance stays visible (soft-keep). Outcomes keeps Indicator + KPI stacks only (O-6 not claimed).

**After migrate / fixture sync:** desks may come back dirty — re-run apply.

---

## Run (dev / test site)

```bash
bench --site anyadha.local console
```

```python
# apply (writes snapshot under snapshots/, then hides)
exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/apply.py").read(), globals())

# revert (restores from latest snapshot)
exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/revert.py").read(), globals())
```

Or load helpers only:

```python
SOFT_HIDE_WHAT = False
exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/apply.py").read(), globals())
run()          # apply
# after loading revert.py:
# run()        # revert latest
# run("2026-09-28T…")  # named snapshot stem
```

Then:

```bash
bench --site anyadha.local clear-cache
```

Same on the test bench site when you want the clean desk there.

---

## Files

| Path | Purpose |
|---|---|
| [`manifest_v1.json`](manifest_v1.json) | Hide targets + sidebar/card clean + reasons (v1.2) |
| [`apply.py`](apply.py) | Snapshot → apply |
| [`revert.py`](revert.py) | Restore from snapshot |
| `snapshots/` | Timestamped JSON state (gitignored contents except `.gitkeep`) |

Git-tracked copy: this folder under `apps/anyadha_pmo/docs/ui_soft_hide/`.

**Runtime apply path** (snapshots live next to the design pack copy you execute):

```python
exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/apply.py").read(), globals())
```

If you prefer this docs copy, use the same `apply.py` here — both point at the design pack directory for snapshots unless you edit `pack_dir`.

---

## Rollback

`revert.py` restores Workspace / Desktop Icon / DocType / Workspace Link / Sidebar / card tables from the newest `snapshots/*.json` (or a name you pass). Re-apply is safe (idempotent).

---

## Out of scope

See `out_of_scope` in the manifest. Notably: no Governance hide, no S6 approval sunset, no O-6 merge, no S8 DocType delete, no fixture JSON rewrite in the app (fresh install still shows full desks until you run apply on that site).
