from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_limit = fields.Float(string='Sales Limit', readonly=False, config_parameter='practice.sales_limit')



