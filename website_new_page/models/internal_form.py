from odoo import fields, models, api


class InternalForm(models.Model):
    _name = 'internal.form'
    _description = 'Internal Form'

    user_id = fields.Many2one('res.users', required=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    message = fields.Text(string="Message", required=True)
