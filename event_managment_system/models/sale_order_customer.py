from datetime import datetime, timedelta
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _generate_monthly_report(self):
        # Get today's date
        today = fields.Date.today()

        # Calculate first day and last day of the current month
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        # Search for orders within the last month
        orders = self.env['sale.order'].search([
            ('date_order', '>=', first_day_of_last_month),
            ('date_order', '<=', last_day_of_last_month)
        ])

        # Group orders by customer
        customer_orders_dict = {}
        for order in orders:
            if order.user_id in customer_orders_dict:
                customer_orders_dict[order.user_id].append(order)
            else:
                customer_orders_dict[order.user_id] = [order]

        for customer, customer_orders in customer_orders_dict.items():
            # Prepare email content
            order_table = """
                <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;">
                    <thead>
                        <tr style="background-color: #4CAF50; color: white;">
                            <th style="border: 1px solid #dddddd; padding: 8px;">Order</th>
                            <th style="border: 1px solid #dddddd; padding: 8px;">Customer</th>
                            <th style="border: 1px solid #dddddd; padding: 8px;">Date</th>
                            <th style="border: 1px solid #dddddd; padding: 8px;">Amount</th>
                            <th style="border: 1px solid #dddddd; padding: 8px;">Invoice Status</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            for order in customer_orders:
                currency_symbol = order.currency_id.symbol or ''  # Fetch currency symbol
                amount_with_symbol = "{} {}".format(currency_symbol, order.amount_total)  # Concatenate symbol with amount
                order_table += """
                    <tr>
                        <td style="border: 1px solid #dddddd; padding: 8px;">{}</td>
                        <td style="border: 1px solid #dddddd; padding: 8px;">{}</td>
                        <td style="border: 1px solid #dddddd; padding: 8px;">{}</td>
                        <td style="border: 1px solid #dddddd; padding: 8px;">{}</td>
                        <td style="border: 1px solid #dddddd; padding: 8px;">{}</td>
                    </tr>
                """.format(order.name, order.partner_id.name, order.date_order.date(), amount_with_symbol, dict(order._fields['invoice_status'].selection).get(order.invoice_status, ''))

            order_table += """
                    </tbody>
                </table>
            """

            body_html = """
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            font-size: 16px;
                            line-height: 1.6;
                        }}
                        .container {{
                            max-width: 800px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            background-color: #f2f2f2;
                            padding: 20px;
                            text-align: center;
                            background-color: #4CAF50; 
                            color: white;
                            font-family: Arial, sans-serif;
                        }}
                        .header h1 {{
                            margin: 0;
                            font-size: 24px;
                        }}
                        .content {{
                            padding: 20px;
                            background-color: #fff;
                            border-radius: 5px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        .table-container {{
                            margin-top: 20px;
                        }}
                        .footer {{
                            margin-top: 20px;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Monthly Report</h1>
                        </div>
                        <div class="content">
                            <p>Dear {customer_name},</p>
                            <p>Here is your monthly report:</p>
                            <div class="table-container">
                                {order_table}
                            </div>
                            <p>Thank you.</p>
                        </div>
                        <div class="footer">
                            <p>This is an automated email. Please do not reply.</p>
                        </div>
                    </div>
                </body>
                </html>
            """.format(
                customer_name=customer.name,
                order_table=order_table
            )

            # Create mail records
            mail_values = {
                'subject': "Monthly Report",
                'body_html': body_html,
                'email_to': customer.email,
            }
            mail = self.env['mail.mail'].create(mail_values)

            # Send email
            mail.send()

        # Update next call to the first day of the next month
        nextcall_date = first_day_of_current_month + timedelta(days=32)
        nextcall_date = nextcall_date.replace(day=1)
        self.env['ir.cron'].search([('name', '=', 'Customer : Monthly Report')]).write({'nextcall': nextcall_date})

        return True
