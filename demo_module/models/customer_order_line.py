from odoo import fields, models, api


class CustomerOrderLine(models.Model):
    _name = 'demo.customer.order.line'
    _description = 'it contain demo custonmer order data details'

    name = fields.Char(string='Name')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    disability = fields.Boolean(string='Disability')
    image = fields.Binary(string='Profile Photo')
    email = fields.Char(string='Email')
    dob = fields.Date(string='Date Of Birth')
    country = fields.Many2one('res.country', string='Country')

