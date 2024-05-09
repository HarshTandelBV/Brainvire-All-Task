from odoo import fields, models


class EventSponsor(models.Model):
    _name = "event.sponsor"
    _description = "Event Sponsors details"

    name = fields.Char(string="Name")
    logo = fields.Binary(string="Logo")
    website = fields.Char(string="Website")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone No")
    sponsorship_level = fields.Selection([
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze')
    ])
    event_ids = fields.Many2many('event.event',string="Event Details")