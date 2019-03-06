# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class ProductCategory(models.Model):
    _inherit = 'product.category'

    nature_code_id = fields.Many2one(
        comodel_name='product.codification',
        domain=[('name_struct', '=', 'nature')],
        string='Nature Produit',
        default=lambda self: self.get_nature_code()
    )
    parent_nature_code = fields.Char(
        string='Nature Produit héritée',
        compute='_get_parent_codes'
    )
    gamme_code_id = fields.Many2one(
        comodel_name='product.codification',
        domain=[('name_struct', '=', 'gamme')],
        string='Code de Gamme',
        default=lambda self: self.get_gamme_code()
    )
    parent_gamme_code = fields.Char(
        string='Code de Gamme hérité',
        compute='_get_parent_codes'
    )
    display_current_sequence = fields.Char(
        string='Sequence active',
        compute='_display_current_sequence'
    )

    @api.depends('gamme_code_id', 'nature_code_id')
    def _get_parent_codes(self):
        rec = self[0]
        # equivalent in this case to self.ensure_one()
        # and not necessary to walk over the parent's left and right trees
        if rec.parent_id:
            _natcode_id, _gamcode_id = rec.parent_id.get_nature_code(), rec.parent_id.get_gamme_code()
            rec.parent_nature_code = _natcode_id.display_name if _natcode_id else False
            rec.parent_gamme_code = _gamcode_id.display_name if _gamcode_id else False
        else:
            rec.parent_nature_code = rec.parent_gamme_code = False

    @api.depends('gamme_code_id')
    def _display_current_sequence(self):
        rec = self[0]
        _seq_code = rec.get_sequence_code()
        rec.display_current_sequence = False if not _seq_code else _seq_code.code

    @api.onchange('parent_id','nature_code_id','gamme_code_id')
    def onchange_code(self):
        for rec in self:
            rec.parent_nature_code = rec.nature_code_id.value_code if rec.nature_code_id else rec.get_nature_code()
            rec.parent_gamme_code = rec.gamme_code_id.value_code if rec.gamme_code_id else rec.get_gamme_code()

    def get_nature_code(self):
        if self.nature_code_id:
            return self.nature_code_id
        else:  # recursion call on parent's category
            return False if not self.parent_id else self.parent_id.get_nature_code()

    def get_gamme_code(self):
        if self.gamme_code_id:
            return self.gamme_code_id
        else:  # recursion call on parent's category
            return False if not self.parent_id else self.parent_id.get_gamme_code()

    def get_sequence_code(self):
        """return founded sequence on nature_code or gamme_code
           related objects, with priority on gamme_code"""
        # rec = self[0] # see comment below on '_get_parent_codes'
        if self.gamme_code_id:  # self.gamme_code_id.product_num_sequence_id could be False or Defined : stop recursion
            return self.gamme_code_id.product_num_sequence_id
        else:  # Call recursion on parent's id if avalaible
            return False if not self. parent_id else self.parent_id.get_sequence_code()

    def get_full_code(self, prewiew=True, sep=False):
        _nature = self.get_nature_code()
        _gamme = self.get_gamme_code()
        _sequence_obj = self.get_sequence_code()
        if _nature and _gamme and _sequence_obj:
            if prewiew:  # that give preview of next sequence number
                _seq_num = _sequence_obj.preview_next_code() if _sequence_obj else '00000'
            else:  # that increment counter
                _seq_num = self.env['ir.sequence'].next_by_code(self.get_sequence_code().code) if _sequence_obj else '00000'
            if sep:
                # _current_code = f"{_nature.value_code}.{_gamme.value_code}.{_seq_num}"
                _current_code = "{}.{}.{}".format(_nature.value_code, _gamme.value_code, _seq_num)
            else:
                # _current_code = f"{_nature.value_code}{_gamme.value_code}{_seq_num}"
                _current_code = "{}{}{}".format(_nature.value_code, _gamme.value_code, _seq_num)
        else:
            _current_code = "Erreur: le Nature, la Gamme ou la séquence n'ont pas éré correctement fourni pour le calcul"
        return _current_code
