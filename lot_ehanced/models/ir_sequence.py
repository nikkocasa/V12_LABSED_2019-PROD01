# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime
from dateutil import parser


import logging
_logger = logging.getLogger(__name__)


class IrSequence_Letters(models.Model):
    _inherit = 'ir.sequence'

    _letters = [(95,'_')] + [(x, chr(x)) for x in range(ord('A'),ord('A')+26)]

    working_date = fields.Datetime()

    use_letters = fields.Boolean(
        string='Use letter',
        default=False,
        help='Use letters instead of short number format for year and month'

    )
    first_year = fields.Integer(
        String="Set year for 'A'",
        Default='2014',
        help='i.e. if A=2014, B will be 2015, C=2016 etc.. After Z, A will be an other time'
    )
    first_month = fields.Selection(
        _letters,
        String="Set Letter for 01 (January)",
        default=False,
        help="Choosing 'A' ==> 'B'=february. 'Z' ==> 'A'=february /'_' ==> ignore letter replacement for month only"
    )
    editable = fields.Boolean(
        string='may be changed',
        default=True
    )

    def _get_prefix_suffix(self):
        """Overide ir.sequence.py method for adding letter year/month display"""
        def _interpolate_letters(_text, _year, _month, _year_pat, _month_pat):
            _working_date = datetime.today() if not self.working_date else parser.parse(self.working_date)
            _working_year, _working_month = _working_date.year, _working_date.month
            _year_char = chr(ord('A') + max(0, (_working_year - _year)))
            # this is for avoiding replacment just for month - keep letter for year et digits for month
            _month_char = chr(64 + ((_month - ord('A') + _working_month) % 26)) if _month in range(65,91) else "{0:02d}".format(_working_month)
            for _pattern in _year_pat:
                while _text.find(_pattern) >= 0:
                    _text = _text.replace(_pattern, _year_char)
            for _pattern in _month_pat:
                while _text.find(_pattern) >= 0:
                    _text = _text.replace(_pattern, _month_char)
            return _text

        _def_prefix, _def_suffix = self.prefix, self.suffix
        if self.use_letters:
            if self.prefix:
                self.prefix = _interpolate_letters(self.prefix, self.first_year, self.first_month,
                                                   ['%(year)s', '%(y)s'], ['%(month)s'])
            if self.suffix:
                self.suffix = _interpolate_letters(self.suffix, self.first_year, self.first_month,
                                                   ['%(year)s', '%(y)s'], ['%(month)s'])
        res = super(IrSequence_Letters, self)._get_prefix_suffix()
        self.prefix, self.suffix = _def_prefix, _def_suffix
        return res

    def preview_next_code(self):
        _prefix, _suffix = self._get_prefix_suffix()
        _name = _prefix + ("{:0" + str(self.padding) + "d}").format(self.number_next_actual) + _suffix
        return _name
        # if self.working_date:
        #     _prefix, _suffix = self._get_prefix_suffix()
        #     _name = _prefix + f"{self.number_next_actual:0{self.padding}d}" + _suffix
        #     return _name

    # def _get_prefix_suffix(self):
    #     def _interpolate(s, d):
    #         return (s % d) if s else ''
    #
    #     def _interpolation_dict():
    #         now = range_date = effective_date = datetime.now(pytz.timezone(self._context.get('tz') or 'UTC'))
    #         if self._context.get('ir_sequence_date'):
    #             effective_date = datetime.strptime(self._context.get('ir_sequence_date'), '%Y-%m-%d')
    #         if self._context.get('ir_sequence_date_range'):
    #             range_date = datetime.strptime(self._context.get('ir_sequence_date_range'), '%Y-%m-%d')
    #
    #         sequences = {
    #             'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
    #             'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
    #         }
    #         res = {}
    #         for key, format in sequences.items():
    #             res[key] = effective_date.strftime(format)
    #             res['range_' + key] = range_date.strftime(format)
    #             res['current_' + key] = now.strftime(format)
    #
    #         return res
    #
    #     d = _interpolation_dict()
    #     try:
    #         interpolated_prefix = _interpolate(self.prefix, d)
    #         interpolated_suffix = _interpolate(self.suffix, d)
    #     except ValueError:
    #         raise UserError(_('Invalid prefix or suffix for sequence \'%s\'') % (self.get('name')))
    #     return interpolated_prefix, interpolated_suffix
    #
