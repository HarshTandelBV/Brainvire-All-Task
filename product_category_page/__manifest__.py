{
    'name': 'Product category page',
    'version': '1.0',
    'summary': 'Product category page',
    'description': 'It shows all the products category wise',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['sale', 'base','website'],
    'data': [
        'views/portal_template.xml',
        'views/product_category_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'product_category_page/static/**/*',
        ],
    },
    'installable': True,
}
