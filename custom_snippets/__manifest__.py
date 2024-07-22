{
    'name': 'custom snippets',
    'version': '1.0',
    'summary': 'custom snippets related code ',
    'description': 'custom snippets related code written here',
    'category': '/sales/custom snippets',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['base','website'],
    'data': [
        'views/basic_snippet.xml',
        'views/dynamic_snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_snippets/static/src/js/cart_details.js',
        ],
    },
    'installable': True,
}