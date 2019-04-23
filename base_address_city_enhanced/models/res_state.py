# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class State(models.Model):
    _inherit = 'res.country.state'

    # country_id = fields.Many2one(
    #     string="Country",
    #     comodel_name='res.country'
    # )
    area_ids = fields.One2many(
        string="Area list",
        comodel_name='res.country.state.area',
        inverse_name='state_id'
    )
    areas_count = fields.Integer(
        string='Number of Areas embeded',
        compute='_count_areas',
        store=True
    )

    @api.multi
    def _count_areas(self):
        for rec in self:
            rec.areas_count = len(rec.area_ids.ids)
            return rec.areas_count
