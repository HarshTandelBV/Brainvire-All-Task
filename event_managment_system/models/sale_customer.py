from datetime import date

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    sale_ids = fields.One2many('sale.order','partner_id',string='sales Details')
    total_sale_amount = fields.Float(compute="_compute_total")
    dob = fields.Date(string="DOB")

    def _compute_total(self):
        total = 0
        for item in self.sale_ids:
            total = total + item.amount_total
        self.total_sale_amount = round(total, 2)

    @api.model
    def _customer_birthday_reminder(self):
        today = date.today()
        customer_with_birthday = self.search([('dob', '=', today)])

        for customer in customer_with_birthday:
            self.env['mail.mail'].create({
                'subject': "Happy Birthday!",
                'body_html': f"<p>Happy Birthday, {customer.name}!</p>",
                'email_to': customer.email,
            }).send()

    def action_customer_sale_details(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('event_managment_system.customer_email_template')
        ctx = {
            'default_model': 'res.partner',
            'default_res_ids': self.ids,
            'default_template_id': mail_template if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
