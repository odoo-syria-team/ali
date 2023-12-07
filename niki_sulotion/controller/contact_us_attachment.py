from odoo.addons.website_crm.controllers.website_form import WebsiteForm
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, AccessDenied
import base64


class CrmContactUsControllerInherit(http.Controller):
    @http.route(['/web/attachment'], type='json', auth='public')
    def create_attachment(self, **dat):
        data_list = []
        print("========", dat)
        for data in dat['data']:
            data = data.split('base64')[1] if data else False
            data_list.append((0, 0, {'attachments': data}))
        request.env['ir.attachment'].sudo().create(
            {
                'name': dat['name'],
                'type': 'binary',
                'datas': 'data'
            })


class WebsiteFormInherit(WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        result = super(WebsiteFormInherit, self).insert_record(request, model, values, custom, meta=meta)
        if model.model == 'crm.lead':
            lead_sudo = request.env['crm.lead'].sudo()
            last_lead = lead_sudo.search([], order='create_date desc', limit=1)
            print("model-----------------", model.model)
            print("values-----------------", values)
            # if lead_sudo:
            print("last_lead-----------------", last_lead)

        return result


# contact us form view
class ContactUSFrom(http.Controller):
    @http.route('/contactus', auth="public", csrf=False, website=True,
                methods=['GET', 'POST'])
    def contact_us(self, **post):
        if request.httprequest.method == 'POST':
            # try:
                self._write_vals()

                return request.redirect('/contactus-thank-you')

            # except UserError as e:
            #     return str(e)
            # except Exception as e:
            #     return str(e)

        else:
            try:
                return request.render('niki_sulotion.conatct_us_form_inherit', {})
            except UserError as e:
                return str(e)
            except Exception as e:
                return str(e)

    def _write_vals(self):

        form_dict = {}
        file_name = 'Attachment'
        crm_lead_vals = {}

        form = request.httprequest.form
        files = request.httprequest.files

        for key, value in zip(form.keys(), form.values()):
            form_dict[key] = form.getlist(key)

        attachment = files.get('attachments')
        content = base64.b64encode(attachment.read())
        length = len(content)

        for key, value in zip(form_dict.keys(), form_dict.values()):
            print('===================', key, value)
            if key in ['partner_name', 'phone', 'email_from', 'description', 'name']:
                crm_lead_vals[key] = value[0]

            if key == 'partner_id':
                if request.env.user.id != 4:
                    crm_lead_vals[key] = request.env.user.partner_id.id
                    crm_lead_vals['user_id'] = request.env.user.id
                if request.env.user.id == 4:
                    crm_lead_vals['contact_name'] = value[0]
                    crm_lead_vals['user_id'] = None

            if key == 'file_name':
                file_name = value[0]

        crm_lead_id = request.env['crm.lead'].sudo().create(crm_lead_vals)
        if length != 0:
            request.env['ir.attachment'].sudo().create({
                'name': file_name,
                'res_id': crm_lead_id.id,
                'res_model': 'crm.lead',
                'datas': content,
            })