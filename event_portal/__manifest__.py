{
    'name': 'Event Portal',
    'version': '1.0',
    'summary': 'Event portal code written here',
    'description': 'Event Portal code',
    'category': '/event/event_portal',
    'author': 'Harsh',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['base','portal','website'],
    'data': [
        'views/portal_template.xml',
    ],
    'installable': True,
}