# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging, re

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    ### Add feature to better controlling phone number input ###

    phone_country_id = fields.Many2one(
        string='Country code',
        comodel_name='res.country',
        defaul='res.partner.country_id'
    )
    mobile_country_id = fields.Many2one(
        string='Country code',
        comodel_name='res.country',
        defaul='res.partner.country_id'
    )

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if not self.phone: # not self.phone_country_id or
            self.phone_country_id = self.country_id
        if not self.mobile: # not self.mobile_country_id or
            self.mobile_country_id = self.country_id

    @api.onchange('phone_country_id', 'mobile_country_id')
    def _onchange_country_phone(self):
        self._compute_tel_str()

    @api.onchange('phone', 'mobile')
    def _compute_tel_str(self):
        def format_phone(phone, country_code, old_code):
            # strip non-numeric characters
            if not phone or len(phone) == 0:
                return ''
            else:
                country_code = str(country_code) if country_code else ''
                old_code = str(old_code) if old_code else ''
                # tel = phone.encode('ascii', 'ignore')
                # supprime le format type +33 (0) 12 34 56 78 90 par +33  12 34 56 78 90
                # et tout ensuite tout ce qui n'est pas numerique / re.sub(r'\D','',string)
                tel = re.sub(r'\D', '', phone.replace('(0)', '')).replace('(0)', '', 1)
                # et on supprime les '00' eventuels en tête de numéro
                tel = tel if tel[0:2] != '00' else tel[2:]
                # puis on supprime le code pays (pour le remettre après)
                if tel[0:len(country_code)] == country_code:
                    tel = tel[len(country_code):]
                if tel[0:len(old_code)] == old_code:
                    tel = tel[len(old_code):]
                if len(tel) < 9:
                    tel += ' ' * (10 - len(tel))
                if tel[0] == '0':
                    if len(country_code) == 0:
                        return '{} {} {} {} {}'.format(tel[:-8], tel[-8:-6], tel[-6:-4], tel[-4:-2], tel[-2:])
                    else:
                        return '+{} {} {} {} {}'.format(country_code, tel[-9:-6], tel[-6:-4], tel[-4:-2], tel[-2:])
                elif len(country_code) == 0:
                    return '+{} {} {} {} {}'.format(tel[:-9], tel[-9:-6], tel[-6:-4], tel[-4:-2], tel[-2:])
                else:
                    return '+{} {} {} {} {}'.format(country_code, tel[:-6], tel[-6:-4], tel[-4:-2], tel[-2:])

        for record in self:
            _code = record.country_id.phone_code if not record.phone_country_id else record.phone_country_id.phone_code
            _old_code = False if not self._origin else self._origin.phone_country_id.phone_code
            record.phone = format_phone(record.phone, _code, _old_code)
            _code = record.country_id.phone_code if not record.mobile_country_id else record.mobile_country_id.phone_code
            _old_code = False if not self._origin else self._origin.mobile_country_id.phone_code
            record.mobile = format_phone(record.mobile, _code, _old_code)
            for child in record.child_ids:
                _code = child.country_id.phone_code if not child.phone_country_id else child.phone_country_id.phone_code
                _old_code = False if not self._origin else self._origin.phone_country_id.phone_code
                child.phone = format_phone(child.phone, _code, _old_code)
                _code = child.country_id.phone_code if not child.mobile_country_id else child.mobile_country_id.phone_code
                _old_code = False if not self._origin else self._origin.mobile_country_id.phone_code
                child.mobile = format_phone(child.mobile, _code, _old_code)