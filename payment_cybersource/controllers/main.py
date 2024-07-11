from odoo import http
from odoo.http import request
import json


class PaymentController(http.Controller):

    @http.route('/cybersource/get_signature', type='json', auth='public', methods=['POST'], csrf=False)
    def get_signature(self, **kwargs):
        payload = kwargs.get('payload')
        request_method = kwargs.get('request_method')
        request_path = kwargs.get('request_path')

        # Get the payment provider record
        provider = request.env['payment.provider'].sudo().search([('code', '=', 'cybersource')], limit=1)

        if not provider:
            return {'error': 'Cybersource provider not found'}

        signature_header = provider.get_cybersource_signature_header(payload, request_method, request_path)
        return {'signature': signature_header}
