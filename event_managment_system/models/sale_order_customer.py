import base64
from datetime import datetime, timedelta
from odoo import models, fields, api
import xlsxwriter


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _xlsx_report_generator(self, orders):
        # Create Excel workbook and worksheet
        workbook = xlsxwriter.Workbook('/tmp/monthly_report.xlsx')
        worksheet = workbook.add_worksheet('Sale Report')
        product_worksheet = workbook.add_worksheet('Product-wise Sales')

        # Define formats
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter',
                                             'fg_color': '#D3C5E5', 'font_color': '#735DA5', 'border': 1})

        title_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 16, 'valign': 'vcenter',
                                            'fg_color': '#735DA5', 'font_color': 'white'})

        cell_format = workbook.add_format({'fg_color': '#E6E3EA', 'border': 1})
        numeric_cell_format = workbook.add_format({'fg_color': '#E6E3EA', 'border': 1, 'align': 'right'})
        cell_date_format = workbook.add_format({'num_format': 'dd-mm-yyyy', 'align': 'right', 'fg_color': '#E6E3EA',
                                                'border': 1})
        cell_amount_format = workbook.add_format({'num_format': '#,##0.00', 'align': 'right', 'fg_color': '#E6E3EA',
                                                  'border': 1})

        # Write title
        worksheet.merge_range('A1:F1', 'Monthly Sales Report', title_format)
        worksheet.set_row(0, 40)
        worksheet.set_row(1, 30)
        worksheet.set_column('A:A', 20)  # Order Ref
        worksheet.set_column('B:B', 30)  # Customer
        worksheet.set_column('C:C', 20)  # Salesperson
        worksheet.set_column('D:D', 15)  # Date
        worksheet.set_column('E:E', 20)  # Invoice Status
        worksheet.set_column('F:F', 15)  # Amount
        # Write headers
        headers = ['Order', 'Customer', 'Salesperson', 'Date', 'Invoice Status', 'Amount']
        for col, header in enumerate(headers):
            worksheet.write(1, col, header, header_format)

        # Write data
        for row, order in enumerate(orders, start=2):
            currency_symbol = order.currency_id.symbol or ''
            amount_with_symbol = f"{order.amount_total} {currency_symbol} "
            invoice_status = dict(order._fields['invoice_status'].selection).get(order.invoice_status, '')
            worksheet.write(row, 0, order.name or '', cell_format)
            worksheet.write(row, 1, order.partner_id.name or '', cell_format)
            worksheet.write(row, 2, order.user_id.name or '', cell_format)
            worksheet.write(row, 3, order.date_order.date().strftime('%Y-%m-%d'), cell_date_format)
            worksheet.write(row, 4, invoice_status, cell_format)
            worksheet.write(row, 5, amount_with_symbol, cell_amount_format)

            # Write title for Product-wise Sales worksheet
            product_worksheet.merge_range('A1:E1', 'Product-wise Sales', title_format)
            product_worksheet.set_row(0, 30)
            product_worksheet.set_column('A:A', 30)  # Product
            product_worksheet.set_column('B:B', 15)  # Unit Price
            product_worksheet.set_column('C:C', 15)  # Quantity
            product_worksheet.set_column('D:D', 15)  # Total Sales
            product_worksheet.set_column('E:E', 15)  # Tax Included


            # Write headers for Product-wise Sales worksheet
            product_worksheet.write(1, 0, 'Product', header_format)
            product_worksheet.write(1, 1, 'Unit Price', header_format)
            product_worksheet.write(1, 2, 'Quantity', header_format)
            product_worksheet.write(1, 3, 'Total Sales', header_format)
            product_worksheet.write(1, 4, 'Tax Included', header_format)

            # Calculate product-wise sales
            product_sales = {}
            for order in orders:
                for line in order.order_line:
                    product_name = line.product_id.name
                    if product_name in product_sales:
                        product_sales[product_name]['price'] += line.price_unit
                        product_sales[product_name]['qty'] += line.product_uom_qty
                        product_sales[product_name]['sales'] += line.price_subtotal
                        product_sales[product_name]['sales_with_tax'] += line.price_total
                    else:

                        product_sales[product_name] = {'price': line.price_unit, 'qty' : line.product_uom_qty, 'sales': line.price_subtotal, 'sales_with_tax':line.price_total}

            # Write data for Product-wise Sales worksheet
            row = 2
            for product, data in product_sales.items():
                product_worksheet.write(row, 0, product, cell_format)
                product_worksheet.write(row, 1, data['price'], cell_amount_format)
                product_worksheet.write(row, 2, data['qty'], numeric_cell_format)
                product_worksheet.write(row, 3, data['sales'], cell_amount_format)
                product_worksheet.write(row, 4, data['sales_with_tax'], cell_amount_format)
                row += 1

        # Close workbook
        workbook.close()

        # Read the Excel file and encode as base64
        with open('/tmp/monthly_report.xlsx', 'rb') as file:
            report_data = base64.b64encode(file.read())

        return report_data

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

            report_data = self._xlsx_report_generator(customer_orders)
            print(customer.name)
            # Create mail records
            attachment_data = {
                'name': 'monthly_report.xlsx',
                'datas': report_data,
                'res_model': 'mail.compose.message',
                'res_id': 0,
            }
            mail_values = {
                'subject': "Monthly Report",
                'email_to': customer.email,
                'attachment_ids': [(0, 0, attachment_data)],
            }
            template = self.env.ref('event_managment_system.email_template_monthly_report')

            template.send_mail(customer.id,force_send=True,
                               email_values=mail_values)

        return True
