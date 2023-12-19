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
    
    