{
    'name': 'Sales Approval',
    'version': '1.0',
    'summary': 'Sales Approval code written here',
    'description': 'Sales Approval code',
    'category': '/sales/Sales Approval',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['sale','base'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_config_settings_view.xml',
        'views/sale_order_view.xml',
        'views/sale_approval_view.xml',
    ],
    'installable': True,
}