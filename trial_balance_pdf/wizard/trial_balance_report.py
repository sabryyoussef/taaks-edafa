from odoo import fields, models

selection_field = {
    'posted': 'Posted Entries only',
    'draft': 'Include UnPosted Entries'
}

class TrialBalanceReport(models.TransientModel):
    """Create new model"""
    _name = 'trial.balance.report'
    _description = 'trial balance report'

    start_date = fields.Date(
        string="Start Date",
        help="Select start date to fetch the trial balance data"
    )
    end_date = fields.Date(
        string="End Date",
        help="Select end date to fetch the trial balance data"
    )
    journals_ids = fields.Many2many(
        'account.journal',
        string="Journals",
        help="Select the journals to be included in the trial balance"
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        help="Select the company of the journals",
        default=lambda self: self.env.company
    )
    state = fields.Selection([
        ('posted', 'Posted Entries only'),
        ('draft', 'Include UnPosted Entries'),
    ], tracking=True, string="State", help="Select the state of journal entries to be included in the report")

    def button_to_get_pdf(self):
        """It will create the report using defined query"""
        where_conditions = []
        parameters = []
        state_value = ""
        currency = self.env.user.company_id.currency_id.symbol

        # Define initial conditions for balances before the start date
        initial_conditions = []
        initial_parameters = []

        if self.start_date:
            initial_conditions.append("account_move_line.date < %s")
            initial_parameters.append(self.start_date)
        if self.company_id:
            initial_conditions.append("account_move_line.company_id = %s")
            initial_parameters.append(self.company_id.id)
        if self.journals_ids:
            journal_ids = [journal.id for journal in self.journals_ids]
            initial_conditions.append("journal_id IN %s")
            initial_parameters.append(tuple(journal_ids))

        initial_where_query = " AND ".join(initial_conditions)
        initial_query = """
            SELECT
                account_move_line.account_id AS account_id,
                SUM(account_move_line.debit) AS initial_debit,
                SUM(account_move_line.credit) AS initial_credit
            FROM
                account_move_line
            {}
            GROUP BY
                account_move_line.account_id
        """.format("WHERE " + initial_where_query if initial_conditions else "")

        self.env.cr.execute(initial_query, tuple(initial_parameters))
        initial_balances = self.env.cr.dictfetchall()

        initial_balances_dict = {rec['account_id']: rec for rec in initial_balances}

        where_conditions = []
        if self.start_date:
            where_conditions.append("account_move_line.date >= %s")
            parameters.append(self.start_date)
        if self.end_date:
            where_conditions.append("account_move_line.date <= %s")
            parameters.append(self.end_date)
        if self.company_id:
            where_conditions.append("account_move_line.company_id = %s")
            parameters.append(self.company_id.id)
        if self.state == 'posted':
            where_conditions.append("parent_state = 'posted'")
        if self.state == 'draft':
            where_conditions.append("parent_state in ('posted', 'draft')")
        if self.journals_ids:
            journal_ids = [journal.id for journal in self.journals_ids]
            where_conditions.append("journal_id IN %s")
            parameters.append(tuple(journal_ids))

        where_query = " AND ".join(where_conditions)
        query = """
            SELECT
                account_move_line.account_id AS account_id,
                account_account.code AS code,
                account_account.name AS ac_name,
                SUM(account_move_line.debit) AS debit,
                SUM(account_move_line.credit) AS credit,
                SUM(account_move_line.debit) - SUM(account_move_line.credit) AS balance
            FROM
                account_move_line
            JOIN
                account_account ON account_account.id = account_move_line.account_id
            {}
            GROUP BY
                account_move_line.account_id,
                account_account.name,
                account_account.code
        """.format("WHERE " + where_query if where_conditions else "")

        self.env.cr.execute(query, tuple(parameters))
        main_query = self.env.cr.dictfetchall()

        total_credit = 0.0
        total_debit = 0.0
        total_initial_debit = 0.0
        total_initial_credit = 0.0

        for rec in main_query:
            account_id = rec['account_id']
            initial_balance = initial_balances_dict.get(account_id, {'initial_debit': 0.0, 'initial_credit': 0.0})
            rec['initial_debit'] = initial_balance['initial_debit']
            rec['initial_credit'] = initial_balance['initial_credit']
            rec['initial_balance'] = rec['initial_debit'] - rec['initial_credit']
            # Ensure ac_name is a string
            account_name = rec.get('ac_name', '')
            if isinstance(account_name, dict):
                account_name = account_name.get('en_US', '')  # Adjust this line based on your data structure
            account_name = str(account_name).strip().replace('\n', ' ').replace('\r', '')
            rec['ac_name'] = account_name
            total_credit += rec['credit']
            total_debit += rec['debit']
            total_initial_debit += rec['initial_debit']
            total_initial_credit += rec['initial_credit']

        total_initial_balance = total_initial_debit - total_initial_credit
        balance = (total_debit - total_credit)
        # balance = total_initial_balance + (total_debit - total_credit)

        if self.state:
            state_value = selection_field[self.state]
        journals = str(self.journals_ids.mapped('name'))
        result = journals[1:-1].replace("'", "")

        data = {
            'query': main_query,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_init_debit': round(total_initial_debit, 2),
            'total_init_credit': round(total_initial_credit, 2),
            'total_init_balance': round(total_initial_balance, 2),
            'total_credit': round(total_credit, 2),
            'total_debit': round(total_debit, 2),
            'balance': round(balance, 2),
            'currency': currency,
            'state': state_value,
            'journals_name': result
        }
        return self.env.ref(
            'trial_balance_pdf.action_report_trial_balance').report_action(
            self, data=data)
