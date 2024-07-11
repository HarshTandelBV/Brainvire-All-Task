from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def capture_in_cybersource(self):
        provider = self.env['payment.provider'].search([('code', '=', 'cybersource')], limit=1)

        if not provider:
            raise ValueError("Cybersource provider not configured.")

        payment_data = {
            "clientReferenceInformation": {
                "code": self.name
            },
            "processingInformation": {
                "capture": True
            },
            "orderInformation": {
                "amountDetails": {
                    "totalAmount": self.amount_total,
                    "currency": self.currency_id.name
                },
                "billTo": {
                    "firstName": self.partner_id.name,
                    "lastName": self.partner_id.name,
                    "address1": self.partner_id.street,
                    "locality": self.partner_id.city,
                    "administrativeArea": self.partner_id.state_id.code,
                    "postalCode": self.partner_id.zip,
                    "country": self.partner_id.country_id.code,
                    "email": self.partner_id.email
                }
            },
            "paymentInformation": {
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "12",
                    "expirationYear": "2031",
                    "securityCode": "123"
                }
            }
        }

        print(payment_data)
        response = provider.make_payment_request(payment_data)
        print(response)

        if response.get('status') == 'AUTHORIZED':
            self.action_approve()

            invoice = self._create_invoices()
            if invoice:
                invoice.action_post()

                # Create payment transaction record
                self.env['payment.transaction'].create({
                    'amount': self.amount_total,
                    'currency_id': self.currency_id.id,
                    'provider_id': provider.id,
                    'payment_method_id': provider.id,
                    'reference': self.name,
                    'partner_id': self.partner_id.id,
                    'state': 'done',
                    'sale_order_ids': [(6, 0, [self.id])],
                })
            else:
                raise UserError("Invoice creation failed.")
