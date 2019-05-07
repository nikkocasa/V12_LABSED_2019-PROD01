# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    city_id = fields.Many2one(
        comodel_name="res.city",
        string="City"
    )
    # zip_code= fields.Char(
    #     string='Zip code'
    # )
    area_id_name = fields.Char(
        related="city_id.area_id.name",
        string="Area",
        index=True
    )
    state_id_name = fields.Char(
        related="city_id.state_id_name",
        string="State",
        index=True
    )
    country_id_name = fields.Char(
        related="city_id.country_id_name",
        string='Country',
        index=True
    )