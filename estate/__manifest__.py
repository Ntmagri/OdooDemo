# -*- coding: utf-8 -*-

{
    'name': 'Estate Property',
    'version': '1.3',
    'category': 'Marketing/Online Appointment',
    'sequence': 215,
    'summary': 'Allow people to book meetings in your agenda',
    'website': 'https://www.odoo.com/app/appointments',
    'description': """
        Allow clients to Schedule Appointments through the Portal
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml', #If it's before any view it will throw an error, so it needs to be the last.
        ],
    'installable': True,
    'application': True,

}

