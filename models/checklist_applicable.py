# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_l=logging.getLogger(__name__)



class ChecklistApplicableApplicant(models.Model):
    _name = "checklist.applicable.applicant"
    _description = "Applicant Applicable Checklist"

    name = fields.Char("Checklist")
    provided = fields.Boolean("Provided")
    acceptable = fields.Boolean("Acceptable")
    notes = fields.Char("Notes")
    application_id = fields.Many2one("application", "Applicant", help="Application ID")
    sequence = fields.Integer("Sequence")
    state = fields.Char("State")
    type = fields.Selection(
        [("individual", "Individual"), ("self", "Self Applicable"),("paye", "PAYE Applicable")],
        string="Checklist Type",
        store=True
        
    )
    applicant_type = fields.Selection(
        [("applicant1", "Applicant 1"), ("applicant2", "Applicant 2")],
        string="Applicant Type",
        store=True
        
    )
