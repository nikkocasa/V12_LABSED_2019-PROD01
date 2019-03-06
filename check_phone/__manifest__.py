# -*- coding: utf-8 -*-
{
    'name': "Check_phone",

    'summary': """
        Check if phone number are in a correct format""",

    'description': """
        Test format phone number after validating any phone field
    """,

    'author': "Nicolas Farrié",
    'website': "http://www.es-natura.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'sedarome',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/partner.xml',
    ],
}