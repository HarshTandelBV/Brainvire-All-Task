from odoo import fields, models, api


class OwlTodoList(models.Model):
    _name = 'owl.todo.list'
    _description = 'OWL todo list app'

    name = fields.Char(string='Task Name')
    completed = fields.Boolean()
    color = fields.Char()
