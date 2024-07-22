from odoo import http
from odoo.http import request

class SaleOrderSearch(http.Controller):

    @http.route('/sale_order_search', type='json', auth='public', methods=['POST'])
    def search_sale_order(self, search_query="s00182"):
        SaleOrder = request.env['sale.order']
        sale_orders = SaleOrder.search([('name', 'ilike', search_query)])
        results = []
        for order in sale_orders:
            results.append({
                'name': order.name,
                'products': ', '.join(order.order_line.mapped('product_id.name')),
                'amount_total': order.amount_total,
                'tax': order.amount_tax,
                'portal_url': order.get_portal_url(),
            })
        return results