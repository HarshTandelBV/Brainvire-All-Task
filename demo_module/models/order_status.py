from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class OrderLine(models.Model):
    _name = 'demo.order.line'
    _description = 'Order Line'

    product_id = fields.Many2one('demo.product', string='Product')
    product_qty = fields.Integer(string='Quantity')
    price = fields.Float(compute='_compute_price', string='Price')
    order_id = fields.Many2one('demo.order.status', string='Order')

    @api.depends('product_id', 'product_qty')
    def _compute_price(self):
        for line in self:
            quantity_available = line.product_id.qty
            if quantity_available:
                if line.product_qty <= quantity_available:
                    line.price = line.product_id.price * line.product_qty
                else:
                    raise ValidationError(_(f"Only {line.product_id.qty} Quantity is available!"))
            else:
                line.price = 0.0


class OrderStatus(models.Model):
    _name = 'demo.order.status'
    _description = 'Order Status'

    name = fields.Many2one('demo.customer', string='Customer')
    status = fields.Selection(
        [('paid', 'Paid'),
         ('unpaid', 'Unpaid')],
        string='Order Status'
    )
    lines = fields.One2many('demo.order.line', 'order_id', string='Order Lines')

    @api.depends('status')
    def _update_product_qty(self):
        for order in self:
            if self.status == 'paid':
                for line in order.lines:
                    line.product_id.qty -= line.product_qty
            elif self.status == 'unpaid':
                for line in order.lines:
                    line.product_id.qty += line.product_qty

    @api.model
    def create(self, values):
        order = super(OrderStatus, self).create(values)
        order._update_product_qty()
        return order

    @api.model
    def write(self, vals):
        if 'status' in vals:
            old_status = self.status
            result = super(OrderStatus, self).write(vals)
            if self.status != old_status:
                self._update_product_qty()
            return result
        else:
            return super(OrderStatus, self).write(vals)
