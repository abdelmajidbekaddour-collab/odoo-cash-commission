from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    commission_employee_ids = fields.Many2many(
        'hr.employee',
        'account_move_commission_employee_rel',  # تغيير اسم جدول الربط لتجنب التعارض
        'move_id',
        'employee_id',
        string='Commission Employees',
        compute='_compute_commission_employee_ids',
        store=True,
        readonly=False,
        help="اختر الموظفين الذين سيحصلون على العمولة"
    )

    @api.depends('invoice_user_id')
    def _compute_commission_employee_ids(self):
        for move in self:
            # البحث عن الموظف المرتبط بالمستخدم المختار في الفاتورة
            employee = self.env['hr.employee'].search([('user_id', '=', move.invoice_user_id.id)], limit=1)
            if employee:
                move.commission_employee_ids = [fields.Command.set([employee.id])]
            else:
                move.commission_employee_ids = [fields.Command.clear()]