# -*- coding: utf-8 -*-

from odoo import models, _

class WizardGiftWarning(models.TransientModel):
    _name = "wizard.gift.warning"
    _description = "Gift Warning Wizard"

    def gift_warning_save(self):
        application_id = self.env.context.get("active_id")
        application = self.env["application"].browse(application_id)
        application.write({'state': "application_form_received"})
        application.with_context(self.env.context).load_checklist_items("application_form_received")