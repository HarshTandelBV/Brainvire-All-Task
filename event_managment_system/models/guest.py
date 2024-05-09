from odoo import fields, models,api


class EventGuest(models.Model):
    _name = 'event.guest'
    _description = "event speakers details"

    name = fields.Char(string="Name")
    profession = fields.Char(string="Profession")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Phone No")
    image = fields.Binary(string="Image")
    total_event = fields.Integer(string="Total Events", compute="_compute_total_event_count")
    event_ids = fields.Many2many('event.event',string="Events")

    @api.depends

    # @api.model
    # def name_get(self):
    #     return [(rec.id, f"{rec.name} - {rec.bio}") for rec in self]

    def check_orm(self):
        search_var = self.env['event.guest'].search([])
        search_var_cond = self.env['event.guest'].search([('profession', '=', 'singer')])
        search_var_or_cond = self.env['event.guest'].search(['|', ('profession', '=', 'singer'), ('bio', '=', 'magician')])
        search_var_and_cond = self.env['event.guest'].search([('profession', '=', 'singer'), ('profession', '=', 'magician')])
        search_total = self.env['event.guest'].search_count([])
        browse_var_cond = self.env['event.guest'].browse(['profession', '=', 'singer'])
        browse_var = self.env['event.guest'].browse(3)
        browse_var_multiple = self.env['event.guest'].browse([3, 5])
        ref_var = self.env.ref("event_managment_system.view_event_guest_form")

        print("search -----------", search_var)
        print("search with cond-----------", search_var_cond)
        print("search with or cond-----------", search_var_or_cond)
        print("search with and cond-----------", search_var_and_cond)
        print("search count-----------", search_total)
        print("browse var with cond-----------",
              browse_var_cond)  # it will return the intput which we have given so in browse we give id or list of ids
        print("browse with single id-----------", browse_var, 'name----', browse_var.name, 'email------',
              browse_var.email)
        print("browse multiple id-----------", browse_var_multiple)

        print('for browse multiple variable')
        for rec in browse_var_multiple:
            print("name---", rec.name, 'email---------', rec.email)

        print("for search")
        for rec in search_var:
            print("name---", rec.name, 'email---------', rec.email)

        print("ref var-----------", ref_var)  # to get browsable id dont use ".id"
        print("ref type-----------", ref_var.type, 'name------', ref_var.name)

        create_var = self.env['event.speaker'].create({
            "name": "denial",
            "profession": "dancer",
            "email": "denial@gmail.com",
            "mobile": "4412543412",
        })

        print("create var---------", create_var)  # to get browsable id use '.id'

        # to apply write operation first we need to get browse id
        brw_id = self.env['event.speaker'].browse(3)
        brw_id.write({
            "name": "rahul",
            "email": "rahul@gmail.com"
        })
        brw_id.copy()
        # brw_id.unlink()

        if brw_id.exists():
            print("id is already exists>>>")
        else:
            print("id is not exists>>>>")
