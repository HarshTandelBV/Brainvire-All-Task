# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Payment Provider: Cybersource',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 370,
    'summary': "Payment Provider cybersource for testing purpose.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment','sale'],
    'data': [
        'views/capture_button_view.xml',
        'views/payment_provider_view.xml',
        'data/payment_provider_data.xml',
    ],
    'assets': {
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
