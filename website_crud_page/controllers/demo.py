from odoo import http
from odoo.http import request

class DemoController(http.Controller):

    @http.route('/my/demo', type='http', auth='user', website=True)
    def portal_demo_data(self, **kw):
        demo_companies = request.env['demo.company'].sudo().search([])
        return request.render('website_crud_page.portal_demo_data_template', {
            'demo_companies': demo_companies,
        })

    @http.route('/my/demo/create', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def portal_demo_create(self, **kw):
        if request.httprequest.method == 'POST':
            name = kw.get('name')
            description = kw.get('description')
            if name:
                request.env['demo.company'].sudo().create({
                    'name': name,
                    'description': description,
                })
                return request.redirect('/my/demo')
        return request.render('website_crud_page.portal_demo_create_template')

    @http.route('/my/demo/edit/<int:company_id>', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def portal_demo_edit(self, company_id, **kw):
        company = request.env['demo.company'].sudo().browse(company_id)
        if request.httprequest.method == 'POST':
            name = kw.get('name')
            description = kw.get('description')
            if name:
                company.sudo().write({
                    'name': name,
                    'description': description,
                })
                return request.redirect('/my/demo')
        return request.render('website_crud_page.portal_demo_edit_template', {
            'company': company
        })

    @http.route('/my/demo/delete/<int:company_id>', type='http', auth='user', website=True)
    def portal_demo_delete(self, company_id, **kw):
        company = request.env['demo.company'].sudo().browse(company_id)
        if company.exists():
            company.sudo().unlink()
        return request.redirect('/my/demo')
