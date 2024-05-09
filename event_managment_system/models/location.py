from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class EventLocation(models.Model):
    _name = "event.location"
    _description = "event locations details"
    _rec_name = "location_name"

    location_name = fields.Char(string="Location")
    address = fields.Text(string="Address")
    capacity = fields.Integer(string="Capacity")
    priority = fields.Selection([
        ('0', '0 Star'),
        ('1', '1 Star'),
        ('2', '2 Star'),
        ('3', '3 Star'),
        ('4', '4 Star'),
        ('5', '5 Star')
    ], string="Priority")
    facilities = fields.Many2many('event.facilities', string="Facilities")

    _sql_constraints = [
        ('unique_location_name', 'UNIQUE(location_name)', 'Location name must be unique!')
    ]

