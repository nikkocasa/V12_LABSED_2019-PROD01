# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class Country(models.Model):
    _inherit = 'res.country'

    zip_name = fields.Char(
        string='Local name for ZIP code',
    )
    zip_format = fields.Char(
        string='Local Format',
        help="Empty means Anything, or give a example"
    )

