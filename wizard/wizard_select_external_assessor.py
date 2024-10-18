# -*-coding: utf-8 -*-

from odoo import models, fields, _ 
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class WizardSelectExternalAssessor(models.TransientModel):
    _name = "wizard.select.external.assessor"
    _description = "Wizard Select External Assessor"

    user = fields.Many2one("res.users", "External Assessor")
    category_id = fields.Char("Category ID")
    company_id = fields.Many2one("res.company", "Company")
    assignee = fields.Many2one("res.users", "Assignee")


    def transfer(self):
        self.ensure_one()
        context = dict(self.env.context or {})
        application_id  = context.get("active_id")
        application = self.env["application"].browse(application_id)
        application.write({
            'state': "external_assessor",
            'assignee': self.user, 
            'external_assessor_user': self.user
        })

        template = self.env.ref("appsmod2.email_template_appsmod2_external_assessor")
        uid = context.get("uid")
        for user in self.env["res.users"].browse(uid):
            if not user.email:
                raise UserError(_(f"Cannot send email: User {user.name} has no email address."))

            context["lang"] = user.lang
            application.message_post_with_template(template.id)



        