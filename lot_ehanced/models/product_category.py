# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ProductCategory_lot_sequence(models.Model):
    _inherit = 'product.category'

    product_lot_sequence_id = fields.Many2one(
        string="Sequence for product tracking",
        comodel_name='ir.sequence',
        default=False,
        help="Choose the sequence which will be used to compute serial Lot ou Number when creating new lot"
    )
    display_ProdLotSequId = fields.Char(
        string="Lot Sequence active (héritée)",
        compute='_display_ProdLotSequId'
    )

    @api.depends('product_lot_sequence_id')
    def _display_ProdLotSequId(self):
        rec = self[0]
        _seq_code = rec.get_product_lot_sequence_code()
        # rec.display_ProdLotSequId = False if not _seq_code else f"{_seq_code.code} ({_seq_code.name})"
        rec.display_ProdLotSequId = False if not _seq_code else "{} ({})".format(_seq_code.code, _seq_code.name)


    def get_product_lot_sequence_code(self):
        """return founded sequence on nature_code or gamme_code
           related objects, with priority on gamme_code"""
        # rec = self[0] # see comment below on ' module product_ehanced.models.product_category.py/_get_parent_codes'
        if self.product_lot_sequence_id:
            # self.product_lot_sequence_id could be False or Defined : stop recursion
            return self.product_lot_sequence_id
        else:  # Call recursion on parent's id if avalaible
            return False if not self. parent_id else self.parent_id.get_product_lot_sequence_code()

