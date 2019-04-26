# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

def bget(_defined, _not_defined):
    return _defined if _defined else _not_defined

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'


    _ContainerType = [('aluminiun_bottle', 'Estagnon aliminuim'),
                      ('glass_bottle', 'Bouteille verre'),
                      ('plastic bottle', 'Flacon plastique'),
                      ('plastic bucket', 'Seau plastique'),
                      ('plastic bag', 'Sac plastique'),
                      ('plastic cask', 'Fût plastique'),
                      ('paper bag', 'Sac papier'),
                      ('cardboard cask', 'Fût en carton')
                      ]

    supplier_id = fields.Many2one(
        string='Nom du Fournisseur',
        comodel_name='res.partner',
        domain=[('supplier', '=', True)],
        # required=True,
        # ondelete='restrict',
        help=_("Ne pas oublier !! information imortante")
    )
    production_date = fields.Datetime(
        string="Date de production",
        required=True,
        copy=False
    )
    container_type = fields.Selection(
        string='type de contenant',
        selection=_ContainerType,
        copy=False
    )
    container_weight = fields.Float(
        string='Tare contenant en kg',
        digits=(6, 4),
        copy=False
    )
    lot_density = fields.Float(
        string="Densité du lot (Kg/Litre)",
        help="Permet de contrôler le volume restant par le poids",
        digits=(6,4)
    )
    info_prod_density = fields.Char(
        string="Densité produit (Min / Moy / Max)",
        compute='_getProdDensities',
        store=False
    )
    with_samples = fields.Boolean(
        string="Échantillonnage",
        copy=False
    )
    with_analyses = fields.Boolean(
        string="Analyses",
        copy=False
    )
    security_form = fields.Boolean(
        string="Fiche sécurité",
    )
    security_form_attach =fields.Many2one(
        comodel_name="ir.attachment",
        string="Fichier lié",
        copy=False
    )
    chromato_file = fields.Boolean(
        string="Chromato",
        copy=False
    )
    chromato_file_attach =fields.Many2one(
        comodel_name="ir.attachment",
        string="Fichier lié",
        copy=False
    )
    ifra_form = fields.Boolean(
        string="Fiche IFRA",
        copy=False
    )
    ifra_form_attach =fields.Many2one(
        comodel_name="ir.attachment",
        string="Fichier lié",
        copy=False
    )
    technical_data =fields.Boolean(
        string="Fiche technique",
        copy=False
    )
    technical_data_attach =fields.Many2one(
        comodel_name="ir.attachment",
        string="Fichier lié",
        copy=False
    )
    allergen_list =fields.Boolean(
        string="Fiche allergènes",
        copy=False
    )
    allergen_list_attach =fields.Many2one(
        comodel_name="ir.attachment",
        string="Fichier lié",
        copy=False
    )
    summary_att = fields.Char(
        string="SITAC",
        size=6,
        compute='_check_summary_att',
        store=True
    )
    sequence_editable = fields.Boolean(
        compute='_onchange_prod_seq_edit',
        store=False
    )

    @api.onchange('product_id')
    def _getProdDensities(self):
        if self.product_id:
            self.info_prod_density = _("Kg/Litre : Min: ") + "{:05.3f}".format(self.product_id.density_min) \
                                     + _("\n/Moy: ") + "{:05.3f}".format(self.product_id.density_moy) \
                                     + _("/ Max: ") + "{:05.3f}".format(self.product_id.density_max)
        else:
            self.info_prod_density = ""
        # return self.info_prod_density

    @api.onchange('product_id')
    def _onchange_prod_seq_edit(self):
        self.ensure_one()
        if self.product_id:
            if self.product_id.sequence_id:
                self.sequence_editable = self.product_id.sequence_id.editable
            elif self.product_id.categ_id.product_lot_sequence_id:
                self.sequence_editable = self.product_id.categ_id.product_lot_sequence_id.editable
            else:
                self.sequence_editable = True

    @api.onchange('product_id', 'production_date')
    def _onchange_product_id_prod_date(self):
        self.ensure_one()
        if self.product_id and self.production_date:
            if self.product_id.use_sequence_lot:
                _seq_id = self.product_id.sequence_id if self.product_id.sequence_id else self.product_id.categ_id.product_lot_sequence_id
                _seq_rec = self.env['ir.sequence'].search([('id', '=', _seq_id.id)])
                _seq_rec[0].working_date = self.production_date
                self.name = _seq_rec[0].preview_next_code()

    @api.constrains('product_id', 'production_date')
    def _set_lot_number(self):
        self.ensure_one()
        if self.product_id and self.production_date:
            if self.product_id.use_sequence_lot:
                _seq_id = self.product_id.sequence_id if self.product_id.sequence_id else self.product_id.categ_id.product_lot_sequence_id
                _seq_rec = self.env['ir.sequence'].search([('id', '=', _seq_id.id)])
                _seq_rec[0].working_date = self.production_date
                self.name = _seq_rec[0].next_by_code(_seq_id.code)

    @api.onchange('allergen_list', 'technical_data', 'ifra_form', 'chromato_file', 'security_form')
    def _check_summary_att(self):
        for rec in self:
            if rec.with_analyses:
                res = "_" if not rec.security_form_attach else "S"
                res += "_" if not rec.ifra_form_attach else "I"
                res += "_" if not rec.technical_data_attach else "T"
                res += "_" if not rec.allergen_list_attach else "A"
                res += "_" if not rec.chromato_file_attach else "C"
            else:
                res = '_____'
            rec.summary_att = res

