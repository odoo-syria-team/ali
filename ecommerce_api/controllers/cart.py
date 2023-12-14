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



class Cart(http.Controller):
    
    url = 'https://gtec-security1.odoo.com'
    db = 'gtec-security1'
    username ='marketing@gtecsecurity.co.uk'
    password = 'GTECWeb$ite'

    @http.route('/cart/<int:product_id>',  auth="public",csrf=False, website=True, methods=['POST'])
    def add_item_to_cart(self,product_id, **kw):
        response = ''            
        authe = request.httprequest.headers
        product_id=int(product_id)
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
        product_data = models.execute_kw(self.db, uid, self.password, 'product.product', 'search_read', [[['id' , '=' , product_id]]],{'fields':['list_price','description_sale']})
        if valid_token:
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id']})

            user_partner = user_partner[0]['partner_id'][0]
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id']})
            if user_quot:
                print("user_quot[0]['id'] " ,user_quot[0]['id'] )
                
                cart_id= models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'create', [{'product_id':product_id,'order_id': int(user_quot[0]['id']) ,'name':user_quot[0]['description_sale'],'customer_lead': 2.0,'salesman_id': '1','price_unit':0.0,'product_uom_qty' : 1.0,'product_uom':'1'}])

                response=json.dumps({"data":[] , 'message' : 'Product had been added to your cart'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                cart_id= models.execute_kw(self.db, uid, self.password, 'sale.order', 'create', [{'partner_id' :user_partner }])
                cart_line_id= models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'create', [{'product_id' :product_id,'order_id': cart_id ,'name':user_quot[0]['description_sale'],'customer_lead': 2.0,'salesman_id': '1','price_unit':product_data[0]['list_price'],'product_uom_qty' : 1.0,'product_uom':'1'}])
                response=json.dumps({"data":[] , 'message' : 'Product had been added to your cart'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
            response=json.dumps({"data":[] , 'message' : 'Invalid Token'})
            return Response(
            response, status=403,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )



    @http.route('/cart/my_cart',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_my_cart(self, **kw):
        response = ''            
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
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id']})

            user_partner = user_partner[0]['partner_id'][0]
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id' , 'amount_total','amount_tax','amount_paid']})
            if user_quot:
                
                user_carts = models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'search_read', [[['order_id' , '=' , int(user_quot[0]['id'])]]],{'fields':['id','name' ,'product_uom','price_unit']})
                for i in user_carts:
                    product_id = i['id']
                    image_url = self.url + '/web/image?' + 'model=product.product&id=' + str(product_id) + '&field=image'
                    i['image'] = image_url
                response=json.dumps({"data":{'items':user_carts,'invoice':user_quot}, 'message' : 'Cart Details'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                response=json.dumps({"data":[], 'message' : "you don't have cart"})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
                
                response=json.dumps({"data":[] , 'message' : 'Invalid token'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)])

    @http.route('/cart/my_cart',  auth="public",csrf=False, website=True, methods=['POST'])
    def confirm_my_cart(self, **kw):
        response = ''            
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
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id']})

            user_partner = user_partner[0]['partner_id'][0]
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id' , 'amount_total','amount_tax','amount_paid']})
            if user_quot:
                
                user_carts = models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'search_read', [[['order_id' , '=' , int(user_quot[0]['id'])]]],{'fields':['id','name' ,'product_uom','price_unit']})
                id = int(user_carts[0]['id'])
                models.execute_kw(self.db, uid, self.password, 'sale.order', 'write', [[id], {'state': 'sale'}]) 
                models.execute_kw(self.db, uid, self.password, 'sale.order', 'write', [[id], {'state': 'done'}]) 
                response=json.dumps({"data":{'items':user_carts,'invoice':user_quot}, 'message' : 'Cart Details'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                response=json.dumps({"data":[], 'message' : "you don't have cart"})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
                
                response=json.dumps({"data":[] , 'message' : 'Invalid token'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)])


    @http.route('/cart/<int:id>',  auth="public",csrf=False, website=True, methods=['DELETE'])
    def delete_item_in_my_cart(self,id, **kw):
        response = ''            
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
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id']})

            user_partner = user_partner[0]['partner_id'][0]
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id' , 'amount_total','amount_tax','amount_paid']})
            if user_quot:
                result = models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'unlink', [[id]])
                user_carts = models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'search_read', [[['order_id' , '=' , int(user_quot[0]['id'])]]],{'fields':['id','name' ,'product_uom_qty','price_unit']})
                for i in user_carts:
                    product_id = i['id']
                    image_url = self.url + '/web/image?' + 'model=product.product&id=' + str(product_id) + '&field=image'
                    i['image'] = image_url
                response=json.dumps({"data":{'items':user_carts,'invoice':user_quot}, 'message' : 'Cart Details'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                response=json.dumps({"data":[], 'message' : "you don't have cart"})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
                
                response=json.dumps({"data":[] , 'message' : 'Invalid token'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)])


    @http.route('/cart/<int:id>',  auth="public",csrf=False, website=True, methods=['put'])
    def increase_item_in_my_cart(self,id,count, **kw):
        response = ''            
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
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id']})

            user_partner = user_partner[0]['partner_id'][0]
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id', 'amount_total','amount_tax','amount_paid']})
            if user_quot:
                models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'write', [[id], {'product_uom_qty': count}])    
                user_carts = models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'search_read', [[['order_id' , '=' , int(user_quot[0]['id'])]]],{'fields':['id','name' ,'product_uom_qty','price_unit']})
                for i in user_carts:
                    product_id = i['id']
                    image_url = self.url + '/web/image?' + 'model=product.product&id=' + str(product_id) + '&field=image'
                    i['image'] = image_url
                response=json.dumps({"data":{'items':user_carts,'invoice':user_quot}, 'message' : 'Cart Details'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                response=json.dumps({"data":[], 'message' : "you don't have cart"})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
                
                response=json.dumps({"data":[] , 'message' : 'Invalid token'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)])
