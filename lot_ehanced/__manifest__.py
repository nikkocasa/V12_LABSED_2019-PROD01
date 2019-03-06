# -*- coding: utf-8 -*-
{
    'name': "Lot Management ehanced",

    'summary': """
        Ajoute des champs spécifiques aux modèles 'stock.production.lot' 
        pour conserver des données particulières aux matières demandant 
        un suivi documentaire et/ou avec echantillonage""",

    'description': """
        Ajoute les champs au modèle  'stock.production.lot':
            - Fournisseur du lot,
            - Date de production du lot,
            - Un champ booléen "Echantillonage" qui affiche/masque :
                - Une copie de la quantité d’origine (lecture seule)
                - un champ calculé du total des prélèvements, avec mis à jour de la quantité du lot 
                - Un onglet supplémentaire "Echantillons":
                    - Date de prélèvement
                    - Méthode de prélèvement 
                    - Quantité prélevée
                    - Destination : ['Temoin test', 'Analyse', ']
            - Un champ booléen "Analyses préalables", affiche/masque :
              Onglet "Documents d’analyse":     
                - FIche de sécurite,
                - Chromato,
                - Analyse IFRA
                - Autre
                
        Menus Crées :
            - aucun""",
    'author': "Nicolas Farrié",
    'website': "http://www.sedarome.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sedarome',
    'version': '10.0.01',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/production_lot.xml',
        'views/product.xml',
        'views/product_category.xml',
        'views/ir_sequence.xml',
    ],
}