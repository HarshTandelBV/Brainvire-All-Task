{
    'name': 'Website pop up task',
    'version': '1.0',
    'summary': 'website pop up related code ',
    'description': 'website pop up related code written here',
    'category': '/sales/website pop up view',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['sale', 'base', 'website', 'web'],
    'data': [
        'views/website_button_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_popup/static/src/js/sale_order_info.js',
        ],
    },
    'installable': True,
}
