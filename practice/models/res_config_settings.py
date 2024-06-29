from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_discount = fields.Float(string='Discount', readonly=False, config_parameter='practice.custom_discount')


