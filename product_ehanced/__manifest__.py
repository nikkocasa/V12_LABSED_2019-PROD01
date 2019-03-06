# -*- coding: utf-8 -*-
{
    'name': "product_ehanced",

    'summary': """
        Ajoute des champs spécifique aux modèles 'product.template' et 'lot' 
        pour conserver des données particulières aux matières premières""",

    'description': """
        Ajoute des champs spécifique aux modèles 'product.template' et 'lot' 
        pour conserver des données particulières aux matières premières :
        - Product.template :
            - 
    """,

    'author': "Nicolas Farrié",
    'website': "http://www.sedarome.fr",
    'category': 'sedarome',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_codification.xml',
        'views/product.xml',
        'views/product_category.xml',
    ],
}