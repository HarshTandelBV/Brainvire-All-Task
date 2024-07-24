{
    'name': 'Custom Dashboard in portal',
    'version': '1.0',
    'category': 'Website/Website',
    'summary': 'custom dashboard in website (portal)',
    'description': """
        custom dashboard in website (portal) which shows the products sold in a proper manner.
    """,
    'author': 'Harsh Tandel',
    'depends': ['base', 'sale','website'],
    'data': [
        'views/portal_template.xml',
        'views/product_sales_template_view.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_dashboard/static/src/scss/style.scss',
            ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
