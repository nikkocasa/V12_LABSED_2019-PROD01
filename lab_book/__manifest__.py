# -*- coding: utf-8 -*-
{
    'name': "lab_book",

    'summary': """
        Gestion du cahier de laboratoire
        Permet de saisir au fil de l'eau les
        événement dans un chrono, lié avec la gestion des numéros de lots""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nicolas Farrié",
    'website': "http://www.es-natura.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sedarome',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/product_codification.xml',
    ],
}