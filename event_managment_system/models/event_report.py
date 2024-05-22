import logging

from odoo import api, fields, models


class EventReport(models.Model):
    _name = "event.event.report"
    _description = "It provides the reporting details of the event management system"
    _auto = True

    name = fields.Char(string="Name", readonly=True)
    description = fields.Text(string="Description", readonly=True)
    start_date = fields.Datetime(string='Start Date', readonly=True)
    end_date = fields.Datetime(string="End Date", readonly=True)
    location = fields.Char(string="Location", readonly=True)
    registration_open_date = fields.Datetime(string='Registration Open Date', readonly=True)
    registration_close_date = fields.Datetime(string='Registration Close Date', readonly=True)
    session_count = fields.Integer(string="Total Sessions", readonly=True)
    ticket_count = fields.Integer(string='Total Tickets', readonly=True)
    attendee_count = fields.Integer(string='Total Attendee', readonly=True)
    attendee = fields.Char(string="Attendee", readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', readonly=True)
    dob = fields.Date(string="Date of birth", readonly=True)
    email = fields.Char(string="Email", readonly=True)
    registration_status = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('cancelled', 'Cancelled')], string='Registration Status', readonly=True)

    # Define methods to construct SQL queries
    def generate_report(self):
        query = """
            SELECT 
                e.name,
                e.description,
                e.start_date,
                e.end_date,
                e.location,
                e.registration_open_date,
                e.registration_close_date,
                (SELECT COUNT(*) FROM event_track WHERE event = e.id) AS session_count,
                (SELECT COUNT(*) FROM event_ticket WHERE event_id = e.id) AS ticket_count,
                (SELECT COUNT(*) FROM event_registration WHERE event = e.id) AS attendee_count,
                r.attendee,
                r.gender,
                r.dob,
                r.email,
                r.registration_status
            FROM 
                event_event e
            LEFT JOIN 
                event_registration r ON r.event = e.id
            GROUP BY 
                e.id ,e.name, e.description, e.start_date, e.end_date, e.location, e.registration_open_date, 
                e.registration_close_date, r.attendee, r.gender, r.dob, r.email, r.registration_status
            ORDER BY 
                e.name
        """

        self.env.cr.execute(query)
        data = self.env.cr.fetchall()  # Fetch all the results

        report_data = []
        for row in data:
            event_data = {
                'name': row[0],
                'description': row[1],
                'start_date': row[2],
                'end_date': row[3],
                'location': row[4],
                'registration_open_date': row[5],
                'registration_close_date': row[6],
                'session_count': row[7],
                'ticket_count': row[8],
                'attendee_count': row[9],
                'attendee': row[10],
                'gender': row[11],
                'dob': row[12],
                'email': row[13],
                'registration_status': row[14],
            }
            report_data.append(event_data)

        return report_data
