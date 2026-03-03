
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.model_create_multi
    def create(self, vals_list):
        # 1. إنشاء سجلات التسوية
        records = super(AccountPartialReconcile, self).create(vals_list)

        # 2. إجبار أودو على حفظ البيانات في قاعدة البيانات (ضروري في أودو 18)
        records.flush_recordset()

        # 3. استدعاء دالة العمولات
        # نستخدم sudo لتجنب أي مشاكل في الصلاحيات
        records.sudo()._create_cash_commission()

        return records


    def _create_cash_commission(self):
        commission_line_obj = self.env['sale.cash.commission.line']
        commission_vals_list = []

        for rec in self:
            # 1. تحديد أي طرف هو الفاتورة (Invoice/Credit Note) وأي طرف هو الدفع
            # في المرتجعات، الفاتورة قد تكون في الطرف الدائن أو المدين حسب نوع التسوية
            move_debit = rec.debit_move_id.move_id
            move_credit = rec.credit_move_id.move_id

            invoice_move = False
            # نتحقق من النوع (out_invoice هي فاتورة، out_refund هو إشعار دائن/مرتجع)
            if move_debit.move_type in ['out_invoice', 'out_refund']:
                invoice_move = move_debit
            elif move_credit.move_type in ['out_invoice', 'out_refund']:
                invoice_move = move_credit

            # التحقق من وجود الفاتورة وحالتها
            if not invoice_move or invoice_move.state != 'posted':
                continue

            # 2. تحديد المعامل (Sign)
            # الفاتورة العادية (+) والمرتجع (-)
            sign = -1 if invoice_move.move_type == 'out_refund' else 1

            # جلب الموظفين المرتبطين
            employees = invoice_move.commission_employee_ids
            if not employees:
                continue

            # 3. حساب النسبة بناءً على المبلغ المدفوع
            # نستخدم abs() لتجنب المشاكل في حال كانت المبالغ مسجلة بالسالب في بعض الحالات
            total_to_compare = abs(invoice_move.amount_total)
            ratio = abs(rec.amount) / total_to_compare if total_to_compare > 0 else 0

            invoice_lines = invoice_move.invoice_line_ids.filtered(lambda l: l.display_type == 'product')

            for employee in employees:
                for line in invoice_lines:
                    # التحقق من عدم التكرار
                    existing = commission_line_obj.search_count([
                        ('reconcile_id', '=', rec.id),
                        ('employee_id', '=', employee.id),
                        ('invoice_line_id', '=', line.id)
                    ])
                    if existing > 0:
                        continue

                    product = line.product_id
                    if not product:
                        continue

                    # جلب النسبة
                    user_rule = product.product_tmpl_id.user_commission_ids.filtered(
                        lambda r: r.employee_id == employee
                    )
                    actual_rate = user_rule[0].commission_rate if user_rule else product.commission_rate

                    if actual_rate <= 0:
                        continue

                    # حساب المبالغ مع مراعاة الإشارة (موجب للفاتورة وسالب للمرتجع)
                    # price_subtotal في أودو يكون دائماً موجباً في المرتجع، لذا الـ sign هنا حاسم
                    proportional_paid = (line.price_subtotal * ratio) * sign
                    commission_amount = (proportional_paid * actual_rate) / 100

                    commission_vals_list.append({
                        'invoice_id': invoice_move.id,
                        'invoice_line_id': line.id,
                        'employee_id': employee.id,
                        'product_id': product.id,
                        'reconcile_id': rec.id,
                        'paid_amount': proportional_paid,
                        'commission_rate': actual_rate,
                        'commission_amount': commission_amount,
                        'date': fields.Date.context_today(self),
                    })

        if commission_vals_list:
            commission_line_obj.create(commission_vals_list)
