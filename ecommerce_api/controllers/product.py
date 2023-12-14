from odoo import http
# from werkzeug.wrappers import Response
import logging
from datetime import datetime
import xmlrpc.client as xmlrpclib
import json
from odoo import models, fields, api
import math
import os
import requests
from odoo.http import request ,Response
# from odoo.http import JsonRequest
import re
import socket
from os import path
import random
import string

_logger = logging.getLogger(__name__)


from pathlib import Path



class Product(http.Controller):
    
    url = 'https://gtec-security1.odoo.com'
    db = 'gtec-security1'
    username ='marketing@gtecsecurity.co.uk'
    password = 'GTECWeb$ite'


    @http.route('/search',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_search(self,term=None):
        response = ''
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db,self.username, self.password, {})
        if term == None:
            response = json.dumps({ 'data': [], 'message': 'Please add keyword'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )
        if uid:

            # Search products by text
            text_search_domain = ['|',('name', 'ilike', str(term)),('description_sale', 'ilike', str(term))]
            product_ids = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [text_search_domain],{'fields':['id','name','type','uom_name', 'cost_currency_id','categ_id','list_price' ] })
            for product in product_ids:
                product_id = product['id']
                image_url = self.url + '/web/image?' + 'model=product.template&id=' + str(product_id) + '&field=image'
                product['image'] = image_url

            try:
                response = json.dumps({"data":{'product':product_ids},'message': 'All product'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

            except:
                response = json.dumps({"data":[],'message': 'No products for this Term'})
                return Response(
                response, status=404,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
                    
    



    @http.route('/categories/all', auth="public", csrf=False, website=True, methods=['GET'])
    def get_all_categories(self, page=int(1), limit=None):
        response = ''
        page = int(page)

        if page is None:
            page = int(1)
        else:
            pass
        if limit is None:
            limit = 10
        else:
            limit = int(limit)

        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})

        category_ids = models.execute_kw(self.db, uid, self.password, 'product.public.category', 'search_read',[[['parent_id', '=', False]]],{'fields': ['id', 'name', 'sequence']})
        for i in category_ids:
            category_id = i['id']
            image_url = self.url + '/web/image?' + 'model=product.public.category&id=' + str(category_id) + '&field=image_1920'
            i['image'] = image_url

        try:
            response = json.dumps({"data": {'categories': category_ids}, 'message': 'All Categories'})
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('accept', 'application/json'), ('Content-Length', 100)]
            )

        except:
            response = json.dumps({"data": [], 'message': 'No Categories now'})
            return Response(
                response, status=404,
                headers=[('Content-Type', 'application/json'), ('accept', 'application/json'), ('Content-Length', 100)]
            )


    @http.route('/categories/subcategories/<int:parent_id>',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_subcategories(self, parent_id):
        response = ''

       
        
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db,self.username, self.password, {})

        category_ids = models.execute_kw(
        self.db, uid, self.password, 'product.public.category', 'search_read',[[['parent_id', '=', parent_id]]],{'fields': ['id', 'name', 'sequence']})
        for i in category_ids:
            category_id = i['id']
            image_url = self.url + '/web/image?' + 'model=product.public.category&id=' + str(category_id) + '&field=image_1920'
            i['image'] = image_url
    
        try:
            response = json.dumps({"data":{'categories':category_ids},'message': 'All Categories'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        except:
            response = json.dumps({"data":[],'message': 'No Categories now'})
            return Response(
            response, status=404,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )
    
    @http.route('/category/product/<int:category_id>',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_product_by_category_id(self,category_id, page= int(1), **kw):
        response = ''

        page = int(page)

        if page == None:
            page = int(1)
        else:
            pass
        valid_token = False
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db,self.username, self.password, {})
        try:
            
            if authe:
                if 'Authorization' in authe:
                    token = authe['Authorization'].replace('Bearer ', '')
                    valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_token' , '=' , token]]],{'fields':['x_studio_user_name']})
                else :
                    pass
        except Exception as e:
            response = json.dumps({ 'data': 'no data', 'message': str(e)})
            return Response(
            response, status=401,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )

       
        if valid_token:
            product_id = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [[['public_categ_ids' , '=' , category_id]]],{'fields':['id','name','type','uom_name', 'cost_currency_id','categ_id','list_price'], 'offset': (page-1)*5, 'limit': 5})
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id','property_product_pricelist']})
            user_product_pricelist_id =user_partner[0]['property_product_pricelist'][0] 
            user_partner = user_partner[0]['partner_id'][0]
            
            
            
            product_price_list = models.execute_kw(self.db, uid, self.password, 'product.pricelist.item', 'search_read', [[['pricelist_id' , '=' , user_product_pricelist_id]]],{'fields':['product_id','fixed_price']})
            for product in product_id:
                for prod in user_product_pricelist_id:
                    if product['product_id'][0] == prod['product_id'][0] :
                        product['list_price'] = prod['fixed_price']
        else:
            product_id = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [[['categ_id' , '=' , category_id]]],{'fields':['id','name','type','uom_name', 'cost_currency_id','categ_id'], 'offset': (page-1)*5, 'limit': 5})
        x = 0
        for i in product_id:
            product_id = i['id']
            image_url = self.url + '/web/image?' + 'model=product.template&id=' + str(product_id) + '&field=image'
            i['image'] = image_url
            categ_id = i['categ_id'][0]

            categ_name = i['categ_id'][1]

            product_id[x]['categ_id'] = categ_id
            product_id[x]['categ_name'] = categ_name
            x+=1
        try:
            response = json.dumps({"data":{'product':product_id},'message': 'All product'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        except:
            response = json.dumps({"data":[],'message': 'No products for this ID'})
            return Response(
            response, status=404,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )


    @http.route('/product/<int:product_id>',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_product_by_id(self,product_id, page= int(1), **kw):
        response = ''

        page = int(page)

        if page == None:
            page = int(1)
        else:
            pass
            
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db,self.username, self.password, {})
        try:
            token = authe['Authorization'].replace('Bearer ', '')
            valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_token' , '=' , token]]],{'fields':['x_studio_user_name']})
        except Exception as e:
            response = json.dumps({ 'data': 'no data', 'message': 'Unauthorized!'})
            return Response(
            response, status=401,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )

       
        if valid_token:
            product_id = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [[['id' , '=' , product_id]]],{'fields':['id','name','type','uom_name', 'cost_currency_id','categ_id','list_price'], 'offset': (page-1)*5, 'limit': 5})
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id','property_product_pricelist']})
            user_product_pricelist_id =user_partner[0]['property_product_pricelist'][0] 
            user_partner = user_partner[0]['partner_id'][0]
            
            
            
            product_price_list = models.execute_kw(self.db, uid, self.password, 'product.pricelist.item', 'search_read', [[['pricelist_id' , '=' , user_product_pricelist_id]]],{'fields':['product_id','fixed_price']})
            for product in product_id:
                for prod in user_product_pricelist_id:
                    if product['product_id'][0] == prod['product_id'][0] :
                        product['list_price'] = prod['fixed_price']
        else:
            product_id = models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [[['id' , '=' , product_id]]],{'fields':['id','name','type','uom_name', 'cost_currency_id','categ_id'], 'offset': (page-1)*5, 'limit': 5})
        x = 0
        for i in product_id:
            product_id = i['id']
            image_url = self.url + '/web/image?' + 'model=product.template&id=' + str(product_id) + '&field=image'
            i['image'] = image_url
            categ_id = i['categ_id'][0]

            categ_name = i['categ_id'][1]

            product_id[x]['categ_id'] = categ_id
            product_id[x]['categ_name'] = categ_name
            x+=1
        try:
            response = json.dumps({"data":{'product':product_id},'message': 'All product'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        except:
            response = json.dumps({"data":[],'message': 'No products for this ID'})
            return Response(
            response, status=404,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )


    @http.route('/shipping/all',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_shipping_methods(self, **kw):
        response = ''

        
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db,self.username, self.password, {})
        
        shipping_id = models.execute_kw(self.db, uid, self.password, 'delivery.carrier', 'search_read', [[['id' , '!=' , 1]]],{'fields':['id','name','delivery_type','fixed_price', 'free_over','amount']})
        
      
        
        try:
            response = json.dumps({"data":{'shipping_methods':shipping_id},'message': 'All shipping methods'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        except:
            response = json.dumps({"data":[],'message': 'No shipping methods now'})
            return Response(
            response, status=404,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

    
    @http.route('/shipping/<int:shipping_id>',  auth="public",csrf=False, website=True, methods=['POST'])
    def add_shipping_to_cart(self,shipping_id, **kw):
        response = ''
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url), allow_none=True)
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url), allow_none=True)
        uid = common.authenticate(self.db,self.username, self.password, {})
        try:
            token = authe['Authorization'].replace('Bearer ', '')
            valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_token' , '=' , token]]],{'fields':['x_studio_user_name']})
        except Exception as e:
            response = json.dumps({ 'data': 'no data', 'message': 'Unauthorized!'})
            return Response(
            response, status=401,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )

       
        if valid_token:
            shipping_id = models.execute_kw(self.db, uid, self.password, 'delivery.carrier', 'search_read', [[['id' , '=' , shipping_id]]],{'fields':['id','name','delivery_type','fixed_price', 'free_over','amount','product_id']})
            user_id =int(valid_token[0]['x_studio_user_name'][0])
            print('shipping_id >>>>>>' , shipping_id) 
            print('shipping_id >>>>>>' , shipping_id[0]['name'])
            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id','property_product_pricelist']})
            user_product_pricelist_id =user_partner[0]['property_product_pricelist'][0] 
            user_partner = user_partner[0]['partner_id'][0]
            
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id']})
            if user_quot:
                
                print('user_quot' , user_quot[0]['id'])
                
                try:
                    product_ship_id =  models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [[['id' , '=' , shipping_id[0]['product_id'][0]]]],{'fields':['lst_price' , 'product_tmpl_id']})
                    print('product_ship_id' , product_ship_id)
                    product_ship_temp_id =  models.execute_kw(self.db, uid, self.password, 'product.template', 'search_read', [[['id' , '=' , int(product_ship_id[0]['product_tmpl_id'][0])]]],{'fields':['list_price']})
                    print('product_ship_id' , product_ship_id)
                    cart_line_id= models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'create', [{'product_id' :shipping_id[0]['product_id'][0],'order_id': user_quot[0]['id'] ,'name':shipping_id[0]['name'],'customer_lead': 2.0,'salesman_id': '1','price_unit' :product_ship_temp_id[0]['list_price'],'product_uom_qty' : 1.0,'product_uom':'1'}])
                except Exception as e: 
                    response=json.dumps({"data":[],"message":str(e)})
                    return Response(
                    response, status=403,
                    headers=[('Content-Type', 'application/json'), ('Accept', 'application/json')]
                )

            else:
                response = json.dumps({"data":[],'message': "You don't have cart to add shipping method"})
                return Response(
                response, status=404,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )
        else:
            response = json.dumps({"data":[],'message': 'Invalid Token'})
            return Response(
            response, status=403,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )
        try:
            response = json.dumps({"data":{'shipping_methods':shipping_id},'message': 'All shipping methods'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        except:
            response = json.dumps({"data":[],'message': 'No shipping methods now'})
            return Response(
            response, status=404,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

    