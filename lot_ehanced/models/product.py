# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    use_sequence_lot = fields.Boolean(
        string='Use a sequence',
        default=False
    )
    sequence_id = fields.Many2one(
        string='Sequence',
        comodel_name='ir.sequence',
        default=False,
        help='Choose the sequence which cill be used to compute serial Lot ou Number when creating new lot'
    )

    @api.onchange('use_sequence_lot')
    def _on_change_use_sequence_lot(self):
        self.ensure_one()
        if not self.use_sequence_lot:
            self.sequence_id = False

    @api.onchange('tracking')
    def _on_change_tracking(self):
        self.ensure_one()
        if self.tracking:
            if self.tracking == 'none':
                self.use_sequence_lot = False
                self.sequence_id = False
