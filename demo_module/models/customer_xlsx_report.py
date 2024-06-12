import base64
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import io
import xlsxwriter

class CustomerExcelReport(models.TransientModel):
    _name = "demo.customer.report"
    _description = "This is a model which will generate the Event Excel report"

    file = fields.Binary('Prepared file', readonly=True, attachment=True)
    file_name = fields.Char('File Name', readonly=True)

    @api.model
    def print_xlsx_report(self, record_ids):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Customer Report')

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
        data = self.env['demo.customer'].browse(record_ids)

        worksheet.merge_range('A1:I1', f'Customer Report', title_format)
        worksheet.set_row(0, 40)
        worksheet.set_row(1, 30)
        worksheet.set_column('A:A', 20)  # Name
        worksheet.set_column('B:B', 20)  # gender
        worksheet.set_column('C:C', 30)  # address
        worksheet.set_column('D:D', 30)  # phone
        worksheet.set_column('E:E', 20)  # disability
        worksheet.set_column('F:F', 30)  # image
        worksheet.set_column('G:G', 30)  # email
        worksheet.set_column('H:H', 30)  # dob
        worksheet.set_column('I:I', 15)  # country

        worksheet.write('A2', 'Name', header_format)
        worksheet.write('B2', 'Gender', header_format)
        worksheet.write('C2', 'Address', header_format)
        worksheet.write('D2', 'Phone', header_format)
        worksheet.write('E2', 'Disability', header_format)
        worksheet.write('F2', 'Image', header_format)
        worksheet.write('G2', 'Email', header_format)
        worksheet.write('H2', 'DOB', header_format)
        worksheet.write('I2', 'Country', header_format)

        row = 2

        for customer in data:
            col = 0
            worksheet.write(row, col, customer.name, cell_format)
            col += 1
            worksheet.write(row, col, customer.gender, cell_format)
            col += 1
            worksheet.write(row, col, customer.address, cell_date_format)
            col += 1
            worksheet.write(row, col, customer.phone, cell_date_format)
            col += 1
            worksheet.write(row, col, customer.disability, cell_format)
            col += 1
            worksheet.write(row, col, customer.image, cell_date_format)
            col += 1
            worksheet.write(row, col, customer.email, cell_date_format)
            col += 1
            worksheet.write(row, col, customer.dob, cell_format)
            col += 1
            worksheet.write(row, col, customer.country.name, cell_format)
            row += 1

        workbook.close()
        output.seek(0)
        file_data = output.read()
        output.close()

        # Write file data to the record
        record = self.create({
            'file': base64.b64encode(file_data),
            'file_name': 'customer_report.xlsx'
        })

        # Return the file download URL
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=%s&id=%s&field=file&download=true&filename=%s' % (
                self._name, record.id, record.file_name),
            'target': 'new',
        }
