from odoo import fields, models, _, api


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = 'it provide all the commission details of the salesman'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        store=True
    )

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")

    sale_order_ids = fields.One2many('sale.commission.online', 'commission_id', string='Sale Orders', compute='calculate_orders')
    total_orders = fields.Integer(string='Total Orders', compute='calculate_orders')
    total_commission_value = fields.Float(string='Total Commission', compute='calculate_orders')

    # @api.depends('user_id','start_date','end_date')
    def calculate_orders(self):
        if self.user_id:
            # print(self.user_id.name)
            list_of_order = self.env['sale.commission.online'].search(
                [('salesperson_id.name', '=', self.user_id.name), ('create_date', '>=', self.start_date),
                 ('create_date', '<=', self.end_date)])
            for item in list_of_order:
                print(item)
            self.total_orders = len(list_of_order)
            self.total_commission_value = round(sum(order.total_commission for order in list_of_order),2)
            self.sale_order_ids = [(6, 0, list_of_order.ids)]
        else:
            self.sale_order_ids = [(5, 0, 0)]

    class SaleCommissionOnline(models.Model):
        _name = 'sale.commission.online'
        _description = 'it provide all the commission details of the salesman'

        number = fields.Char(string='Number')
        customer_id = fields.Many2one('res.partner', string='Customer')
        salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson", readonly=True)
        total_amount = fields.Float(string='Total Amount')
        create_date = fields.Datetime(string="Creation Date", index=True, readonly=True)
        order_value = fields.Integer(string='If Cart Value Above', readonly=True)
        percentage = fields.Float( string='Percentage', readonly=True)
        total_commission = fields.Float(string='Total Commission', store=True)
        commission_id = fields.Many2one('sale.commission', string='Commission')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        sale_commission_online_obj = self.env['sale.commission.online']
        for order in self:
            if order.user_id.order_value < order.amount_total:
                total_commission = order.amount_total * (order.user_id.percentage / 100)
            else:
                total_commission = 0
            order_data = {
                'number': self.name,
                'customer_id': self.partner_id.id,
                'salesperson_id': self.user_id.id,
                'total_amount': self.amount_total,
                'create_date': self.date_order,
                'order_value': self.user_id.order_value,
                'percentage': self.user_id.percentage,
                'total_commission': total_commission
            }
        sale_commission_online_obj.create(order_data)
        res = super(SaleOrder, self).action_confirm()
        return res

    def action_cancel(self):
        sale_commission_online_obj = self.env['sale.commission.online']
        lines_to_delete = sale_commission_online_obj.search([('number', '=', self.name)])
        lines_to_delete.unlink()
        print(self.name)
        # lines_to_delete.unlink()
        res = super()._action_cancel()
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    order_value = fields.Integer(string='If order Value Above', store=True)
    percentage = fields.Float(string='Percentage', store=True)
