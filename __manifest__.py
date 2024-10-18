# -*- coding: utf-8 -*-
{
    'name'          : "SAM - Secure Application Management",
    'author'        : "Target Integration",
    'summary'       : "This module implements Application Module of Target Integration",
    'description'   : """
                    This module will create the workflow needed to support the Test & Affordability Calculator's functionality as described in the tickets
                    #9844, #9851, #9853, #9854, #9855, #9856, #55394
                    """,
    'website'       : "http://www.targetintegration.com",
    'category'      : "Uncategorized",
    'version'       : "17.0.1.1",
    # any module necessary for this one to work correctly
    'depends'       : ["base", "mail", "contacts"],
    'data'          : [
                    'security/appsmod2_security.xml',
                    'security/ir.model.access.csv',
                    'data/partner_data.xml',
                    'data/default_checklist_data.xml',
                    'data/ir_sequence_data.xml',
                    'data/mail_templates.xml',
                    'views/documents_applicable_views.xml',
                    'views/mortgage_product_views.xml',
                    'views/res_company_views.xml',
                    'views/res_partner_views.xml',
                    'views/application_checklist_views.xml',
                    'views/application_views.xml',
                    'views/application_views_full.xml',
                    'views/appsmod2_menus.xml',
                    'wizard/wizard_decline_views.xml',
                    'wizard/wizard_limits_not_eligible_views.xml',
                    'wizard/wizard_pre_application_not_complete_views.xml',
                    'wizard/wizard_select_external_assessor_views.xml',
                    'wizard/wizard_select_senior_loan_officer_views.xml',
                    'wizard/wizard_accept_application_views.xml',
                    'wizard/wizard_gift_warning_views.xml',
                    'report/external_layout.xml',
                    'report/decline_letter_report.xml',
                    'report/in_principal_letter_report.xml',
                    'report/affordability_calculator_report.xml',
                    'report/offer_letter_2020_report.xml',
                    'report/offer_letter_report.xml',
                    'report/esis_report.xml',
                    'report/esis_2020_report.xml',
                    'report/drawdown_letter_report.xml',
                    'report/appsmod2_reports.xml'
                ],
    'external_dependencies': {
        'python': ['numpy', 'numpy-financial']
    },
    'assets': {

        'web.assets_backend':[
        #   "appsmod2/static/js/warning_popup.js",
          
        ]
   
    },
    'application'   : True,
    'sequence'      : 1
}
