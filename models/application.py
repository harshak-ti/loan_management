# -*-coding: utf-8 -*-

import math
import base64
import logging
import numpy as np
import numpy_financial as npf

from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import logging 
_l=logging.getLogger(__name__)

ADDRESS_FORMAT_CLASSES = {
    '%(city)s %(state_code)s\n%(zip)s': 'o_city_state',
    '%(zip)s %(city)s': 'o_zip_city'
}

STANDARD_GIFT_TO_DEPOSIT = 50.0

STANDARD_MORTGAGE_SERVICE_RATIO = 50.0

STANDARD_TOTAL_DEBT_SERVICE_RATIO = 50.0

STANDARD_STRESSED_MORTGAGE_SERVICE_RATIO = 40.0

STATE_SELECTION = [
    ('draft', "Draft"),
    ('limits_eligible', "Limits Eligible"),
    ('limits_not_eligible', "Limits Not Eligible"),
    ('pre_application_complete', "Pre-Application Complete"),
    ('pre_application_not_complete', "Pre-Application Not Complete"),
    ('application_requested', "Application Requested"),
    ('application_pack_returned', "Application Pack Returned"),
    ('consent_signed', "Consent Signed"),
    ('application_form_received', "Application Form Received"),
    ('external_assessor', "External Assessor"),
    ('ready_for_assessment', "Ready For Assessment"),
    ('valuation_report', "Awaiting Valuation Report"),
    ('property_overvalued', "Property Over-Valued"),
    ('submit', "Submit for Final Review"),
    ('accepted', "Accepted"),
    ('funds_drawn_down', "Funds Drawn Down"),
    ('decline', "Declined")
]

YES_NO = [
    ('yes', "Yes"),
    ('no', "No")
]

PAYMENT_FREQUENCY = [
    ('weekly', "Weekly"),
    ('fortnightly', "Fortnightly"),
    ('monthly', "Monthly")
]

SINGLE = [
    ('1300', "1300"),
    ('2050', "2050")
]

PURPOSE_OF_MORTGAGE = [
    ('moving', "Moving Home"),
    ('building', "Building Home"),
    ('switching', "Switching Mortgage Provider"),
    ('topup', "Top Up"),
    ('buy_first_home', "Buy First Home")
]

MONTH_SELECTION = [
    ('0', "0"),
    ('1', "1"),
    ('2', "2"),
    ('3', "3"),
    ('4', "4"),
    ('5', "5"),
    ('6', "6"),
    ('7', "7"),
    ('8', "8"),
    ('9', "9"),
    ('10', "10"),
    ('11', "11"),
    ('12', "12")
    ]

BER_RATING = [
    ('a1', "A1"),
    ('a2', "A2"),
    ('a3', "A3"),
    ('b1', "B1"),
    ('b2', "B2"),
    ('b3', "B3"),
    ('c1', "C1"),
    ('c2', "C2"),
    ('c3', "C3"),
    ('d1', "D1"),
    ('d2', "D2"),
    ('e1', "E1"),
    ('e2', "E2"),
    ('f', "F"),
    ('g', "G"),
    ('exempt', "Exempt"),
    ('unknown', "Unknown")
]

SAM_GENERAL_TERMS_CONDITIONS = """
<div style=\"font-family: Calibri; font-size: 14px; color: rgb(34, 34, 34); background-color: #FFF;margin-left:7mm \">
    <h3 style='text-align:center'>GENERAL HOME LOAN CONDITIONS</h3><br/>
    <ol style="list-style-type:none">
        <li class="mt-1">
            <h5>1. Definitions</h5>
            “Credit Union’s Mortgage Rate” means the interest rate as may from time to time be applicable to the Loan. “Loan” means the sum of money which the Credit Union has in the Credit Union’s Loan Offer agreed to advance to the Borrower and includes the unpaid balance of any sum due. “Loan Offer” / “Letter of Offer” means the document issued by the Credit Union specifying the amount, terms and conditions upon which the Credit Union will make the Loan. “Loan Term” means the term of the Loan specified in the Loan Offer as amended or varied in writing from time to time. “Loan Payment Date” means the date on which the Loan Repayments falls due. “Mortgage” means the first legal charge for present and future advances which incorporates the General Housing Loan Mortgage Conditions / General Mortgage Terms and Conditions. “Mortgage Balance” means the amount owed by the borrower to the Credit Union under the terms of the Mortgage at any given time and can include not only the Loan Payment but also property insurance, legal costs, expenses or other sums recoverable pursuant to the terms of the Mortgage.
        </li>
        <br/>
        <li>
            <h5>2. Advance and Repayment</h5>
            2.1 Drawdown of the Loan shall be subject to compliance with the terms and conditions of the Loan Offer.<br/><br/>
            2.2 The interest rate shall be the interest rate applicable at the date of drawdown of the Loan.<br/><br/>
            2.3 Interest is calculated daily on the principal balance of the Loan outstanding.<br/><br/>
            2.4 The Loan is repayable as indicated in the Loan Offer. This will be monthly, fortnightly or weekly as set out in the Loan Offer. For the purposes of interest calculation, the first repayment is deemed payable one month after funds draw down. Insofar as is practicable, the Borrower’s preference for the first and subsequent Loan Payment Dates will be accommodated by the Credit Union.<br/><br/>
            2.5 If the Borrower wishes to round up or increase the [monthly, fortnightly or weekly] loan repayment amount as set out Loan Offer this should be discussed with the credit union in advance of signing the direct debit mandate and where practicable will be accommodated by the credit union. Rounding up on the direct debit mandate will accelerate the repayment of the Loan and as a result the figures on the amortisation table will change. This may also result in the Loan being repaid earlier. <br/><br/>
            2.6 Repayments made before the Loan Payment Date will reduce the interest charged. Payments made after the Loan Payment Date will result in a higher than scheduled interest amount charged, although there are no direct charges for late or missed payments.<br/><br/>
            2.7 If the due date for a repayment falls on a non-business day, such as a weekend or bank holiday then the repayment may be paid on the next working day. Additional interest may accrue in such cases. This could cause the total amount payable by you to increase.<br/><br/>
            2.8 Other factors such as the exact day of drawdown, rounding in calculation, a change in the regular repayment date or an additional day in leap years can also impact the number of Loan Repayments or the total amount you pay under this credit agreement.<br/>
        </li>
        <br/>
        <li>
            <h5>3. Interest</h5>
            <h5>3.1 Variable Interest Rate</h5>
            In the case of variable interest rate Loans, the Credit Union can vary the interest rate at any time during the Loan Term. This could cause your repayment amount to increase or decrease over the Loan Term. In the event of a rate change, we may either continue to apply the same Loan Repayments in which case the Loan Term will alter or we may apply a variation in repayments over the Loan Term.<br/>
            The Credit Union will notify the Borrower on paper or on another durable medium if the interest rate changes. In the case of fixed rate Loans, the interest rate will remain the same for the agreed fixed interest rate period set out in the Loan Offer. <br/>
            Variable interest rate gives you flexibility. Payments in excess of those agreed may be made at the discretion of the Borrower, at any time during the period of the Loan without additional cost. <span>A capital reduction or lumpsum payment made against the mortgage by a borrower on a variable rate mortgage will have the effect of reducing the term where the borrower remains on the same mortgage repayment.  The borrower also has the option of reducing the mortgage repayment over the remaining term and if they choose this option, this request needs to be put in writing to the Credit Union who will advise of the new monthly repayment.</span><br/>
            <br/>
            <h5>3.2 Fixed Interest Rate</h5>
            In the case of a fixed interest rate the following conditions apply:<br/>
            3.2.1 This is a Loan Offer with a fixed interest rate as set out in the Particulars of Home Loan.  A fixed rate loan is calculated on the basis that the loan will not be repaid ahead of maturity of the fixed interest rate term.  It is on this basis that the Credit Union is prepared to commit itself to holding its lending rate fixed for the agreed period and incur certain third party costs on your behalf, such as valuation, legal and registration fees. Nonetheless, the Borrower is entitled to prepay the loan in full at any time or to convert to a variable rate or other fixed rate that the Credit Union may offer during the fixed term of the loan or to make a capital repayment in excess of the scheduled instalments.  In any of these circumstances, the Credit Union is entitled, subject to the provisions of section 121(2) of the Consumer Credit Act 1995, to recoup an early breakage cost from the Borrower.  The Credit Union limits this cost to those it has committed itself to or incurred to facilitate the loan Offer and will only impose an early breakage cost on the Borrower if the Borrower is prepaying the loan in full.  If the Borrower wishes to make a full prepayment, the Credit Union will confirm the sum payable and the Borrower is obliged to pay it in full prior to the release of the Credit Union’s security.<br/><br/>
            3.2.2 While on a fixed interest rate, the interest rate and Loan Repayment remain the same for the agreed fixed interest rate period. During this time the interest rate will not change. The Borrower is entitled to prepay the Loan in full at any time or to convert to a variable rate or another fixed rate that the Credit Union may offer during the Loan Term or to make a capital repayment in excess of the scheduled instalments.<br/><br/>
            3.2.3 In any of these circumstances, unless specified otherwise as a special condition of offer, an early breakage charge is payable where the fixed interest rate period has not expired, and the following applies to early redemption of a fixed interest rate mortgage:<br/>
            The breakage charge is calculated as follows:<br/>

            amount (A) x remaining term in days divided by 365 (U) x difference in cost of funds (D%). <br/>

            Definition of terms used in this formula:<br/>
            (A) amount - The amount being repaid early or the amount being converted to a variable rate or another fixed rate period.<br/>
            (U) remaining term in days - Remaining number of days left before the fixed rate is due to expire.<br/>
            (D) difference in cost of funds - The difference between the original cost of funds and the cost of funds for the fixed rate period remaining (including the third party costs incurred).<br/><br/>
            3.2.4 At the end of an unbroken fixed interest rate period, the interest rate on your Loan will default to the standard variable interest rate then offered by the Credit Union at that time unless the Borrower chooses an alternative interest rate, if on offer by the Credit Union to the Borrower at that time. Our standard variable interest rate is a variable interest rate. If the interest rate on your Loan defaults or otherwise converts to a variable interest rate then offered by the Credit Union, your interest rate and the amount of your Loan Repayment instalments could increase or decrease during the Loan Term and your interest rate could be higher than the fixed interest rate that applied during any fixed interest rate period.
        </li>
        <br/>
        <li>
            <h5>4. Annual Percentage rate of Charge (the “APRC”) – circumstances under which it can be amended</h5>
            4.1 The APRC specified in the Loan Offer means the total cost of the Loan to the Borrower expressed as an annual percentage of the total cost of the Loan on an annual basis equating to the present value of all commitments (loans, repayments and charges), future or existing agreed by the Credit Union and the Borrower concerned.<br/>
            <br/>
            4.2 The APRC is as stated in the Important Information in the Loan Offer and subject to change in accordance with the succeeding paragraph.<br/>
            <br/>
            4.3 The APRC may change from time to time subject to local market conditions, and, for example:<br/>
                a. If the interest rate changes between the date of the Loan Offer and the date of drawdown, or,<br/>
                b. If the drawdown date differs from the date of the APRC calculation, or,<br/>
                c. If the interval by which the interest is charged changes, or<br/>
                d. If the Borrower overpays the Loan Repayments or makes a capital reduction, thus reducing the Mortgage Balance.<br/><br/>
            4.4 The following assumptions were used when calculating the APRC:<br/>
                i. That the Loan Offer remains valid for the period set out in the Loan Offer as specified in the Important Information<br/>
                ii. That the Borrower and Credit Union will comply with the Loan terms and conditions for the Loan Term.<br/>
                iii. That the interest rate as set out in the Loan Offer will not change for the Loan Term.<br/>
                iv. That the Borrower will drawdown the full amount of the Loan in one instalment as soon as the Borrower is permitted to do so under the Loan Offer.<br/>
        </li>
        <br/>
        <li>
            <h5>5. Amortisation Table </h5>
            5.1 You have a right to receive on request and free of charge a statement of account in the form of an amortisation table. You may make this request at any time during the term of the Loan.<br/><br/>
            5.2 An amortisation table will assume that repayments will fall on a working day. If the due date for a repayment falls on a non-business day the figures in the amortisation table may vary as additional interest may accrue.<br/>
        </li>
        <br/>
        <li>
            <h5>6. The Mortgage </h5>
            6.1 Where the Loan Offer is extended to joint Borrowers, it is assumed that the title to or ownership of the property secured by the Mortgage will be in their joint names.  Where title is in the name of only one of the joint Borrowers, the spouse or civil partner of the Borrower on title, whether a legal owner or not, is required to be party to the Mortgage if the property is a shared home or a family home and in such cases, the Borrower not on title is required to execute both a Consent of Spouse/Civil Partner and a Deed of Confirmation and Postponements in such form as the Credit Union shall prescribe.<br/>
            <br/>
            6.2 As a condition precedent to the drawdown of the Loan and to secure its repayment, the Borrower shall grant a Mortgage to the Credit Union in respect of the property secured which will always rank ahead of all other creditors of the Borrower and ensure that the Credit Union is repaid ahead of such other creditors.</li>
        </li>
        <br/>
        <li>
            <h5>7. Occupation of the Property</h5>
            The Borrower must personally occupy the secured property unless otherwise agreed in writing by the Credit Union.
        </li>
        <br/>
        <li>
            <h5>8. Insurance of the Property</h5>
            The property must be fully insured with a comprehensive policy of insurance acceptable by the Credit Union either in the joint names of the Borrower and the Credit Union or otherwise noting the Credit Union’s interest and in either case, to the full reinstatement value.
        </li>
        <br/>
        <li>
            <h5>9. Insurance of the Property</h5>
            <h5>9.1 Life Assurance</h5>
            9.1.1 A Life Policy in the amount of the Loan and for the Loan term must be effected and assigned to the Credit Union.<br/>
            <br/>
            9.1.2 The Life Policy premiums will be payable directly by the Borrower to the life assurance company and payment of the premiums and maintenance of the life policy is the sole responsibility of the Borrower.<br/>
            <br/>
            9.1.3 Where the Borrower comprises two or more persons, the Credit Union requires life cover on the life of each Borrower unless otherwise specified in the Loan Offer.<br/>
            <br/>
            9.1.4 The life policy required under the Special Conditions of Offer must be sufficient to cover the Mortgage Balance from time to time based on the assumption that the terms of the Loan Offer have been complied with and noting that any extension of the Loan Term may give rise to a shortfall. However, the Borrower is responsible for any shortfall if the life cover is insufficient to repay the Loan.<br/><br/>
            <h5>9.2 Block Life Cover</h5>
            9.2.1 Where the Credit Union has chosen to acquire a block life policy in its favour, it may at its sole discretion renew its own block life policy annually.<br/>
            <br/>
            9.2.2 There is no insurance policy or contract in place with the Borrower, or for the Borrower, in respect of the Loan. The Credit Union is not obliged, as part of the Loan Offer to maintain its block life policy.<br/>
            <br/>
            9.2.3 At its discretion, the Credit Union may alter or cancel its block life cover. If notified by the Credit Union to do so, at any time during the term of this Loan, the Borrower may be required to ensure that a life insurance policy, which can fully repay the Mortgage Balance is taken out in the interest of the Credit Union.<br/>
            <br/>
            9.2.4 Where a block life policy is acquired by the Credit Union it will be contained in the Special Conditions of Offer. The Borrower should consider the special condition in full. The Borrower is not prevented from acquiring additional life cover for his own interest irrespective of the existence of a block life policy.<br/>
            <br/>
            9.2.5 For the avoidance of doubt, any arrangements made by the Credit Union in accordance with this clause 9.2 shall in no way relieve the Borrower of his or her obligations under clause 9.1.
        </li>
        <br/>
        <li>
            <h5>10. No Liability </h5>
            The Credit Union will not incur any liability in respect of the contents of the valuation report or structural survey required.
        </li>
        <br/>
        <li>
            <h5>11. Interpretation</h5>
            11.1 The singular includes the plural and vice versa and the masculine includes the feminine, common and neuter genders.<br/><br/>
            11.2 Obligations undertaken by more than one person are jointly and several obligations.<br/>
            <br/>
            11.3 Any reference to a specified statute includes any extensions, re-enactments or amendments to that statute or any regulations or order made thereunder and any general reference to “statute” or “statutes” includes any regulations made thereunder.<br/>
            <br/>
            11.4 In the event of any conflict between these general terms and conditions and the terms and conditions of the loan offer (and it’s special conditions), the Loan Offer shall prevail.
        </li>
        <br/>
        <li>
            <h5>12. Title Documents</h5>
            The Credit Union shall be entitled to retain custody of the title deeds until such time as all sums due under the terms of the Mortgage are discharged in full.
        </li>
        <br/>
        <li>
            <h5>13. Governing Law: Jurisdiction</h5>
            The Loan Offer and Acceptance shall be governed by and construed in accordance with the laws of Ireland. The Courts of Ireland shall have jurisdiction to hear any disputes arising in connection with the Loan Offer and Acceptance.
        </li>
    </ol>

</div>
"""

