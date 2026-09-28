# Anyadha PMO — User Manual

## Agreements (Grants and CSR)

Grants and CSR use the **same Agreement** form. Choose **Agreement Type**: Grant, CSR, Government, or Commercial.

1. Open **Grants and Donor Management** or **CSR Management**.
2. Create an **Agreement**.
3. Set **Company**, **Funding Party**, and **Contracted Total**.
4. Link one or more **Projects** on the Agreement (same Company as the Agreement).
5. Optional: attach the signed file, agreement number, and conditions.

CSR desk lists Agreements typed CSR. Do **not** create the old “CSR Agreement” record — that path is retired for day-to-day use.

On a cleaned Desk (soft-hide applied on the site), **Grants** and **CSR** left menus and cards show **Funding Party**, **Agreement**, **Project**, and **Deliverable** (Grants also shows **Funding Source**). Old twin DocTypes stay out of those desks.

### Case thread on the Agreement

Open a saved Agreement to work the funding story in one place:

- The blue status strip shows type, status, company, funding party, project count, and open deliverables.
- Use the **Case** button group to **Create Project**, **Create Deliverable**, or open the linked Proposal / Funding Party.
- Prefer the Agreement form for “what happens next” — Grants and CSR desks stay as filtered lists.

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

1. Create a **Proposal** with title, donor, and requested amount.
2. When ready, use **Case → Promote to Agreement** (choose Company and Agreement Type).
3. The new Agreement keeps the Proposal link and copies donor / amount.
4. If an Agreement already exists, **Open Agreement** (or Agreements) from the Proposal.

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

These remain in the system for history but normal users should not create new ones:

- Grant Agreement (thin twin), CSR Agreement, CSR Project
- Standalone Project Budget (use budget lines on Project)
- Old Grant Reporting / Donor Report / UC / CSR Report masters (use Deliverable instead)
