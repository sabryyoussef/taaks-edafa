# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class CustomReports(models.Model):
    _name = 'custom.reports'

    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    account_partner_ids = fields.Many2many('res.partner',string="Account Name")
    account_id = fields.Many2one('account.account',string="Account Code")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

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
        if account_data:
            for acc in account_data:
                data = {}
                if 'partner_id' in acc and acc['partner_id']:
                    partner_id = self.env['res.partner'].browse(acc['partner_id'][0])
                    previous_search_domain = [
                        ('date', '<', self.start_date),
                        ('company_id', '=', self.company_id.id),
                        ('account_id', '=', self.account_id.id),
                        ('partner_id','=',partner_id.id)
                    ]
                    previous_account_data = self.env['account.move.line'].sudo().read_group(
                        domain=previous_search_domain,
                        fields=['partner_id', 'debit:sum', 'credit:sum', 'balance:sum'],groupby=['partner_id']
                    )
                    previous_balance = 0
                    if previous_account_data:
                        previous_balance += previous_account_data[0]['balance']
                    data.update({
                        'code':self.account_id.code,
                        'name':partner_id.name,
                        'debit':acc['debit'],
                        'credit':acc['credit'],
                        'previous_balance':previous_balance ,
                        'final':acc['balance'] + previous_balance
                    })
                    result.append(data)
            return result
        else:
            pass

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




