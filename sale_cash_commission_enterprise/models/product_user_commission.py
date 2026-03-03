from odoo import models, fields



class ProductUserCommission(models.Model):
    _name = 'product.user.commission'
    _description = 'User Product Commission Rate'

   # user_id = fields.Many2one('res.users', string="Salesperson", required=True)
    # إضافة domain=[] تضمن عدم وجود فلاتر مخفية
    # user_id = fields.Many2one(
    #     'res.users',
    #     string="Salesperson",
    #     required=True,
    #     domain=[]
    # )
    # التغيير هنا ليشمل الموظف
    employee_id = fields.Many2one('hr.employee', string="Salesperson (Employee)", required=True)
    product_tmpl_id = fields.Many2one('product.template', string="Product", required=True)
    commission_rate = fields.Float(string="Commission %", required=True)
    _sql_constraints = [
        ('user_product_unique', 'unique(employee_id, product_tmpl_id)',
         'لا يمكنك وضع نسبتين عمولة لنفس المندوب في نفس المنتج!')
    ]