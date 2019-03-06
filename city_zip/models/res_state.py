# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class State(models.Model):
    _inherit='res.country.state'


    area_ids = fields.One2many(
        string="Area list",
        comodel_name='res.country.state.area',
        inverse_name='state_id'
    )

