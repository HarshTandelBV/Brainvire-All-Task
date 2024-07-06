from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleApproval(models.Model):
    _name = 'sale.approval'
    _description = 'sale approval'

    name = fields.Char(string="Order Reference")
    partner_name = fields.Char(string="Customer")
    date_order = fields.Datetime(
        string="Order Date", required=True, copy=False,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
        default=fields.Datetime.now)
    amount_total = fields.Monetary(string="Total", store=True)
    currency_id = fields.Many2one(comodel_name='res.currency')

