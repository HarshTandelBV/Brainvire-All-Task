from odoo import models, api,_
from odoo.exceptions import UserError


class HrExpenseButton(models.Model):
    _inherit = 'hr.expense'

    @api.model
    def send_email_method(self, record_ids):
        # Your logic to send email
        records = self.browse(record_ids)
        template_id = self.env.ref('event_managment_system.email_template_id').id

        if not template_id:
            raise UserError(_('Email template not found. Please configure an email template.'))

        for record in records:
            # Send email using the template
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(record.id, force_send=True)

        return True
