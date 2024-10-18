# -*- coding: utf-8 -*-

import logging

from odoo.tests import tagged, Form
from odoo.addons.base.tests.test_form_create import TestFormCreate

_logger = logging.getLogger(__name__)

@tagged('at_install', 'cuda_sam')
class TestFormCreateExtended(TestFormCreate):

    def test_create_res_partner(self):
        _logger.critical(f"\n==================Cuda - SAM Overriding Partner Form=====================\n")
        partner_form = Form(self.env['res.partner'])
        partner_form.first_name = "First Name"
        partner_form.last_name = "Last Name"
        partner_form.member_id = "TEST123"
        partner_form.DOB = "1997-10-14"
        # YTI: Clean that brol
        if hasattr(self.env['res.partner'], 'property_account_payable_id'):
            property_account_payable_id = self.env['account.account'].create({
                'name': 'Test Account',
                'user_type_id': self.env.ref('account.data_account_type_payable').id,
                'code': 'TestAccountPayable',
                'reconcile': True
            })
            property_account_receivable_id = self.env['account.account'].create({
                'name': 'Test Account',
                'user_type_id': self.env.ref('account.data_account_type_receivable').id,
                'code': 'TestAccountReceivable',
                'reconcile': True
            })
            partner_form.property_account_payable_id = property_account_payable_id
            partner_form.property_account_receivable_id = property_account_receivable_id
        partner_form.save()