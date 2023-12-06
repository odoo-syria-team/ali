from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, AccessDenied
from odoo.addons.portal.controllers.portal import pager
from odoo.addons.portal.controllers import portal
# from bs4 import BeautifulSoup
# import json, re
import base64


# document list view
class DocumentNikkiTemplate(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(DocumentNikkiTemplate, self)._prepare_home_portal_values(counters)
        values['document_count'] = request.env['document.nikki'].search_count(
            [('partner_id', '=', request.env.user.partner_id.id)])
        return values

    @http.route(['/my/documents', '/my/documents/page/<int:page>'], auth="user", csrf=False, website=True,
                methods=['GET'])
    def get_documents(self, sortby='id', page=1, search='', search_in='Category'):

        try:
            sorted_list = {
                'id': {'label': 'Latest', 'order': 'id desc'},
                'file_name': {'label': 'File Name', 'order': 'file_name'},
                'category_id': {'label': 'Category', 'order': 'category_id'}
            }
            default_order_by = sorted_list[sortby]['order']
            search_list = {
                'File Name': {'label': 'File Name', 'input': 'File Name', 'domain': [('file_name', 'ilike', search),
                                                                                     ('partner_id', '=',
                                                                                      request.env.user.partner_id.id)]},
                'Category': {'label': 'Category', 'input': 'Category', 'domain': [('category_id.name', 'ilike', search),
                                                                                  ('partner_id', '=',
                                                                                   request.env.user.partner_id.id)]},
            }
            search_domain = search_list[search_in]['domain']

            total_document_ids = http.request.env['document.nikki'].sudo().search_count(search_domain)

            page_details = pager(url='/my/documents',
                                 total=total_document_ids,
                                 page=page,
                                 url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
                                 step=10
                                 )

            document_ids = http.request.env['document.nikki'].sudo().search(search_domain,
                                                                            limit=10, order=default_order_by,
                                                                            offset=page_details['offset'])

            return request.render('niki_sulotion.document_nikki_list', {
                'user_id': request.env.user,
                'page_name': 'document_list_page',
                'document_ids': document_ids,
                'pager': page_details,
                'sortby': sortby,
                'search_in': search_in,
                'search': search,
                'searchbar_inputs': search_list,
                'searchbar_sortings': sorted_list
            })
        except UserError as e:
            return str(e)
        except Exception as e:
            return str(e)


# document form view
class DocumentNikkiTemplateFrom(http.Controller):
    @http.route('/my/documents/<int:document_id>', auth="user", csrf=False, website=True, methods=['GET', 'POST'])
    def get_document_record(self, document_id):
        user_document_id = request.env['document.nikki'].sudo().search(
            [('id', '=', document_id), ('partner_id', '=', request.env.user.partner_id.id)])
        if request.httprequest.method == 'POST':
            try:
                self._write_vals(user_document_id)

                return request.redirect('/my/documents')

            except UserError as e:
                return str(e)
            except Exception as e:
                return str(e)

        else:
            try:
                if document_id not in user_document_id.ids:
                    raise AccessDenied()

                return request.render('niki_sulotion.document_nikki_form', {
                    'user_id': request.env.user,
                    'page_name': 'documnet_form_page',
                    'document_id': user_document_id,
                    'category_ids': http.request.env['category.nikki'].sudo().search([]),
                    'file_data_base64': base64.b64encode(user_document_id.file_data)
                })
            except UserError as e:
                return str(e)
            except Exception as e:
                return str(e)

    # create document record
    @http.route('/my/documents/create', auth="user", csrf=False, website=True, methods=['GET', 'POST'])
    def create_document_record(self):
        if request.httprequest.method == 'POST':
            try:
                document_id = request.env['document.nikki'].sudo().create(
                    {'partner_id': request.env.user.partner_id.id})
                self._write_vals(document_id)
                return request.redirect('/my/documents')

            except UserError as e:
                return str(e)
            except Exception as e:
                return str(e)

        else:
            try:
                return request.render('niki_sulotion.document_nikki_form', {
                    'user_id': request.env.user,
                    'page_name': 'documnet_create_page',
                    'category_ids': http.request.env['category.nikki'].sudo().search([]),
                })
            except UserError as e:
                return str(e)
            except Exception as e:
                return str(e)

    def _write_vals(self, user_document_id):

        form_dict = {}
        form_file_dict = {}
        document_vals = {}

        form = request.httprequest.form
        form_files = request.httprequest.files
        for key, value in zip(form.keys(), form.values()):
            form_dict[key] = form.getlist(key)

        for key, value in zip(form_files.keys(), form_files.values()):
            form_file_dict[key] = form_files.getlist(key)

        for key, value in zip(form_dict.keys(), form_dict.values()):
            if key == 'category_id':
                document_vals[key] = request.env['category.nikki'].sudo().search([('id', '=', value[0])])
            if key == 'file_name':
                document_vals[key] = value[0]

        for key, value in zip(form_file_dict.keys(), form_file_dict.values()):
            if 'check_file' in form_dict.keys():
                if key == 'file_data':
                    document_vals['file_data'] = base64.b64encode(value[0].read())

        user_document_id.sudo().write(document_vals)

    # delete record
    @http.route('/my/documents/delete/<int:document_id>', auth="user", csrf=False, website=False,
                methods=['GET', 'POST'])
    def delete_document_record(self, document_id):
        try:
            user_document_id = request.env['document.nikki'].sudo().search(
                [('id', '=', document_id), ('partner_id', '=', request.env.user.partner_id.id)])
            if user_document_id:
                user_document_id.sudo().unlink()
            return request.redirect('/my/documents')

        except UserError as e:
            return str(e)
        except Exception as e:
            return str(e)
