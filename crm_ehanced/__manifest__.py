# -*- coding: utf-8 -*-
{
    'name': "crm_ehanced",

    'summary': """
        Ajouts de champs spécifiques pour Sedarome""",

    'description': """
        Ajouts de champs spécifiques
        Sedarome :
        lead_language: Langue de la piste
        date_contact; Date ou la piste a été vue ou reçue (diff de la date de saisie)
    """,

    'author': "Nicolas Farrié",
    'website': "http://www.es-natura.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sedarome',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'partner_firstname'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
    ],
}