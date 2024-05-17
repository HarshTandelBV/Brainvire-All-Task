# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Event Managment System',
    'version': '1.0.0',
    'summary': 'Event Managment System',
    'sequence': -100,
    'description': """
Gaming Cafe
====================
The specific and easy-to-use customer event management system in Odoo allows you to keep track of your customer data, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.
    """,
    'category': 'Event/Event Managment System',
    'website': 'https://www.odoo.com/',
    'depends': ['base', 'sale', 'stock', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/email_template.xml',
        'wizard/booking_payment_status_wizard_view.xml',
        'wizard/sale_order_report_wizard_view.xml',
        'wizard/sale_order_excel_report_wizard_view.xml',
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
        'views/sale_commission_view.xml',
        'views/sale_customer_view.xml',
        'report/event_report.xml',
        'report/invoice_report.xml',
        'report/commission_report.xml',
        'report/sale_customer_report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
