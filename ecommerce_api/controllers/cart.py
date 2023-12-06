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
        product_data = models.execute_kw(self.db, uid, self.password, 'product.product', 'search_read', [[['id' , '=' , product_id]]],{'fields':['list_price']})
        if valid_token:
            user_id =int(valid_token[0]['x_studio_user_name'][0])

            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]],{'fields':['partner_id']})

            user_partner = user_partner[0]['partner_id'][0]
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id']})
            if user_quot:
                print("user_quot[0]['id'] " ,user_quot[0]['id'] )
                
                cart_id= models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'create', [{'product_id':product_id,'order_id': int(user_quot[0]['id']) ,'name':'a','customer_lead': 2.0,'salesman_id': '1','price_unit':0.0,'product_uom_qty' : 1.0,'product_uom':'1'}])

                response=json.dumps({"data":[] , 'message' : 'Product had been added to your cart'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                cart_id= models.execute_kw(self.db, uid, self.password, 'sale.order', 'create', [{'partner_id' :user_partner }])
                cart_line_id= models.execute_kw(self.db, uid, self.password, 'sale.order.line', 'create', [{'product_id' :product_id,'order_id': cart_id ,'name':'a','customer_lead': 2.0,'salesman_id': '1','price_unit':product_data[0]['list_price'],'product_uom_qty' : 1.0,'product_uom':'1'}])
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
