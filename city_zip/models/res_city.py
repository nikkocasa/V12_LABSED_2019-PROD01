# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class City(models.Model):
    _name = 'res.city'

    name = fields.Char(
        string='City Name'
    )
    airport_code = fields.Char(
        string='Airport Code',
        size=3
    )
    insee_code = fields.Char(
        string='INSEE',
        size=7
    )
    zip_ids = fields.Many2many(
        string="ZIP",
        comodel_name='res.zip',
        help="Not mandatory: leave blank if there is more than one zip code for this town"
    )
    area_id = fields.Many2one(
        string="Area",
        comodel_name='res.country.state.area'
    )
    state_id_name = fields.Char(
        related="area_id.state_id.name",
        string='State',
        index=True
    )
    country_id_name = fields.Char(
        related="area_id.state_id.country_id.name",
        string='Country',
        index=True
    )
    long = fields.Float(
        string="Longitude",
        digits=(12, 10)
    )
    lat = fields.Float(
        string="Latitude",
        digits=(12, 10)
    )
    gps_coord = fields.Char(
        string='Coord. GPS (lat, Long)',
        size=28,
        compute='_get_coord_gps()',
        store=True
    )
    population = fields.Integer(
        string='Population'
    )

    @api.onchange('long', 'lat')
    def _set_gps_coord(self):
        self.gps_coord = self._get_coord_gps()

    def _get_coord_gps(self):
        return "({0:12.10f}, {1:12.10f})".format(self.lat if self.lat else 0.0,
                                               self.long if self.long else 0.0)
