from odoo import models, fields


class ResLocation(models.Model):
    _name = 'res.location'
    _description = 'Shop Locations'

    name = fields.Char(string='Location Name', required=True)
