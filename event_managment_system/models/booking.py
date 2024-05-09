from odoo import fields, models, _
from odoo.exceptions import UserError


class EventBooking(models.Model):
    _name = "event.booking"
    _description = "Event booking details"
    _rec_name = "attendee_id"

    event_id = fields.Many2one('event.event', string="Event")
    attendee_id = fields.Many2one('event.registration', string="Attendee", domain="[('event','=',event_id)]")
    booking_date = fields.Datetime(string="Booking Date", help="Enter your booking date for the event")
    status = fields.Selection(related='attendee_id.registration_status', string="Status")
    total_price = fields.Monetary(string="Total Price")
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'INR')]).id,
                                  readonly=True)
    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    ], default='unpaid', string="Payment Status", required=True)
    payment_transaction_id = fields.Char(string="Payment Transaction Id", help="Enter the transaction id carefully")

    def unlink(self):
        for rec in self:
            if rec.payment_status == 'paid':
                raise UserError(_("Record cannot be deleted if payment status is paid"))
        return super(EventBooking, self).unlink()

    def write(self, vals):
        if 'payment_status' in vals and vals['payment_status'] == 'paid':
            vals['status'] = 'confirmed'
            attendee_reg = self.env['event.registration'].browse(self.attendee_id.id)
            if attendee_reg and attendee_reg.registration_status == 'draft' or 'cancelled':
                attendee_reg.registration_status = 'confirmed'
        return super(EventBooking, self).write(vals)

    def action_done(self):
        for rec in self:
            rec.payment_status = 'paid'

    def payment_status_update(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'booking.payment.status.wizard',
            'view_mode': 'form',
            'target': 'new'
        }
