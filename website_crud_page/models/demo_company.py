from odoo import fields, models


class DemoCompany(models.Model):
    _name = 'demo.company'
    _description = 'Demo Company'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
