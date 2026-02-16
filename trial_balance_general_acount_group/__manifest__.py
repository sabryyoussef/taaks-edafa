
#############################################################################
{
    'name': "General Trial Balance PDF Report with account group",
    'version': '16.0.1.0.0',
    'category': "Accounting",
    'summary': """This module will helps to get the general trial balance report in 
    PDF format with account group""",
    'description': """The module provides a pdf report of the general trial balance in
     the Odoo Community Version's Accounting App.""",
 
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'report/trial_balance_report.xml',
        'wizard/trial_balance_report_view.xml',
        'views/account_account.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
