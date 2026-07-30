{
    'name': 'QA Equipment Loans',
    'version': '17.0.1.0.0',
    'summary': 'QA fixture module for ERPeek Migration Pipeline E2E (17.0 syntax on purpose)',
    'category': 'Inventory',
    'author': 'ERPeek QA',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/loan_views.xml',
    ],
    'installable': True,
    'application': True,
}
