# S8 proof — funding twin drop

| | |
|---|---|
| **Status** | Implemented in app; apply on site via `bench migrate` |
| **Patch** | `anyadha_pmo.patches.v2_2.drop_s8_funding_twins` |
| **Scope** | Dormant Grant/CSR twin DocTypes only (not PMO IRM — that is S7) |

## Gate

1. Empty-check each twin DocType (row count).
2. If any rows remain and `s8_force_drop_funding_twins` is **not** set in site_config → patch **throws** (no drop).
3. If empty, or force flag is set → delete rows (force only) and `frappe.delete_doc("DocType", …, force=True)`.

## Dropped DocTypes

See `S8_FUNDING_TWINS` in `anyadha_pmo/patches/v2_2/drop_s8_funding_twins.py`.

Live path after drop: **Funding Party → Agreement (`PMO Grant`) → Project → budget/funder children → Deliverable**.

## Verify

```bash
bench --site <site> migrate   # after empty-check or force flag
bench --site <site> run-tests --app anyadha_pmo --module anyadha_pmo.tests.test_s8_twin_drop
```

Force wipe of leftover scaffold (dev/test only):

```bash
bench --site <site> set-config s8_force_drop_funding_twins 1
bench --site <site> migrate
```
