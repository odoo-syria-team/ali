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



class Banners(http.Controller):
    
    url = 'https://gtec-security1.odoo.com'
    db = 'gtec-security1'
    username ='marketing@gtecsecurity.co.uk'
    password = 'GTECWeb$ite'


    @http.route('/banners',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_mybanners(self, **kw):
        response = ''            
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db,self.username, self.password, {})

        banners = models.execute_kw(self.db, uid, self.password, 'x_slider_gtec', 'search_read', [[['id' , '!=' , 0]]],{'fields':['id']})
        x = 0
        if banners:
            for i in banners:
                
                banners_id = i['id']
                image_url = self.url + '/web/image?' + 'model=x_slider_gtec&id=' + str(banners_id) + '&field=x_studio_binary_field_64g_1hi0esu21'
                i['image'] = image_url            
                x += 1
        
        else:
            response = json.dumps({"data":{'banners':[]},'message': 'No Images'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        
        try:
            response = json.dumps({"data":{'banners':banners},'message': 'All Images'})
            return Response(
            response, status=200,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

        except:
            response = json.dumps({"data":[],'message': 'No Images found'})
            return Response(
            response, status=404,
            headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
        )

    @http.route('/cart/addres',  auth="public",csrf=False, website=True, methods=['GET'])
    def add_address_to_cart(self, **kw):
        response = ''            
        body =json.loads(request.httprequest.data)
        po_ref = body.get('reference', False)
        comment = body.get('comment', False)
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
            user_quot = models.execute_kw(self.db, uid, self.password, 'sale.order', 'search_read', [['&',['state' ,'=' ,'draft'],['partner_id' , '=' , user_partner]]],{'fields':['id','message_ids']})
            if user_quot:
                
                log_note = {
                    'body': 'Comment : %s' % comment,
                    'model': 'sale.order',
                    'res_id': user_quot[0]['id'],
                    'message_type': 'comment',
                }

                # Append the log note to the existing messages
                existing_messages = user_quot[0]['message_ids'].append((0, 0, log_note))
                
                id = int(user_quot[0]['id'])
                # Update the chatter field of the sale order with the updated messages
                x = models.execute_kw(self.db,uid,self.password,'mail.message','create', [{'body': 'Comment : %s' % comment,
                    'model': 'sale.order',
                    'res_id': user_quot[0]['id'],
                    'message_type': 'comment',}])
                 
                response=json.dumps({"data":[] , 'message' : 'address had been added to your cart'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                response=json.dumps({"data":[] , 'message' : 'this cart not belong to you '})
                return Response(
                response, status=403,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
                response=json.dumps({"data":[] , 'message' : 'Invlid Token'})
                return Response(
                response, status=403,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )