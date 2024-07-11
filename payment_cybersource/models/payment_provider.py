import base64
import hashlib
import hmac
import json
from datetime import datetime
import pytz
import requests
from odoo import models, fields, api
from odoo.addons.payment_cybersource import const


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cybersource', "Cybersource")], ondelete={'cybersource': 'set default'})

    cybersource_merchant_id = fields.Char(string='Cybersource Merchant ID')
    cybersource_api_key_id = fields.Char(string='Cybersource API Key ID')
    cybersource_secret_key = fields.Char(string='Cybersource Secret Key')

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'cybersource':
            return default_codes
        return const.DEFAULT_PAYMENT_METHODS_CODES

    @api.model
    def _get_payment_method_information(self):
        """Override to add createtest payment method information to the
        existing methods.
        """
        res = super()._get_payment_method_information()
        res['createtest'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res

    @staticmethod
    def get_digest(payload):
        hashobj = hashlib.sha256()
        hashobj.update(json.dumps(payload).encode('utf-8'))
        hash_data = hashobj.digest()
        digest = base64.b64encode(hash_data).decode('utf-8')
        return f'SHA-256={digest}'

    def get_signature(self, method, time, digest):

        secret_key = self.cybersource_secret_key
        merchant_id = self.cybersource_merchant_id
        key_id = self.cybersource_api_key_id

        resource = '/pts/v2/payments'

        request_host = 'apitest.cybersource.com'
        header_list = []

        header_list.append(f'keyid="{key_id}"')
        header_list.append('algorithm="HmacSHA256"')
        postheaders = "host date request-target digest v-c-merchant-id"
        header_list.append(f'headers="{postheaders}"')

        signature_list = [
            f'host: {request_host}\n',
            f'date: {time}\n',
            f'request-target: {method.lower()} {resource}\n',
            f'digest: {digest}\n',
            f'v-c-merchant-id: {merchant_id}'
        ]

        sig_value = ''.join(signature_list)
        secret = base64.b64decode(secret_key)
        hash_value = hmac.new(secret, sig_value.encode('utf-8'), hashlib.sha256)
        signature = base64.b64encode(hash_value.digest()).decode('utf-8')

        header_list.append(f'signature="{signature}"')
        token = ', '.join(header_list)
        return token

    def make_payment_request(self, payload):

        utc_now = datetime.now(pytz.UTC)
        time = utc_now.strftime('%a, %d %b %Y %H:%M:%S GMT')

        digest = self.get_digest(payload)
        signature = self.get_signature('POST', time, digest)

        headers = {
            "host": "apitest.cybersource.com",
            "signature": signature,
            "digest": digest,
            "v-c-merchant-id": self.cybersource_merchant_id,
            "date": time,
            "Content-Type": "application/json"
        }

        request_target = 'https://apitest.cybersource.com/pts/v2/payments'

        try:
            response = requests.post(request_target, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
