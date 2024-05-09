from odoo import models, fields, _


class EventSession(models.Model):
    _name = "event.track"
    _description = "Event sessions details"

    event = fields.Many2one("event.event", string="Event")
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
    guest_ids = fields.Many2many('event.guest', string="Guests")
    event_counts = fields.Integer(string="Total Sessions", compute='_compute_event_count')

    def _compute_event_count(self):
        for rec in self:
            event_counts = self.env['event.track'].search_count([('event', '=', rec.event)])
            self.event_counts = event_counts

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)
        default['start_time'] = None
        default['end_time'] = None
        return super(EventSession, self).copy(default)
