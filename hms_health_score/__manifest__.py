{
    'name': 'Health Score System',
    'version': '1.0',
    'category': 'Healthcare',
    'author': 'Kalpan Desai',
    'depends': ['base', 'mail', 'hms_administraion', 'hms_case', 'hms_laboratory', 'hms_pharmacy'],
    'data': [
        'security/ir.model.access.csv',
        'data/health_score_data.xml',
        'data/ir_cron.xml',
        'views/disease_master_views.xml',
        'views/health_score_views.xml',
        'views/inherited_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
