{
    'name': "City Address area",

    'summary': """This Module Add res_city table to res group 
                  and manage partner form in order to restrict keyrring city name at those defined""",

    'description': """
        Linked with contacts module, the module add 'city' ans 'zip' menu
        above localization menu of contacts configuration
    """,

    'author': "Nicolas Farrié",
    'website': "http://www.es-natura.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sedarome',
    'version': '12.0.01',
    'application': 'True',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'base_address_extended'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_city.xml',
        'views/res_area.xml',
        'views/res_state.xml',
        'views/res_country.xml',
        'views/partner.xml',
        'views/menus.xml',
        # 'data/res.country.state.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-


