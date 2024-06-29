from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    custom_note = fields.Char(string='Custom Note')

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['custom_note'] = ui_order.get('custom_note')
        return order_fields
