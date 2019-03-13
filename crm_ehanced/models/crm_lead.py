# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_firstname = fields.Char(
        "First name",
        index=True,
    )
    contact_lastname = fields.Char(
        "Last name",
        index=True,
    )
    contact_name = fields.Char(
        string="Full Name",
        compute="_compute_name",
        # inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True
    )
    title_shortcut = fields.Char(
        compute="_get_title_shortcut",
        required=False,
        size=6,
        store=True
    )
    lead_language = fields.Many2one(
                    comodel_name="res.lang",
                    string='Langue du contact')
    other_lang_ids = fields.Many2many(
        comodel_name='res.lang',
        relation='crm_lead_lang_rel',
        column1='lead_id',
        column2='land_id',
        string='Other language')
    date_contact = fields.Date(string="Date du contact")

    @api.onchange("title")
    def _get_title_shortcut(self):
        for rec in self:
            rec.title_shortcut = self.env["res.partner.title"].search([('id', '=', rec.title.id)]).shortcut if rec.title else ""

    @api.multi
    @api.depends("contact_firstname", "contact_lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for record in self:
            record.contact_name = self.env["res.partner"]._get_computed_name(
                record.contact_lastname, record.contact_firstname,
            )

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
                    "name": self.contact_name,
                })
                # if 'name' in lead_partner_data:
                #     del lead_partner_data['name']
            if self.contact_firstname:
                lead_partner_data.update({
                    "firstname": self.contact_firstname,
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
                    "contact_name": partner.name,
                    "contact_firstname": partner.firstname,
                    "contact_lastname": partner.lastname,
                    "lead_language": partner.lang,
                })
        return result

