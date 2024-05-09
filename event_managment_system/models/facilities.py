from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError


class LocationFacilities(models.Model):
    _name = "event.facilities"
    _description = "Location's Facilities"
    _rec_name = "tags_id"

    tags_id = fields.Char(string="Tags")
    category = fields.Selection([
        ('accommodation', 'Accommodation'),
        ('dining_and_catering', 'Dining and Catering'),
        ('recreation_and_leisure', 'Recreation and Leisure'),
        ('business_and_meeting', 'Business and Meeting'),
        ('entertainment_and_activities', 'Entertainment and Activities'),
        ('concierge_services', 'Concierge Services'),
        ('additional_services', 'Additional Services'),
        ('event_specific', 'Event-specific'),
        ('wedding_services_and_packages', 'Wedding Services and Packages'),
        ('security_and_safety_measures', 'Security and Safety Measures')
    ])


# first task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    image = fields.Binary(string='Image')
    nick_name = fields.Char(string="Nick Name")

    def action_new_print(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if not line.is_available:
                    raise ValidationError("One or more products in the order are not available in sufficient quantity.")
        return res

    def action_cancel(self):
        """ Cancel SO after showing the cancel wizard when needed. (cfr :meth:`_show_cancel_wizard`)

        For post-cancel operations, please only override :meth:`_action_cancel`.

        note: self.ensure_one() if the wizard is shown.
        """

        if not self.image:
            if not self.image:
                raise UserError(_("You cannot cancel a locked order. Please upload image first."))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_name = fields.Char(string="Custom Name")
    is_available = fields.Boolean(string='Is Available', compute='_compute_available_or_not')

    @api.depends('product_uom_qty', 'order_id.partner_id')
    def _compute_available_or_not(self):
        for rec in self:
            product = rec.product_id
            if product:
                product_tmpl_id = product.product_tmpl_id
                virtual_available = self.env['product.template'].browse(product_tmpl_id.id).virtual_available
                rec.is_available = rec.product_uom_qty <= virtual_available
            else:
                rec.is_available = False

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'custom_name': self.custom_name,
        })
        return values


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['custom_name', 'nick_name']
        return fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    nick_name = fields.Char(string="Nick Name", related='sale_id.nick_name')


class StockMove(models.Model):
    _inherit = 'stock.move'
    custom_name = fields.Char(string="custom name")



