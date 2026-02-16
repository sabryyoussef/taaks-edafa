# Trial Balance PDF Report — User Guide

## Installation
- Install the module **Trial Balance PDF Report** from Apps.
- Ensure Accounting is installed (dependency: `account`).

## Access / Menu
- Go to: **Accounting → Reporting → Audit Reports → Trial Balance**

## How to generate the PDF
1. Open **Trial Balance**.
2. Set **Start Date** and/or **End Date**.
3. Optionally select **Journals**.
4. Select **State**:
   - **Posted Entries only**: only posted move lines
   - **Include UnPosted Entries**: includes posted and draft
5. Click **PDF**.

## Output
The PDF includes per account:
- Code, Account name
- Initial debit/credit and initial balance (before Start Date)
- Period debit/credit and balance (within date range)
- Totals at the end of the report

## Notes
- If no dates are provided, the report includes all data (not usually recommended).
- Journal filter is optional.
