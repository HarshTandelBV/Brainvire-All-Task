{
    'name': 'Website new page view',
    'version': '1.0',
    'summary': 'website new page related code ',
    'description': 'website new page related code written here',
    'category': '/sales/website get view',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['sale','base'],
    'data': [
        'security/ir.model.access.csv',
        'views/thank_you_page_view.xml',
        'views/custom_page_view.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_new_page/static/src/js/custom_widget.js',
        ],
    },
    'installable': True,
}