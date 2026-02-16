# -*- coding: utf-8 -*-

from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestTrialBalancePdf(TransactionCase):
    def test_report_action_is_defined(self):
        self.assertTrue(self.env.ref('trial_balance_pdf.action_report_trial_balance'))

    def test_wizard_returns_report_action(self):
        wizard = self.env['trial.balance.report'].create({
            'start_date': fields.Date.to_date('2026-01-01'),
            'end_date': fields.Date.to_date('2026-01-31'),
            'state': 'posted',
        })
        action = wizard.button_to_get_pdf()
        self.assertIsInstance(action, dict)
        self.assertEqual(action.get('type'), 'ir.actions.report')
        self.assertEqual(action.get('report_name'), 'trial_balance_pdf.report_trial_balance')
        self.assertIn('data', action)
        self.assertIn('query', action['data'])
        self.assertIsInstance(action['data']['query'], list)