_logger = logging.getLogger(__name__)

#TODO: Check this classs
class format_address(object):
    @api.model
    def fields_view_get_address(self, arch):
        address_format = self.env.user.company_id.country_id.address_format or ''
        for format_pattern, format_class in ADDRESS_FORMAT_CLASSES.items():
            if format_pattern in address_format:
                doc = etree.fromstring(arch)
                for address_node in doc.xpath("//div[@class='o_address_format']"):
                    # add address format class to address block
                    address_node.attrib['class'] += ' ' + format_class
                    if format_class.startswith('o_zip'):
                        zip_fields = address_node.xpath("//field[@name='zip']")
                        city_fields = address_node.xpath("//field[@name='city']")
                        if zip_fields and city_fields:
                            # move zip field before city field
                            city_fields[0].addprevious(zip_fields[0])
                arch = etree.tostring(doc)
                break
        return arch


class Application(models.Model):
    _name = "application"
    _description = "Application"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _default_company_id(self):
        return self.env.user.company_id

    def _default_interest_rate_increase(self):
        company_id = self.env.user.company_id
        return float(company_id.interest_rate_increase)

    def _default_country_id(self):
        country = self.env["res.country"].search([('name', '=', "Ireland")], limit=1)
        return country.id

    def _default_red_image(self):
        img_path = get_module_resource("appsmod2", "static/img", "red.png")
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read())


    def _default_green_image(self):
        img_path = get_module_resource("appsmod2", "static/img", "green.png")
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read())

    name = fields.Char("Application Reference", readonly=True, tracking=True, copy=False, default=lambda self: _('New'))
    state = fields.Selection(STATE_SELECTION, "Status",readonly=True, tracking=True, default="draft", copy=False)
    original_assignee = fields.Many2one("res.users", "Indicator - Original Assignee", default=lambda self: self.env.user, copy=False)
    officer_category_id = fields.Integer("Indicator - External Assessor ID", compute="_compute_officer_category_id")
    senior_officer_category_id = fields.Integer("Indicator - Senior Officer Category ID", compute="_compute_senior_officer_category_id")
    field_mry_tab_check = fields.Boolean("Indicator - MRY Tab Visibility", compute="_compute_mry_tab_visibility") 
    field_paye_check = fields.Boolean("Indicator - PAYE Visibility", compute="_compute_pay_visibility")
    field_self_check = fields.Boolean("Indicator - Self Visibility", compute="_compute_self_visibility")

    # Column2
    assignee = fields.Many2one("res.users", "Assignee", copy=False, default=lambda self: self.env.user, tracking=True)
    external_assessor_user = fields.Many2one("res.users", "Indicator - External Assessor", copy=False)
    company_id = fields.Many2one("res.company", "Company", tracking=True, default=_default_company_id)

    # New code 2020
    mortgage_product_id = fields.Many2one("mortgage.product", "Mortgage Product", required=True, ondelete="restrict")
    mortgage_type = fields.Selection([
        ('variable_rate', "Variable Rate Mortgage"),
        ('fixed_variable_rate', "Fixed Rate Into Variable Mortgage")
    ], default="variable_rate", string="Mortgage Type", required=True)

    mortgrage_term_months = fields.Selection(MONTH_SELECTION, string="Mortgage Term Months", default='0', tracking=True, copy=False)
    mortgrage_term_year = fields.Char("Mortgage Term Years", tracking=True, copy=False)
    monthly_repayment = fields.Float("Monthly Repayment", digits=(16, 2),compute="_compute_repayment", store=True, copy=False, tracking=True)

    loan_to_value = fields.Float("Loan To Value %",compute="_compute_loan_to_value", store=True, tracking=True, copy=False)
    loan_to_income_ratio = fields.Float("Loan To Income Ratio",compute="_compute_loan_to_income_ratio", store=True, tracking=True, copy=False)
    mortgage_service_ratio = fields.Float("Mortgage Service Ratio %", compute="_compute_service_ratio", store=True, tracking=True, copy=False)
    total_debt_service_ratio = fields.Float("Total Debt Service Ratio %", compute="_compute_service_ratio", store=True, tracking=True, copy=False)

    net_disposable_inc = fields.Float("Net Disposable Income", compute="_compute_service_ratio", store=True, tracking=True, copy=False, help="Net Disposable Income")
    gift_to_deposit = fields.Float("Gift to Deposit %",compute="_compute_gift_to_deposit", store=True, tracking=True, copy=False, help="What percentage of deposit can come from Gift.")
    max_lend_facility = fields.Float("Max Lend Facility",compute="_compute_loan_to_income_ratio", store=True, tracking=True, copy=False, help="Maximum amount that can be lended based on given information.")

    # For Stress Test
    monthly_income_reduced = fields.Float("Monthly Income Reduced %",compute="_compute_monthly_income_reduced",store=True, tracking=True, copy=False, help="Monthly Income Reduced % (For Stress Test)")
    interest_rate_increase = fields.Float("Interest Rate Increase %", tracking=True, copy=False, default=_default_interest_rate_increase)
    stressed_income = fields.Float("Stressed Income",compute="_compute_stressed_income", store=True, tracking=True, copy=False)
    stressed_allowable_income = fields.Float("Stressed Allowable Income",compute="_compute_stressed_allowable_income", store=True, tracking=True, copy=False, help="Stressed Allowable Monthly Income")
    stressed_monthly_repayment = fields.Float("Stressed Monthly Repayment", compute="_compute_stressed_monthly_repayment", store=True, tracking=True, copy=False)
    stressed_mortgage_service_ratio = fields.Float("Stressed Mortgage Service Ratio", compute="_compute_stressed_service_ratio", store=True, tracking=True, copy=False)
    stressed_total_debt_service_ratio = fields.Float("Stressed Total Debt Service Ratio", compute="_compute_stressed_service_ratio", store=True, tracking=True, copy=False, help="Total Debt Service Ratio for Stress Test")
    stressed_net_disposable_income = fields.Float("Stressed Net Disposable Income", compute="_compute_stressed_service_ratio", store=True, tracking=True, copy=False)

    # Address fields
    street = fields.Char("Street", copy=False)
    street2 = fields.Char("Street2", copy=False)
    zip = fields.Char("EIRCODE", size=24, change_default=True, copy=False)
    city = fields.Char("City", copy=False)
    state_id = fields.Many2one("res.country.state", "County", ondelete="restrict")
    country_id = fields.Many2one("res.country", "Country", ondelete="restrict", default=_default_country_id)

    purpose_of_mortgage = fields.Selection(PURPOSE_OF_MORTGAGE, "Purpose Of Mortgage", default='moving', tracking=True)
    ber_rating = fields.Selection(BER_RATING, "BER Rating")
    ber_cert_no = fields.Char("BER Cert No.")
    mprn_no = fields.Char("MPRN No.")

    # ESIS fields
    esis_payment_frequency = fields.Selection(PAYMENT_FREQUENCY, "Payment Frequency", default="monthly", tracking=True, required=True)
    esis_weekly_repayment = fields.Float("Weekly Repayment", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_fortnightly_repayment = fields.Float("Fortnightly Repayment", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_no_of_repayment = fields.Integer("No. Of Repayments", compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_total_repaid = fields.Float("Total Repaid", digits=(16, 2), compute="_compute_total_repaid", store=True, tracking=True, copy=False)
    esis_cost_of_credit = fields.Float("Cost of Credit", digits=(16, 2), compute="_compute_total_repaid", store=True, tracking=True, copy=False)
    esis_cost_per_1 = fields.Float("Cost per €1", digits=(16, 2), compute="_compute_total_repaid", store=True, tracking=True, copy=False)
    esis_interest_rate = fields.Float("Interest Rate + 1%", digits="Interest Rates", compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_monthly_repayment_1 = fields.Float("Monthly Repayment + 1%", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_fortnightly_repayment_1 = fields.Float("Fortnightly Repayment + 1%", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_weekly_repayment_1 = fields.Float("Weekly Repayment + 1%", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False, help="Fortnightly Weekly + 1%")
    esis_monthly_repayment_2 = fields.Float("Monthly Repayment + 2%", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_fortnightly_repayment_2 = fields.Float("Fortnightly Repayment + 2%", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False)
    esis_weekly_repayment_2 = fields.Float("Weekly Repayment + 2%", digits=(16, 2), compute="_compute_repayment", store=True, tracking=True, copy=False, help="Fortnightly Weekly + 2%")
    esis_aprc = fields.Float("APRC", compute="_compute_aprc", store=True, tracking=True, copy=False, help="Annual Percentage Rate of Charge")
    esis_aprc_1 = fields.Float("APRC + 1%", compute="_compute_aprc", store=True, tracking=True, copy=False, help="Annual Percentage Rate of Charge + 1%")

    # Column 1
    first_time_buyer = fields.Selection(YES_NO, string="First Time Buyer", default="yes", tracking=True, copy=False)
    first_time_buyer_value = fields.Float("First Time Value", default=90.0, copy=False)
    single = fields.Selection(SINGLE, "Single/Couple", default="1300", copy=False, tracking=True)
    applicant_1 = fields.Many2one("res.partner", "Applicant 1", tracking=True, copy=False)
    applicant_1_age = fields.Char("Applicant 1 Age", compute="_compute_applicant_1_age", store=True, tracking=True, copy=False)
    applicant_1_age_end_of_term = fields.Char("Applicant 1 Age: End of Term", compute="_compute_applicant_age_end_of_term", store=True, tracking=True, copy=False)
    no_of_dependents = fields.Char("No of Dependents", tracking=True, copy=False)
    ndi_monthly = fields.Float("Required NDI Monthly", compute="_compute_ndi_monthly", store=True, tracking=True, copy=False)
    property_value = fields.Float("Property Value", digits=(16, 2), tracking=True, copy=False)
    mortgage_amount = fields.Float("Mortgage Amount", digits=(16, 2), tracking=True, copy=False)
    interest_rate = fields.Float("Interest Rate", digits="Interest Rates", tracking=True, copy=False)
    total_basic_income_1 = fields.Float("Applicant 1 Total Basic Income", tracking=True, copy=False)
    total_net_basic_income_1 = fields.Float("Applicant 1 Total Net Basic Income", tracking=True, copy=False)
    total_other_income_1 = fields.Float("Applicant 1 Total Other Net Income", tracking=True, copy=False)
    total_income = fields.Float("Total Net Income", compute="_compute_income", store=True, tracking=True, copy=False)
    self_employed_1 = fields.Selection(YES_NO, "Applicant 1 Self Employed?", default="no", tracking=True, copy=False)
    other_income_counted = fields.Float("% Of Other Income Counted", default=100, tracking=True, copy=False)
    nd2_income_counted = fields.Float("% Of 2nd Income Counted", default=100, tracking=True, copy=False)

    total_sustainable_income = fields.Float("Total Sustainable Income",compute="_compute_income", store=True, tracking=True, copy=False)
    allowable_monthly_income = fields.Float("Allowable Monthly Income",compute="_compute_income", store=True, tracking=True, copy=False)

    applicant_1_p60 = fields.Float("Applicant 1 P60 Income For Last Year", tracking=True, copy=False, help="P60 Income For Last Year")
    applicant_1_ann_pen = fields.Float("Applicant 1 Annual Pension Contribution", tracking=True, copy=False)
    applicant_1_exi_mor = fields.Float("Applicant 1 Existing Mortgage Commitments", tracking=True, copy=False)
    applicant_1_rental_income = fields.Float("Applicant 1 Rental Income", tracking=True, copy=False)
    debt_repay = fields.Float("Monthly Debt Repayments", tracking=True, copy=False)
    property_co = fields.Float("Future Property Costs", tracking=True, copy=False)
    maintenance = fields.Float("Maintenance", tracking=True, copy=False)
    childcare = fields.Float("Monthly Childcare Costs", tracking=True, copy=False)
    total_short_term = fields.Float("Total Short Term Debt",compute="_compute_total_short_term", store=True, tracking=True, copy=False)

    gifts_towards_deposit = fields.Selection(YES_NO, "Gifts Towards Deposit", tracking=True, default="no", copy=False)
    values_of_gifts = fields.Float("Values of Gifts", tracking=True, copy=False)
    gifts_letter_received = fields.Selection(YES_NO, "Gift Letter Received", default="yes", tracking=True, copy=False)
    contribution_to_valuation = fields.Float("Contribution to Valuation", tracking=True, copy=False)
    contribution_to_revaluation = fields.Float("Contribution to Revaluation", tracking=True, copy=False)
    once_off_costs = fields.Float("Other Once Off Costs", tracking=True, copy=False)
    applicant_1_eu_citizen = fields.Selection(YES_NO, "Applicant 1 EU Citizen", default="yes", copy=False)
    applicant_1_credit_risk = fields.Selection(YES_NO, "Applicant 1 Are Credit Checks Acceptable?", default="yes", tracking=True, copy=False, help="Is Credit Risk Acceptable?")
    
    # Column 3
    date_of_offer = fields.Date("Date of Offer")
    date_of_offer_plus_1 = fields.Date("Date of Offer + 1", help="Date of Offer")
    date_of_offer_plus_2 = fields.Date("Date of Offer + 2", help="Date Of Offer")

    applicant_2 = fields.Many2one("res.partner", "Applicant 2", tracking=True, copy=False)
    applicant_2_age = fields.Char("Applicant 2 Age", compute="_compute_applicant_2_age", store=True, tracking=True, copy=False)
    applicant_2_age_end_of_term = fields.Char("Applicant 2 Age: End of Term", compute="_compute_applicant_age_end_of_term", store=True, tracking=True, copy=False)
    total_basic_income_2 = fields.Float("Applicant 2 Total Basic Income", tracking=True, copy=False, help="Total Basic Income of Applicant 2")
    total_net_basic_income_2 = fields.Float("Applicant 2 Total Net Basic Income", tracking=True, copy=False)
    total_other_income_2 = fields.Float("Applicant 2 Total Other Net Income", tracking=True, copy=False)
    self_employed_2 = fields.Selection(YES_NO, default="no", string="Applicant 2 Self Employed?", tracking=True, copy=False)
    applicant_2_p60 = fields.Float("Applicant 2 P60 Income For Last Year", tracking=True, copy=False, help="P60 Income For Last Year")
    applicant_2_ann_pen = fields.Float("Applicant 2 Annual Pension Contribution", tracking=True, copy=False)
    applicant_2_exi_mor = fields.Float("Applicant 2 Existing Mortgage Commitments", tracking=True, copy=False)
    applicant_2_rental_income = fields.Float("Applicant 2 Rental Income", tracking=True, copy=False)
    applicant_2_eu_citizen = fields.Selection(YES_NO, default="yes", string="Applicant 2 EU Citizen", tracking=True, copy=False)
    applicant_2_credit_risk = fields.Selection(YES_NO, default="yes", string="Applicant 2 Are Credit Checks Acceptable?", help="Is Credit Risk Acceptable?")

    # Duration of fixed rate term as per product
    term_at_starting_rate = fields.Integer("Term At Starting Rate", tracking=True, copy=False)
    fixed_interest_rate = fields.Float("Fixed Interest Rate", digits="Interest Rates", tracking=True, copy=False)
    fixed_term_payment = fields.Float("Fixed Term Payment",compute="_compute_term_repayment", store=True, tracking=True, copy=False)
    repayment_at_variable = fields.Float("Repayment at Variable",compute="_compute_term_repayment", store=True, tracking=True, copy=False)
    repayment_at_variable_plus1 = fields.Float("Repayment at Variable + 1%", compute="_compute_term_repayment", store=True, tracking=True, copy=False)
    repayment_at_variable_plus2 = fields.Float("Repayment at Variable + 2%", compute="_compute_term_repayment", store=True, tracking=True, copy=False)
    max_possible_repayment = fields.Float("Max Possible Repayment", compute="_compute_term_repayment", store=True, tracking=True, copy=False)
    avg_repayment = fields.Float("Average Repayment", compute="_compute_total_repaid", store=True, tracking=True, copy=False)
    avg_rate = fields.Float("Average Rate", digits="Interest Rates", compute="_compute_total_repaid", store=True, tracking=True, copy=False)
    avg_repayment_plus1 = fields.Float("Average Repayment + 1%", compute="_compute_total_repaid", store=True, tracking=True, copy=False)
    is_old_application = fields.Boolean("Old Application", copy=False)

    # Assessment 
    character_demonstrated = fields.Selection(YES_NO, default='no', string="Applicant 1 Is Character Demonstrated?", tracking=True, copy=False, help="- Credit Checks in order\n- All Financial Commitments met\n- Explanation for all DDs and SOs\n- No erratic pattern in statements\n- No unusual movements in accounts")
    affordablity_established = fields.Selection(YES_NO, default="no", string="Applicant 1 Is Affordability Established?", tracking=True, copy=False, help="- Income and Expenditure an in application\n- Assessed Finances within policy limits\n- Impending change in circumstances ( eg. child care costs?)")
    secure_employment = fields.Selection(YES_NO, default="no", string="Applicant 1 Secure Employment?", tracking=True, copy=False, help="- Permanency of Employment\n- Low risk sector or skills transferable to another sector\n- Established Employer")
    certified_value = fields.Selection(YES_NO, default="no", string="Do you have a certified value of property?", tracking=True, copy=False)
    certified_property_value = fields.Float("What is the certified value of property?", digits=(16, 2), tracking=True, copy=False)

    character_demonstrated_applicant_2 = fields.Selection(YES_NO, default='no', string="Applicant 2 Is Character Demonstrated?", tracking=True, copy=False, help="- Credit Checks in order\n- All Financial Commitments met\n- Explanation for all DDs and SOs\n- No erratic pattern in statements\n- No unusual movements in accounts")
    affordablity_established_applicant_2 = fields.Selection(YES_NO, default="no", string="Applicant 2 Is Affordability Established?", tracking=True, copy=False, help="- Income and Expenditure an in application\n- Assessed Finances within policy limits\n- Impending change in circumstances ( eg. child care costs?)")
    secure_employment_applicant_2 = fields.Selection(YES_NO, default="no", string="Applicant 2 Secure Employment?", tracking=True, copy=False, help="- Permanency of Employment\n- Low risk sector or skills transferable to another sector\n- Established Employer")

    # Decline Letter Text 
    decline_message = fields.Text("Declination Message", copy=False)
    decline_reason = fields.Char("Declination Reason", copy=False)

    # Cover Note Tab 
    body_html = fields.Text("Cover Note", copy=False)

    # Special Conditions Tab 
    body_special_conditions = fields.Text("Special Conditions", copy=False)
    user_needs_general_conditions = fields.Boolean("Attach SAM General Terms & Conditions to Letter of Offer?", copy=False)
    general_terms_and_conditions = fields.Text("SAM General Terms and Conditions")

    # Documents Tab 
    documents_uniquely_applicable_line = fields.One2many("documents.uniquely.applicable", "application_id", "Documents Uniquely Applicable")
    documents_applicable_applicant1_line = fields.One2many("documents.applicable.applicant", "application_id", "Applicant 1 Documents", domain=lambda self:[('applicant_type', '=', 'applicant1')])
    documents_applicable_applicant2_line = fields.One2many("documents.applicable.applicant", "application_id", "Applicant 2 Documents", domain=lambda self:[('applicant_type', '=', 'applicant2')])


    # Checklist Tab 
    jointly_applicable_line = fields.One2many("jointly.applicable", "application_id", "Jointly Applicable")

   

    checklist_applicable_applicant_line1 = fields.One2many("checklist.applicable.applicant", "application_id", "Applicant Checklist", domain=lambda self:[('applicant_type', '=', 'applicant1'),('type', '=', 'individual')])
    checklist_applicable_applicant_line2 = fields.One2many("checklist.applicable.applicant", "application_id", "Applicant Checklist", domain=lambda self:[('applicant_type', '=', 'applicant2'),('type', '=', 'individual')])
   


    checklist_self_applicable_applicant_line1 = fields.One2many("checklist.applicable.applicant", "application_id", "Applicant 1 Checklist Self",domain=lambda self:[('applicant_type', '=', 'applicant1'),('type', '=', 'self')])
    checklist_self_applicable_applicant_line2 = fields.One2many("checklist.applicable.applicant", "application_id", "Applicant 1 Checklist Self",domain=lambda self:[('applicant_type', '=', 'applicant2'),('type', '=', 'self')])
 
    checklist_paye_applicable_applicant_line1 = fields.One2many("checklist.applicable.applicant", "application_id", "Applicant 1 Checklist Paye",domain=lambda self:[('applicant_type', '=', 'applicant1'),('type', '=', 'paye')])
    checklist_paye_applicable_applicant_line2 = fields.One2many("checklist.applicable.applicant", "application_id", "Applicant 1 Checklist Paye",domain=lambda self:[('applicant_type', '=', 'applicant2'),('type', '=', 'paye')])
   
    # MRY Tab 
    applicant_1_net_profit_1 = fields.Float("Applicant 1 Net Profit - MRY", tracking=True, copy=False, help="Net Profit")
    applicant_1_net_profit_2 = fields.Float("Applicant 1 Net Profit - MRY 1", tracking=True, copy=False, help="Net Profit")
    applicant_1_net_profit_3 = fields.Float("Applicant 1 Net Profit - MRY 2", tracking=True, copy=False, help="Net Profit")

    applicant_1_plus_depreceation_1 = fields.Float("Applicant 1 Plus Depreciation - MRY", tracking=True, copy=False, help="Plus Depreciation")
    applicant_1_plus_depreceation_2 = fields.Float("Applicant 1 Plus Depreciation - MRY 1", tracking=True, copy=False, help="Plus Depreciation")
    applicant_1_plus_depreceation_3 = fields.Float("Applicant 1 Plus Depreciation - MRY 2", tracking=True, copy=False, help="Plus Depreciation")

    applicant_1_plus_interest_paid_1 = fields.Float("Applicant 1 Plus Interest Paid - MRY", tracking=True, copy=False, help="Plus Interest Paid")
    applicant_1_plus_interest_paid_2 = fields.Float("Applicant 1 Plus Interest Paid - MRY 1", tracking=True, copy=False, help="Plus Interest Paid")
    applicant_1_plus_interest_paid_3 = fields.Float("Applicant 1 Plus Interest Paid - MRY 2", tracking=True, copy=False, help="Plus Interest Paid")

    applicant_1_plus_remuneration_1 = fields.Float("Applicant 1 Plus Remuneration - MRY", tracking=True, copy=False, help="Plus Renumeration")
    applicant_1_plus_remuneration_2 = fields.Float("Applicant 1 Plus Remuneration - MRY 1", tracking=True, copy=False, help="Plus Renumeration")
    applicant_1_plus_remuneration_3 = fields.Float("Applicant 1 Plus Remuneration - MRY 2", tracking=True, copy=False, help="Plus Renumeration")

    applicant_1_plus_pension_1 = fields.Float("Applicant 1 Plus Pension - MRY", tracking=True, copy=False, help="Plus Pension")
    applicant_1_plus_pension_2 = fields.Float("Applicant 1 Plus Pension - MRY 1", tracking=True, copy=False, help="Plus Pension")
    applicant_1_plus_pension_3 = fields.Float("Applicant 1 Plus Pension - MRY 2", tracking=True, copy=False, help="Plus Pension")

    applicant_1_trading_profit_1 = fields.Float("Applicant 1 Trading Profit - MRY", compute="_compute_mry", store=True, tracking=True, copy=False, help="Trading Profit")
    applicant_1_trading_profit_2 = fields.Float("Applicant 1 Trading Profit - MRY 2", compute="_compute_mry_1", store=True, tracking=True, copy=False, help="Trading Profit")
    applicant_1_trading_profit_3 = fields.Float("Applicant 1 Trading Profit - MRY 3", compute="_compute_mry_2", store=True, tracking=True, copy=False, help="Trading Profit")

    applicant_1_average_trading_profit = fields.Float("Applicant 1 Average Trading Profit", compute="_compute_avg_trading_profit_1", store=True, tracking=True, copy=False, help="Average Trading Profit")
    applicant_1_less_business_repayments = fields.Float("Applicant 1 Less Business Repayments", tracking=True, copy=False, help="Less Business Repayments")
    applicant_1_surplus = fields.Float("Applicant 1 Surplus", compute="_compute_surplus_1", store=True, tracking=True, copy=False, help="Surplus")

    applicant_1_notice_1 = fields.Float("Applicant 1 Notice of Assessment - MRY", tracking=True, copy=False, help="Notice of Assessment")
    applicant_1_notice_2 = fields.Float("Applicant 1 Notice of Assessment - MRY 1", tracking=True, copy=False, help="Notice of Assessment")
    applicant_1_notice_3 = fields.Float("Applicant 1 Notice of Assessment - MRY 3", tracking=True, copy=False, help="Notice of Assessment")

    applicant_2_net_profit_1 = fields.Float("Applicant 2 Net Profit - MRY", tracking=True, copy=False, help="Net Profit")
    applicant_2_net_profit_2 = fields.Float("Applicant 2 Net Profit - MRY 1", tracking=True, copy=False, help="Net Profit")
    applicant_2_net_profit_3 = fields.Float("Applicant 2 Net Profit - MRY 2", tracking=True, copy=False, help="Net Profit")

    applicant_2_plus_depreceation_1 = fields.Float("Applicant 2 Plus Depreciation - MRY", tracking=True, copy=False, help="Plus Depreciation")
    applicant_2_plus_depreceation_2 = fields.Float("Applicant 2 Plus Depreciation - MRY 1", tracking=True, copy=False, help="Plus Depreciation")
    applicant_2_plus_depreceation_3 = fields.Float("Applicant 2 Plus Depreciation - MRY 2", tracking=True, copy=False, help="Plus Depreciation")

    applicant_2_plus_interest_paid_1 = fields.Float("Applicant 2 Plus Interest Paid - MRY", tracking=True, copy=False, help="Plus Interest Paid")
    applicant_2_plus_interest_paid_2 = fields.Float("Applicant 2 Plus Interest Paid - MRY 1", tracking=True, copy=False, help="Plus Interest Paid")
    applicant_2_plus_interest_paid_3 = fields.Float("Applicant 2 Plus Interest Paid - MRY 2", tracking=True, copy=False, help="Plus Interest Paid")

    applicant_2_plus_remuneration_1 = fields.Float("Applicant 2 Plus Remuneration - MRY", tracking=True, copy=False, help="Plus Renumeration")
    applicant_2_plus_remuneration_2 = fields.Float("Applicant 2 Plus Remuneration - MRY 1", tracking=True, copy=False, help="Plus Renumeration")
    applicant_2_plus_remuneration_3 = fields.Float("Applicant 2 Plus Remuneration - MRY 2", tracking=True, copy=False, help="Plus Renumeration")

    applicant_2_plus_pension_1 = fields.Float("Applicant 2 Plus Pension - MRY", tracking=True, copy=False, help="Plus Pension")
    applicant_2_plus_pension_2 = fields.Float("Applicant 2 Plus Pension - MRY 1", tracking=True, copy=False, help="Plus Pension")
    applicant_2_plus_pension_3 = fields.Float("Applicant 2 Plus Pension - MRY 2", tracking=True, copy=False, help="Plus Pension")

    applicant_2_trading_profit_1 = fields.Float("Applicant 2 Trading Profit - MRY", compute="_compute_mry2", store=True, tracking=True, copy=False, help="Trading Profit")
    applicant_2_trading_profit_2 = fields.Float("Applicant 2 Trading Profit - MRY 2", compute="_compute_mry2_1", store=True, tracking=True, copy=False, help="Trading Profit")
    applicant_2_trading_profit_3 = fields.Float("Applicant 2 Trading Profit - MRY 3", compute="_compute_mry2_2", store=True, tracking=True, copy=False, help="Trading Profit")

    applicant_2_average_trading_profit = fields.Float("Applicant 2 Average Trading Profit", compute="_compute_avg_trading_profit_2", store=True, tracking=True, copy=False, help="Average Trading Profit")
    applicant_2_less_business_repayments = fields.Float("Applicant 2 Less Business Repayments", tracking=True, copy=False, help="Less Business Repayments")
    applicant_2_surplus = fields.Float("Applicant 2 Surplus", compute="_compute_surplus_2", store=True, tracking=True, copy=False, help="Surplus")

    applicant_2_notice_1 = fields.Float("Applicant 2 Notice of Assessment - MRY", tracking=True, copy=False, help="Notice of Assessment")
    applicant_2_notice_2 = fields.Float("Applicant 2 Notice of Assessment - MRY 1", tracking=True, copy=False, help="Notice of Assessment")
    applicant_2_notice_3 = fields.Float("Applicant 2 Notice of Assessment - MRY 3", tracking=True, copy=False, help="Notice of Assessment")


    # Indicators to show tabs
    hide_load_checklist = fields.Boolean("Indicator - Hide Checklist", copy=False)
    show_checklist = fields.Boolean("Indicator - Show Checklist", copy=False)
    show_cover_note = fields.Boolean("Indicator - Show Cover Note", copy=False)
    show_special = fields.Boolean("Indicator - Show Speical Conditions", copy=False)
    show_assessment = fields.Boolean("Indicator - Show Assessment", copy=False)

    image_red_1 = fields.Binary("Red Image 1", readonly=True, default=_default_red_image, attachment=False)
    image_red_2 = fields.Binary("Red Image 2", readonly=True, default=_default_red_image, attachment=False)
    image_red_3 = fields.Binary("Red Image 3", readonly=True, default=_default_red_image, attachment=False)
    image_red_4 = fields.Binary("Red Image 4", readonly=True, default=_default_red_image, attachment=False)
    image_red_5 = fields.Binary("Red Image 5", readonly=True, default=_default_red_image, attachment=False)
    image_red_8 = fields.Binary("Red Image 8", readonly=True, default=_default_red_image, attachment=False)
    image_red_9 = fields.Binary("Red Image 9", readonly=True, default=_default_red_image, attachment=False)

    image_green_1 = fields.Binary("Green Image 1", readonly=True, default=_default_green_image, attachment=False)
    image_green_2 = fields.Binary("Green Image 2", readonly=True, default=_default_green_image, attachment=False)
    image_green_3 = fields.Binary("Green Image 3", readonly=True, default=_default_green_image, attachment=False)
    image_green_4 = fields.Binary("Green Image 4", readonly=True, default=_default_green_image, attachment=False)
    image_green_5 = fields.Binary("Green Image 5", readonly=True, default=_default_green_image, attachment=False)
    image_green_8 = fields.Binary("Green Image 8", readonly=True, default=_default_green_image, attachment=False)
    image_green_9 = fields.Binary("Green Image 9", readonly=True, default=_default_green_image, attachment=False)

    show_image_1 = fields.Boolean("Image Visibility 1", copy=False)
    show_image_2 = fields.Boolean("Image Visibility 2", copy=False)
    show_image_3 = fields.Boolean("Image Visibility 3", copy=False)
    show_image_4 = fields.Boolean("Image Visibility 4", copy=False)
    show_image_5 = fields.Boolean("Image Visibility 5", copy=False)
    show_image_8 = fields.Boolean("Image Visibility 8", copy=False)
    show_image_9 = fields.Boolean("Image Visibility 9", copy=False)


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env["ir.sequence"].with_company(vals.get("company_id")).next_by_code("application.number") or _("New")
        if 'checklist_applicable_applicant_line1' in vals:
            for applicant in vals['checklist_applicable_applicant_line1']:
                applicant[2]['applicant_type'] = 'applicant1'
                applicant[2]['type'] = 'individual'
        
        if 'checklist_applicable_applicant_line2' in vals:
            for applicant in vals['checklist_applicable_applicant_line2']:
                applicant[2]['applicant_type'] = 'applicant2'
                applicant[2]['type'] = 'individual'


        if 'checklist_self_applicable_applicant_line1' in vals:
            for applicant in vals['checklist_self_applicable_applicant_line1']:
                applicant[2]['applicant_type'] = 'applicant1'
                applicant[2]['type'] = 'self'
        
        if 'checklist_self_applicable_applicant_line2' in vals:
            for applicant in vals['checklist_self_applicable_applicant_line2']:
                applicant[2]['applicant_type'] = 'applicant2'
                applicant[2]['type'] = 'self'


        if 'checklist_paye_applicable_applicant_line1' in vals:
            for applicant in vals['checklist_paye_applicable_applicant_line1']:
                applicant[2]['applicant_type'] = 'applicant1'
                applicant[2]['type'] = 'paye'
        
        if 'checklist_paye_applicable_applicant_line2' in vals:
            for applicant in vals['checklist_paye_applicable_applicant_line2']:
                applicant[2]['applicant_type'] = 'applicant2'
                applicant[2]['type'] = 'paye'

        if 'documents_applicable_applicant1_line' in vals:
            for applicant in vals['documents_applicable_applicant1_line']:
                applicant[2]['applicant_type'] = 'applicant1'
        
        if 'documents_applicable_applicant2_line' in vals:
            for applicant in vals['documents_applicable_applicant2_line']:
                applicant[2]['applicant_type'] = 'applicant2'
                
        return super(Application, self).create(vals)

    def _compute_officer_category_id(self):
        for application in self:
            application.officer_category_id = self.env.ref("appsmod2.group_appsmod2_external_user").id

    def _compute_senior_officer_category_id(self):
        for application in self:
            application.senior_officer_category_id = self.env.ref("appsmod2.group_appsmod2_loan_officer").id

    @api.depends("self_employed_1", "self_employed_2")
    def _compute_mry_tab_visibility(self):
        for application in self:
            if application.self_employed_1 and application.self_employed_2:
                if application.self_employed_1 == 'no' and application.self_employed_2 == 'no':
                    application.field_mry_tab_check = False
                else:
                    application.field_mry_tab_check = True
            else:
                if application.self_employed_1 and application.self_employed_1 == 'no':
                    application.field_mry_tab_check = False
                else:
                    application.field_mry_tab_check = True

    @api.depends("self_employed_1", "self_employed_2")
    def _compute_pay_visibility(self):
        for application in self:
            application.field_paye_check = application.self_employed_1 == "no" or (application.applicant_2 and application.self_employed_2 == "no")

    @api.depends("self_employed_1", "self_employed_2")
    def _compute_self_visibility(self):
        for application in self:
            application.field_self_check = application.self_employed_1 == "yes" or (application.applicant_2 and application.self_employed_2 == "yes")


    @api.depends("applicant_1")
    def _compute_applicant_1_age(self):
        for application in self:
            if application.applicant_1:
                if application.applicant_1.DOB:
                    application.applicant_1_age = self._calculate_age(application.applicant_1.DOB)
                else:
                    raise UserError(_("Please maintain Date Of Birth for Applicant."))

    @api.depends("applicant_2")
    def _compute_applicant_2_age(self):
        for application in self:
            if application.applicant_2:
                if application.applicant_2.DOB:
                    application.applicant_2_age = self._calculate_age(application.applicant_2.DOB)
                else:
                    raise UserError(_("Please maintain Date of Birth for Applicant 2."))

    @api.depends("applicant_1_age", "applicant_2_age", "mortgrage_term_year", "mortgrage_term_months")
    def _compute_applicant_age_end_of_term(self):
        for application in self:
            if application.applicant_1_age:
                application.applicant_1_age_end_of_term = self._calculate_age_end_of_term(application.applicant_1_age, int(application.mortgrage_term_year or 0), application.mortgrage_term_months)
            if application.applicant_2_age:
                application.applicant_2_age_end_of_term = self._calculate_age_end_of_term(application.applicant_2_age, int(application.mortgrage_term_year or 0), application.mortgrage_term_months)

    def _calculate_age_end_of_term(self, age, mortgage_years, mortgage_months):
        end_of_term_age = int(age)
        years = 0
        months = 0
        if mortgage_years:
            years += mortgage_years
        if int(mortgage_months):
            if int(mortgage_months) == 12:
                years += 1
            else:
                months = int(mortgage_months)
        end_of_term_age = f"{end_of_term_age + years} years"
        if months:
            end_of_term_age += f" {months} months"

        return end_of_term_age

    def _calculate_age(self, dob):
        today = fields.Date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @api.depends("total_net_basic_income_1", "total_other_income_1", "total_net_basic_income_2", "total_other_income_2", "other_income_counted", "nd2_income_counted")
    def _compute_income(self):
        """
            compute and assign total_income, total_sustainable_income, and allowable_monthly_income.
        """
        for application in self:
            total_net_basic_income_1 = int(application.total_net_basic_income_1 or 0)
            total_other_income_1 = int(application.total_other_income_1 or 0)
            total_net_basic_income_2 = int(application.total_net_basic_income_2 or 0)
            total_other_income_2 = int(application.total_other_income_2 or 0)
            other_income_counted = int(application.other_income_counted or 0)
            second_income_counted = int(application.nd2_income_counted or 0)

            application.total_income = total_net_basic_income_1 + total_other_income_1 + total_net_basic_income_2 + total_other_income_2
            application.total_sustainable_income = total_net_basic_income_1 + total_other_income_1 * (other_income_counted/100) + total_net_basic_income_2 * (second_income_counted/100) + total_other_income_2 * (other_income_counted/100)
            application.allowable_monthly_income = round(application.total_sustainable_income / 12, 2)

    @api.depends("property_value", "mortgage_amount", "first_time_buyer")
    def _compute_loan_to_value(self):
        """
            compute and assign loan_to_value ratio.
        """
        for application in self:
            if application.property_value:
                application.loan_to_value = round((application.mortgage_amount / application.property_value) * 100, 2)
            else:
                application.loan_to_value = 0.0

            if application.loan_to_value:
                if application.company_id and application.company_id.ltv:
                    application.show_image_1 = application.loan_to_value < application.company_id.ltv
                else:
                    if application.first_time_buyer == "yes":
                        application.show_image_1 = application.loan_to_value <= 90
                    else:
                        application.show_image_1 = application.loan_to_value <= 80
            else:
                application.show_image_1 = False

    @api.depends("total_basic_income_1", "total_basic_income_2", "mortgage_amount", "first_time_buyer")
    def _compute_loan_to_income_ratio(self):
        """
            compute and assign loan_to_income_ratio and max_lend_facility
        """
        for application in self:
            total_basic_income_1 = float(application.total_basic_income_1 or 0)
            total_basic_income_2 = float(application.total_basic_income_2 or 0)

            if application.first_time_buyer == 'yes':
                application.first_time_buyer_value = 4
            else:
                application.first_time_buyer_value = 3.5

            max_lend_facility = total_basic_income_1 + total_basic_income_2
            application.max_lend_facility = max_lend_facility * application.first_time_buyer_value

            if max_lend_facility:
                application.loan_to_income_ratio = round(application.mortgage_amount / max_lend_facility, 2)

                if application.company_id.lti:
                    application.show_image_2 = application.loan_to_income_ratio < application.company_id.lti
                else:
                    application.show_image_2 = application.loan_to_income_ratio <= application.first_time_buyer_value

    @api.depends("company_id")
    def _compute_monthly_income_reduced(self):
        for application in self:
            application.monthly_income_reduced = application.company_id.monthly_income_reduced

    @api.depends("total_income", "monthly_income_reduced")    
    def _compute_stressed_income(self):
        for application in self:
            application.stressed_income = float(application.total_income - ((application.total_income / 100) * application.monthly_income_reduced))

    @api.depends("allowable_monthly_income", "monthly_income_reduced")
    def _compute_stressed_allowable_income(self):
        for application in self:
            application.stressed_allowable_income = float(application.allowable_monthly_income - ((application.allowable_monthly_income / 100) * application.monthly_income_reduced))

    @api.onchange('mortgage_product_id')
    def onchange_mortgage_product_id(self):
        # new code 2020
        self.ensure_one()
        if self.mortgage_product_id:
            self.interest_rate = self.mortgage_product_id.variable_interest_rate
            self.term_at_starting_rate = self.mortgage_product_id.fixed_term
            self.fixed_interest_rate = self.mortgage_product_id.fixed_interest_rate
            self.mortgage_type = self.mortgage_product_id.mortgage_type

    @api.depends("single", "no_of_dependents")
    def _compute_ndi_monthly(self):
        for application in self:
            ndi_monthly = 0
            if application.single:
                ndi_monthly += int(application.single)
            if application.no_of_dependents:
                ndi_monthly += (int(application.no_of_dependents) * 250)

            application.ndi_monthly = ndi_monthly

    @api.depends("values_of_gifts", "property_value", "mortgage_amount")
    def _compute_gift_to_deposit(self):
        for application in self:
            difference = float(application.property_value - application.mortgage_amount)
            if int(difference):
                application.gift_to_deposit = (application.values_of_gifts / difference) * 100

            if application.company_id.gift_to_deposit:
                application.show_image_5 = application.gift_to_deposit < application.company_id.gift_to_deposit
            else:
                application.show_image_5 = application.gift_to_deposit < STANDARD_GIFT_TO_DEPOSIT

    def _calculate_number_of_repayments(self):
        """
        Based on repayment frequency, returns total numbers of repayments for given loan term
        """
        self.ensure_one()
        total_years = int(self.mortgrage_term_year or 0) + (int(self.mortgrage_term_months) / 12)
        number_of_repayments = 0
        if self.esis_payment_frequency == "monthly":
            number_of_repayments = math.trunc(total_years * 12)
        elif self.esis_payment_frequency == "weekly":
            number_of_repayments = math.trunc(total_years * 52)
        elif self.esis_payment_frequency == "fortnightly":
            number_of_repayments = math.trunc(total_years * 26)
        else:
            raise UserError(_("Unsupported repayment frequency"))
        return number_of_repayments

    def _compute_repayment_amount(self, mortgage_amount, interest_rate, number_of_repayments, repayment_frequency):
        """
        compute repayment amount for weekly, fortnighly and monthly repayments, based on interest rate, amount and loan term.
        """

        self.ensure_one()
        _logger.info(f"\n==>_compute_repayment_amount interest_rate: {interest_rate}")
        return round(-1 * (npf.pmt((interest_rate / 100) / repayment_frequency, number_of_repayments, mortgage_amount)), 3)


    @api.depends("interest_rate", "mortgage_amount", "mortgrage_term_year", "mortgrage_term_months", "esis_payment_frequency")
    def _compute_repayment(self):
        """
        Compute Monthly Repayment from given mortgage_amount and interest rate.

        Parameters:
            interest_rate: Rate of Interst
            mortgage_amount: Principal Amount
            mortgrage_term_year: Duration of mortgage in years
            mortgrage_term_months: Duration of mortgrage in months(if any)
            esis_payment_frequency: Frequency of repayment
        """
        for application in self:
            application.monthly_repayment = 0.0
            application.esis_monthly_repayment_1 = 0.0
            application.esis_monthly_repayment_2 = 0.0
            application.esis_weekly_repayment = 0.0
            application.esis_weekly_repayment_1 = 0.0
            application.esis_weekly_repayment_2 = 0.0
            application.esis_fortnightly_repayment = 0.0
            application.esis_fortnightly_repayment_1 = 0.0
            application.esis_fortnightly_repayment_2 = 0.0
            application.esis_no_of_repayment = 0
            application.esis_interest_rate = application.interest_rate + 1
            _logger.info(f"\n==>_compute_repayment application: {application.name} ==>interest rate: {application.interest_rate} ==>esis_interest_rate: {application.esis_interest_rate}")

            # calculate number of repayments for weekly, fortnightly, and monthly repayments 
            term_in_years = int(application.mortgrage_term_year or 0) + (int(application.mortgrage_term_months) / 12)
            monthly_repayments_term = math.trunc(term_in_years * 12)
            weekly_repayments_term = math.trunc(term_in_years * 52)
            fortnightly_repayments_term = math.trunc(term_in_years * 26)
            _logger.info(f"\n==>term_in_years: {term_in_years}\n==>monthly_repayments_term: {monthly_repayments_term}\n==>weekly_repayments_term: {weekly_repayments_term}\n==>fortnightly_repayments_term: {fortnightly_repayments_term}")

            if application.interest_rate and monthly_repayments_term:
                # Compute monthly repayments
                application.monthly_repayment = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate, monthly_repayments_term, 12)
                application.esis_monthly_repayment_1 = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate + 1, monthly_repayments_term, 12)
                application.esis_monthly_repayment_2 = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate + 2, monthly_repayments_term, 12)

            if application.interest_rate and weekly_repayments_term:
                # for fixed to variable interest rate, we have to calculate fixed repayment amount and separtely and then calculate remaining loan amount after fixed term
                if application.mortgage_type == "fixed_variable_rate":
                    fixed_rate_terms = application.term_at_starting_rate * 52
                    outstanding_balance = self.calculate_outstanding_balance(application.fixed_interest_rate, weekly_repayments_term, application.mortgage_amount, fixed_rate_terms)
                    variable_rate_terms = weekly_repayments_term - fixed_rate_terms
                    outstanding_loan_amount = outstanding_balance.get("outstanding_amount", 0.0)
                    application.esis_weekly_repayment = self._compute_repayment_amount(outstanding_loan_amount, application.interest_rate, variable_rate_terms, 52)
                    application.esis_weekly_repayment_1 = self._compute_repayment_amount(outstanding_loan_amount, application.interest_rate + 1, variable_rate_terms, 52)
                    application.esis_weekly_repayment_2 = self._compute_repayment_amount(outstanding_loan_amount, application.interest_rate + 2, variable_rate_terms, 52)
                else:
                    application.esis_weekly_repayment = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate, weekly_repayments_term, 52)
                    application.esis_weekly_repayment_1 = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate + 1, weekly_repayments_term, 52)
                    application.esis_weekly_repayment_2 = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate + 2, weekly_repayments_term, 52)

            if application.interest_rate and fortnightly_repayments_term:
                # for fixed to variable interest rate, we have to calculate fixed repayment amount and separtely and then calculate remaining loan amount after fixed term
                if application.mortgage_type == "fixed_variable_rate":
                    fixed_rate_terms = application.term_at_starting_rate * 26
                    outstanding_balance = self.calculate_outstanding_balance(application.fixed_interest_rate, fortnightly_repayments_term, application.mortgage_amount, fixed_rate_terms)
                    variable_rate_terms = fortnightly_repayments_term - fixed_rate_terms
                    outstanding_loan_amount = outstanding_balance.get("outstanding_amount", 0.0)
                    application.esis_fortnightly_repayment = self._compute_repayment_amount(outstanding_loan_amount, application.interest_rate, variable_rate_terms, 26)
                    application.esis_fortnightly_repayment_1 = self._compute_repayment_amount(outstanding_loan_amount, application.interest_rate + 1, variable_rate_terms, 26)
                    application.esis_fortnightly_repayment_2 = self._compute_repayment_amount(outstanding_loan_amount, application.interest_rate + 2, variable_rate_terms, 26)
                else:
                    application.esis_fortnightly_repayment = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate, fortnightly_repayments_term, 26)
                    application.esis_fortnightly_repayment_1 = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate + 1, fortnightly_repayments_term, 26)
                    application.esis_fortnightly_repayment_2 = self._compute_repayment_amount(application.mortgage_amount, application.interest_rate + 2, fortnightly_repayments_term, 26)

            if application.esis_payment_frequency == "weekly":
                application.esis_no_of_repayment = weekly_repayments_term
            elif application.esis_payment_frequency == "fortnightly":
                application.esis_no_of_repayment = fortnightly_repayments_term
            elif application.esis_payment_frequency == "monthly":
                application.esis_no_of_repayment = monthly_repayments_term
            
    @api.depends("mortgrage_term_year", "mortgrage_term_months", "mortgage_amount", "fixed_interest_rate", "monthly_repayment", "esis_payment_frequency")
    def _compute_term_repayment(self):

        for application in self:
            application.fixed_term_payment = 0.0
            application.repayment_at_variable = 0.0
            application.repayment_at_variable_plus1 = 0.0
            application.repayment_at_variable_plus2 = 0.0
            application.max_possible_repayment = application.monthly_repayment

            total_years = int(application.mortgrage_term_year or 0) + (int(application.mortgrage_term_months) / 12)
            if application.esis_payment_frequency == "monthly":
                repayment_frequency = 12
            elif application.esis_payment_frequency == "fortnightly":
                repayment_frequency = 26
            elif application.esis_payment_frequency == "weekly":
                repayment_frequency = 52
            else:
                raise UserError(_(f"Unsupported repayment frequency: {application.esis_payment_frequency}"))

            total_repayments_term = math.trunc(total_years * repayment_frequency)
            fixed_repayments_term = math.trunc(application.term_at_starting_rate * repayment_frequency)
            if total_repayments_term:
                application.fixed_term_payment = self._compute_repayment_amount(application.mortgage_amount, application.fixed_interest_rate, total_repayments_term, repayment_frequency)
                _logger.info(f"\n==>Fixed term payment for {application.name}")

                # calculate repayments after fixed term
                outstanding_balance = application.calculate_outstanding_balance(
                    annual_interest_rate = application.fixed_interest_rate, 
                    number_of_periods = total_repayments_term,
                    amount = application.mortgage_amount,
                    specified_period = fixed_repayments_term,
                    frequency = application.esis_payment_frequency)

                _logger.info(f"\n==>outstanding_balance: {outstanding_balance}")
                outstanding_amount = outstanding_balance.get("outstanding_amount", 0.0)
                variable_repayments_term = total_repayments_term - fixed_repayments_term
                application.repayment_at_variable = self._compute_repayment_amount(outstanding_amount, application.interest_rate, variable_repayments_term, repayment_frequency)
                application.repayment_at_variable_plus1 = self._compute_repayment_amount(outstanding_amount, application.interest_rate + 1, variable_repayments_term, repayment_frequency)
                application.repayment_at_variable_plus2 = self._compute_repayment_amount(outstanding_amount, application.interest_rate + 2, variable_repayments_term, repayment_frequency)

                if application.mortgage_type == "fixed_variable_rate":
                    application.max_possible_repayment = max(application.fixed_term_payment, application.repayment_at_variable)

    def calculate_outstanding_balance(self, annual_interest_rate, number_of_periods, amount, specified_period, frequency="monthly"):
        if frequency == "monthly":
            repayment_multiplier = 12
        elif frequency == "fortnightly":
            repayment_multiplier = 26
        elif frequency == "weekly":
            repayment_multiplier = 52
        else:
            raise UserError(_("Unsupported repayment frequency"))

        total_installment_amount = 0
        total_installment_interest_amount = 0
        principal_amount = amount

        monthly_payement = self._compute_repayment_amount(amount, annual_interest_rate, number_of_periods, repayment_multiplier)
        for i in range(int(specified_period)):
            interest_at_installment = (annual_interest_rate / 100) / repayment_multiplier *  principal_amount
            installment_capital = monthly_payement - interest_at_installment

            # Calculate outstanding capital which will be principal amount for the next iteration
            principal_amount = principal_amount - installment_capital
            total_installment_amount += monthly_payement
            total_installment_interest_amount += interest_at_installment
        return {
            'outstanding_amount': principal_amount,
            'total_repayment_amount': total_installment_amount,
            'total_interest_paid_amount': total_installment_interest_amount
        }

    def get_monthly_payement(self, annual_interest_rate, number_of_periods, amount, frequency="monthly"):
        """
        Calculate Payments.
        
        Parameters:
            annual_interest_rate: Interst Rate,
            number_of_periods: Duration,
            amount: Principal Amount,
            frequency: monthly / fortnightly / weekly
        """
        if frequency == "weekly":
            months = 52
        elif frequency == "fortnightly":
            months = 26
        else:
            months = 12

        return round(-1 * (npf.pmt((annual_interest_rate / 100) / months, number_of_periods, float(amount))), 2)

    @api.depends("debt_repay", "property_co", "childcare", "maintenance")
    def _compute_total_short_term(self):
        for application in self:
            application.total_short_term = float(application.debt_repay + application.property_co + application.childcare + application.maintenance)

    @api.depends("allowable_monthly_income", "monthly_repayment", "total_short_term", "max_possible_repayment", "esis_payment_frequency")
    def _compute_service_ratio(self):
        for application in self:
            if application.esis_payment_frequency == "weekly":
                tmp_monthly_repayment = float(application.max_possible_repayment) * 30.4 / 7
            elif application.esis_payment_frequency == "fortnightly":
                tmp_monthly_repayment = float(application.max_possible_repayment) * 30.4 / 14
            elif application.esis_payment_frequency == "monthly":
                tmp_monthly_repayment = float(application.max_possible_repayment)
            else:
                raise Exception(_("Unknown ESIS Payment Frequency"))

            #if the mortage_type is variable rate we should be using the monthly_repayment to calculate all figures as net_disposable_inc, total_debt_service_ratio, mortgage_service ratio
            if application.mortgage_type == "variable_rate":
                tmp_monthly_repayment = application.monthly_repayment

            application.net_disposable_inc = float(application.allowable_monthly_income) - float(tmp_monthly_repayment + application.total_short_term)

            if application.allowable_monthly_income:
                application.mortgage_service_ratio = round((tmp_monthly_repayment / application.allowable_monthly_income) * 100, 2)
                application.total_debt_service_ratio = round(((tmp_monthly_repayment + application.total_short_term) / application.allowable_monthly_income) * 100, 2)

                if application.company_id.mortgage_service_ratio:
                    application.show_image_3 = application.mortgage_service_ratio < float(application.company_id.mortgage_service_ratio)
                else:
                    application.show_image_3 = application.mortgage_service_ratio < STANDARD_MORTGAGE_SERVICE_RATIO
                
                if application.company_id.debt_service_ratio:
                    application.show_image_4 = application.total_debt_service_ratio < float(application.company_id.debt_service_ratio)
                else:
                    application.show_image_4 = application.total_debt_service_ratio < STANDARD_TOTAL_DEBT_SERVICE_RATIO

    @api.depends("interest_rate", "mortgage_amount", "mortgrage_term_year", "mortgrage_term_months", "interest_rate_increase")
    def _compute_stressed_monthly_repayment(self):
        for application in self:
             _logger.info(f"\n==>_compute_stressed_monthly_repayment application: {application.name} ==>interest_rate: {application.interest_rate}")
             mortgage_term = (int(application.mortgrage_term_year or 0) * 12) + int(application.mortgrage_term_months)
             if (application.interest_rate + application.interest_rate_increase) and mortgage_term:
                 application.stressed_monthly_repayment = round(-1 * (npf.pmt(((application.interest_rate + application.interest_rate_increase) / 100) / 12, mortgage_term, application.mortgage_amount)), 3)

    @api.depends("stressed_allowable_income", "stressed_monthly_repayment", "total_short_term")
    def _compute_stressed_service_ratio(self):
        """
        Compute and Assign stressed_mortgage_service_ratio, stressed_total_debt_service_ratio, stressed_net_disposable_income.
        """
        for application in self:
            if application.stressed_allowable_income:
                application.stressed_mortgage_service_ratio = round((application.stressed_monthly_repayment / application.stressed_allowable_income) * 100, 2)
                application.stressed_total_debt_service_ratio = round(((application.stressed_monthly_repayment + application.total_short_term) / application.stressed_allowable_income) * 100, 2)
                application.stressed_net_disposable_income = application.stressed_allowable_income - (application.stressed_monthly_repayment + application.total_short_term)

                if application.company_id.stressed_mortgage_service_ratio:
                    application.show_image_8 = application.stressed_mortgage_service_ratio < application.company_id.stressed_mortgage_service_ratio
                else:
                    application.show_image_8 = application.stressed_mortgage_service_ratio < STANDARD_STRESSED_MORTGAGE_SERVICE_RATIO

                if application.company_id.stressed_debt_service_ratio:
                    application.show_image_9 = application.stressed_total_debt_service_ratio < application.company_id.stressed_debt_service_ratio
                else:
                    application.show_image_9 = application.stressed_total_debt_service_ratio < STANDARD_TOTAL_DEBT_SERVICE_RATIO

    @api.depends("monthly_repayment", "mortgrage_term_year", "mortgrage_term_months", "esis_payment_frequency", "mortgage_amount", "repayment_at_variable", "term_at_starting_rate", "fixed_term_payment")
    def _compute_total_repaid(self):
        for application in self:
            application.esis_total_repaid = 0.0
            application.esis_cost_per_1 = 0.0
            application.avg_repayment = 0.0
            application.esis_cost_of_credit = 0.0

            number_of_repayments = application._calculate_number_of_repayments()
            if application.mortgage_type == "variable_rate":
                if application.esis_payment_frequency == "weekly":
                    application.esis_total_repaid = application.esis_weekly_repayment * number_of_repayments
                elif application.esis_payment_frequency == "fortnightly":
                    application.esis_total_repaid = application.esis_fortnightly_repayment * number_of_repayments
                elif application.esis_payment_frequency == "monthly":
                    application.esis_total_repaid = application.monthly_repayment * number_of_repayments
            else:
                repayment_frequency = 0
                if application.esis_payment_frequency == "monthly":
                    repayment_frequency = 12
                elif application.esis_payment_frequency == "fortnightly":
                    repayment_frequency = 26
                elif application.esis_payment_frequency == "weekly":
                    repayment_frequency = 52

                fixed_repayments_term = math.trunc(application.term_at_starting_rate * repayment_frequency)
                variable_repayments_term = number_of_repayments - fixed_repayments_term
                application.esis_total_repaid = (application.fixed_term_payment * fixed_repayments_term) + (application.repayment_at_variable * variable_repayments_term)
            
            if number_of_repayments:
                application.avg_repayment = application.esis_total_repaid / number_of_repayments
                
            
            if application.avg_repayment and application.mortgage_amount:
                temp_avg_repayment = 0.0
                if application.esis_payment_frequency == "weekly":
                    temp_avg_repayment = application.avg_repayment * 30.4 / 7
                elif application.esis_payment_frequency == "fortnightly":
                    temp_avg_repayment = application.avg_repayment * 30.4 / 14
                elif application.esis_payment_frequency == "monthly":
                    temp_avg_repayment = application.avg_repayment

                monthly_repayments_term = int(application.mortgrage_term_year or 0) * 12 + int(application.mortgrage_term_months)
                application.avg_rate = (npf.rate(monthly_repayments_term, -1 * temp_avg_repayment, application.mortgage_amount, 0) * 12) * 100
                application.avg_repayment_plus1 = self._compute_repayment_amount(application.mortgage_amount, application.avg_rate + 1, monthly_repayments_term, 12)
                # application.avg_rate = (npf.rate(((float(application.mortgrage_term_year) * 12) + float(application.mortgrage_term_months)), -1 * tmp_avg_repayment, application.mortgage_amount, 0) * 12) * 100
                # application.avg_repayment_plus1 = round(-1 * (npf.pmt(((application.avg_rate + 1) / 100) / 12, (application.mortgrage_term_year * 12) + float(application.mortgrage_term_months), application.mortgage_amount)), 2)

            if application.mortgage_amount:
                application.esis_cost_of_credit = application.esis_total_repaid - application.mortgage_amount
                application.esis_cost_per_1 = application.esis_total_repaid / application.mortgage_amount

            if application.esis_payment_frequency == "monthly":
                step = 12
                multiplier = 1
            elif application.esis_payment_frequency == "fortnightly":
                step = 26
                multiplier = 2
            elif application.esis_payment_frequency == "weekly":
                step = 52
                multiplier = 4
            else:
                raise Exception(_(f"Unsupported Payment Frequency: {application.esis_payment_frequency}"))

    @api.depends("monthly_repayment", "avg_repayment", "esis_monthly_repayment_1", "avg_repayment_plus1", "mortgage_amount", "mortgrage_term_year", "mortgrage_term_months", "contribution_to_valuation", "contribution_to_revaluation", "once_off_costs")
    def _compute_aprc(self):
        for application in self:
            mortgage_term = int(application.mortgrage_term_year or 0) + (float(application.mortgrage_term_months) / 12)

            if application.esis_payment_frequency == "weekly":
                tmp_monthly_repayment = (float(application.avg_repayment) * 30.4 ) / 7
            elif application.esis_payment_frequency == "fortnightly":
                tmp_monthly_repayment = (float(application.avg_repayment) * 30.4) / 14
            elif application.esis_payment_frequency == "monthly":
                tmp_monthly_repayment = application.avg_repayment
            else:
                raise Exception(_(f"Unsupported Payment Frequency: {application.esis_payment_frequency}"))

            if mortgage_term and application.monthly_repayment:
                esis_aprc_value = npf.rate(mortgage_term * 12, -1 * tmp_monthly_repayment, application.mortgage_amount - (application.contribution_to_valuation + application.contribution_to_revaluation + application.once_off_costs), 0)
                esis_aprc_value = (np.power(esis_aprc_value + 1, 12) - 1) * 100
                application.esis_aprc = round(esis_aprc_value, 3)

            if mortgage_term and application.esis_monthly_repayment_1:
                esis_aprc_value = npf.rate(mortgage_term * 12, -1 * application.avg_repayment_plus1, application.mortgage_amount - (application.contribution_to_valuation + application.contribution_to_revaluation + application.once_off_costs), 0)
                esis_aprc_value = (np.power(esis_aprc_value + 1, 12) - 1) * 100
                application.esis_aprc_1 = round(esis_aprc_value, 3)

    @api.depends("applicant_1_net_profit_1", "applicant_1_plus_depreceation_1", "applicant_1_plus_interest_paid_1", "applicant_1_plus_remuneration_1",  "applicant_1_plus_pension_1")
    def _compute_mry(self):
        for application in self:
            application.applicant_1_trading_profit_1 = int(application.applicant_1_net_profit_1) + int(application.applicant_1_plus_depreceation_1) + int(application.applicant_1_plus_interest_paid_1) + int(application.applicant_1_plus_remuneration_1) +  int(application.applicant_1_plus_pension_1)

    @api.depends("applicant_1_net_profit_2", "applicant_1_plus_depreceation_2", "applicant_1_plus_interest_paid_2", "applicant_1_plus_remuneration_2",  "applicant_1_plus_pension_2")
    def _compute_mry_1(self):
        for application in self:
            application.applicant_1_trading_profit_2 = int(application.applicant_1_net_profit_2) + int(application.applicant_1_plus_depreceation_2) + int(application.applicant_1_plus_interest_paid_2) + int(application.applicant_1_plus_remuneration_2) +  int(application.applicant_1_plus_pension_2)
  
    @api.depends("applicant_1_net_profit_3", "applicant_1_plus_depreceation_3", "applicant_1_plus_interest_paid_3", "applicant_1_plus_remuneration_3",  "applicant_1_plus_pension_3")
    def _compute_mry_2(self):
        for application in self:
            application.applicant_1_trading_profit_3 = int(application.applicant_1_net_profit_3) + int(application.applicant_1_plus_depreceation_3) + int(application.applicant_1_plus_interest_paid_3) + int(application.applicant_1_plus_remuneration_3) +  int(application.applicant_1_plus_pension_3)

    @api.depends("applicant_1_trading_profit_1", "applicant_1_trading_profit_2", "applicant_1_trading_profit_3")
    def _compute_avg_trading_profit_1(self):
        for application in self:
            application.applicant_1_average_trading_profit = round((float(application.applicant_1_trading_profit_1) + float(application.applicant_1_trading_profit_2) + float(application.applicant_1_trading_profit_3)) / 3, 2)

    @api.depends("applicant_1_average_trading_profit", "applicant_1_less_business_repayments")
    def _compute_surplus_1(self):
        for application in self:
            application.applicant_1_surplus = float(application.applicant_1_average_trading_profit) - float(application.applicant_1_less_business_repayments)

    @api.depends("applicant_2_net_profit_1", "applicant_2_plus_depreceation_1", "applicant_2_plus_interest_paid_1", "applicant_2_plus_remuneration_1",  "applicant_2_plus_pension_1")
    def _compute_mry2(self):
        for application in self:
            application.applicant_2_trading_profit_1 = int(application.applicant_2_net_profit_1) + int(application.applicant_2_plus_depreceation_1) + int(application.applicant_2_plus_interest_paid_1) + int(application.applicant_2_plus_remuneration_1) +  int(application.applicant_2_plus_pension_1)

    @api.depends("applicant_2_net_profit_2", "applicant_2_plus_depreceation_2", "applicant_2_plus_interest_paid_2", "applicant_2_plus_remuneration_2",  "applicant_2_plus_pension_2")
    def _compute_mry2_1(self):
        for application in self:
            application.applicant_2_trading_profit_2 = int(application.applicant_2_net_profit_2) + int(application.applicant_2_plus_depreceation_2) + int(application.applicant_2_plus_interest_paid_2) + int(application.applicant_2_plus_remuneration_2) +  int(application.applicant_2_plus_pension_2)
    
    @api.depends("applicant_2_net_profit_3", "applicant_2_plus_depreceation_3", "applicant_2_plus_interest_paid_3", "applicant_2_plus_remuneration_3",  "applicant_2_plus_pension_3")
    def _compute_mry2_2(self):
        for application in self:
            application.applicant_2_trading_profit_3 = int(application.applicant_2_net_profit_3) + int(application.applicant_2_plus_depreceation_3) + int(application.applicant_2_plus_interest_paid_3) + int(application.applicant_2_plus_remuneration_3) +  int(application.applicant_2_plus_pension_3)

    @api.depends("applicant_2_trading_profit_1", "applicant_2_trading_profit_2", "applicant_2_trading_profit_3")
    def _compute_avg_trading_profit_2(self):
        for application in self:
            application.applicant_2_average_trading_profit = round((float(application.applicant_2_trading_profit_1) + float(application.applicant_2_trading_profit_2) + float(application.applicant_2_trading_profit_3)) / 3, 2)

    @api.depends("applicant_2_average_trading_profit", "applicant_2_less_business_repayments")
    def _compute_surplus_2(self):
        for application in self:
            application.applicant_2_surplus = float(application.applicant_2_average_trading_profit) - float(application.applicant_2_less_business_repayments)

    def action_recalculate_dob(self):
        self.ensure_one()
        if self.applicant_1.DOB:
            self.applicant_1_age = self._calculate_age(self.applicant_1.DOB)
        if self.applicant_2 and self.applicant_2.DOB:
            self.applicant_2_age = self._calculate_age(self.applicant_2.DOB)

    def action_limits_eligible(self):
        self.ensure_one()

        self.check_checklist()
        values = {'state': "limits_eligible"}
        if not self.applicant_2:
            values.update({'applicant_2_age': "", 'applicant_2_age_end_of_term': "", 'total_basic_income_2': "", 'total_net_basic_income_2': "", 'total_other_income_2': "", 'self_employed_2': "no"})
        self.write(values)

        self.load_checklist_items("limits_eligible")

    def action_limits_not_eligible(self):
        self.ensure_one()
        self.check_checklist()

        context = dict(self.env.context or {})
        limits_not_eligible_form = self.env.ref("appsmod2.wizard_limits_not_eligible_view_form")
        return {
            'name': _("Limits Not Eligible"),
            'type': "ir.actions.act_window",
            'view_mode': "form",
            'res_model': "wizard.limits.not.eligible",
            'views': [(limits_not_eligible_form.id, "form")],
            'view_id': limits_not_eligible_form.id,
            'target': "new",
            'context': context
        }

    def action_pre_application_complete(self):
        self.ensure_one()

        if self.applicant_1.member_id == False:
            raise UserError(_("Please Maintain Member ID for Applicant 1"))
        if self.applicant_2 and self.applicant_2.member_id == False:
            raise UserError(_("Please Maintain Member ID for Applicant 2"))

        self.check_checklist()
        self.write({'state': "pre_application_complete"})
        self.load_checklist_items("pre_application_complete")

    def action_pre_application_not_complete(self):
        self.ensure_one()
        self.check_checklist()
        context = dict(self.env.context or {})
        pre_application_not_complete_form = self.env.ref("appsmod2.wizard_pre_application_not_complete_view_form")
        return {
            'name': _("Pre-Application Not Complete"),
            'type': "ir.actions.act_window",
            'view_mode': "form",
            'res_model': "wizard.pre.application.not.complete",
            'views': [(pre_application_not_complete_form.id, "form")],
            'view_id': pre_application_not_complete_form.id,
            'target': "new",
            'context': context
        }

    def action_request_application(self):
        self.ensure_one()
        self.check_checklist()
        self.write({'state': "application_requested", 'show_checklist': True})
        self.load_checklist_items("application_requested")

    def action_application_pack_returned(self):
        self.ensure_one()
        self.check_checklist()
        self.write({'state': "application_pack_returned"})
        self.load_checklist_items("application_pack_returned")

    def action_consent_signed(self):
        self.ensure_one()
        self.check_checklist()
        self.write({'state': "consent_signed"})
        self.load_checklist_items("consent_signed")

    def action_application_form_received(self):
        self.ensure_one()
        self.check_checklist()

        if self.gift_to_deposit > STANDARD_GIFT_TO_DEPOSIT:
            # raise UserError(_(f"Generally Gift is Not Supposed to be more than {int(STANDARD_GIFT_TO_DEPOSIT)}%"))
            context = dict(self.env.context or {})
            warning_form = self.env.ref("appsmod2.wizard_gift_warning_view_form")
            return {
                'name': _("Gift Warning"),
                'type': "ir.actions.act_window",
                'view_mode': "form",
                'res_model': "wizard.gift.warning",
                'views': [(warning_form.id, "form")],
                'view_id': warning_form.id,
                'target': "new",
                'context': context
            }
        else:
            self.write({
                'state': "application_form_received",
                'show_cover_note': True
            })
            self.load_checklist_items("application_form_received")

    def action_submit_to_external(self):
        self.ensure_one()
        self.check_checklist()

        context = dict(self.env.context or {})
        context.update({
            'default_category_id': self.officer_category_id,
            'default_company_id': self.company_id.id,
            'default_assignee': self.assignee.id
        })

        external_assessor_selection_form = self.env.ref("appsmod2.wizard_select_external_assessor_view_form")
        return {
            'name': _("External Assessor"),
            'type': "ir.actions.act_window",
            'view_mode': "form",
            'res_model': "wizard.select.external.assessor",
            'views': [(external_assessor_selection_form.id, "form")],
            'view_id': external_assessor_selection_form.id,
            'target': "new",
            'context': context
        }

    def action_submit_for_internal_assessment(self):
        self.ensure_one()
        self = self.sudo()

        self.check_checklist()
        message = """<div style=\"font-family: Calibri; font-size: 14px; color: rgb(34, 34, 34); background-color: #FFF;margin-left:7mm \">
                        <h3 style='text-align:center'>Special Conditions of Offer</h3>\n\n
                        <br/>
                        <ol>
                            <li>Drawdown of this Offer is subject to the Form of Acceptance being signed by the Borrower(s), and witnessed, and the full signed Letter of Offer being returned to the Credit Union.</li>
                            <li>A fully completed direct debit mandate is to be forwarded to the Credit Union prior to drawdown.</li>
                            <li>Please note the Loan must drawdown within XXXXX months of the date of the Letter of Offer (“the drawdown period”). In the event that the Loan does not drawdown within the drawdown period, the Letter of Offer will lapse and the Borrower(s) must reapply with a new application and new updated supporting documentation. In exceptional circumstances and before the expiry of the drawdown period, the Credit Union in agreement with the Borrower[s] can extend the drawdown period (“the revised drawdown period"). For any other amendment(s) to the Letter of Offer agreed between the Credit Union and the Borrower(s) during the drawdown period, the drawdown period does not change and continues to run from the date of the Letter of Offer.</li>
                            <li>Satisfactory identification for """+str(self.applicant_1.name)+""" in compliance with Anti Money Laundering Regulations must be presented to the Credit Union.</li>
                            <li>Drawdown is subject to Insurance on the property held as security proving satisfactory to the Credit Union and the Credit Union’s interest being noted on the policy.</li>
                            <li>Satisfactory life cover must be obtained by the Borrower(s) and the completed original Assignment of Life Policy Form must be submitted to and accepted by the Credit Union prior to drawdown.</li>
                            <li>The Credit Union is obliged by the Central Bank (Supervision and Enforcement) Act 2013 (Section 48)(Housing Loan Requirements) Regulations 2015 to ensure that the Loan to Value percentage does not exceed that set out in the Letter of Offer and does not breach Central Bank limits. In the event that the loan is not drawn down within [xxxx] months of the original valuation the Credit Union will require a revaluation of the property prior to the loan being made available for drawdown. In these circumstances, the Borrower(s) will be required to pay for this revaluation report at a cost of [insert €].</li>
                            <li>Borrower’s to open a joint account with the credit union prior to drawdown for the purposes of advancement of funds.</li>
                            <li>Borrower(s) to redeem existing <Free Text> loan with current outstanding balance of €<Free Text> prior to drawdown and the Credit Union to be satisfied with same.</li>
                            <li>Borrower(s) to redeem existing credit card balance with current outstanding balance of €<Free Text> prior to drawdown and the Credit Union to be satisfied with same.</li>
                            <li>Borrower(s) to redeem existing overdraft facility with current negative balance of €<Free Text> prior to drawdown and the Credit Union to be satisfied with same.</li>
                            <li>The Borrower(s) solicitor must confirm to the Credit Union prior to draw down that a parking space is included in the purchase price of the property held by security.{note to lender: this should not be selected as a SC unless the car space is included in the description of the security in the loan offer or in the property address}.</li>
                            <li>The Borrower(s) must provide the Credit Union prior to draw down with confirmation from the property management agency or selling agent as to the annual management company charge applicable to the property held by security.</li>
                            <li>The Borrower(s) must provide the Credit Union prior to draw down with an architect/surveyor’s report that any extension or building works affecting the property held by security comply fully with planning permissions.</li>
                            <li><b>Block Life Cover</b>: The Credit Union has chosen to acquire a block life policy, in its favour, safeguarding the repayment of your mortgage loan, in the event that you die during the term of this loan (subject to certain Terms and Conditions, which are available from the Credit Union). At the Credit Union’s sole discretion, it may renew its own block life policy annually. For the avoidance of doubt, there is no insurance policy or contract in place with you, or for you, in respect of your mortgage loan. The Credit Union is not obliged, as part of this mortgage loan agreement to maintain its block life policy. At its discretion, the Credit Union may alter or cancel its block life cover.If notified by the Credit Union to do so, at any time during the term of this loan, you may be required to ensure that a mortgage life insurance policy, which can fully repay the mortgage loan balance and any accrued interest and charges, is taken out in the interest of the Credit Union, if you or your partner died during the term of the mortgage loan. You should seek appropriate advice from a qualified insurance broker, and upon arrangement of an appropriate life insurance policy, provide details of this policy and assignment to the Credit Union.You may choose to acquire this policy from a life provider of your choice, however, this policy must comply with the standards and indemnity required by the Credit Union and premiums must be paid by you to keep the policy in force, during the term of the mortgage loan. If you fail to maintain an adequate life insurance policy in favor of the Credit Union, to the value of the outstanding loan principal, accrued interest and charges, or fail to maintain payment of premiums on such a policy, then the Credit Union may take out such a policy, with a provider of its choosing and you will be obliged to pay for all costs, both set-up and recurring, as part of your loan repayments. The Credit Union’s block life cover, which it acquires in its own interest only, is not a savings or investment product and has no cash value unless a valid claim is made. You have no claim to the Credit Union’s own block life policy.</li>                                                
                            <h4 style='text-align:center' class="mt-3">FIXED RATE (NOTE: IF USING SAM GENERAL TERMS AND CONDITIONS OF LOAN (GTCs) PLEASE DELETE SC  16, 17 & 18 BELOW AS THEY ARE MORE APPROPRIATELY CONTAINED IN THE GTCs). </h4>\n\n
                            <li>This is a Loan Offer with a fixed interest rate for [x] years as set out in the Particulars of Home Loan.  A fixed rate loan is calculated on the basis that the loan will not be repaid ahead of maturity of the fixed interest rate term.  It is on this basis that the Credit Union is prepared to commit itself to holding its lending rate fixed for the agreed period and incur certain third party costs on your behalf, such as valuation, legal and registration fees. Nonetheless, the Borrower is entitled to prepay the loan in full at any time or to convert to a variable rate or other fixed rate that the Credit Union may offer during the fixed term of the loan or to make a capital repayment in excess of the scheduled instalments.  In any of these circumstances, the Credit Union is entitled, subject to the provisions of section 121(2) of the Consumer Credit Act 1995, to recoup an early breakage cost from the Borrower.  The Credit Union limits this cost to those it has committed itself to or incurred to facilitate the loan Offer and will only impose an early breakage cost on the Borrower if the Borrower is prepaying the loan in full.  If the Borrower wishes to make a full prepayment, the Credit Union will confirm the sum payable and the Borrower is obliged to pay it in full prior to the release of the Credit Union’s security.</li>
                            <li>While on a fixed interest rate, the interest rate and mortgage repayment remains the same for the agreed fixed interest rate period. During this time the interest rate will not change. The Borrower is entitled to prepay the loan in full at any time or to convert to a variable rate or other fixed rate that the Credit Union may offer during the term of the loan or to make a capital repayment in excess of the scheduled instalments.  In any of these circumstances an early breakage charge is payable by the Borrower where the fixed interest rate period has not expired.  The breakage charge is calculated as follows: amount (A) x remaining term in days divided by 365 (U) x difference in cost of funds (D%).  Definition of terms used in this formula: 
                            (A) amount - The amount being repaid early or the amount being converted to a variable rate or another fixed rate period. 
                            (U) remaining term in days - Remaining number of days left before the fixed rate is due to expire. 
                            (D) difference in cost of funds - The difference between the original cost of funds and the cost of funds for the fixed rate period remaining (excluding the third party costs incurred). 
                            </li>
                            <li>At the end of an unbroken fixed interest rate period, the interest rate on your loan will default to the standard variable interest rate then offered by the credit union at that time unless you choose an alternative interest rate, if on offer by the credit union to you at that time. Our standard variable interest rate is a variable interest rate. If the interest rate on your loan defaults or otherwise converts to a variable interest rate then offered by the credit union, your interest rate and the amount of your instalments could increase or decrease during the remaining term of your loan and your interest rate could be higher than the fixed interest rate that applied during any fixed interest rate period.</li>
                            <h4 style='text-align:center' class="mt-3">(NOTE: IF USING SAM GENERAL TERMS AND CONDITIONS OF LOAN (GTCs) AND THE CREDIT UNION DOES NOT INCLUDE THIRD PARTY COSTS IN THE BREAKAGE CHARGE, THE CREDIT UNION SHOULD SELECT SC 19 (AMEND AS APPROPRIATE)</h4>\n\n
                            <li>No third party costs are incurred by the credit union and such costs are not applicable in the calculation of the breakage charge OR the calculation of the breakage charge does not include the third party costs. General Home Loan Condition 3.2.3 is amended accordingly.</li>
                            <h4 style='text-align:center' class="mt-3">TOP-UP/ADDITIONAL MORTGAGE LOAN</h4>\n\n
                            <li>This Offer is a top-up loan in the sum of €[X] that will increase your mortgage borrowings from the credit union from €[Y] to €[Z] for the repayment of which the Credit Union will continue to rely on the first legal charge for all present and future advances dated [		] that it holds on the property at [        ] [comprised in Folio __].</li>
                            <li>The Credit Union is obliged by the Central Bank (Supervision and Enforcement) Act 2013 (Section 48)(Housing Loan Requirements) Regulations 2015 to ensure that the Loan to Value Ratio does not exceed that set out in the Letters of Offer and does not breach Central Bank limits. For the calculation of this ratio, ‘Loan’ is the total mortgage borrowings from the credit union including this loan. Prior to the drawdown of a top-up loan therefore, the Credit Union will require an acceptable revaluation of the property as at a date not later than [X] months prior to drawdown.  If a valuation is submitted but the top-up loan not drawn down within [X] months, an updated valuation may be required at the Borrower’s cost.</li>
                            <li>If the life cover obtained by the Borrower and assigned to the Credit Union as a condition of the drawdown of the loan, on [insert date] is no longer sufficient, the Borrower will be required to increase the cover or obtain a new policy and a new Assignment of Life Policy Form must be submitted to and accepted by the Credit Union prior to drawdown.</li>                            </ol>
                     </div>"""

        values = {}
        external_user_domain = None
        if self.assignee != self.original_assignee:
            template = self.env.ref("appsmod2.email_template_appsmod2_original_assignee")
            context = self._context

            for user in self.env["res.users"].browse(context["uid"]):
                if not user.email:
                    raise UserError(_(f"Cannot send email: User {user.name} has no email address."))
                
                self.with_context(context).message_post_with_template(template.id)
                external_user_id = self.env.ref("appsmod2.appsmod2_application_external_user_rule")
                if external_user_id:
                    external_user_domain = external_user_id.domain_force
                    new_domain = "['|', ('external_assessor_user', '=', user.id), ('assignee', '=', user.id)]"
                    external_user_id.write({'domain_force': new_domain})
            values = {'state': "ready_for_assessment", 'assignee': self.original_assignee.id, 'show_special': True, 'show_assessment': True, 'body_special_conditions': message}
        else:
            values = {'state': "ready_for_assessment", 'show_special': True, 'show_assessment': True, 'body_special_conditions': message}

        values.update({'general_terms_and_conditions': SAM_GENERAL_TERMS_CONDITIONS})

        # external_user_id.write({'domain_force': external_user_domain})
        self.write(values)
        self.load_checklist_items("ready_for_assessment")

    def action_check_application(self):
        self.ensure_one()
        self.check_checklist()
        
        if self.certified_value == "no":
            if self.state != "valuation_report":
                self.load_checklist_items("valuation_report")
            self.write({'state': "valuation_report"})
        elif self.property_value > self.certified_property_value:
            if self.state != "property_overvalued":
                self.write({'state': "property_overvalued"})
                self.load_checklist_items("property_overvalued")
        elif self.certified_property_value:
            context = dict(self.env.context or {})
            context.update({
                'default_category_id': self.senior_officer_category_id,
                'default_original_assignee': self.assignee.id
            })
            senior_loan_officer_selection_form = self.env.ref("appsmod2.wizard_select_senior_loan_officer_view_form")
            return {
                'name': _("Senior Loan Officer"),
                'type': "ir.actions.act_window",
                'view_mode': "form",
                'res_model': "wizard.select.senior.loan.officer",
                'views': [(senior_loan_officer_selection_form.id, "form")],
                'view_id': senior_loan_officer_selection_form.id,
                'target': "new",
                'context': context
            }

    def action_accept_application(self):
        self.ensure_one()

        self.check_checklist()
        context = dict(self.env.context or {})
        acceptance_form = self.env.ref("appsmod2.wizard_accept_application_view_form")
        return {
            'name': _("Accept Application"),
            'type': "ir.actions.act_window",
            'view_mode': "form",
            'res_model': "wizard.accept.application",
            'views': [(acceptance_form.id, "form")],
            'view_id': acceptance_form.id,
            'target': "new",
            'context': context
        }

    def action_funds_drawn(self):
        self.write({'state': "funds_drawn_down"})

    def action_move_back(self):
        self.ensure_one()
        if self.state == "limits_eligible":
            self.remove_checklist_items(self.state)
            self.write({'state': "draft"})
            self.reinitialize_checklist("draft")
        elif self.state == "pre_application_complete":
            self.remove_checklist_items("limits_not_eligible")
            self.remove_checklist_items(self.state)
            self.write({'state': "limits_eligible"})
            self.reinitialize_checklist("limits_eligible")
        elif self.state == "pre_application_not_complete":
            self.remove_checklist_items(self.state)
            self.write({'state': "limits_eligible"})
            self.reinitialize_checklist("limits_eligible")
        elif self.state == "application_requested":
            self.remove_checklist_items(self.state)
            self.remove_checklist_items("pre_application_not_complete")
            self.write({'state': "pre_application_complete", 'show_checklist': False})
            self.reinitialize_checklist("pre_application_complete")
        elif self.state == "application_pack_returned":
            self.remove_checklist_items(self.state)
            self.write({'state': "application_requested"})
            self.reinitialize_checklist("application_requested")
        elif self.state == 'consent_signed':
            self.remove_checklist_items(self.state)
            self.write({'state': 'application_pack_returned','show_cover_note': False})
            self.reinitialize_checklist('application_pack_returned')
        elif self.state == 'application_form_received':
            self.remove_checklist_items(self.state)
            self.write({'state': 'consent_signed'})
            self.reinitialize_checklist('consent_signed')
        elif self.state == 'external_assessor':
            self.write({'state': 'application_form_received','assignee': self.original_assignee.id})
            self.reinitialize_checklist('application_form_received')
        elif self.state == 'ready_for_assessment':
            self.remove_checklist_items(self.state)
            self.write({'state': 'application_form_received','show_special': False,'show_assessment': False})
            self.reinitialize_checklist('application_form_received')
        elif self.state == 'valuation_report':
            self.remove_checklist_items('ready_for_assessment')
            self.remove_checklist_items(self.state)
            self.write({'state': 'application_form_received','show_special': False,'show_assessment': False})
            self.reinitialize_checklist('application_form_received')
        elif self.state == 'property_overvalued':
            self.remove_checklist_items('ready_for_assessment')
            self.remove_checklist_items('valuation_report')
            self.remove_checklist_items(self.state)
            self.write({'state': 'application_form_received','show_special': False,'show_assessment': False})
            self.reinitialize_checklist('application_form_received')
        elif self.state == 'submit':
            self.remove_checklist_items(self.state)
            self.remove_checklist_items('valuation_report')
            self.remove_checklist_items('property_overvalued')
            self.write({'state': 'ready_for_assessment','assignee': self.original_assignee.id})
            self.reinitialize_checklist('ready_for_assessment')

    def action_print_decline_letter(self):
        return self.env.ref("appsmod2.decline_letter_report").report_action(self)
    
    def action_print_drawdown_letter(self):
        return self.env.ref("appsmod2.drawdown_letter_report").report_action(self)

    def action_print_principal_approval_letter(self):
        return self.env.ref("appsmod2.principal_approval_letter_report").report_action(self)

    def action_print_affordability_calculator(self):
        return self.env.ref("appsmod2.affordability_calculator_report").report_action(self)

    def action_letter_of_offer(self):
        return self.env.ref("appsmod2.letter_of_offer").report_action(self)

    def action_print_letter_of_offer_2020(self):
        self.ensure_one()
        if self.is_old_application:
            return self.action_letter_of_offer()
        return self.env.ref("appsmod2.letter_of_offer_2020").report_action(self)

    def action_print_esis(self):
        return self.env.ref("appsmod2.esis_report").report_action(self)

    def action_print_esis_2020(self):
        self.ensure_one()
        if self.is_old_application:
            return self.action_print_esis()
        return self.env.ref("appsmod2.esis_2020_report").report_action(self)


    def load_checklist_items(self, state):
        self.ensure_one()
        _logger.info(f"\n==============context: {self.env.context}=====================\n")
        application_id = self.env.context.get("active_id", False) or self.id

        all_applicants = self.env["application.checklist"].search([('type', '=', "all_applicants"), ('active', '=', True), ('applicable_for_eu_citizen', '=', False), ('state', '=', state)])
        if all_applicants:
            values = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state} for checklist in all_applicants]
            self.env["jointly.applicable"].create(values)

        individually_applicable = self.env["application.checklist"].search([('type', '=', "all_applicants_individual"), ('active', '=', True), ('applicable_for_eu_citizen', '=', False), ('state', '=', state)])
        if individually_applicable:
            values1 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant1',type:'individual'} for checklist in individually_applicable]
            self.env["checklist.applicable.applicant"].create(values1)
            if self.applicant_2:
                values2 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant2',type:'individual'} for checklist in individually_applicable]
                self.env["checklist.applicable.applicant"].create(values2)
            
        self_applicable = self.env["application.checklist"].search([('type', '=', 'self_employed'), ('active', '=', True), ('applicable_for_eu_citizen', '=', False), ('state', '=', state)])
        if self_applicable:
            if self.self_employed_1 == "yes":
                values1 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant1',type:'self'} for checklist in self_applicable]
                self.env["checklist.applicable.applicant"].create(values1)
            if self.applicant_2 and self.self_employed_2 == "yes":
                values2 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant2',type:'self'} for checklist in self_applicable]
                self.env["checklist.applicable.applicant"].create(values2)

        paye_applicable = self.env["application.checklist"].search([('type', '=', 'paye_employees'), ('active', '=', True), ('applicable_for_eu_citizen', '=', False), ('state', '=', state)])
        if paye_applicable:
            if self.self_employed_1 == "no":
                values1 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant1',type:'paye'} for checklist in paye_applicable]
                self.env["checklist.applicable.applicant"].create(values1)
            if self.applicant_2 and self.self_employed_2 == "no":
                values2 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant2',type:'paye'} for checklist in paye_applicable]
                self.env["checklist.applicable.applicant"].create(values2)

        # Add EU Citizen Checklist Items 
        individually_applicable = self.env['application.checklist'].search([('type', '=', 'all_applicants_individual'), ('active', '=', True), ('applicable_for_eu_citizen', '=', True), ('state', '=', state)])
        if individually_applicable:
            if self.applicant_1_eu_citizen == "yes":
                values1 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant1',type:'individual'} for checklist in individually_applicable]
                self.env['checklist.applicable.applicant'].create(values1)
            if self.applicant_2 and self.applicant_2_eu_citizen == "yes":
                values2 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant2',type:'individual'} for checklist in individually_applicable]
                self.env['checklist.applicable.applicant'].create(values2)

        self_applicable = self.env['application.checklist'].search([('type', '=', 'self_employeed'), ('active', '=', True), ('applicable_for_eu_citizen', '=', True), ('state', '=', state)])
        if self_applicable:
            if self.applicant_1_eu_citizen == "yes" and self.self_employed_1 == "yes":
                values1 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant1',type:'self'} for checklist in self_applicable]
                self.env['checklist.applicable.applicant'].create(values1)
            if self.applicant_2 and self.applicant_2_eu_citizen == "yes" and self.self_employed_2 == "yes":
                values2 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant2',type:'self'} for checklist in self_applicable]
                self.env['checklist.applicable.applicant'].create(values2)

        paye_applicable = self.env['application.checklist'].search([('type', '=', 'paye_employees'), ('active', '=', True), ('applicable_for_eu_citizen', '=', True), ('state', '=', state)])
        if paye_applicable:
            if self.applicant_1_eu_citizen == "yes" and self.self_employed_1 == "no":
                values1 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant1',type:'paye'} for checklist in paye_applicable]
                self.env['checklist.applicable.applicant'].create(values1)
            if self.applicant_2 and self.applicant_2_eu_citizen == "yes" and self.self_employed_2 == "no":
                values2 = [{'name': checklist.name, 'application_id': application_id, 'sequence': checklist.sequence, 'state': state,'applicant_type':'applicant2',type:'paye'} for checklist in paye_applicable]
                self.env['checklist.applicable.applicant'].create(values2)

    def check_checklist(self):
        self.ensure_one()
        applicant1_passed = True
        applicant2_passed = True
        jointly_passed = True


        message_error = "Following Checklist Items Failed: \n"
        jointly_error = "\nJOINTLY\n"
        applicant1_error = "\nAPPLICANT 1\n"
        applicant2_error = "\nAPPLICANT 2\n"

        all_applicants = self.env["jointly.applicable"].search([('application_id', '=', self.id)])
        for checklist in all_applicants:
            if not checklist.acceptable:
                jointly_error = f"{jointly_error}- {checklist.name}\n"
                jointly_passed = False

        individually_applicable1 = self.env["checklist.applicable.applicant"].search([('application_id', '=', self.id),('applicant_type', '=', 'applicant1'),('type', '=', 'individual')])
        for checklist in individually_applicable1:
            if not checklist.acceptable:
                applicant1_error += f"- {checklist.name}\n"
                applicant1_passed = False

        if self.applicant_1_credit_risk == "no":
            applicant1_error += f"- Credit Risk Not Acceptable\n"
            applicant1_passed = False

        individually_applicable2 = self.env["checklist.applicable.applicant"].search([('application_id', '=', self.id),('applicant_type', '=', 'applicant2'),('type', '=', 'individual')])
        for checklist in individually_applicable2:
            if not checklist.acceptable:
                applicant2_error += f"- {checklist.name}\n"
                applicant2_passed = False

        if self.applicant_2_credit_risk == "no":
            applicant2_error += f"- Credit Risk Not Acceptable\n"
            applicant2_passed = False

        self_applicable1 = self.env["checklist.applicable.applicant"].search([('application_id', '=', self.id),('applicant_type', '=', 'applicant1'),('type', '=', 'self')])
        for checklist in self_applicable1:
            if not checklist.acceptable:
                applicant1_error += f"- {checklist.name}\n"
                applicant1_passed = False

        self_applicable2 = self.env["checklist.applicable.applicant"].search([("application_id", '=', self.id),('applicant_type', '=', 'applicant2'),('type', '=', 'self')])
        for checklist in self_applicable2:
            if not checklist.acceptable:
                applicant2_error += f"- {checklist.name}\n"
                applicant2_passed = False

        paye_applicable1 = self.env["checklist.applicable.applicant"].search([("application_id", '=', self.id),('applicant_type', '=', 'applicant1'),('type', '=', 'paye')])
        for checklist in paye_applicable1:
            if not checklist.acceptable:
                applicant1_error += f"- {checklist.name}\n"
                applicant1_passed = False
            
        paye_applicable2 = self.env["checklist.applicable.applicant"].search([('application_id', '=', self.id),('applicant_type', '=', 'applicant2'),('type', '=', 'paye')])
        for checklist in paye_applicable2:
            if not checklist.acceptable:
                applicant2_error += f"- {checklist.name}\n"
                applicant2_passed = False

        if not jointly_passed:
            message_error += jointly_error
        if not applicant1_passed:
            message_error += applicant1_error
        if not applicant2_passed:
            message_error += applicant2_error

        if jointly_passed and applicant1_passed and applicant2_passed:
            return True
        else:
            raise UserError(_(message_error))

    def remove_checklist_items(self, state):
        self.ensure_one()
        application_id = self.id

        domain = [('type', '=', 'all_applicants'), ('applicable_for_eu_citizen', '=', False), ('state', '=', str(state))]
        all_applicants = self.env["application.checklist"].search(domain).mapped("name")
        if all_applicants:
            self.env["jointly.applicable"].search([('name', 'in', all_applicants), ('application_id', '=', application_id)]).unlink()

        domain[0] = ('type', '=', "all_applicants_individual")
        individually_applicable = self.env["application.checklist"].search(domain).mapped("name")
        if individually_applicable:
            self.env["checklist.applicable.applicant"].search([('name', 'in', individually_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant1'),('type', '=', 'individual')]).unlink()
            if self.applicant_2:
                self.env["checklist.applicable.applicant"].search([('name', 'in', individually_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant2'),('type', '=', 'individual')]).unlink()

        domain[0] = ('type', '=', 'self_employed')
        self_applicable = self.env["application.checklist"].search(domain).mapped("name")
        if self_applicable:
            if self.self_employed_1 == "yes":
                self.env["checklist.applicable.applicant"].search([('name', 'in', self_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant1'),('type', '=', 'self')]).unlink()
            if self.self_employed_2 == "yes":
                self.env["checklist.applicable.applicant"].search([('name', 'in', self_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant2'),('type', '=', 'self')]).unlink()

        domain[0] = ('type', '=', 'paye_employees')
        paye_applicable = self.env["application.checklist"].search(domain).mapped("name")
        if paye_applicable:
            if self.self_employed_1 == "no":
                self.env["checklist.applicable.applicant"].search([('name', 'in', paye_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant1'),('type', '=', 'paye')]).unlink()
            if self.applicant_2 and self.self_employed_2 == "no":
                self.env["checklist.applicable.applicant"].search([('name', 'in', paye_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant2'),('type', '=', 'paye')]).unlink()

        # EU Citizens Checklist Items 
        domain = [('type', '=', 'all_applicants_individual'), ('applicable_for_eu_citizen', '=', True), ('state', '=', str(state))]
        individually_applicable = self.env["application.checklist"].search(domain).mapped("name")
        if individually_applicable:
            if self.applicant_1_eu_citizen == "yes":
               self.env["checklist.applicable.applicant"].search([('name', 'in', individually_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant1'),('type', '=', 'individual')]).unlink()
        if self.applicant_2 and self.applicant_2_eu_citizen == "yes":
               self.env["checklist.applicable.applicant"].search([('name', 'in', individually_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant2'),('type', '=', 'individual')]).unlink()

        domain[0] = ('type', '=', 'self_employed')
        self_applicable = self.env["application.checklist"].search(domain).mapped("name")
        if self_applicable:
            if self.self_employed_1 == "yes" and self.applicant_1_eu_citizen == "yes":
               self.env["checklist.applicable.applicant"].search([('name', 'in', self_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant1'),('type', '=', 'self')]).unlink()
            if self.self_employed_2 == "yes" and self.applicant_2_eu_citizen == "yes":
               self.env["checklist.applicable.applicant"].search([('name', 'in', self_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant2'),('type', '=', 'self')]).unlink()

        domain[0] = ('type', '=', 'paye_employees')
        paye_applicable = self.env["application.checklist"].search(domain).mapped("name")
        if paye_applicable:
            if self.self_employed_1 == "no" and self.applicant_1_eu_citizen == "yes":
               self.env["checklist.applicable.applicant"].search([('name', 'in', paye_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant1'),('type', '=', 'paye')]).unlink()
            if self.applicant_2 and self.self_employed_2 == "no" and self.applicant_2_eu_citizen == "yes":
               self.env["checklist.applicable.applicant"].search([('name', 'in', paye_applicable), ('application_id', '=', application_id),('applicant_type', '=', 'applicant2'),('type', '=', 'paye')]).unlink()

    def reinitialize_checklist(self, state):
        self.ensure_one()
        base_domain = [('state', '=', state), ('application_id', '=', self.id)]
        #reinitialize the jointly applicable
        self.env['jointly.applicable'].search(base_domain).write({'provided' : False, 'acceptable' : False})
        #reinitiliaze applicable applicant1
        applicant1_applicable_domain = base_domain + [('applicant_type', '=', 'applicant1'),('type', '=', 'individual')]
        self.env['checklist.applicable.applicant'].search(applicant1_applicable_domain).write({'provided' : False, 'acceptable' : False})
        #reinitialize applicable applicant2
        applicant2_applicable_domain = base_domain + [('applicant_type', '=', 'applicant2'),('type', '=', 'individual')]
        self.env['checklist.applicable.applicant'].search(applicant2_applicable_domain).write({'provided' : False, 'acceptable' : False})
        #reinitialize self applicable applicant1
        applicant1_self_applicable_domain = base_domain + [('applicant_type', '=', 'applicant1'),('type', '=', 'self')]
        self.env['checklist.applicable.applicant'].search(applicant1_self_applicable_domain).write({'provided' : False, 'acceptable' : False})
        #reinitialize self applicable applicant2
        applicant2_self_applicable_domain = base_domain + [('applicant_type', '=', 'applicant2'),('type', '=', 'self')]
        self.env['checklist.applicable.applicant'].search(applicant2_self_applicable_domain).write({'provided' : False, 'acceptable' : False})	
        #reinitialize paye applicable applicant1
        applicant1_paye_applicable_domain = base_domain + [('applicant_type', '=', 'applicant1'),('type', '=', 'paye')] 	
        self.env['checklist.applicable.applicant'].search(applicant1_paye_applicable_domain).write({'provided' : False, 'acceptable' : False})
        #reinitialize paye applicable applicant2
        applicant2_paye_applicable_domain = base_domain + [('applicant_type', '=', 'applicant2'),('type', '=', 'paye')]
        self.env['checklist.applicable.applicant'].search(applicant2_paye_applicable_domain).write({'provided' : False, 'acceptable' : False})

    def action_decline(self):
        self.ensure_one()
        context = dict(self.env.context)
        decline_form = self.env.ref("appsmod2.wizard_decline_view_form")

        return {
            'name': _("Declination Confirmation"),
            'type': "ir.actions.act_window",
            'view_mode': "form",
            'res_model': "wizard.decline",
            'views': [(decline_form.id, "form")],
            'view_id': decline_form.id,
            'target': 'new',
            'context': context
        }
