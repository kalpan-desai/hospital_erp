# -*- coding: utf-8 -*-
{
    'name': 'Case Management',
    'version': '1.0',
    'summary': 'Hospital Case Management',
    'sequence': 10,
    'description': """
        Manage Hospital Patient Cases, Admissions, Vitals, and Billing Integration.
    """,
    'category': 'Healthcare',
    'author': 'Kalpan Desai',
    'depends': ['base', 'mail', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hms_case_views.xml',
        'views/hms_case_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
