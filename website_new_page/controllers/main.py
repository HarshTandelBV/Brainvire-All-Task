import requests
from odoo import http
from odoo.http import request


class NewPageViewController(http.Controller):
    @http.route('/new_page', type='http', auth="public", website=True)
    def new_page_route(self, **kwargs):
        return request.render("website_new_page.new_page")

    @http.route('/new_page/submit', type='http', auth="public", website=True, csrf=False)
    def new_page_submit(self, **post):
        if post.get('name') and post.get('email') and post.get('message'):
            if request.env.user.id != http.request.env.ref('base.public_user').id:
                # If the user is signed in (not a public user)
                request.env['internal.form'].sudo().create({
                    'user_id': request.env.user.id,
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'message': post.get('message'),
                })
            else:
                # If the user is not signed in (public user)
                request.env['public.form'].sudo().create({
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'message': post.get('message'),
                })
            return request.redirect('/thank_you')

    @http.route('/thank_you', type='http', auth="public", website=True)
    def thank_you_page(self, **kwargs):
        return request.render("website_new_page.thank_you_page")
