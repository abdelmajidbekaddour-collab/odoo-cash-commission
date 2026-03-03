from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleCashCommissionPeriod(models.Model):
    _name = 'sale.cash.commission.period'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'فترة عمولة المبيعات للموظفين'
    _order = 'date_from desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    # تغيير الحقل ليرتبط بالموظف
    employee_id = fields.Many2one('hr.employee', string='الموظف', required=True)
    date_from = fields.Date(string='من تاريخ', required=True)
    date_to = fields.Date(string='إلى تاريخ', required=True)

    state = fields.Selection([
        ('draft', 'مسودة'),
        ('closed', 'مغلقة'),
        ('paid', 'رُحلت للرواتب')
    ], default='draft', string='الحالة')

    payslip_id = fields.Many2one(
        'hr.payslip',
        string='Payslip',
        readonly=True,
        copy=False
    )

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    commission_line_ids = fields.One2many('sale.cash.commission.line', 'period_id', string='سطور العمولات')
    total_amount = fields.Monetary(compute='_compute_total', store=True, currency_field='currency_id',
                                   string='إجمالي العمولة')

    @api.depends('commission_line_ids.commission_amount')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.commission_line_ids.mapped('commission_amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.cash.commission.period') or '/'
        return super().create(vals_list)

    def action_close(self):
        for rec in self:
            lines = self.env['sale.cash.commission.line'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'open'),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to),
                ('period_id', '=', False)
            ])
            if not lines:
                raise UserError(_("No open commission records for this employee in this period."))

            lines.write({'period_id': rec.id, 'state': 'closed'})
            rec.state = 'closed'

    def write(self, vals):
        res = super().write(vals)

        if 'state' in vals:
            for rec in self:

                # عندما تصبح الفترة Paid
                if vals['state'] == 'paid':
                    rec.commission_line_ids.write({'state': 'invoiced'})

                # عند الرجوع من Paid إلى Closed
                elif vals['state'] == 'closed':
                    rec.commission_line_ids.filtered(
                        lambda l: l.state == 'invoiced'
                    ).write({'state': 'closed'})

        return res