# General Trial Balance with Account Groups — User Guide

## Installation
- Install the module **General Trial Balance PDF Report with account group** from Apps.
- Ensure Accounting is installed (dependency: `account`).

## Access / Menu
- Go to: **Accounting → Reporting → Audit Reports → General Trial Balance with group account**

## How to generate the PDF
1. Open **General Trial Balance with group account**.
2. Set **Start Date** and **End Date** (required).
3. Optionally select **Account Groups**.
4. Select **State**:
   - **Posted Entries only**
   - **Include UnPosted Entries**
5. Click **PDF**.

## Output
The PDF includes per account:
- Code, Account name
- Account type (display label)
- Previous balances (initial debit/credit)
- Period movements (debit/credit)
- Final debit/credit columns (initial + movement)
- Totals row

## Notes
- If Account Groups are selected, only accounts in those groups are included.
- The report template contains Arabic labels; printing depends on your PDF rendering/fonts.
