{
    'name': 'QA Service Requests',
    'version': '19.0.1.0.0',
    'summary': 'QA fixture module for the ERPeek Migration Pipeline 18.0 to 19.0 test',
    'category': 'Sales',
    'author': 'ERPeek QA',
    'license': 'LGPL-3',
    'depends': ['sale_management', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/service_request_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
}
