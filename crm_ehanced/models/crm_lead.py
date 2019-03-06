# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_name = fields.Char(string="Prénom")
    contact_lastname = fields.Char(string="Nom")
    lead_language = fields.Man2one(
                    comodel_name="res.lang",
                    string='Langue du contact')
    date_contact = fields.Date(string="Date du contact")

    @api.multi
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        """Ensure first and last names of contact match those in lead."""
        lead_partner_data = super(CrmLead, self)._create_lead_partner_data(
            name,
            is_company,
            parent_id
        )
        if not is_company:
            lead_partner_data.update({
                    "lang": self.lead_language,
                })
            if self.contact_name:
                lead_partner_data.update({
                    "firstname": self.contact_name,
                })
                if 'name' in lead_partner_data:
                    del lead_partner_data['name']
            if self.contact_lastname:
                lead_partner_data.update({
                    "lastname": self.contact_lastname,
                })
                if 'name' in lead_partner_data:
                    del lead_partner_data['name']
        return lead_partner_data

    def _onchange_partner_id_values(self, partner_id):
        """Recover first and last names from partner if available."""
        result = super(CrmLead, self)._onchange_partner_id_values(partner_id)

        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if not partner.is_company:
                result.update({
                    "contact_name": partner.firstname,
                    "contact_lastname": partner.lastname,
                    "lead_language": partner.lang,
                })
        return result
