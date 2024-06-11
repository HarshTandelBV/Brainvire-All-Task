{
    'name': 'demo',
    'version': '1.0',
    'summary': 'it is created for practice purpose',
    'depends': ['base', 'mail','planning'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/customer_view.xml',
        'views/customer_order_line_view.xml',
        'views/product_view.xml',
        'views/order_status.xml',
        'views/demo_order_view.xml',
        'report/order_status_report.xml',
        'data/email_template.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'demo_module/static/src/js/planning_button.js',
            'demo_module/static/src/views/planning_button.xml',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
