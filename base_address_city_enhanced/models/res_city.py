# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResCity(models.Model):
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
        digits=(13, 10)
    )
    long = fields.Float(
        string="Longitude",
        digits=(13, 10)
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
