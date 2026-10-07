# UI soft-hide (Desk only) — reversible

Soft-hides hollow PMO IRM desks from **Desk UI**. Does **not** delete IRM DocTypes (S7). Funding twins were **removed in S8** — they are no longer soft-hide targets.

**Lasting desk shape** (grill 2026-09-28 + U7/S6 + S8): keep this UI going forward; S7 hard-retires IRM later. v1.4: S8 twins gone from app; Central Approval sunset on Governance. Revert only for debug. Prefer this apply over mass Workspace fixture PRs (merge-light).

You run these scripts (same pattern as [`../import_seed.py`](../import_seed.py)).

**Authority:** suite BUILD_SPEC §10 · seam §5 · FIELD_MAP_S1 · soft-hide grill package · S8 twin drop.

---

## What apply does

| Lever | Effect |
|---|---|
| Workspace `is_hidden = 1` | Hides Compliance / Risk / Audit / SOP + old M&E / PERF desks |
| Desktop Icon `hidden = 1` | Matching **app** icons under Anyadha PMO |
| DocType `in_create = 0` | Soft-hides Create for hollow IRM DocTypes |
| Workspace Link hide / ensure | **Right cards** on Grants / CSR / Project match suite targets |
| **Workspace Sidebar items** | **Left menu** on keep-visible desks — suite-target DocTypes only |
| Agreement `route_options` | Grants sidebar → `agreement_type=Grant`; CSR → `CSR` |

**Grants:** Funding Party · Agreement · Project · Deliverable · Funding Source  
**CSR:** Funding Party · Agreement · Project · Deliverable  

Governance stays visible (soft-keep; Central Approval sunset). Outcomes keeps Indicator + KPI stacks only (O-6 not claimed).

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

Then:

```bash
bench --site anyadha.local clear-cache
```

---

## Files

| Path | Purpose |
|---|---|
| [`manifest_v1.json`](manifest_v1.json) | Hide targets + sidebar/card clean (v1.4) |
| [`apply.py`](apply.py) | Snapshot → apply |
| [`revert.py`](revert.py) | Restore from snapshot |
| `snapshots/` | Timestamped JSON state (gitignored contents except `.gitkeep`) |

**Runtime apply path** (snapshots live next to the design pack copy you execute):

```python
exec(open("/Users/tapasya./frappe/frappe/design/anyadha_pmo/ui_soft_hide/apply.py").read(), globals())
```

---

## Out of scope

See `out_of_scope` in the manifest. Notably: no Board/RPT soft-hide (only Central Approval), no O-6 merge, no S7 IRM DocType delete.
