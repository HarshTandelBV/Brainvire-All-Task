from odoo import fields, models, api
from datetime import date, datetime


class Practice(models.Model):
    _name = 'practice.practice'
    _description = "practice"
    _rec_name = 'display_name'

    customer_id = fields.Many2one('res.partner', 'Customer')
    title = fields.Many2one(related='customer_id.title')
    display_name = fields.Char(compute='_compute_display_name')
    dob = fields.Date('DOB')
    age = fields.Integer('Age', compute='compute_age')

    @api.depends('dob')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.depends('customer_id.name', 'title')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.title.name or ''} . {rec.customer_id.name or ''}"

    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []

        if name:
            domain = ['|','|', ('customer_id.name', operator, name), ('display_name', operator, name),('customer_id.email', operator, name)]

        records = self.search(domain + args, limit=limit)
        return [(record.id, record.display_name) for record in records]

    def name_get(self):
        result = []
        for rec in self:
            name = rec.display_name
            result.append((rec.id, name))
        return result