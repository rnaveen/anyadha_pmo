# Anyadha PMO — User Manual

## Agreements (Grants and CSR)

Grants and CSR use the **same Agreement** form. Choose **Agreement Type**: Grant, CSR, Government, or Commercial.

1. Open **Grants and Donor Management** or **CSR Management**.
2. Create an **Agreement**.
3. Set **Company**, **Funding Party**, and **Contracted Total**.
4. Link one or more **Projects** on the Agreement (same Company as the Agreement).
5. Optional: attach the signed file, agreement number, and conditions.

CSR desk lists Agreements typed CSR. Do **not** create the old “CSR Agreement” record — that path is retired for day-to-day use.

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

## What not to use day-to-day

These remain in the system for history but normal users should not create new ones:

- Grant Agreement (thin twin), CSR Agreement, CSR Project
- Standalone Project Budget (use budget lines on Project)
- Old Grant Reporting / Donor Report / UC / CSR Report masters (use Deliverable instead)
