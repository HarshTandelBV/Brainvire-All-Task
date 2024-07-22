{
    'name': 'Website crud page',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'crud app',
    'description': """
        This module defines a crud page functionality.
    """,
    'author': 'Harsh Tandel',
    'depends': ['base', 'sale', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/demo_company_views.xml',
        'views/demo_template.xml',
        'views/create_template.xml',
        'views/edit_template.xml',
        'views/portal_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_crud_page/static/src/scss/demo_styles.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
