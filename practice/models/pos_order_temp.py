from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    custom_note = fields.Char(string='Custom Note',readonly=True)
    discount_applied = fields.Boolean(string='Discount Applied', readonly=True)
    location = fields.Char(string='Location')
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['custom_note'] = ui_order.get('custom_note')
        order_fields['discount_applied'] = ui_order.get('discount_applied')
        order_fields['location'] = ui_order.get('location')
        return order_fields


