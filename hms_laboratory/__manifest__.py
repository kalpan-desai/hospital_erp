# -*- coding: utf-8 -*-
{
    'name': 'Laboratory Management',
    'version': '1.0',
    'summary': 'Hospital Laboratory Management',
    'sequence': 11,
    'description': """
        Manage Hospital Lab Orders, Tests, and Reports with Mailing and Priority.
    """,
    'category': 'Healthcare',
    'author': 'Kalpan Desai',
    'depends': ['base', 'mail', 'product', 'account', 'hms_case'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hms_lab_views.xml',
        'views/hms_lab_menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
