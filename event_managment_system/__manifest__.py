# -*- coding: utf-8 -*-
{
    'name': 'Event Management System',
    'version': '1.0.0',
    'summary': 'Event Management System',
    'sequence': -100,
    'description': """
Event Managment System
====================
The specific and easy-to-use customer event management system in Odoo allows you to keep track of your customer data, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.
    """,
    'category': 'Event/Event Management System',
    'website': 'https://www.odoo.com/',
    'depends': ['base', 'sale', 'stock', 'sale_management', 'mail', 'web', 'website', 'hr_expense', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/email_template.xml',
        'data/birthday_reminder.xml',
        'data/customer_monthly_report.xml',
        'wizard/booking_payment_status_wizard_view.xml',
        'wizard/sale_order_report_wizard_view.xml',
        'wizard/sale_order_excel_report_wizard_view.xml',
        'wizard/event_xlsx_report_wizard.xml',
        'views/menu.xml',
        'views/event_view.xml',
        'views/attendee_view.xml',
        'views/booking_view.xml',
        'views/location_view.xml',
        'views/session_view.xml',
        'views/sponsor_view.xml',
        'views/facilities_view.xml',
        'views/guest_view.xml',
        'views/ticket_view.xml',
        'views/event_controller.xml',
        'views/sale_commission_view.xml',
        'views/sale_customer_view.xml',
        'views/event_report_view.xml',
        'views/purchase_order_template.xml',
        'report/event_report.xml',
        'report/invoice_report.xml',
        'report/commission_report.xml',
        'report/sale_customer_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'event_managment_system/static/src/js/hr_expense_button.js',
            'event_managment_system/static/src/js/form_controller.js',
            'event_managment_system/static/src/views/hr_expense_button.xml',
            'event_managment_system/static/src/views/form_controller.xml',
        ],
        'web.assets_frontend': [
            'event_managment_system/static/src/js/purchase_order.js',
        ]
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
