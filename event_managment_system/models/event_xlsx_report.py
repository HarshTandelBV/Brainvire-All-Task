import base64
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import io
import xlsxwriter
from odoo.tools.misc import xlsxwriter as odoo_xlsxwriter
from odoo import models


class EventExcelReport(models.TransientModel):
    _name = "event.excel.report"
    _description = "This is a wizard which will generate the Event Excel report"

    file = fields.Binary('Prepared file', readonly=True, attachment=True)
    file_name = fields.Char('File Name', readonly=True)

    def print_xlsx_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Excel Report')
        att_worksheet = workbook.add_worksheet('Attendee Report')

        # invoice_worksheet = workbook.add_worksheet('Customer Details')

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
        event_report = self.env['event.event.report']
        data = event_report.generate_report()

        worksheet.merge_range('A1:J1', f'Event Report', title_format)
        worksheet.set_row(0, 40)
        worksheet.set_row(1, 30)
        worksheet.set_column('A:A', 20)  # Name
        worksheet.set_column('B:B', 30)  # Description
        worksheet.set_column('C:C', 30)  # Start Date
        worksheet.set_column('D:D', 30)  # End Data
        worksheet.set_column('E:E', 20)  # Location
        worksheet.set_column('F:F', 30)  # Reg Start Date
        worksheet.set_column('G:G', 30)  # Reg End Date
        worksheet.set_column('H:H', 10)  # Total Sessions
        worksheet.set_column('I:I', 10)  # Total Tickets
        worksheet.set_column('J:J', 10)  # Total Attendee

        worksheet.write('A2', 'Name', header_format)
        worksheet.write('B2', 'Description', header_format)
        worksheet.write('C2', 'Start Date', header_format)
        worksheet.write('D2', 'End Data', header_format)
        worksheet.write('E2', 'Location', header_format)
        worksheet.write('F2', 'Reg Start Date', header_format)
        worksheet.write('G2', 'Reg End Date', header_format)
        worksheet.write('H2', 'Total Sessions', header_format)
        worksheet.write('I2', 'Total Tickets', header_format)
        worksheet.write('J2', 'Total Attendee', header_format)

        row = 2

        for event in data:
            col = 0
            worksheet.write(row, col, event.get('name', ''), cell_format)
            col += 1
            worksheet.write(row, col, event.get('description', ''), cell_format)
            col += 1
            worksheet.write(row, col, str(event.get('start_date', '')), cell_date_format)
            col += 1
            worksheet.write(row, col, str(event.get('end_date', '')), cell_date_format)
            col += 1
            worksheet.write(row, col, event.get('location', ''), cell_format)
            col += 1
            worksheet.write(row, col, str(event.get('registration_open_date', '')), cell_date_format)
            col += 1
            worksheet.write(row, col, str(event.get('registration_close_date', '')), cell_date_format)
            col += 1
            worksheet.write(row, col, event.get('session_count', ''), cell_format)
            col += 1
            worksheet.write(row, col, event.get('ticket_count', ''), cell_format)
            col += 1
            worksheet.write(row, col, event.get('attendee_count', ''), cell_format)
            row += 1

        att_worksheet.merge_range('A1:E1', f'Attendee Report', title_format)
        att_worksheet.set_row(0, 40)
        att_worksheet.set_row(1, 30)
        att_worksheet.set_column('A:A', 20)  # attendee
        att_worksheet.set_column('B:B', 20)  # gender
        att_worksheet.set_column('C:C', 20)  # dob
        att_worksheet.set_column('D:D', 20)  # email
        att_worksheet.set_column('E:E', 20)  # registration status

        att_worksheet.write('A2', 'Name', header_format)
        att_worksheet.write('B2', 'Gender', header_format)
        att_worksheet.write('C2', 'DOB', header_format)
        att_worksheet.write('D2', 'Email', header_format)
        att_worksheet.write('E2', 'Registration Status', header_format)

        att_row = 2

        for event in data:
            col = 0
            att_worksheet.write(att_row, col, event.get('attendee', ''), cell_format)
            col += 1
            att_worksheet.write(att_row, col, event.get('gender', ''), cell_format)
            col += 1
            att_worksheet.write(att_row, col, str(event.get('dob', '')), cell_date_format)
            col += 1
            att_worksheet.write(att_row, col, str(event.get('email', '')), cell_format)
            col += 1
            att_worksheet.write(att_row, col, event.get('registration_status', ''), cell_format)
            att_row += 1

        workbook.close()
        output.seek(0)
        file_data = output.read()
        output.close()

        self.write({
            'file': base64.b64encode(file_data),
            'file_name': 'event_report.xlsx'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=%s&id=%s&field=file&download=true&filename=%s' % (
                self._name, self.id, self.file_name),
            'target': 'New',
        }
