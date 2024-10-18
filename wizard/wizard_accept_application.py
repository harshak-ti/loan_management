# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, _

import logging

_logger = logging.getLogger(__name__)

class WizardAcceptApplication(models.TransientModel):
    _name = "wizard.accept.application"
    _description = "Wizard Accept Application"

    message = fields.Text("Approval Comments")

    def add_months(self, start_date, months):
        end_date = None
        if start_date:
            end_date = (datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(months=months)).strftime("%Y-%m-%d")
        return end_date

    def accept_application(self):
        application_id = self.env.context.get("active_id")
        application = self.env["application"].browse(application_id)

        today = fields.Date.today()
        today_1 = self.add_months(str(today), 1)
        today_2 = self.add_months(str(today), 2)

        application.message_post(body=_(self.message))
        application.write({
            'state': "accepted",
            'date_of_offer': today,
            'date_of_offer_plus_1': today_1,
            'date_of_offer_plus_2': today_2
        })