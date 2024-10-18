# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _default_country(self):
        country = self.env["res.country"].search([('name', '=', "Ireland")], limit=1)
        return country

    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    member_id = fields.Char("Member ID")
    # Used as DOB in v9
    DOB = fields.Date("Date of Birth")

    # Adds default country attribute
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=_default_country)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    # _sql_constraints = [
    #     ('member_unique', "unique(member_id, company_id)", "Member ID must be Unique per Company!")
    # ]

    @api.onchange("first_name", "last_name")
    def _onchange_first_last_name(self):
        "Set fullname for partner if first and last names are given instead of fullname when creating contact."

        fullname = ""
        if self.first_name:
            fullname += self.first_name
        if self.last_name:
            fullname += " " + self.last_name

        self.write({'name': fullname})


class CountryState(models.Model):
    _inherit = "res.country.state"

    def name_get(self):
        "Remove country code from display name for state."
        names = []
        for state in self:
            names.append((state.id, state.name))
        return names
