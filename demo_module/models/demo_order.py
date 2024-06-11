from odoo import fields, models, api


class DemoOrder(models.Model):
    _name = 'demo.order'
    _description = 'Description'

    customer_id = fields.Many2one('demo.customer', 'Customer')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], 'Gender')
    phone = fields.Char('Phone')

    @api.onchange('gender')
    def _onchange_gender(self):
        for rec in self:
            return {'domain': {'customer_id': [('gender', '=', rec.gender)]}}

    @api.onchange('customer_id')
    def _onchange_phone(self):
        if self.customer_id:
            self.phone = self.customer_id.phone
        else:
            self.phone = False
