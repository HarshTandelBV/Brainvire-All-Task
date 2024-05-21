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
    attendee = fields.Char(string="Attendee",readonly=True)
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
    def _select(self):
        return """
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
            r.age,
            r.email,
            r.registration_status
        """

    def _from(self):
        return """
        event_event e
        LEFT JOIN event_registration r ON r.event = e.id
        """

    def _where(self):
        pass

    def _group_by(self):
        return """
        e.name,
        e.description,
        e.start_date,
        e.end_date,
        e.location,
        e.registration_open_date,
        e.registration_close_date,
        session_count,
        ticket_count,
        attendee_count,
        r.attendee,
        r.gender,
        r.dob,
        r.age,
        r.email,
        r.registration_status,
        e.id
        """

    def _order_by(self):
        return """
        attendee_count
        """

    # Define other methods as needed to compute fields or perform other tasks

    # Define a property to combine all the parts of the query
    @property
    def _table_query(self):
        return f"""
                SELECT {self._select()}
                FROM {self._from()}
                {self._where() if self._where() else ""}
                GROUP BY {self._group_by()}
                ORDER BY {self._order_by()}
            """
