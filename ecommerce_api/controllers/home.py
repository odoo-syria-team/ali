from odoo import http
from odoo.http import request, Response
import xmlrpc.client as xmlrpclib
import json


class Home(http.Controller):
    url = 'https://gtec-security1.odoo.com'
    db = 'gtec-security1'
    username = 'marketing@gtecsecurity.co.uk'
    password = 'GTECWeb$ite'

    @http.route('/home', auth="public", csrf=False, website=True, methods=['GET'])
    def home(self, **kw):
        try:
            response = ''
            valid_token = False
            authe = request.httprequest.headers
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            uid = common.authenticate(self.db, self.username, self.password, {})

            banner_ids = models.execute_kw(self.db, uid, self.password, 'x_slider_gtec', 'search_read',
                                           [[['id', '!=', 0]]], {'fields': ['id']})
            for banner_id in banner_ids:
                banners = banner_id['id']
                image_url = self.url + '/web/image?' + 'model=x_slider_gtec&id=' + str(
                    banners) + '&field=x_studio_binary_field_64g_1hi0esu21'
                banner_id['image'] = image_url

            category_ids = models.execute_kw(self.db, uid, self.password, 'product.public.category', 'search_read',
                                             [[['parent_id', '=', False]]],
                                             {'fields': ['id', 'name', 'sequence', 'x_studio_brand']})
            for category_id in category_ids:
                category = category_id['id']
                category_id['image'] = self.url + '/web/image?' + 'model=product.public.category&id=' + str(category) + '&field=image_1920'

                sub_category_ids = models.execute_kw(
                    self.db, uid, self.password, 'product.public.category', 'search',
                    [[['parent_id', '=', category]]]
                )

                if sub_category_ids:
                    category_id['sub_category'] = True
                else:
                    category_id['sub_category'] = False

            try:
                if authe:
                    if 'Authorization' in authe:
                        token = authe['Authorization'].replace('Bearer ', '')
                        valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read',
                                                        [[['x_studio_user_token', '=', token]]],
                                                        {'fields': ['x_studio_user_name']})
                    else:
                        pass

            except Exception as e:
                response = json.dumps({'data': 'no data', 'message': str(e)})
                return Response(
                    response, status=401,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
                )

            crm_tag = models.execute_kw(self.db, uid, self.password, 'product.tag', 'search_read',
                                        [[['name', '=', 'featured']]], {'fields': ['id', 'name']})
            if crm_tag:
                id = crm_tag[0]['id']
                if valid_token:

                    products = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read',
                                                 [[['product_tag_ids', '=', id]]], {
                                                     'fields': ['id', 'name', 'type', 'uom_name', 'cost_currency_id',
                                                                'categ_id', 'list_price', 'description_sale',
                                                                'x_studio_specifications', 'x_studio_why_and_when',
                                                                'x_studio_product_feature_mobile', 'tax_string']})
                    user_id = int(valid_token[0]['x_studio_user_name'][0])

                    user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read',
                                                     [[['id', '=', user_id]]],
                                                     {'fields': ['partner_id', 'property_product_pricelist']})
                    user_product_pricelist_id = user_partner[0]['property_product_pricelist']
                    user_partner = user_partner[0]['partner_id'][0]

                    product_price_list = models.execute_kw(self.db, uid, self.password, 'product.pricelist.item',
                                                           'search_read',
                                                           [[['pricelist_id', '=', user_product_pricelist_id]]],
                                                           {'fields': ['product_id', 'fixed_price']})
                    for product in products:
                        for prod in product_price_list:
                            if product['product_id'][0] == prod['product_id'][0]:
                                product['list_price'] = prod['fixed_price']
                else:
                    products = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read',
                                                 [[['product_tag_ids', '=', id]]], {
                                                     'fields': ['id', 'name', 'type', 'uom_name', 'cost_currency_id',
                                                                'categ_id', 'list_price', 'description_sale',
                                                                'x_studio_specifications', 'x_studio_why_and_when',
                                                                'x_studio_product_feature_mobile', 'tax_string']})
                x = 0
                for i in products:
                    product_id = i['id']
                    image_url = self.url + '/web/image?' + 'model=product.template&id=' + str(
                        product_id) + '&field=image_1920'
                    i['image'] = image_url
                    categ_id = i['categ_id'][0]
                    categ_name = i['categ_id'][1]
                    products[x]['categ_name'] = categ_name
                    products[x]['categ_id'] = categ_id
                    # if products[x]['tax_string']:
                    #     products[x]['list_price'] = self.extract_float_value(products[x]['tax_string'])
                    # products[x]['list_price'] = products[x]['list_price'] if valid_token else None
                    products[x]['list_price'] = products[x]['list_price'] if valid_token else None
                    x += 1

            else:
                products = []

            response = json.dumps({"data": {'banners': banner_ids, 'categories': category_ids, 'product': products}, 'message': 'All Images'})
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('accept', 'application/json'), ('Content-Length', 100)]
            )

        except Exception as e:
        
            response = json.dumps({'message': str(e)})
        
            return Response(response, status=500, headers=[('Content-Type', 'application/json')])
