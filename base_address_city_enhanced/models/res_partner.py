# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    ### Add a new column to the res.partner model, to constrains city
    # from a res_partner_city table where state_id  is mandatory and point to a country id which is mandatory too
    # original fields are : (in class res.partner (file res_partner.py)
    # see it at https: // fossies.org / dox / odoo - 8.0.0 / openerp_2addons_2base_2res_2res__partner_8py_source.html
    # line:265/:  'city': fields.char('City'),
    # line:266/:  'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
    # line:267/:  'country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
    ###

    # city_id = fields.Many2one(
    #     comodel_name="res.city",
    #     string="City"
    # )
    # zip = fields.Char(
    #     related="re.city.zipcode",
    #     string='Zip code',
    #     index=True
    # )
    # area_id_name = fields.Char(
    #     related="city_id.area_id.name",
    #     string="Area",
    #     index=True
    # )
    # state_id_name = fields.Char(
    #     related="city_id.area_id.state_id.name",
    #     string="State",
    #     index=True
    # )
    # country_id_name = fields.Char(
    #     related="city_id.area_id.state_id.country_id.name",
    #     string='Country',
    #     index=True
    # )

    # @api.onchange('city_id')
    # def _onchange_city(self):
    #     self.ensure_one()
    #     self.city = ''
    #     if self.city_id:
    #         self.city = self.city_id.name
    #         self.zip = self.city_id.zipcode
    #         self.area_id = self.city_id.area_id
    #         self.state_id = self.city_id.area_id.state_id
    #         self.country_id = self.city_id.area_id.state_id.country_id
    #         if len(self.city_id.zip_ids.ids) == 1:
    #             # set zip code directly
    #             self.zip, self.zip_id = self.city_id.zip_ids.name, self.city_id.zip_ids.id
    #         elif self.zip_id and not (self.zip_id.id in self.city_id.zip_ids.ids):
    #             # the city previously selected is not linked to this zip code
    #             self.zip_id, self.zip = False, ''
    #         return {'domain': {
    #             'zip_id': [('id', 'in', self.city_id.zip_ids.ids)],
    #         }}
    #     else:  # city_id is empty : reseting domain on zip_id list
    #         self.city = ''
    #         return {'domain': {
    #             'zip_id': self.city_id.zip_ids.ids,
    #         }}
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
    #
    # @api.constrains('city_id', 'zip')
    # def set_state_country(self):
    #     for r in self:
    #         if r.city_id:
    #             r.city = r.city_id.name
    #             r.area_id = r.city_id.area_id
    #             r.state_id = r.city_id.area_id.state_id
    #             r.country_id = r.city_id.area_id.state_id.country_id
