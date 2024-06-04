import pdb

from odoo import fields, models


class BookingPaymentStatusWizard(models.TransientModel):
    _name = "booking.payment.status.wizard"
    _description = "This is a wizard which will update the information of booking"

    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    ], string="Payment Status", required=True)

    def update_payment_status(self):
        pdb.set_trace()
        print("Changed Successfully")

        self.env['event.booking'].browse(self._context.get('active_ids')).update({'payment_status': self.payment_status})
        return True
