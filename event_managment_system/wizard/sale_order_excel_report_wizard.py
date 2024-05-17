import base64
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import io
import xlsxwriter
from odoo.tools.misc import xlsxwriter as odoo_xlsxwriter
from odoo import models


class SaleOrderExcelReportWizard(models.TransientModel):
    _name = "sale.order.excel.report.wizard"
    _description = "This is a wizard which will generate the Sale Order Excel report"

    start_date = fields.Date(string="Starting date", required=True)
    end_date = fields.Date(string="Ending date", required=True)
    file = fields.Binary('Prepared file', readonly=True, attachment=True)
    file_name = fields.Char('File Name', readonly=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError("Starting date cannot be after ending date.")

    def print_xlsx_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sales Report')
        invoice_worksheet = workbook.add_worksheet('Customer Details')

        # Formatting the data
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter',
                                             'fg_color': '#D3C5E5', 'font_color': '#735DA5', 'border': 1})

        title_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 16, 'valign': 'vcenter',
                                            'fg_color': '#735DA5', 'font_color': 'white'})

        cell_format = workbook.add_format({'fg_color': '#E6E3EA', 'border': 1})
        cell_date_format = workbook.add_format(
            {'num_format': 'dd-mm-yyyy', 'align': 'right', 'fg_color': '#E6E3EA', 'border': 1})
        cell_numeric_format = workbook.add_format(
            {'align': 'right', 'fg_color': '#E6E3EA', 'border': 1})
        cell_amount_format = workbook.add_format(
            {'num_format': '#,##0.00', 'align': 'right', 'fg_color': '#E6E3EA', 'border': 1})

        # Fetching the data
        sales = self.env['sale.order'].search(
            [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)])
        invoices = self.env['account.move'].search([])

        worksheet.merge_range('A1:G1', f'Sales Order Report From {self.start_date} To {self.end_date}', title_format)
        worksheet.set_row(0, 40)
        worksheet.set_row(1, 30)
        worksheet.set_column('A:A', 20)  # Order Ref
        worksheet.set_column('B:B', 30)  # Customer
        worksheet.set_column('C:C', 40)  # Email
        worksheet.set_column('D:D', 20)  # Date Order
        worksheet.set_column('E:E', 20)  # Salesperson
        worksheet.set_column('F:F', 30)  # Status
        worksheet.set_column('G:G', 15)  # Total Amount

        worksheet.write('A2', 'Order Ref', header_format)
        worksheet.write('B2', 'Customer', header_format)
        worksheet.write('C2', 'Email', header_format)
        worksheet.write('D2', 'Date Order', header_format)
        worksheet.write('E2', 'Salesperson', header_format)
        worksheet.write('F2', 'Status', header_format)
        worksheet.write('G2', 'Total Amount', header_format)

        row = 2

        for sale in sales:
            col = 0
            worksheet.write(row, col, sale.name or '', cell_format)
            col += 1
            worksheet.write(row, col, sale.partner_id.name or '', cell_format)
            col += 1
            worksheet.write(row, col, sale.partner_id.email or '', cell_format)
            col += 1
            worksheet.write(row, col, sale.date_order or '', cell_date_format)
            col += 1
            worksheet.write(row, col, sale.user_id.name or '', cell_format)
            col += 1
            worksheet.write(row, col, dict(sale._fields['invoice_status'].selection).get(sale.invoice_status, ''),
                            cell_format)
            col += 1
            worksheet.write(row, col, f'{sale.amount_total} {sale.currency_id.symbol}' or '', cell_amount_format)
            row += 1

        invoice_worksheet.merge_range('A1:F1', 'Invoice Details', title_format)
        invoice_worksheet.set_row(0, 40)
        invoice_worksheet.set_row(1, 30)
        invoice_worksheet.set_column('A:A', 20)  # Name
        invoice_worksheet.set_column('B:B', 30)  # Phone
        invoice_worksheet.set_column('C:C', 15)  # Email
        invoice_worksheet.set_column('D:D', 15)  # City
        invoice_worksheet.set_column('E:E', 15)  # State
        invoice_worksheet.set_column('F:F', 15)  # Country

        invoice_worksheet.write('A2', 'Name', header_format)
        invoice_worksheet.write('B2', 'Customer', header_format)
        invoice_worksheet.write('C2', 'Invoice Date', header_format)
        invoice_worksheet.write('D2', 'Due Date', header_format)
        invoice_worksheet.write('E2', 'Tax Included', header_format)
        invoice_worksheet.write('F2', 'Total', header_format)

        invoice_row = 2

        for invoice in invoices:
            col = 0
            invoice_worksheet.write(invoice_row, col, invoice.name or '', cell_format)
            col += 1
            invoice_worksheet.write(invoice_row, col, invoice.invoice_partner_display_name or '', cell_format)
            col += 1
            invoice_worksheet.write(invoice_row, col, invoice.invoice_date or '', cell_date_format)
            col += 1
            invoice_worksheet.write(invoice_row, col, str(invoice.invoice_date_due) or '', cell_date_format)
            col += 1
            invoice_worksheet.write(invoice_row, col, f'{invoice.amount_untaxed_signed} {invoice.currency_id.symbol}' or '', cell_amount_format)
            col += 1
            invoice_worksheet.write(invoice_row, col, f'{invoice.amount_total_signed} {invoice.currency_id.symbol}', cell_amount_format)
            invoice_row += 1

        workbook.close()
        output.seek(0)
        file_data = output.read()
        output.close()

        self.write({
            'file': base64.b64encode(file_data),
            'file_name': 'sale_order_report.xlsx'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=%s&id=%s&field=file&download=true&filename=%s' % (
                self._name, self.id, self.file_name),
            'target': 'New',
        }
