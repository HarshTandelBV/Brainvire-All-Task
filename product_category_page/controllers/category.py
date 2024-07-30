from odoo import http
from odoo.http import request


class ProductSaleController(http.Controller):

    @http.route('/category', type='http', auth='public', website=True)
    def product_category(self, page=1, **kwargs):
        product_category = request.env['product.category'].search([])
        return request.render('product_category_page.product_category_view', {
            'category': product_category
        })

    @http.route('/category/<model("product.category"):category>', type='http', auth='public', website=True)
    def products_by_category(self, category, **kwargs):
        products = request.env['product.template'].search([('categ_id', '=', category.id)])
        return request.render('product_category_page.products_by_category_view', {
            'category': category,
            'products': products
        })
