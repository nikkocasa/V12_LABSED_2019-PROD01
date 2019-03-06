# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo import exceptions

class ProductCodification(models.Model):
    _name = 'product.codification'

    """ This table stores and compute product codification parameters
    """

    sequence = fields.Integer()

    _zone = [('nature', 'Nature produit'),('gamme', 'Code gamme produit')]

    name_struct = fields.Selection(
        selection=_zone,
        string='Zone'
    )
    type_code = fields.Selection(
        selection=[('int', 'Entier'), ('string', 'Texte')],
        string='Type'
    )
    value_code = fields.Char(
        string='Valeur'
    )
    label_code = fields.Char(
        string='Libellé'
    )
    text_code = fields.Text(
        string='Commentaires'
    )
    barcode_char = fields.Char(
        string='Car.CodeBarre',
        size=12,
        compute="_set_char_barcode"
    )
    name = fields.Char(
        compute='_set_name',
        string='Nom code',
        store=True
    )
    display_name = fields.Char(
        compute='_set_name',
        string='Nom complet',
        store=True
    )
    product_num_sequence_id = fields.Many2one(
        string='Sequence Number',
        comodel_name='ir.sequence',
        default=False,
        help='Choose the sequence which will be used to compute product Numbe creating new one'
    )

    _sql_constraints = [
        ('set_uniq_value_code', 'unique (value_code)', 'Valeur: doit être unique dans la base')]

    @api.one
    @api.depends('type_code', 'value_code', 'text_code')
    def _set_name(self):
        for rec in self:
            rec.name = '{}: {}'.format(rec.value_code, rec.label_code)
            rec.display_name = '{}: {}{}'.format(rec.value_code,
                                                 rec.label_code,
                                                 (" / " + rec.text_code) if rec.text_code else "")

    @api.onchange('value_code')
    def _set_maj(self):
        for rec in self:
            if rec.value_code:
                rec.value_code.upper()

    @api.one
    @api.depends('type_code', 'value_code')
    def _set_char_barcode(self):
        for rec in self:
            if rec.type_code and rec.value_code:
                if rec.type_code == 'int':
                    rec.barcode_char = '{}'.format(int(rec.value_code)) # 180824 : {:02d}
                elif rec.type_code == 'string':
                    rec.barcode_char = ''.join(['{:02d}'.format(ord(c) - 64) for c in rec.value_code.upper()])
                    # this produce a string type '010203' from 'ABC' or 'abc'

    @api.onchange('value_code', 'type_code')
    def _check_value_code(self):
        # this is to be sure that '00001' is stored as '1'
        self.ensure_one()
        if self.value_code and self.type_code == 'int':
            try:
                self.value_code = str(int(float(self.value_code)))
            except ValueError:
                raise exceptions.except_orm(_('Erreur de saisie'),
                                            _("Lorsque le 'type' est 'Entier', seul un nombre peut être saisi"))
