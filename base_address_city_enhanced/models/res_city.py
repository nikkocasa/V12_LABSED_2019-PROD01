# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


# class City(models.Model):
#     _name = 'res.city'
#     _description = 'City'
#     _order = 'name'
#
#     name = fields.Char("Name", required=True, translate=True)
#     zipcode = fields.Char("Zip")
#     country_id = fields.Many2one('res.country', string='Country', required=True)
#     state_id = fields.Many2one(
#         'res.country.state', 'State', domain="[('country_id', '=', country_id)]")

class City(models.Model):
    _inherit = 'res.city'
    _description = 'City sedarome extended'
    _order = 'name'

    _sql_constraints = [
            ('city_zip_uniq', 'UNIQUE (name, zipcode)',  'This City with this Zip Code already exist in the database !')
    ]

    airport_code = fields.Char(
        string='Airport Code',
        size=3
    )
    insee_code = fields.Char(
        string='INSEE',
        size=7
    )
    # zip_ids = fields.Many2many(
    #     string="ZIP's",
    #     comodel_name='res.city',
    #     column1='name',
    #     column2='zipcode',
    #     help="Not mandatory: leave blank if there is more than one zip code for this town"
    # )
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
    population = fields.Integer(
        string='Population'
    )
    lat = fields.Float(
        string="Latitude",
        digits=(12, 10)
    )
    long = fields.Float(
        string="Longitude",
        digits=(12, 10)
    )
    # gps_coord = fields.Char(
    #     string='Coord. GPS (lat, Long)',
    #     size=28,
    #     compute='_get_coord_gps()',
    #     store=True
    # )
    #
    # @api.onchange('long', 'lat')
    # def _set_coord_gps(self):
    #     self.gps_coord = self._get_coord_gps()
    #
    # def _get_coord_gps(self):
    #     return "({0:12.10f}, {1:12.10f})".format(self.lat if self.lat else 0.0, self.long if self.long else 0.0)
    #
    # @api.onchange('area_id')
    # def _set_back_state_country(self):
    #     for rec in self:
    #         rec.state_id = rec.area_id.state_id
    #         rec.country_id = rec.state_id.country_id
