{
    'name': 'demo',
    'version': '1.0',
    'summary': 'it is created for practice purpose',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/customer_view.xml',
        'views/customer_order_line_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
