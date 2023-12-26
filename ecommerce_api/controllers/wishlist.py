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



class WishList(http.Controller):
    
    url = 'https://gtec-security1.odoo.com'
    db = 'gtec-security1'
    username ='marketing@gtecsecurity.co.uk'
    password = 'GTECWeb$ite'

    @http.route('/wishlist/mine',  auth="public",csrf=False, website=True, methods=['GET'])
    def get_my_wishlist(self,idd= None, **kw): 
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
            user_wishlist = models.execute_kw(self.db, uid, self.password, 'product.wishlist', 'search_read', [[['partner_id' , '=' , user_partner]]],{'fields':['id' , 'partner_id','price','product_id']})
            if user_wishlist:
                
                for i in user_wishlist:
                    product_id = i['product_id']
                    image_url = self.url + '/web/image?' + 'model=product.product&id=' + str(product_id) + '&field=image'
                    i['image'] = image_url
                response=json.dumps({"data":{'wishlist':user_wishlist}, 'message' : 'wishlist Details'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
            else:
                response=json.dumps({"data":[], 'message' : "you don't have wishlist"})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )
        else:
                
                response=json.dumps({"data":[] , 'message' : 'Invalid token'})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)])

    @http.route('/wishlist/<int:product_id>', auth="public", csrf=False, website=True, methods=['POST'])
    def add_to_wishlist(self, product_id, **kw):
        response = ''
        
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})
        
        try:
            token = authe['Authorization'].replace('Bearer ', '')
            valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read',
                                            [[['x_studio_user_token', '=', token]]],
                                            {'fields': ['x_studio_user_name']})
        except Exception as e:
            response = json.dumps({'data': 'no data', 'message': 'Unauthorized!'})
            return Response(
                response, status=401,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
            )
        
        if valid_token:
            user_id = int(valid_token[0]['x_studio_user_name'][0])
            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read',
                                            [[['id', '=', user_id]]], {'fields': ['partner_id']})
            user_partner = user_partner[0]['partner_id'][0]
            
            # Check if the product with the given ID exists
            product_exists = models.execute_kw(self.db, uid, self.password, 'product.product', 'search_count',
                                                [[['id', '=', product_id]]])
            if product_exists:
                # Create a new record in the product.wishlist model
                wishlist_data = {
                    'partner_id': user_partner,
                    'product_id': product_id,
                    'website_id' : 1
                }
                wishlist_id = models.execute_kw(self.db, uid, self.password, 'product.wishlist', 'create', [wishlist_data])
                
                if wishlist_id:
                    response = json.dumps({'data': {'wishlist_id': wishlist_id}, 'message': 'Product added to wishlist'})
                    return Response(
                        response, status=200,
                        headers=[('Content-Type', 'application/json'), ('accept', 'application/json'),
                                ('Content-Length', 100)]
                    )
            else:
                response = json.dumps({'data': [], 'message': 'Product does not exist'})
                return Response(
                    response, status=404,
                    headers=[('Content-Type', 'application/json'), ('accept', 'application/json'),
                            ('Content-Length', 100)]
                )
        else:
            response = json.dumps({'data': [], 'message': 'Invalid token'})
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('accept', 'application/json'), ('Content-Length', 100)]
            )

    @http.route('/wishlist/<int:wishlist_id>', auth="public", csrf=False, website=True, methods=['DELETE'])
    def delete_from_wishlist(self, wishlist_id=None, **kw):
        response = ''
        
        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})
        
        try:
            token = authe['Authorization'].replace('Bearer ', '')
            valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read',
                                            [[['x_studio_user_token', '=', token]]],
                                            {'fields': ['x_studio_user_name']})
        except Exception as e:
            response = json.dumps({'data': 'no data', 'message': 'Unauthorized!'})
            return Response(
                response, status=401,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
            )
        
        if valid_token:
            user_id = int(valid_token[0]['x_studio_user_name'][0])
            user_partner = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read',
                                            [[['id', '=', user_id]]], {'fields': ['partner_id']})
            user_partner = user_partner[0]['partner_id'][0]
            
            # Check if the wishlist ID exists
            wishlist_exists = models.execute_kw(self.db, uid, self.password, 'product.wishlist', 'search_count',
                                                [[['id', '=', wishlist_id], ['partner_id', '=', user_partner]]])
            if wishlist_exists:
                # Delete the wishlist item
                models.execute_kw(self.db, uid, self.password, 'product.wishlist', 'unlink', [[wishlist_id]])
                
                response = json.dumps({'data': {'wishlist_id': wishlist_id}, 'message': 'Product removed from wishlist'})
                return Response(
                    response, status=200,
                    headers=[('Content-Type', 'application/json'), ('accept', 'application/json'),
                            ('Content-Length', 100)]
                )
            else:
                response = json.dumps({'data': [], 'message': 'Wishlist item does not exist'})
                return Response(
                    response, status=404,
                    headers=[('Content-Type', 'application/json'), ('accept', 'application/json'),
                            ('Content-Length', 100)]
                )
        else:
            response = json.dumps({'data': [], 'message': 'Invalid token'})
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('accept', 'application/json'), ('Content-Length', 100)]
            )