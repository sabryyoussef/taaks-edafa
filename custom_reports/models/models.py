# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CustomReports(models.Model):
    _name = 'custom.reports'
    _description = 'Custom Reports'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    account_partner_ids = fields.Many2many('res.partner', string="Account Name")
    account_id = fields.Many2one('account.account', string="Account Code", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError('Start Date must be before or equal to End Date.')

    def get_data(self):
        result = []
        search_domain = [
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('company_id', '=', self.company_id.id),
            ('account_id', '=', self.account_id.id)
        ]
        if self.account_partner_ids:
            search_domain.append(('partner_id', 'in', self.account_partner_ids.ids))

        account_data = self.env['account.move.line'].sudo().read_group(
            domain=search_domain,
            fields=['partner_id', 'debit:sum', 'credit:sum', 'balance:sum'],
            groupby=['partner_id']
        )
        if not account_data:
            return []

        for acc in account_data:
            if not acc.get('partner_id'):
                continue
            partner = self.env['res.partner'].browse(acc['partner_id'][0])
            previous_search_domain = [
                ('date', '<', self.start_date),
                ('company_id', '=', self.company_id.id),
                ('account_id', '=', self.account_id.id),
                ('partner_id', '=', partner.id)
            ]
            previous_account_data = self.env['account.move.line'].sudo().read_group(
                domain=previous_search_domain,
                fields=['partner_id', 'debit:sum', 'credit:sum', 'balance:sum'],
                groupby=['partner_id']
            )
            previous_balance = previous_account_data[0]['balance'] if previous_account_data else 0
            result.append({
                'code': self.account_id.code,
                'name': partner.name,
                'debit': acc['debit'],
                'credit': acc['credit'],
                'previous_balance': previous_balance,
                'final': acc['balance'] + previous_balance,
            })

        return result

    def action_print(self):
        search_domain = [
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('company_id', '=', self.company_id.id),
            ('account_id', '=', self.account_id.id)
        ]
        if self.account_partner_ids:
            search_domain.append(('partner_id', 'in', self.account_partner_ids.ids))

        account_data = self.env['account.move.line'].sudo().read_group(
            domain=search_domain,
            fields=['partner_id', 'debit:sum', 'credit:sum', 'balance:sum'],
            groupby=['partner_id']
        )
        if account_data:
            return self.env.ref('custom_reports.action_employee_custody_report').report_action(self)
        else:
            raise ValidationError('No Data Found on this account for this period')




