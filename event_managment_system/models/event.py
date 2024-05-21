from odoo import models, fields, api, _


class EventEvent(models.Model):
    _name = 'event.event'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Event'

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string="Description")
    start_date = fields.Datetime(string='Start Date', tracking=True)
    end_date = fields.Datetime(string="End Date", tracking=True)
    location = fields.Char(string="Location")
    guest_ids = fields.Many2many('event.guest', string="Guest", tracking=True)
    registration_open_date = fields.Datetime(string='Registration Open Date', tracking=True)
    registration_close_date = fields.Datetime(string='Registration Close Date', tracking=True)
    booking_ids = fields.One2many('event.booking', 'event_id', string='Attendee_list')
    sponsor_ids = fields.Many2many('event.sponsor', string="Sponsors")
    ticket_ids = fields.One2many('event.ticket', 'event_id', string="Tickets record")
    session_count = fields.Integer(string="Total Sessions", compute='_compute_event_count')
    ticket_count = fields.Integer(string='Total Tickets', compute='_compute_ticket_count')
    attendee_count = fields.Integer(string='Total Attendee', compute='_compute_attendee_count')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        domain = args + ['|',('location', operator, name),('description',operator,name)]
        records = self.search(domain,limit=limit)
        return records.name_get()


    def _compute_event_count(self):
        for rec in self:
            session_count = self.env['event.track'].search_count([('event', '=', rec.name)])
            self.session_count = session_count


    def _compute_ticket_count(self):
        for rec in self:
            ticket_count = self.env['event.ticket'].search_count([('event_id', '=', rec.name)])
            self.ticket_count = ticket_count


    def _compute_attendee_count(self):
        for rec in self:
            attendee_count = self.env['event.registration'].search_count([('event', '=', rec.name)])
            self.attendee_count = attendee_count


    def action_open_ticket_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'res_model': 'event.ticket',
            'domain': [('event_id', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


    def action_open_session(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sessions',
            'res_model': 'event.track',
            'domain': [('event', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


    def action_open_attendee_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendee',
            'res_model': 'event.registration',
            'domain': [('event', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


class EventTicket(models.Model):
    _name = 'event.ticket'
    _description = 'Event ticket details'

    event_id = fields.Many2one('event.event', string='Event')
    ticket_type = fields.Char(string="Ticket type")
    price = fields.Integer(string="Price")
    available_ticket = fields.Integer(string="Available tickets")
