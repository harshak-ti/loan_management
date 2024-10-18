# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import mimetypes
import base64


_logger = logging.getLogger(__name__)

PROVIDED_SELECTION = [
    ('provided', "Provided"),
    ('not_provided', "Not Provided")
]

ACCEPTABLE_SELECTION = [
    ('acceptable', "Acceptable"),
    ('not_acceptable', "Not Acceptable")
]

class DocumentsUniquelyApplicable(models.Model):
    _name = "documents.uniquely.applicable"
    _description = "Documents Uniquely Applicable"

    name = fields.Char("Document", required=True, default=lambda self: _("New"))
    data_file = fields.Binary("File", required=True, attachment=False)
    data_file_name = fields.Char("File Name")
    application_id = fields.Many2one("application", "Applicant", help="Application ID")

    @api.constrains('data_file_name','data_file')
    def _check_data_file_format_and_size(self):
        allowed_formats = ['pdf', 'jpg', 'jpeg', 'png']
        max_file_size = 10 * 1024 * 1024  # 10 MB
        for rec in self:
            # self.env['res.config.settings']._check_document_format_and_size(rec.data_file_name, rec.data_file)

            # Get file extension
            file_extension = rec.data_file_name.split('.')[-1].lower()

            # Check if file format is allowed
            if file_extension not in allowed_formats:
                raise models.ValidationError(_("The file format is not allowed. Please upload files in: %s") % ", ".join(allowed_formats))

            # Check if file size exceeds the limit
            if len(rec.data_file) > max_file_size:
                raise models.ValidationError(_("The file size exceeds the maximum allowed size of 10 MB."))

    def unlink(self):
        is_senior_officer = self.user_has_groups("appsmod2.group_appsmod2_loan_officer")
        if not is_senior_officer:
            raise UserError(_("Document Deletion Allowed Only for User with Senior Officer Rights"))
        return super(DocumentsUniquelyApplicable, self).unlink()

    @api.onchange("data_file_name")
    def _onchange_data_filename(self):
        self.ensure_one()
        if self.data_file_name:
            filename = str(self.data_file_name)
            self.name = filename[:-4]
        else:
            self.name = "New"

    #  New method to preview document inline 
    def action_preview_document(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url = f"{base_url}/ti_cuda_report_viewer/static/src/lib/pdfjs/web/viewer.html?file=%2Fweb%2Fcontent%3Fmodel%3D{self._name}%26field%3Ddata_file%26id%3D{self.id}"

        return {
            'name': _("Attachment Preview"),
            'res_model': "ir.actions.act_url",
            'type': "ir.actions.act_url",
            'target': "new",
            'url': url
        }

class DocumentsApplicableApplicant(models.Model):
    _name = "documents.applicable.applicant"
    _description = "Documents Applicable Applicant"

    name = fields.Char("Document", required=True, default=lambda self: _("New"))
    data_file = fields.Binary("File", required=True, attachment=False)
    data_file_name = fields.Char("File Name")
    application_id = fields.Many2one("application", "Applicant", help="Application ID")
    applicant_type = fields.Selection(
        [("applicant1", "Applicant 1"), ("applicant2", "Applicant 2")],
        string="Applicant Type",
        store=True
        
    )

    @api.constrains('data_file_name','data_file')
    def _check_data_file_format_and_size(self):
        allowed_formats = ['pdf', 'jpg', 'jpeg', 'png']
        max_file_size = 10 * 1024 * 1024  # 10 MB
        for rec in self:
            # self.env['res.config.settings']._check_document_format_and_size(rec.data_file_name, rec.data_file)

            # Get file extension
            file_extension = rec.data_file_name.split('.')[-1].lower()

            # Check if file format is allowed
            if file_extension not in allowed_formats:
                raise models.ValidationError(_("The file format is not allowed. Please upload files in: %s") % ", ".join(allowed_formats))

            # Check if file size exceeds the limit
            if len(rec.data_file) > max_file_size:
                raise models.ValidationError(_("The file size exceeds the maximum allowed size of 10 MB."))

    def unlink(self):
        is_senior_officer = self.user_has_groups("appsmod2.group_appsmod2_loan_officer")
        if not is_senior_officer:
            raise UserError(_("Document Deletion Allowed Only for User with Senior Officer Rights"))
        return super(DocumentsUniquelyApplicable, self).unlink()

    @api.onchange("data_file_name")
    def _onchange_data_filename(self):
        self.ensure_one()
        if self.data_file_name:
            filename = str(self.data_file_name)
            self.name = filename[:-4]
        else:
            self.name = "New"

    #  New method to preview document inline 
    def action_preview_document(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url = f"{base_url}/ti_cuda_report_viewer/static/src/lib/pdfjs/web/viewer.html?file=%2Fweb%2Fcontent%3Fmodel%3D{self._name}%26field%3Ddata_file%26id%3D{self.id}"

        return {
            'name': _("Attachment Preview"),
            'res_model': "ir.actions.act_url",
            'type': "ir.actions.act_url",
            'target': "new",
            'url': url
        }
    

class JointlyApplicable(models.Model):
    _name = "jointly.applicable"
    _description = "Documents Jointly Applicable"

    def _default_application_id(self):
        return self.env.context.get("application_id", False)

    name = fields.Char("Checklist")
    provided = fields.Boolean("Provided")
    acceptable = fields.Boolean("Acceptable")
    notes = fields.Char("Notes")
    application_id = fields.Many2one("application", "Applicant", default=_default_application_id, help="Application ID")

    sequence = fields.Integer("Sequence")
    state = fields.Char("State")

    def action_show_document(self):
        pass
