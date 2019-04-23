# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class Area(models.Model):
    _name = 'res.country.state.area'

    name = fields.Char(
        string='Name'
    )
    area_code = fields.Char(
        string='Code',
        size=6
    )
    state_id = fields.Many2one(
        string="State",
        comodel_name='res.country.state'
    )
    city_ids = fields.One2many(
        string='Cities list',
        comodel_name='res.city',
        inverse_name='area_id'
    )

