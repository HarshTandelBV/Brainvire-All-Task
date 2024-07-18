from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    location_ids = fields.Many2many('res.location', string='Locations')

