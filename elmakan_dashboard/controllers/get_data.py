from odoo import models, fields, api
import json                                  
from odoo import http                           
from odoo.http import request,Response          
import requests    


class Partners(http.Controller):
    @http.route('/data/brands', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_brands(self,**kw): 
        result=[]
        headers = request.httprequest.headers 

        if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
            language = "ar"
        else:
            language = 'en'
        brands = request.env['brand.elmakan'].sudo().search([])
        if brands:    
            try:
            
                
                check_image=lambda image:image if image else ''
                for item in brands:
                    result.append({
                        'id':item.id,
                        'title':item.title,              
                        'image':check_image(item.image_url),
                        
                    })
            
            
            
                response = json.dumps({"data":result,'message' : 'All Brands'}) 
                return Response(
                    response, status=200,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
            except Exception as e:
                response = json.dumps({'data':[],'message':str(e)}) 
                return Response(
                    response, status=500,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        else:
            if language=='en':
                message=''
            else:
                message=""
            response = json.dumps({"data":[],'message':message}) 
            return Response(
                response, status=400,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    @http.route('/data/brands/<int:brand_id>', auth="public",csrf=False, website=True, methods=['GET'])
    def get_brand_by_id(self,brand_id=None): 
        result=[]
        headers = request.httprequest.headers

        if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
            language = "ar"
        else:
            language = 'en'
        if brand_id:
            categories = request.env['brand.elmakan'].sudo().search([('id','=',brand_id)])
            if categories:    
                try:
                
                    
                    check_image=lambda image:image if image else ''
                    for item in categories:
                        content_obj = request.env['content.brand.elmakan'].sudo().search([('content_id' , '=' ,item.id)])
                        gallery_obj = request.env['gallery.brand.elmakan'].sudo().search([('gallery_id' , '=' ,item.id)])
                        description_obj = request.env['description.brand.elmakan'].sudo().search([('description_id' , '=' ,item.id)])
                        result.append({
                            'id':item.id,    
                            'title':item.title,              
                            'image':check_image(item.image_url),
                            'content':[{'id':content.id,'text':content.text,'title':content.title,'image_url':content.image_url} for content in content_obj],
                            'gallery':[{'id':gallery.id,'text':gallery.text,'image_url':gallery.image_url} for gallery in gallery_obj],
                            'description':[{'id':description.id,'text':description.text,'description':description.description,'title':description.title} for description in description_obj],
                            
                            
                        })
                
                
                
                    response = json.dumps({"data":result,'message' : 'All categories'}) 
                    return Response(
                        response, status=200,
                        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
                except Exception as e:
                    response = json.dumps({'data':[],'message':str(e)}) 
                    return Response(
                        response, status=500,
                        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
            else:
                if language=='en':
                    message=''
                else:
                    message=""
                response = json.dumps({"data":[],'message':message}) 
                return Response(
                    response, status=400,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]) 
        else:
            if language=='en':
                message=''
            else:
                message=""
            response = json.dumps({"data":[],'message':message}) 
            return Response(
                response, status=400,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    @http.route('/data/categories', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_categories(self,**kw): 
        result=[]
        headers = request.httprequest.headers
        if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
            language = "ar"
        else:
            language = 'en'
        categories = request.env['category.elmakan'].sudo().search([])
        if categories:    
            try:
            
                
                check_image=lambda image:image if image else ''
                for item in categories:
                    result.append({
                        'id':item.id,
                        'text':item.text,    
                        'title':item.title,              
                        'image_url':check_image(item.image_ids.image_url),
                        
                    })
            
            
            
                response = json.dumps({"data":result,'message' : 'All categyre'}) 
                return Response(
                    response, status=200,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
            except Exception as e:
                response = json.dumps({'data':[],'message':str(e)}) 
                return Response(
                    response, status=500,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        else:
            if language=='en':
                message=''
            else:
                message=""
            response = json.dumps({"data":[],'message':message}) 
            return Response(
                response, status=400,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


    @http.route('/data/categories/<int:category_id>', auth="public",csrf=False, website=True, methods=['GET'])
    def get_category_by_id(self,category_id=None): 
        result=[]
        headers = request.httprequest.headers


        if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
            language = "ar"
        else:
            language = 'en'
        if category_id:
            categories = request.env['category.elmakan'].sudo().search([('id','=',category_id)])
            if categories:    
                try:
                
                    
                    check_image=lambda image:image if image else ''
                    for item in categories:
                        content_obj = request.env['category.content.elmakan'].sudo().search([('category_id' , '=' ,item.id)])
                        gallery_obj = request.env['category.gallery.elmakan'].sudo().search([('category_id' , '=' ,item.id)])
                        boxes_obj = request.env['category.boxes.elmakan'].sudo().search([('category_id' , '=' ,item.id)])
                        result.append({
                            'id':item.id,
                            'text':item.text,    
                            'title':item.title,              
                            'image_url':check_image(item.image_ids.image_url),
                            'content':[{'id':content.id,'text':content.text,'title':content.title,'image_url':content.image_url} for content in content_obj],
                            'gallery':[{'id':gallery.id,'text':gallery.text,'image_url':gallery.image_url} for gallery in gallery_obj],
                            'boxes':[{'id':boxes.id,'text':boxes.text,'title':boxes.title} for boxes in boxes_obj],
                            
                            
                        })
                
                
                
                    response = json.dumps({"data":result,'message' : 'All categories'}) 
                    return Response(
                        response, status=200,
                        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
                except Exception as e:
                    response = json.dumps({'data':[],'message':str(e)}) 
                    return Response(
                        response, status=500,
                        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
            else:
                if language=='en':
                    message=''
                else:
                    message=""
                response = json.dumps({"data":[],'message':message}) 
                return Response(
                    response, status=400,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]) 
        else:
            if language=='en':
                message=''
            else:
                message=""
            response = json.dumps({"data":[],'message':message}) 
            return Response(
                response, status=400,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


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


    @http.route('/data/contact', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_contact(self):
        result=[]
        headers = request.httprequest.headers 
        try:
            contact_obj=request.env['contact.elmakan'].sudo().search([])
            if contact_obj:
                check_image=lambda image:image if image else ''
                for item in contact_obj:
                    result.append({
                        'id':item.id,
                        'title':item.title,
                        'text':item.text,
                        'link':item.link ,
                        'icon':item.image_url,
                    })
            
            
            
            response = json.dumps({"data":result,'message' : 'All contact'}) 
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
