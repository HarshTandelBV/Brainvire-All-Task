from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.model
    def action_send_email(self, record_ids):
        _logger.info(f'Record IDs received for email: {record_ids}')
        print('----------', record_ids)
        records = self.browse(record_ids)
        for record in records:
            template_id = self.env.ref('event_managment_system.email_template_id').id
            self.env['mail.template'].browse(template_id).send_mail(record.id, force_send=True)
            _logger.info(f'Email sent to expense record: {record.id}')
