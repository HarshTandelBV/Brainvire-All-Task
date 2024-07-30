{
    'name': 'todo list',
    'version': '1.0',
    'summary': 'todo list related code to understand owl framework',
    'description': 'todo list related code written here',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['base','website'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'todo_list_app/static/src/components/*/*.js',
            'todo_list_app/static/src/components/*/*.xml',
            'todo_list_app/static/src/components/*/*.scss',
        ],
    },
    'installable': True,
}