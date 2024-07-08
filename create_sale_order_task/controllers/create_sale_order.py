from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden

class CreateSaleOrder(http.Controller):

    @http.route('/create_sale_order', type='json', auth="public", methods=['POST'])
    def create_sale_order(self, **kwargs):
        data = request.get_json_data()

        partner_id = data.get('partner_id')
        order_lines = data.get('order_lines', [])

        if not partner_id or not order_lines:
            return Forbidden()

        order_vals = {
            'partner_id': partner_id,
            'order_line': [(0, 0, {
                'product_id': line.get('product_id'),
                'product_uom_qty': line.get('quantity'),
                'price_unit': line.get('price'),
            }) for line in order_lines]
        }

        sale_order = request.env['sale.order'].sudo().create(order_vals)

        return {
            "message": "Sale Order Created",
            "order_id": sale_order.id
        }
