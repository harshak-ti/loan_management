# -*-coding: utf-8 -*-

import logging

from odoo.tests import common, tagged, Form


_logger = logging.getLogger(__name__)

@tagged("at_install", "cuda_sam")
class TestApplication(common.SingleTransactionCase):
    """Test Workflow of Application Process"""

    @classmethod
    def setUpClass(cls):
        _logger.info(f"\nSetting Up Data for Testing Application Process,\n")

        super().setUpClass()

        # Creating Applicants
        Partner = cls.env["res.partner"]
        cls.applicant1 = Partner.create(
            {
                'first_name': "John",
                'last_name': "Doe",
                'member_id': "JD123",
                'DOB': "1997-10-14"
            }
        )
        cls.applicant2 = Partner.create(
            {
                'first_name': "Jane",
                'last_name': "Doe",
                'member_id': "JD321",
                'DOB': "1998-10-14"
            }
        )

        # Creating Mortgage Products
        MortgageProduct = cls.env["mortgage.product"]
        cls.fixed_into_variable_mortgage = MortgageProduct.create(
            {
                'name': "3yr Fixed @3.5%",
                'mortgage_type': "fixed_variable_rate",
                'fixed_interest_rate': 3.5,
                'fixed_term': 3,
                'variable_interest_rate': 4.25
            }
        )
        cls.variable_mortgage = MortgageProduct.create(
            {
                'name': "Variable Rate @4.8%",
                'mortgage_type': "variable_rate",
                'fixed_interest_rate': 0,
                'fixed_term': 0,
                'variable_interest_rate': 4.8
            }
        )

        # Creating Applications
        Application = cls.env["application"]

        single_variable_application = Form(Application)
        single_variable_application.mortgage_product_id = cls.variable_mortgage
        single_variable_application.mortgrage_term_year = 25
        single_variable_application.mortgage_amount = 500000
        single_variable_application.property_value = 750000
        single_variable_application.applicant_1 = cls.applicant1
        single_variable_application.total_basic_income_1 = 150000
        single_variable_application.total_net_basic_income_1 = 150000
        cls.single_variable_application = single_variable_application.save()

        single_fixed_application = Form(Application)
        single_fixed_application.mortgage_product_id = cls.fixed_into_variable_mortgage
        single_fixed_application.mortgrage_term_year = 20
        single_fixed_application.mortgrage_term_months = "6"
        single_fixed_application.mortgage_amount = 350000
        single_fixed_application.property_value = 500000
        single_fixed_application.applicant_1 = cls.applicant1
        single_fixed_application.total_basic_income_1 = 100000
        single_fixed_application.total_net_basic_income_1 = 100000
        single_fixed_application.total_other_income_1 = 3000
        single_fixed_application.other_income_counted = 50
        single_fixed_application.debt_repay = 500
        cls.single_fixed_application = single_fixed_application.save()

    def test_mortgage_product(self):
        """Test interest rate and terms"""

        self.assertEqual(self.single_variable_application.interest_rate, 4.8, msg="Interest rate is incorrect.")
        self.assertEqual(self.single_variable_application.term_at_starting_rate, 0, msg="Term @ starting rate is incorrect.")
        self.assertEqual(self.single_variable_application.fixed_interest_rate, 0, msg="Fixed interest rate is incorrect.")
        self.assertEqual(self.single_variable_application.mortgage_type, "variable_rate", msg="Mortgage type is incorrect.")

        self.assertEqual(self.single_fixed_application.interest_rate, 4.25, msg="Interest rate is incorrect.")
        self.assertEqual(self.single_fixed_application.term_at_starting_rate, 3, msg="Term @ starting rate is incorrect.")
        self.assertEqual(self.single_fixed_application.fixed_interest_rate, 3.50, msg="Fixed interest rate is incorrect.")
        self.assertEqual(self.single_fixed_application.mortgage_type, "fixed_variable_rate", msg="Mortgage type is incorrect.")

    def test_underwritting_metrices(self):
        """Testing underwritting metrices: ltv, lti, service ratio etc."""

        self.assertEqual(self.single_variable_application.loan_to_value, 66.67, msg="Loan to Value is not correct.")
        self.assertEqual(self.single_variable_application.loan_to_income_ratio, 3.33, msg="Loan to Income is not correct.")
        self.assertEqual(self.single_variable_application.mortgage_service_ratio, 22.92, msg="Mortage Service Ratio is not correct.")
        self.assertEqual(self.single_variable_application.total_debt_service_ratio, 22.92, msg="Total Debt Service Ratio is not correct.")
        self.assertEqual(self.single_variable_application.gift_to_deposit, 0, msg="Gift to Deposit \% \is not correct.")

        self.assertEqual(self.single_fixed_application.loan_to_value, 70.0, msg="Loan to Value is not correct.")
        self.assertEqual(self.single_fixed_application.loan_to_income_ratio, 3.5, msg="Loan to Income is not correct.")
        self.assertEqual(self.single_fixed_application.mortgage_service_ratio, 25.01, msg="Mortage Service Ratio is not correct.")
        self.assertEqual(self.single_fixed_application.total_debt_service_ratio, 30.92, msg="Total Debt Service Ratio is not correct.")
        self.assertEqual(self.single_fixed_application.gift_to_deposit, 0, msg="Gift to Deposit \% \is not correct.")

    def test_income(self):
        """Test different incomes based on applicant's income."""

        self.assertEqual(round(self.single_variable_application.total_income, 2), 150000, msg="Total income is incorrect.")
        self.assertEqual(round(self.single_variable_application.total_sustainable_income, 2), 150000, msg="Total sustainable income is incorrect.")
        self.assertEqual(round(self.single_variable_application.allowable_monthly_income, 2), 12500, msg="Allowable monthly income is incorrect.")
        self.assertEqual(round(self.single_variable_application.net_disposable_inc, 2), 9635.02, msg="Net disposable income is incorrect.")
        self.assertEqual(round(self.single_variable_application.max_lend_facility, 2), 525000, msg="Max lend facility is incorrect.")

        self.assertEqual(round(self.single_fixed_application.total_income, 2), 103000, msg="Total income is incorrect.")
        self.assertEqual(round(self.single_fixed_application.total_sustainable_income, 2), 101500, msg="Total sustainable income is incorrect.")
        self.assertEqual(round(self.single_fixed_application.allowable_monthly_income, 2), 8458.33, msg="Allowable monthly income is incorrect.")
        self.assertEqual(round(self.single_fixed_application.net_disposable_inc, 2), 5842.62, msg="Net disposable income is incorrect.")
        self.assertEqual(round(self.single_fixed_application.max_lend_facility, 2), 350000, msg="Max lend facility is incorrect.")

    def test_stress_test(self):
        """Test stress test for application."""

        company_id = self.env.user.company_id
        self.assertEqual(round(self.single_variable_application.monthly_income_reduced, 2), company_id.monthly_income_reduced, msg="Monthly income reduced is not correct.")
        self.assertEqual(round(self.single_variable_application.interest_rate_increase, 2), company_id.interest_rate_increase, msg="Interest rate increase is not correct.")
        self.assertEqual(round(self.single_variable_application.stressed_income, 2), 142500, msg="Stressed income is incorrect.")
        self.assertEqual(round(self.single_variable_application.stressed_allowable_income, 2), 11875, msg="Stressed allowable income is not correct.")
        self.assertEqual(round(self.single_variable_application.stressed_mortgage_service_ratio, 2), 29.22, msg="Stressed mortgage service ratio is incorrect.")
        self.assertEqual(round(self.single_variable_application.stressed_total_debt_service_ratio, 2), 29.22, msg="Stressed total debt service ratio is incorrect.")
        self.assertEqual(round(self.single_variable_application.stressed_net_disposable_income, 2), 8404.64, msg="Stressed net disposable income is incorrect.")

        self.assertEqual(round(self.single_fixed_application.monthly_income_reduced, 2), company_id.monthly_income_reduced, msg="Monthly income reduced is not correct.")
        self.assertEqual(round(self.single_fixed_application.interest_rate_increase, 2), company_id.interest_rate_increase, msg="Interest rate increase is not correct.")
        self.assertEqual(round(self.single_fixed_application.stressed_income, 2), 97850.00, msg="Stressed income is incorrect.")
        self.assertEqual(round(self.single_fixed_application.stressed_allowable_income, 2), 8035.41, msg="Stressed allowable income is not correct.")
        self.assertEqual(round(self.single_fixed_application.stressed_mortgage_service_ratio, 2), 31.45, msg="Stressed mortgage service ratio is incorrect.")
        self.assertEqual(round(self.single_fixed_application.stressed_total_debt_service_ratio, 2), 37.67, msg="Stressed total debt service ratio is incorrect.")
        self.assertEqual(round(self.single_fixed_application.stressed_net_disposable_income, 2), 5008.44, msg="Stressed net disposable income is incorrect.")

    def test_weekly_repayments(self):

        self.single_variable_application.esis_payment_frequency = "weekly"
        self.assertEqual(round(self.single_variable_application.esis_weekly_repayment, 2), 660.63, msg="Weekly repayment is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_weekly_repayment_1, 2), 728.78, msg="Weekly repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_weekly_repayment_2, 2), 800.19, msg="Weekly repayment + 2\% \is incorrect.")
        self.assertEqual(round(self.single_variable_application.fixed_term_payment, 2), 384.62, msg="Fixed term payment is not correct.")
        self.assertEqual(round(self.single_variable_application.repayment_at_variable, 2), 660.63, msg="Repayment at variable is not correct.")
        self.assertEqual(round(self.single_variable_application.repayment_at_variable_plus1, 2), 728.78, msg="Repayment at variable + 1 is not correct.")
        self.assertEqual(round(self.single_variable_application.repayment_at_variable_plus2, 2), 800.19, msg="Repayment at variable + 2 is not correct.")
        self.assertEqual(round(self.single_variable_application.max_possible_repayment, 2), 2864.98, msg="Max possible repayment is not correct.")
        
        # Checking ESIS
        self.assertEqual(round(self.single_variable_application.esis_no_of_repayment, 2), 1300, msg="No. of repayments is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_total_repaid, 2), 858819.00, msg="Total repaid is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_cost_of_credit, 2), 358819.00, msg="Cost of credit is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_cost_per_1, 2), 1.72, msg="Cost per €1 is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_interest_rate, 2), 5.80, msg="Interest rate + 1\% \is incorrect.")
        self.assertEqual(round(self.single_variable_application.avg_repayment, 2), 660.63, msg="Weekly average repayment is incorrect.")
        self.assertEqual(round(self.single_variable_application.avg_repayment_plus1, 2), 3164.90, msg="Weekly average repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_variable_application.avg_rate, 2), 4.81, msg="Average rate is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_aprc, 2), 4.90, msg="APRC is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_aprc_1, 2), 6, msg="APRC + 1\% \is incorrect.")
        self.single_variable_application.esis_payment_frequency = "monthly"

        self.single_fixed_application.esis_payment_frequency = "weekly"
        self.assertEqual(round(self.single_fixed_application.esis_weekly_repayment, 2), 530.64, msg="Weekly repayment is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_weekly_repayment_1, 2), 572.28, msg="Weekly repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_weekly_repayment_2, 2), 615.68, msg="Weekly repayment + 2\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.fixed_term_payment, 2), 460.78, msg="Fixed term payment is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable, 2), 488.39, msg="Repayment at variable is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable_plus1, 2), 526.64, msg="Repayment at variable + 1 is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable_plus2, 2), 566.50, msg="Repayment at variable + 2 is not correct.")
        self.assertEqual(round(self.single_fixed_application.max_possible_repayment, 2), 488.39, msg="Max possible repayment is not correct.")
        
        # Checking ESIS
        self.assertEqual(round(self.single_fixed_application.esis_no_of_repayment, 2), 1066, msg="No. of repayments is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_total_repaid, 2), 515339.80, msg="Total repaid is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_cost_of_credit, 2), 165339.80, msg="Cost of credit is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_cost_per_1, 2), 1.47, msg="Cost per €1 is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_interest_rate, 2), 5.25, msg="Interest rate + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_repayment, 2), 484.34, msg="Weekly average repayment is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_repayment_plus1, 2), 2294.13, msg="Weekly average repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_rate, 2), 4.09, msg="Average rate is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_aprc, 2), 4.20, msg="APRC is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_aprc_1, 2), 5.2, msg="APRC + 1\% \is incorrect.")
        self.single_fixed_application.esis_payment_frequency = "monthly"

    def test_fortnightly_repayments(self):

        self.single_variable_application.esis_payment_frequency = "fortnightly"
        self.assertEqual(round(self.single_variable_application.esis_fortnightly_repayment, 2), 1321.57, msg="Fortnightly repayment is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_fortnightly_repayment_1, 2), 1457.92, msg="Fortnightly repayment + 1\% \is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_fortnightly_repayment_2, 2), 1600.78, msg="Fortnightly repayment + 2\% \is not correct.")
        self.assertEqual(round(self.single_variable_application.fixed_term_payment, 2), 769.23, msg="Fixed term payment is not correct.")
        self.assertEqual(round(self.single_variable_application.repayment_at_variable, 2), 1321.57, msg="Repayment at variable is not correct.")
        self.assertEqual(round(self.single_variable_application.repayment_at_variable_plus1, 2), 1457.92, msg="Repayment at variable + 1 is not correct.")
        self.assertEqual(round(self.single_variable_application.repayment_at_variable_plus2, 2), 1600.78, msg="Repayment at variable + 2 is not correct.")
        self.assertEqual(round(self.single_variable_application.max_possible_repayment, 2), 2864.98, msg="Max possible repayment is not correct.")
        
        # Checking ESIS
        self.assertEqual(round(self.single_variable_application.esis_no_of_repayment, 2), 650, msg="No. of repayments is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_total_repaid, 2), 859020.50, msg="Total repaid is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_cost_of_credit, 2), 359020.50, msg="Cost of credit is not correct.")
        self.assertEqual(round(self.single_variable_application.esis_cost_per_1, 2), 1.72, msg="Cost per €1 is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_interest_rate, 2), 5.80, msg="Interest rate + 1\% \is incorrect.")
        self.assertEqual(round(self.single_variable_application.avg_repayment, 2), 1321.57, msg="Fortnightly average repayment is incorrect.")
        self.assertEqual(round(self.single_variable_application.avg_repayment_plus1, 2), 3165.60, msg="Fortnightly average repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_variable_application.avg_rate, 2), 4.82, msg="Average rate is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_aprc, 2), 4.90, msg="APRC is incorrect.")
        self.assertEqual(round(self.single_variable_application.esis_aprc_1, 2), 6, msg="APRC + 1\% \is incorrect.")
        self.single_variable_application.esis_payment_frequency = "monthly"

        self.single_fixed_application.esis_payment_frequency = "fortnightly"
        self.assertEqual(round(self.single_fixed_application.esis_fortnightly_repayment, 2), 1016.27, msg="Fortnightly repayment is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_fortnightly_repayment_1, 2), 1096.06, msg="Fortnightly repayment + 1\% \is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_fortnightly_repayment_2, 2), 1179.20, msg="Fortnightly repayment + 2\% \is not correct.")
        self.assertEqual(round(self.single_fixed_application.fixed_term_payment, 2), 921.78, msg="Fixed term payment is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable, 2), 977.03, msg="Repayment at variable is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable_plus1, 2), 1053.59, msg="Repayment at variable + 1 is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable_plus2, 2), 1133.36, msg="Repayment at variable + 2 is not correct.")
        self.assertEqual(round(self.single_fixed_application.max_possible_repayment, 2), 977.03, msg="Max possible repayment is not correct.")
        
        # Checking ESIS
        self.assertEqual(round(self.single_fixed_application.esis_no_of_repayment, 2), 533, msg="No. of repayments is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_total_repaid, 2), 515470.46, msg="Total repaid is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_cost_of_credit, 2), 165470.46, msg="Cost of credit is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_cost_per_1, 2), 1.47, msg="Cost per €1 is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_interest_rate, 2), 5.25, msg="Interest rate + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_repayment, 2), 968.93, msg="Fortnightly average repayment is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_repayment_plus1, 2), 2294.69, msg="Fortnightly average repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_rate, 2), 4.09, msg="Average rate is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_aprc, 2), 4.2, msg="APRC is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_aprc_1, 2), 5.2, msg="APRC + 1\% \is incorrect.")
        self.single_fixed_application.esis_payment_frequency = "monthly"

    def test_monthly_repayments(self):
        self.assertEqual(self.single_variable_application.monthly_repayment, 2864.98, msg="Monthly repayment is not correct.")
        self.assertEqual(self.single_variable_application.esis_monthly_repayment_1, 3160.66, msg="Monthly repayment + 1\% \is not correct.")
        self.assertEqual(self.single_variable_application.esis_monthly_repayment_2, 3470.36, msg="Monthly repayment + 2\% \is not correct.")
        self.assertEqual(self.single_variable_application.fixed_term_payment, 1666.67, msg="Fixed term payment is not correct.")
        self.assertEqual(self.single_variable_application.repayment_at_variable, 2864.98, msg="Repayment at variable is not correct.")
        self.assertEqual(self.single_variable_application.repayment_at_variable_plus1, 3160.66, msg="Repayment at variable + 1 is not correct.")
        self.assertEqual(self.single_variable_application.repayment_at_variable_plus2, 3470.36, msg="Repayment at variable + 2 is not correct.")
        self.assertEqual(self.single_variable_application.max_possible_repayment, 2864.98, msg="Max possible repayment is not correct.")
        
        # Checking ESIS
        self.assertEqual(self.single_variable_application.esis_no_of_repayment, 300, msg="No. of repayments is not correct.")
        self.assertEqual(self.single_variable_application.esis_total_repaid, 859494.00, msg="Total repaid is not correct.")
        self.assertEqual(self.single_variable_application.esis_cost_of_credit, 359494.00, msg="Cost of credit is not correct.")
        self.assertEqual(self.single_variable_application.esis_cost_per_1, 1.72, msg="Cost per €1 is incorrect.")
        self.assertEqual(self.single_variable_application.esis_interest_rate, 5.80, msg="Interest rate + 1\% \is incorrect.")
        self.assertEqual(self.single_variable_application.avg_repayment, 2864.98, msg="Monthly average repayment is incorrect.")
        self.assertEqual(self.single_variable_application.avg_repayment_plus1, 3160.65, msg="Monthly average repayment + 1\% \is incorrect.")
        self.assertEqual(self.single_variable_application.avg_rate, 4.8, msg="Average rate is incorrect.")
        self.assertEqual(self.single_variable_application.esis_aprc, 4.90, msg="APRC is incorrect.")
        self.assertEqual(self.single_variable_application.esis_aprc_1, 6, msg="APRC + 1\% \is incorrect.")

        self.assertEqual(round(self.single_fixed_application.monthly_repayment, 2), 2133.80, msg="Monthly repayment is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_monthly_repayment_1, 2), 2325.97, msg="Monthly repayment + 1\% \is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_monthly_repayment_2, 2), 2526.97, msg="Monthly repayment + 2\% \is not correct.")
        self.assertEqual(round(self.single_fixed_application.fixed_term_payment, 2), 1995.69, msg="Fixed term payment is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable, 2), 2115.71, msg="Repayment at variable is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable_plus1, 2), 2281.99, msg="Repayment at variable + 1 is not correct.")
        self.assertEqual(round(self.single_fixed_application.repayment_at_variable_plus2, 2), 2455.22, msg="Repayment at variable + 2 is not correct.")
        self.assertEqual(round(self.single_fixed_application.max_possible_repayment, 2), 2115.71, msg="Max possible repayment is not correct.")
        
        # Checking ESIS
        self.assertEqual(round(self.single_fixed_application.esis_no_of_repayment, 2), 246, msg="No. of repayments is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_total_repaid, 2), 516143.94, msg="Total repaid is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_cost_of_credit, 2), 166143.94, msg="Cost of credit is not correct.")
        self.assertEqual(round(self.single_fixed_application.esis_cost_per_1, 2), 1.47, msg="Cost per €1 is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_interest_rate, 2), 5.25, msg="Interest rate + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_repayment, 2), 2098.15, msg="Monthly average repayment is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_repayment_plus1, 2), 2288.59, msg="Monthly average repayment + 1\% \is incorrect.")
        self.assertEqual(round(self.single_fixed_application.avg_rate, 2), 4.06, msg="Average rate is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_aprc, 2), 4.1, msg="APRC is incorrect.")
        self.assertEqual(round(self.single_fixed_application.esis_aprc_1, 2), 5.2, msg="APRC + 1\% \is incorrect.")