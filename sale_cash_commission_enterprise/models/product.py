from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # النسبة الافتراضية (تستخدم إذا لم يجد النظام نسبة للمستخدم)
    commission_rate = fields.Float(string="Default Commission %")

    # commission_account_id = fields.Many2one(
    #     'account.account',
    #     string="Commission Expense Account",
    #     domain="[('account_type', '=', 'expense')]"
    # )
    # إضافة جدول النسب داخل صفحة المنتج
    user_commission_ids = fields.One2many(
        'product.user.commission',
        'product_tmpl_id',
        string="User Specific Commissions"
    )