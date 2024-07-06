from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', "To Approve"), ('sale',)])

    def action_approve(self):
        for order in self:
            super(SaleOrder, order).action_confirm()


    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'to_approve'}

    def action_confirm(self):
        for order in self:
            sales_limit = float(self.env['ir.config_parameter'].sudo().get_param('practice.sales_limit', default=0.0))
            if order.amount_total > sales_limit:
                order.state = 'to_approve'
            else:
                super(SaleOrder, self).action_confirm()
