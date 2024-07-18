from odoo import fields, models, api


class CustomForm(models.Model):
    _name = 'public.form'
    _description = 'Custom Form'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    message = fields.Text(string="Message", required=True)
