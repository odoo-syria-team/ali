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



class Auth(http.Controller):
    
    url = 'https://gtec-security1.odoo.com'
    db = 'gtec-security1'
    username ='marketing@gtecsecurity.co.uk'
    password = 'GTECWeb$ite'
    
    
    
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


    def generate_random_key(self,length=32):
        """
        Generate a random key without using secrets.

        :param length: Length of the key (default is 32 characters).
        :type length: int
        :return: A randomly generated key.
        :rtype: str
        """
        characters = string.ascii_letters + string.digits
        key = ''.join(random.choice(characters) for _ in range(length))
        return key
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
        confirm_password = body['confirm_password']
        email = body['email']
        phone = body['phone']
        
        username_validation = self._validation(username)
        # password_validation = self._pass_validate(password)
        email_validation = self.check_email(email)
        if confirm_password != password:
            response = json.dumps({"data":[],'message': 'Make sure your passwor and confirm password are the same'})
            return Response(
            response, status=422,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )
        if username_validation == False:
            response = json.dumps({"data":[],'message': 'Please add your name'})
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

            user_id = models.execute_kw(self.db, uid, self.password, 'res.users', 'create', [{'name': username, 'password' : password,'phone' : phone, 'login' :email ,'groups_id': [(6, 0, [models.execute_kw(self.db, uid, self.password, 'res.groups', 'search', [[('name', '=', 'Portal')]])[0]])] }])
           
            if user_id :
                date_now = str(datetime.today())
                key = self.generate_random_key()
                user_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'create', [{'x_name' :key,'x_studio_user_name': user_id, 'x_studio_user_token' : key  }])
                user_details = {"id":user_id,"username" :username,"email":email,"phone" :phone ,"timestamp":date_now}
                
                
              
                response=json.dumps({"data":{"user":user_details,'token' :key}})
                return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'),('accept','application/json'), ('Content-Length', 100)]
            )

    @http.route('/auth/log_in', auth="public",csrf=False, website=True, methods=['POST'])
    def log_in(self,idd= None, **kw):               
            body =json.loads(request.httprequest.data)
            uid = False
            login = body['email']
            message = ''
            password = body['password']
                
                
            sucess_login=False
            
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            uid = common.authenticate(self.db,self.username, self.password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            check_archive_profile = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['login' , '=' , login]]], {
                                        'fields': ['name']})
            if check_archive_profile != []:
                 models.execute_kw(self.db, uid, self.password, 'res.users', 'write', [[check_archive_profile[0]['id']], {'active': True}])
                 
            user_id = common.authenticate(self.db,login, password, {})
            if user_id==False :
                    response=json.dumps({"data":[],'message': 'Email or Password is incorrect'})
                    return Response( response, status=402,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
                    )
            
            
            elif user_id:
                user_data = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' , user_id]]], {
                                        'fields': ['name' , 'phone']})
                
                key = self.generate_random_key()
                user_token_data = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_name' , '=' , user_id]]], {
                                        'fields': ['x_studio_user_name']})
                if user_token_data:

                    user_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'write', [[user_token_data[0]['id']], {'x_name' :key ,'x_studio_user_token': key}])
                else:
                    user_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'create', [{'x_name' :key,'x_studio_user_name': user_id, 'x_studio_user_token' : key  }])

                username = user_data[0]['name']
                date_now = str(datetime.today())
                user_details = [{"id":user_id,"username" :username,"phone" :user_data[0]['phone'] ,"email":login ,"timestamp":date_now}]
                response=json.dumps({"data":{"user":user_details[0],"token":key}, 'message':message})
                return Response( response,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
                )
            else : 
                user_details = [{"id":user_id,"username" :username,"phone" :user_data[0]['phone'] ,"email":login ,"timestamp":date_now}]
                response=json.dumps({"data":{"user":user_details[0] ,"token":key}, 'message':message}) 
                return Response( response, 
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)] 
                )

    @http.route('/auth/log_out', auth="public", csrf=False, website=True, methods=['POST'])
    def log_out(self, idd=None, **kw):
        try:
            authe = request.httprequest.headers

            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            uid = common.authenticate(self.db, self.username, self.password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

            token = authe['Authorization'].replace('Bearer ', '')
            user_token_data = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_token' , '=' , token]]], {
                                        'fields': ['x_studio_user_name']})
            print(' >>>>>>>>>>>> ' , user_token_data)
            if user_token_data:
                print('1')
                user_token = models.execute_kw(
                    self.db, uid, self.password,
                    'x_user_token', 'write', [[int(user_token_data[0]['id'])], {'x_name': ' ', 'x_studio_user_token': ' '}]
                )
                print('1')
                response = {"data": [], 'message': 'You have been logged out'}
                return Response(
                    json.dumps(response), status=200,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', len(response))]
                )
            else:
                response = {"data": [], 'message': 'Invalid Token'}
                return Response(
                    json.dumps(response), status=401,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', len(response))]
                )
        except Exception as e:
            response = json.dumps({'data': 'no data', 'message': str(e)})
            return Response(
                response, status=403,
                headers=[('Content-Type', 'application/json'), ('Content-Length', len(response))]
            )




    @http.route('/edit_profile',  auth="public",csrf=False, website=True, methods=['POST'])
    def edit_profile(self, **kw):
        

        authe = request.httprequest.headers
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))  
        fields = {}
        try:
            token = authe['Authorization'].replace('Bearer ', '')
            valid_token = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_token' , '=' , token]]],{'fields':['x_studio_user_name']})
        except Exception as e:
            response = json.dumps({ 'data': 'no data', 'message': str(e)})
            return Response(
            response, status=401,
            headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
        )
        date_now = str(datetime.today())
              
        body =json.loads(request.httprequest.data)

        

        
            
        if 'name' in body:
            
            
            fields['name']=body['name']

            
        if 'phone' in body :
            
                
                fields['phone']=body['phone']

        id = int(valid_token[0]['x_studio_user_name'][0])
        user_data = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' ,id]]], {'fields': ['login','name',"phone","partner_id"]})

        user_partner = user_data[0]['partner_id'][0]
            
            
        c=models.execute_kw(self.db, uid, self.password, 'res.users', 'write', [[id], fields])
        if 'password' in body:
            if body['password'] == body['confirm_password']:
                c=models.execute_kw(self.db, uid, self.password, 'res.users', 'write', [[id], {'password' : body['password']}])
        if 'email' in body :                
                fields['email']=body['email']
        if 'salutation' in body :                
                fields['x_studio_salutation']=body['salutation']
        if 'company' in body :                
                fields['company_name']=body['company']
        if 'country_id' in body :                
                fields['country_id']=body['country_id']
        if 'address' in body :                
                fields['street']=body['address']
        if 'post_code' in body :                
                fields['x_studio_post_code']=body['post_code']
        if 'find_us' in body :                
                fields['x_studio_find_us']=body['find_us']        

        print('int(user_partner) >> ' , int(user_partner))
        c=models.execute_kw(self.db, uid, self.password, 'res.partner', 'write', [[int(user_partner)], fields])
        user_data = models.execute_kw(self.db, uid, self.password, 'res.users', 'search_read', [[['id' , '=' ,id]]], {'fields': ['name',"login" , "phone"]})
        user_details = [{"id":user_data[0]['id'],"username" :user_data[0]['name'],"phone" :user_data[0]['phone'] ,"email":user_data[0]['login'] ,"timestamp":date_now}]
        response = json.dumps({'data': user_details,'message':'تم تغيير معلوماتك'})
        return Response(
        response, status=200,
        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]
    )   




    @http.route('/auth/delete_account', auth="public", csrf=False, website=True, methods=['POST'])
    def delete_account(self, idd=None, **kw):
        try:
            authe = request.httprequest.headers

            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            uid = common.authenticate(self.db, self.username, self.password, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

            token = authe['Authorization'].replace('Bearer ', '')
            user_token_data = models.execute_kw(self.db, uid, self.password, 'x_user_token', 'search_read', [[['x_studio_user_token', '=', token]]], {
                                        'fields': ['x_studio_user_name']})
            print(int(user_token_data[0]['x_studio_user_name'][0]))
            user_id = int(user_token_data[0]['x_studio_user_name'][0])
            if user_token_data:
                x = models.execute_kw(self.db, uid, self.password, 'res.users', 'unlink', [[user_id]])
                print(x)
                
            

                response = {"data": [], 'message': 'Account deleted successfully'}
                return Response(
                    json.dumps(response), status=200,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', len(response))]
                )
            else:
                response = {"data": [], 'message': 'Invalid Token'}
                return Response(
                    json.dumps(response), status=401,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', len(response))]
                )
        except Exception as e:
            response = json.dumps({'data': 'no data', 'message': str(e)})
            return Response(
                response, status=403,
                headers=[('Content-Type', 'application/json'), ('Content-Length', len(response))]
            )