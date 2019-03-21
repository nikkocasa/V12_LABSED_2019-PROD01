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
    # TODO code ZIP format on the idea of the street format string
    # zip_format = fields.Text(
    #     help="Format to use for streets belonging to this country.\n\n"
    #          "You can use the python-style string pattern with all the fields of the street "
    #          "(for example, use '%(street_name)s, %(street_number)s' if you want to display "
    #          "the street name, followed by a comma and the house number)"
    #          "\n%(street_name)s: the name of the street"
    #          "\n%(street_number)s: the house number"
    #          "\n%(street_number2)s: the door number",
    #     default='%(street_number)s/%(street_number2)s %(street_name)s', required=True)
