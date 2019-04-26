# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, tools, _
from odoo.exceptions import Warning

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # def _get_last_variante_code(self):
    #     print ('kkkkkk')
    #     if len(self) == 1:
    #         # ici, on attribue comme numéro de variante le numéro suivant : i.e., la premiere variante '01', la deuxième '02', etc
    #         if not self.variante_num:
    #             next_variant_num = self.product_tmpl_id.product_variant_count + 1
    #             return next_variant_num

    _part_plant_list = [('fleurs', 'Fleurs'),
                        ('graines', 'Graines'),
                        ('plante_entiere', 'Plante entière'),
                        ('partie aerienne', 'Partie aérienne'),
                        ('sommites_fleuries', 'Sommités fleuries'),
                        ('bois', 'Bois'),
                        ('écorce_agrumes', 'Écorce agrumes'),
                        ('feuilles', 'Feuilles'),
                        ('rameaux', 'Rameaux'),
                        ('aiguilles', 'Aiguilles'),
                        ('baies', 'Baies'),
                        ('cones', 'Cônes'),
                        ('cones_et_rameaux', 'Cônes et rameaux'),
                        ('écorce', 'Écorce'),
                        ('racines', 'Racines'),
                        ('rameaux_et_feuilles_ou_aiguilles', 'Rameaux et feuilles ou aiguilles'),
                        ('boutons_floraux', 'Boutons floraux'),
                        ('resine', 'Résine'),
                        ('fruits', 'Fruits')
                        ]
    _part_plant_list.sort()

    variante_num = fields.Integer(
        string='Code de la variante',
        #default=lambda self: self._get_last_variante_code(),
        readonly = True
    )

    # Botanic Name
    name_latin = fields.Char(
        string="Nom latin",
        translate=False
    )
    # Name as people commonly call it .. could be translatade
    # in any of the user language (erp user or web user)
    name_current = fields.Char(
        string="Nom courant",
        translate=True,
    )
    # the international nomenclature for chimical
    # ans bio-chimical product.
    inci = fields.Char(
        string="Code INCI",
    )
    # Idem as INCI, but IFRA ... an other one necessary
    # to track on product :(
    ifra = fields.Char(
        string="Code IFRA",
    )
    # As INCI and IFRA ..
    cas = fields.Char(
        string="Code CAS",
    )
    raw_plant_material = fields.Selection(
        string="Partie de plante",
        selection=_part_plant_list
    )

    density_moy = fields.Float(
        string="Densité Moyenne constatée(Kg/Litre)",
        help="Permet de contrôler le volume restant par pesage",
        compute='_calc_densty_moy',
        digits=(6,4)
    ) # i.e. liquide could be weight to manage volume stock tracking

    density_min = fields.Float(
        string="Densité Minimale(Kg/Litre)",
        # help="Permet de contrôler le volume restant juste en pesant",
        digits=(6,4)
    )
    density_max = fields.Float(
        string="Densité Maximale (Kg/Litre)",
        # help="Permet de contrôler le volume restant juste en pesant",
        digits=(6,4)
    )
    calculated_code = fields.Char(
        string='Code resultat'
    )
    sale_GS1_EAN13 = fields.Char(
        string="EAN13 Vente (GS1)",
        size=13,
        help="Code à Barre attribué par l'organisme gestionnaire des EAN13 (GS1). Ne pas modifier : données externes"
    )
    _sql_constraints = [
        ('set_uniq_default_code', 'unique (default_code)', 'Le Code Produit doit être unique dans la base')]

    @api.one
    @api.depends('density_min', 'density_max')
    def _calc_densty_moy(self):
        for rec in self:
            rec.density_moy = (rec.density_min + rec.density_max) / 2

    # def action_getProductCode(self):
    #     # Pour les variantes de produit :
    #     # on garde la meme séquence pour toutes les variantes, au détail du nbuméro de variante qui change
    #     # il faut donc récupérer ou stocker dans product.template le code produit
    #     # le récupérer, et en changer
    #     # self.calculated_code = "{}.{:02d}".format(self.categ_id.get_full_code(prewiew=True), self.variante_num)
    #     if self.variante_num and 0 < self.variante_num <= self.product_tmpl_id.product_variant_count:
    #         # la variante a déjà un code entre 1 et le nb de variantes ; sinon, on réattribue
    #         variant_code = self.variante_num
    #     else:
    #         variant_code = self.product_tmpl_id.product_variant_count + 1
    #     # On récupère l'invariant du code produit
    #     if self.product_tmpl_id.calculated_code:
    #         # Le template existe est doit porter le début du code produit, hors num de vgariante
    #         self.calculated_code = self.product_tmpl_id.calculated_code[:-2] + "{:02d}".format(self.variante_num)
    #     else:
    #         self.calculated_code = self.product_tmpl_id.action_getProductCode(variant_code)
    #         # en fait, il faudrait mettre à jour le code produit du template avec ".00" comme num variante

    def action_setProductCode(self):
        if self.calculated_code:
            self.default_code = self.action_getProductCode(modePreview=False)
        else:
            raise Warning(_("Mise à jour de la \'référence interne\'") \
                          + '\n\n' + _("Obtenez un Code avant de l\'affecter pour le vérifier") \
                          + '\n' + _("(Seule l'affection du code incrémente la séquence interne)"))

    def action_setCodeBar(self):
        if self.default_code:
           pure_defaul_code = "".join(self.default_code.split("."))
           _barcode = "".join([ c if ord(c) < 65 else "{:02d}".format(ord(c)-64) for c in pure_defaul_code])
           check_sum = self.ean_checksum(_barcode)
           if check_sum != -1:
              self.barcode = _barcode + str(check_sum)
           else:
              self.barcode = "# Erreur de cheksun"

    def action_getProductCode(self, modePreview=True):
        code = self.categ_id.get_full_code(prewiew=modePreview, sep=True)
        # variant_code = self.variante_num if self.variante_num else 0
        variant_code = self.variante_num if self.variante_num else self._get_last_variante_code()
        self.calculated_code = "{}.{:02d}".format(code, variant_code) if code else _("Erreur, le code ou la variante n'ont pas été correctement défini")
        return self.calculated_code

    def _get_last_variante_code(self):
        if len(self) == 1:
            # ici, on attribue comme numéro de variante le numéro suivant : i.e., la premiere variante '01', la deuxième '02', etc
            if not self.variante_num:
                self.variante_num = self.product_tmpl_id.product_variant_count + 1
                return self.variante_num

    # returns the checksum of the ean13, or -1 if the ean has not the correct length, ean must be a string
    def ean_checksum(self, ean):
        code = list(ean)
        if len(code) <12:
            return -1
        oddsum = evensum = 0
        if len(code) == 13:
            code = code[:-1]  # Remove checksum
        for i in range(len(code)):
            if i % 2 == 0:
                evensum += int(code[i])
            else:
                oddsum += int(code[i])
        total = oddsum * 3 + evensum
        return int((10 - total % 10) % 10)
