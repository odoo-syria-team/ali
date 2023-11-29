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
import jwt
import re
import werkzeug.wrappers
import socket
from os import path
from pathlib import Path 
import pathlib
from telesign.messaging import MessagingClient
from os import environ
from dotenv import load_dotenv
_logger = logging.getLogger(__name__)
load_dotenv()

from pathlib import Path



class Auth(http.Controller):
    url = os.getenv('URL')
    db = os.getenv('db')
    username = os.getenv('username')
    password = os.getenv('password')
    
    
    
    def check_phone_num(self,data):
            val=data

            if val.isdigit():

                return True

            else:
                return False

    
    def _pass_validate(self,data):
        # for i in data:
        #     
        if data:
            pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?.!@$%^&*-])(?=.*\d).{8,}$")
                                
            val = pattern.match(data) 
           
            return val
    def _validation(self,data):
        data = str(data)
        if len(data) != 0 :
            return True
        elif len(data) == 0:
            return False
        else:
            pass
    
    def check_email(self,email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # pass the regular expression
        # and the string into the fullmatch() method
        if(re.fullmatch(regex, email)):
            pass
        else:
            return False
        return True
    @http.route('/auth/register',  auth="public",csrf=False, website=True, methods=['POST'])
    def register(self,idd= None, **kw):      
        
        response = ''  
        body =json.loads(request.httprequest.data)
        username = body['full_name']
        password = body['password']
        email = body['email']
        
        username_validation = self._validation(username)
        password_validation = self._pass_validate(password)
        email_validation = self.check_email(email)

        if username_validation == False:
            response = json.dumps({"data":[],'message': 'يرجى إدخال الاسم '})
            return Response(
            response, status=422,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )

        if email_validation == False:
            response = json.dumps({"data":[],'message': 'Please insert valid e-mail'})
            return Response(
            response, status=422,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )
        
        if password_validation == None:
            response = json.dumps({"data":[],'message': 'يرجى إدخال كلمة المرور تحتوي على 8 محارف على الأقل و حرف كبير و حرف صغير و رمز ولاتحتوي على فراغات'})
            return Response(
            response, status=422,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )

        
        
        
        uid = False
        
        
        
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        if not uid:
            
            uid = common.authenticate(self.db,self.username, self.password, {})
            
       
       
        is_there= models.execute_kw(self.db, uid, self.password, 'res.users', 'search_count', [[['login', '=', email]]])
        
        if is_there != 0:
            response = json.dumps({"data":[],'message': 'This email was used'})
            return Response(
            response, status=422,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )
        else :

            user_id = models.execute_kw(self.db, uid, self.password, 'res.users', 'create', [{'name': username, 'password' : password, 'login' :email  }])
           
            if user_id :
                date_now = str(datetime.today())
            
                # payload = {
                #     'id': user_id,
                #     'username': username,
                #     'password': password ,
                #     'timestamp' : date_now,}
                # SECRET='ali.ammar'
                # enc = jwt.encode(payload, SECRET) 
                # is_token =models.execute_kw(self.db, uid, self.password, 'user.token', 'search_count', [[['user_id' , '=', user_id]]])  
                
                
                # create_user_verification = models.execute_kw(self.db, uid, self.password, 'user.verification', 'create', [{'user_id': user_id, 'type' : '2','is_valid' : True}])
              
              

                # image_path=user[0]['image_path']
                user_details = {"id":user_id,"username" :username,"email":email,"timestamp":date_now}
                
                # if is_token:
                #     models.execute_kw(self.db, uid, self.password, 'user.token', 'write', [['user_id' , '=' , user_id], {'token': enc}])
                # else :
                #     models.execute_kw(self.db, uid, self.password, 'user.token', 'create', [{'user_id': user_id, 'token': enc }])
                # user_token='{"data" :{user:{"%s"} ,"token" : {"%s"} }'%(user_details , enc)
                # response =json.dumps({user_token})
                # user_ver_code = request.env['user.verification'].with_user(2).search([('id','=',create_user_verification)])
                # user_ver_code =models.execute_kw(self.db, uid, self.password,'user.verification', 'search_read', [[['id' , '=' , create_user_verification]] ],{'fields': ['code','is_valid']})
                
              
                response=json.dumps({"data":{"user":user_details}})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )