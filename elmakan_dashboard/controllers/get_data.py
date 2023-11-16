from odoo import models, fields, api
import json                                  
from odoo import http                           
from odoo.http import request,Response          
import requests    


class Partners(http.Controller):
    @http.route('/data/partners', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_partners(self):
        result=[]
        headers = request.httprequest.headers 
        try:
            partner_obj=request.env['res.partner'].sudo().search([])
            if partner_obj:
                #get_title=lambda x:x.containt_ar if language=='ar' else x.containt_en
                #date=lambda x:str(x) if x!=False else "0000-00-00"
                check_image=lambda image:image if image else ''
                for item in partner_obj:
                    result.append({
                        'id':item.id,
                        'name':item.name                
                    })
            
            
            
            response = json.dumps({"data":result,'message' : 'All partners'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        except Exception as e:
            response = json.dumps({'data':[],'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        
    @http.route('/data/hero_section', auth="public",csrf=False, website=True, methods=['GET'])
    def get_hero_section(self):
        result=[]
        headers = request.httprequest.headers 
        try:
            partner_obj=request.env['hero.section.elmakan'].sudo().search([],limit=1)
            if partner_obj:
                #get_title=lambda x:x.containt_ar if language=='ar' else x.containt_en
                #date=lambda x:str(x) if x!=False else "0000-00-00"
                check_image=lambda image:image if image else ''
                for item in partner_obj:
                    result.append({
                        'id':item.id,
                        'title':item.title,
                        'image_url':item.image_url                
                    })
            
            
            
            response = json.dumps({"data":result,'message' : 'Hero Section'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        except Exception as e:
            response = json.dumps({'data':[],'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
