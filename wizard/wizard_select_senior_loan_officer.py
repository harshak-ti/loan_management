# -*-coding: utf-8 -*-

import logging

from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class WizardSelectSeniorLoanOfficer(models.TransientModel):
    _name = "wizard.select.senior.loan.officer"
    _description = "Select Senior Loan Officer"

    user = fields.Many2one("res.users", "Senior Loan Officer")
    original_assignee = fields.Char("Original Assignee")
    category_id = fields.Char("Category ID")

    def transfer(self):
        self.ensure_one()
        context = dict(self.env.context or {})
        application_id = context.get("active_id")
        application = self.env["application"].browse(application_id)

        template = self.env.ref("appsmod2.email_template_appsmod2_senior_loan_officer")
        uid = context.get("uid")

        for user in self.env["res.users"].browse(uid):
            if not user.email:
                raise UserError(_(f"Cannot send email: User {user.name} has no email address"))

            context["lang"] = user.lang
            application.write({'state': 'submit', 'assignee': self.user})
            application.with_context(context).load_checklist_items("submit")

            application.message_post_with_template(template.id)