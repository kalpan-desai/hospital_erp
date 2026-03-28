{
    'name': "Pharmacy Management",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base', 'product', 'sale', 'account'],
    'author': "Kalpan Desai",
    'category': 'Healthcare',
    'description': """
        This Module manages the complete Pharmacy workflow including:
        - Medicine Management
        - Shelf/Storage Location
        - Sales & Invoicing
        - Medicine Schedule
        - Bill Printing
    """,
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/pharmacy_menus.xml',
        'views/pharmacy_views.xml',
        'report/pharmacy_reports.xml',
    ],
    'demo': [],
}
