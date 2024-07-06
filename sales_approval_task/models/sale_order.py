from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', "To Approve"), ('sale',)])

    def action_approve(self):
        for order in self:
            super(SaleOrder, order).action_confirm()

            approval_record = self.env['sale.approval'].search([('name', '=', order.name)])
            if approval_record:
                approval_record.unlink()

    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'to_approve'}

    def action_confirm(self):
        for order in self:
            sales_limit = float(self.env['ir.config_parameter'].sudo().get_param('practice.sales_limit', default=0.0))
            if order.amount_total > sales_limit:
                order.state = 'to_approve'
                self.env['sale.approval'].create({
                    'name': order.name,
                    'partner_name': order.partner_id.name,
                    'date_order': order.date_order,
                    'amount_total': order.amount_total,
                    'currency_id': order.currency_id.id,
                })
            else:
                super(SaleOrder, self).action_confirm()
