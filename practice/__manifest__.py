{
    'name': 'practice',
    'version': '1.0',
    'summary': 'this is practice module',
    'description': 'for practice purpose',
    'category': 'practice',
    'author': 'harsh',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/practice_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,

}