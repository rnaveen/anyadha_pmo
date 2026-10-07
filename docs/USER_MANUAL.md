# Anyadha PMO — User Manual

## Agreements (Grants and CSR)

Grants and CSR use the **same Agreement** form. Choose **Agreement Type**: Grant, CSR, Government, or Commercial.

1. Open **Grants and Donor Management** or **CSR Management**.
2. Create an **Agreement**.
3. Set **Company**, **Funding Party**, and **Contracted Total**.
4. Link one or more **Projects** on the Agreement (same Company as the Agreement).
5. Optional: attach the signed file, agreement number, and conditions.

CSR desk lists Agreements typed CSR. The old separate CSR Agreement / CSR Project forms are **removed** — use typed Agreement and Project.

**Grants** and **CSR** menus show **Funding Party**, **Agreement**, **Project**, and **Deliverable** (Grants also shows **Funding Source**).

### Case thread on the Agreement

Open a saved Agreement to work the funding story in one place:

- The blue status strip shows type, status, company, funding party, project count, and open deliverables.
- Use the **Case** button group to **Create Project**, **Create Deliverable**, or open the linked Proposal / Funding Party.
- Prefer the Agreement form for “what happens next” — Grants and CSR desks stay as filtered lists.
- Optional (when GRC is installed and **Suggest Obligation from Agreement** is on in GRC Settings): **Case → Suggest Obligations** turns Agreement conditions into draft GRC Obligations. With that flag off, create Obligations manually in GRC and link them to the Agreement.

## Funding Party

**Funding Party** is who funds the work (donor, CSR partner, government, or commercial counterparty).

- Add contacts (Finance / Program / Other).
- Optionally link an ERPNext **Customer** (or **Supplier**) so receipts and payments in books use the same party.

## Projects — budget and funders

On a **Project**:

- Enter **Budget Lines** (head, approved, revised, utilized).
- Enter **Funder Lines** (who contributes, amount, any restriction note).

Company is required. Projects linked to an Agreement must use that Agreement’s Company.

### Project without an Agreement

If the Project is not linked yet, the form strip says so. Use **Case → Link Agreement** (same Company) or **Create Agreement**. Once linked, **Open Agreement** takes you to the funding case hub.

## Deliverables

Create a **Deliverable** on the Project for reports and certificates (UC, SOE, narrative, donor/CSR report, milestone, etc.). Set owner, reviewer, due date, status, and attach the file when ready.

From an Agreement, **Case → Create Deliverable** picks a linked Project when more than one is on the Agreement.

## Proposals

1. Create a **Proposal** with title, donor, and requested amount. Optionally set **Project Type** (same list used on Projects) to classify the intended delivery type — it does not create or link a Project.
2. The Proposals list shows title, status, donor, amount, and project type; filter by status, donor, or project type.
3. When ready, use **Case → Promote to Agreement** (choose Company and Agreement Type).
4. The new Agreement keeps the Proposal link and copies donor / amount.
5. If an Agreement already exists, **Open Agreement** (or Agreements) from the Proposal.

## Strategy

1. Open **Strategy and Portfolio**.
2. Create a **Strategic Plan** for one **Company**.
3. Optionally link a **Parent Strategic Plan** (for example a holding Company plan). You can save without a parent.
4. Add **Strategic Initiatives** under the plan — they must use the same Company as the plan.

## Portfolio and nesting

- A **Portfolio** belongs to one Company.
- On a **Project**, set **Portfolio** to nest it. **Programme** is optional.
- Open the Portfolio to see linked Projects for that Company.

## Outcomes and Performance

Open **Outcomes and Performance** for metrics, optional impact tools, and management MIS.

1. Use **Indicator** / **KPI** (and their readings) for what you measure — both appear until a later merge.
2. Use impact tools (frameworks, baseline, visits, evaluations) only when the work needs them.
3. Use management reviews and MIS snapshots for performance reporting.

Do **not** use GRC Review as a day-to-day Outcomes substitute — that stays for assurance and compliance-style reviews.

The old **Monitoring and Evaluation** and **Performance MIS** desks are hidden; use Outcomes and Performance instead.

## Forms

Desk forms group fields by job in multiple columns: identity and status, nesting (portfolio / programme), classification, schedule and ownership, finance, then tables (budget, funders, contacts, conditions).

## What not to use day-to-day

- Old Grant/CSR twin forms are **gone** — use Agreement, Project budget lines, and Deliverable.
- Central Approval (Approval Request / Step / PMO Authority Matrix) — delivery uses Workflow; GRC uses Workflow + GRC Authority Rule. Board, RPT, and Vendor DD stay on Governance.
