{
    'name': 'Cash-Based Sales Commission (Enterprise)',
    'version': '18.0.1.0.2',
    'summary': 'Automate sales commissions based on actual cash collection, supporting partial payments, credit notes, and payroll integration.',
    'description': """
        This module provides an advanced solution for managing sales commissions in Odoo.
        Key features include:
        - Cash-basis calculation (payment reconciliation).
        - Support for partial payments and credit notes.
        - Automated calculation pushed directly to Payroll.
        - Smart validation to prevent data entry errors.
    """,
    'category': 'Sales',
    'author': 'Abdel Madjid',
    'website': 'www.linkedin.com/in/abdelmadjid-bekaddour-97286b3a3',
    'license': 'OPL-1',
    'price': 49.00,
    'currency': 'EUR',
    'depends': [
        'sale',
        'account',
        'hr',
        'hr_payroll',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/payroll_enterpris.xml',
        'views/product_views.xml',
        'views/commission_line_views.xml',
        'views/commission_period_views.xml',
        'views/account_move_views.xml',
        'views/menus.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/config.png',
        'static/description/empoloyee_commission.png',
        'static/description/invoice.png',
        'static/description/commission_line_filters.png',
        'static/description/periods.png',
        'static/description/validation.png',
        'static/description/payslip.png',
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
