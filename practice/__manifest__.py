{
    'name': 'Practice',
    'version': '1.0',
    'summary': 'This is a practice module',
    'description': 'For practice purposes',
    'category': 'Practice',
    'author': 'Harsh',
    'license': 'LGPL-3',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/practice_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'practice/static/src/js/pos_sample_button.js',
            'practice/static/src/xml/pos_sample_button.xml',
            'practice/static/src/pos/chrome.xml',
            'practice/static/src/pos/pos.scss'
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}
