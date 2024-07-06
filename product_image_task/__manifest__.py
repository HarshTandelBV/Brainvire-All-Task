{
    'name': 'Product Image Task',
    'version': '1.0',
    'summary': 'Product Image code written here',
    'description': 'Product image code',
    'category': '/sales/product image',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['sale','base','stock','account'],
    'data': [
        'views/sale_order_line_view.xml'
    ],
    'installable': True,
}