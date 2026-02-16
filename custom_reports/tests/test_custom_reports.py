# -*- coding: utf-8 -*-

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestCustomReports(TransactionCase):
    def _create_account(self, code: str):
        selection = self.env['account.account'].fields_get(['account_type'])['account_type'].get('selection') or []
        account_type = selection[0][0] if selection else 'asset_current'
        return self.env['account.account'].create({
            'name': f'Test Account {code}',
            'code': code,
            'account_type': account_type,
            'company_id': self.env.company.id,
        })

    def test_report_action_is_defined(self):
        self.assertTrue(self.env.ref('custom_reports.action_employee_custody_report'))

    def test_date_range_constraint(self):
        account = self._create_account('TST1001')
        with self.assertRaises(ValidationError):
            self.env['custom.reports'].create({
                'start_date': fields.Date.to_date('2026-02-01'),
                'end_date': fields.Date.to_date('2026-01-01'),
                'account_id': account.id,
            })

    def test_action_print_raises_when_no_data(self):
        account = self._create_account('TST1002')
        report = self.env['custom.reports'].create({
            'start_date': fields.Date.to_date('2026-01-01'),
            'end_date': fields.Date.to_date('2026-01-31'),
            'account_id': account.id,
        })
        with self.assertRaises(ValidationError):
            report.action_print()
