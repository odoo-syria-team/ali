from odoo.addons.website_crm.controllers.website_form import WebsiteForm

from odoo import http
from odoo.http import request


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
