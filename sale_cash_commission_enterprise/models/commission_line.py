from odoo import models, fields, api

class SaleCashCommissionLine(models.Model):
    _name = 'sale.cash.commission.line'
    _description = 'Cash Based Commission Line'
    _order = 'date desc'
    _rec_name = 'invoice_id'

    invoice_id = fields.Many2one('account.move', required=True, ondelete='cascade')
    invoice_line_id = fields.Many2one('account.move.line', required=True)


    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, index=True)
    partner_id = fields.Many2one(related='invoice_id.partner_id', store=True)

    product_id = fields.Many2one('product.product')

    reconcile_id = fields.Many2one('account.partial.reconcile', index=True)

    paid_amount = fields.Monetary(required=True)
    commission_rate = fields.Float(required=True)
    commission_amount = fields.Monetary(required=True)

    currency_id = fields.Many2one(related='invoice_id.currency_id', store=True)

    date = fields.Date(index=True)

    # ← هذا هو المفتاح لربط الـ line مع period
    period_id = fields.Many2one(
        'sale.cash.commission.period',
        string='Commission Period'
    )

    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('invoiced', 'Invoiced')
    ], default='open', index=True)