from odoo import models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def write(self, vals):
        res = super().write(vals)

        if 'state' in vals:
            for slip in self:

                # عند اعتماد الراتب
                if vals['state'] == 'done':
                    periods = self.env['sale.cash.commission.period'].search([
                        ('employee_id', '=', slip.employee_id.id),
                        ('state', '=', 'closed'),
                        ('date_from', '<=', slip.date_to),
                        ('date_to', '>=', slip.date_from),
                    ])
                    periods.write({'state': 'paid'})

                # عند إرجاعه إلى مسودة
                elif vals['state'] == 'draft':
                    periods = self.env['sale.cash.commission.period'].search([
                        ('employee_id', '=', slip.employee_id.id),
                        ('state', '=', 'paid'),
                        ('date_from', '<=', slip.date_to),
                        ('date_to', '>=', slip.date_from),
                    ])
                    periods.write({'state': 'closed'})

        return res