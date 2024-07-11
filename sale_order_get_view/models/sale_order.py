from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form' and not self.env.user.has_group('sales_team.group_sale_manager'):
            for node in arch.xpath("//field"):
                node.attrib['readonly'] = 'True'

        return arch, view
