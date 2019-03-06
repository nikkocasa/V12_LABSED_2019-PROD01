# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class Zip(models.Model):
    _name='res.zip'

    name = fields.Char(
        string='ZIP Code'
    )
    zip_country = fields.Many2one(
        string='Country name',
        comodel_name='res.country',
    )
    zip_format = fields.Char(
        string='Format Code',
        related='zip_country.zip_format'
    )
    city_ids = fields.Many2many(
        string='Cities',
        comodel_name='res.city'
    )

