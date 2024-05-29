from odoo import fields, models, api


class CustomerRegistration(models.Model):
    _name = 'demo.customer'
    _description = 'it contain demo custonmer details'

    name = fields.Char(string='Name')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    disability = fields.Boolean(string='Disability')
    image = fields.Binary(string='Profile Photo')
    email = fields.Char(string='Email')
    dob = fields.Date(string='Date Of Birth')
    country = fields.Many2one('res.country', string='Country')

    # @api.model
    # def create(self, vals_list):
    #
    #     order_line = self.env['demo.customer.order.line']
    #     rtn = super(CustomerRegistration, self).create(vals_list)
    #     order_line.create(vals_list)
    #     return rtn

    @api.onchange('disability')
    def _onchange_disability(self):
        if self.disability == True:
            self.env['demo.customer.order.line'].create({
                'name': self.name,
                'id': self.id
            })
