{
    'name': "Hospital Admin",
    'author': "Kunj Koradiya",
    'description': "This is the description",
    'license': "LGPL-3",
    'depends': ['base'],
    'installable': True,
    'application': True,
    'category': 'Healthcare',
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hospital_patient.xml',
        'views/hospital_ward.xml',
        'views/hospital_bed_views.xml',
        'views/hospital_menu.xml',
    ]
}
