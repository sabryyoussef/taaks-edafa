# Custom Reports — User Guide

## Installation
- Install the module **Custom Reports** from Apps.
- Ensure Accounting is installed (dependency: `account`).

## Access / Menu
- Go to: **Accounting → Reporting → Loan & Custody Reports**

## How to generate the PDF
1. Open **Loan & Custody Reports**.
2. Set **Start Date** and **End Date**.
3. Select **Account Code** (required).
4. Optionally select one or more **Account Name** (partners).
5. Click **Print**.

## Output
The PDF includes, per partner:
- Account code
- Partner name
- Previous balance (before Start Date)
- Debit / Credit for the selected period
- Final balance (previous + period balance)

## Notes / Validation
- If there is no move line data for the chosen criteria, the wizard raises “No Data Found on this account for this period”.
- Start Date must be less than or equal to End Date.

## Troubleshooting
- **No Data Found**: confirm posted journal entries exist on the selected account within the date range, and match the selected company.
- **Missing menu**: confirm you are in the Accounting app and have access rights for internal users.
