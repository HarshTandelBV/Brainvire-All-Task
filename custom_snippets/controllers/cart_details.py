from odoo import http
from odoo.http import request

class CartController(http.Controller):

    @http.route('/shop/cart/get_cart_details', type='json', auth="public", website=True)
    def get_cart_details(self):
        order = request.website.sale_get_order()
        total_items = sum(line.product_uom_qty for line in order.order_line) if order else 0
        total_amount = order.amount_total if order else 0.0
        return {
            'total_items': total_items,
            'total_amount': total_amount,
        }
