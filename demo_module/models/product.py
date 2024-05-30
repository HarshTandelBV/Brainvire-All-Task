from odoo import fields, models, api


class Product(models.Model):
    _name = 'demo.product'
    _description = 'Description'

    name = fields.Char(string='Name')
    # category_id = fields.Many2one(string='Category')
    qty = fields.Integer(string='Quantity')
    price = fields.Float(string='Price')

