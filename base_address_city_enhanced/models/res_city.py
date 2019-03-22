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
            ('city_zip_uniq', 'UNIQUE (name, zipcode, insee_code)',  'This City with this Zip Code already exist in the database !')
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

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.ensure_one()
        if self.country_id: # user coose a country --> select all states
            if self.state_id not in self.country_id.state_ids: # not already chosen
                self.state_id = ''
            return {'domain': {
                'state_id': [('id', 'in', self.country_id.state_ids.ids)],
            }}

    @api.onchange('state_id')
    def _onchange_state_id(self):
        self.ensure_one()
        if self.state_id: # user coose a country --> select all states
            if self.area_id not in self.state_id.area_ids: # not already chosen
                self.area_id = ''
            return {'domain': {
                'area_id': [('id', 'in', self.state_id.area_ids.ids)],
            }}

    @api.onchange('area_id')
    def _onchange_state_id(self):
        self.ensure_one()
        if self.area_id:
            if not self.state_id or self.state_id != self.area_id.state_id:
                self.state_id = self.area_id.state_id

    @api.constrains('state_id', 'area_id')
    def _check_state_id(self):
        for rec in self:
            if rec.area_id:
                if not rec.state_id or rec.state_id != rec.area_id.state_id:
                    rec.state_id = rec.area_id.state_id

    #
    # @api.onchange('zip_id')
    # def _onchange_zip(self):
    #     self.ensure_one()
    #     self.zip = ''
    #     if self.zip_id:
    #         self.zip = self.zip_id.name
    #         self.area_id = self.city_id.area_id
    #         self.state_id = self.city_id.area_id.state_id
    #         self.country_id = self.city_id.area_id.state_id.country_id
    #         if len(self.zip_id.city_ids.ids) == 1:
    #             # set zip code directly
    #             self.city_id, self.city = self.zip_id.city_ids.id, self.zip_id.city_ids.name
    #         elif self.city_id and not (self.city_id.id in self.zip_id.city_ids.ids):
    #             # the city previously selected is not linked to this zip code
    #             self.city_id, self.city = False, ''
    #         return {'domain': {
    #             'city_id': [('id', 'in', self.zip_id.city_ids.ids)],
    #                 }}
    #     else:
    #         self.zip = ''
    #         return {'domain': {
    #             'city_id': self.zip_id.city_ids.ids,
    #                 }}


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
