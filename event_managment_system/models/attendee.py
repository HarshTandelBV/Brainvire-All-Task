from datetime import date, datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class AttendeeRegistration(models.Model):
    _name = "event.registration"
    _description = "attendee registration details"
    _rec_name = 'display_name'

    event = fields.Many2one('event.event', string="Event")
    display_name = fields.Char(compute='_compute_display_name')
    attendee = fields.Char(string="Attendee")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(string="Age", compute='_compute_age', readonly=True, store=True)
    email = fields.Char(string="Email")
    registration_status = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('cancelled', 'Cancelled')], string='Registration Status', tracking=True)
    total_event = fields.Integer(string="Total Event", compute='_compute_total_event')
    seq_num = fields.Char(string='Seq no. ', readonly=True, copy=False, index=True, default=lambda self: _('New'))
    sequence = fields.Integer(string="seq.")

    @api.model
    def birthday_reminder(self):
        today = date.today()
        attendees_with_birthday = self.search([('dob', '!=', False),
                                               ('dob', '!=', None),
                                               ('dob', 'like', f'%-{today.month:02d}-{today.day:02d}')])
        template = self.env.ref('event_managment_system.attendee_email_template')

        for attendee in attendees_with_birthday:
            template.send_mail(attendee.id, force_send=True)

    @api.model
    def default_get(self, fields):
        print(fields)
        res = super(AttendeeRegistration, self).default_get(fields)
        res['registration_status'] = 'draft'
        print(res)
        return res

    @api.depends('attendee')
    def _compute_total_event(self):
        total_event = self.env['event.registration'].search_count([('attendee', '=', self.attendee)])
        self.total_event = total_event

    def unlink(self):
        for rec in self:
            if rec.registration_status == 'draft' or rec.registration_status == 'confirmed':
                raise UserError(_("Record cannot be deleted if it is in draft or confirmed state"))
        return super(AttendeeRegistration, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('seq_num', _('New')) == _('New'):
            vals['seq_num'] = self.env['ir.sequence'].next_by_code('attendee.seq.registration') or _('New')
        rtn = super(AttendeeRegistration, self).create(vals)
        if vals.get('gender') == 'male':
            rtn['attendee'] = 'Mr. ' + rtn['attendee']
        elif vals.get('gender') == 'female':
            rtn['attendee'] = 'Mrs. ' + rtn['attendee']
        else:
            return rtn
        return rtn

    # _sql_constraints = [
    #     ('unique_email', 'unique(email)', 'Email id already exists')
    #     # ('check_age', 'check(age>18)', 'Email id already exists')
    # ]

    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(_("Enter valid Date of Birth"))

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.depends('attendee', 'email')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.attendee or ''} - {rec.email or ''}"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []

        domain = args + ['|', ('attendee', operator, name), ('email', operator, name)]
        records = self.search(domain, limit=limit)
        return [(record.id, record.display_name) for record in records]
