from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager

class ProductSaleController(http.Controller):

    @http.route(['/product_sales', '/product_sales/page/<int:page>'], type='http', auth='public', website=True)
    def product_sales(self, page=1, **kwargs):
        PAGE_SIZE = 10
        try:
            page = int(page)
        except ValueError:
            page = 1

        product_templates = request.env['product.template'].search([('detailed_type', '=', 'product')])
        sale_order_lines = request.env['sale.order.line'].search([])

        total_templates = len(product_templates)

        pager_obj = pager(
            url='/product_sales',
            total=total_templates,
            page=page,
            step=PAGE_SIZE,
            scope=7,
        )

        # Get the current page of product templates
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        templates_page = product_templates[start:end]

        product_data = []
        for template in templates_page:
            products = request.env['product.product'].search([('product_tmpl_id', '=', template.id)])

            # Calculate sales data
            sales_lines = sale_order_lines.filtered(lambda line: line.product_id.product_tmpl_id == template)
            revenue = sum(line.price_unit * line.product_uom_qty for line in sales_lines)

            image_url = f'/web/image/product.template/{template.id}/image_1920'

            product_data.append({
                'id': template.id,
                'name': template.name,
                'sold_quantity': sum(line.product_uom_qty for line in sales_lines),
                'revenue': revenue,
                'image_url': image_url,
                'sales': [{
                    'order': line.order_id.name,
                    'price': line.price_unit,
                    'subtotal': line.price_subtotal,
                    'tax': ', '.join(tax.name for tax in line.tax_id),
                    'quantity': line.product_uom_qty
                } for line in sales_lines]
            })

        # Return the template with pagination data
        return request.render('custom_dashboard.product_sales_page', {
            'products': product_data,
            'pager': pager_obj
        })
